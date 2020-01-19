#!/usr/bin/env python
"""
Given a folder full of MP3 files, add the metadata for the matching tracks
in iTunes.
"""

import glob
import json
import os
import random
import subprocess
import sys
import webbrowser

import eyed3
import hyperlink
import inquirer
import urllib3


def get_itunes_metadata(album_id):
    http = urllib3.PoolManager()

    lookup_url = f"https://itunes.apple.com/lookup?id={album_id}&entity=song"
    resp = http.request("GET", lookup_url)

    itunes_data = json.loads(resp.data)
    results = itunes_data["results"]

    album_types = [
        r
        for r in results
        if r["wrapperType"] == "collection" and r["collectionType"] == "Album"
    ]

    assert len(album_types) == 1, album_types
    album = album_types[0]

    tracks = [r for r in results if r["wrapperType"] == "track"]

    return (album, tracks)


def match_filenames_to_tracks(*, filenames, tracks):
    """
    Given a list of filenames and the track entries from the iTunes API, try
    to build a 1-to-1 mapping between the filenames and the iTunes tracks.
    """
    attempt_count = 0
    ambiguous_filenames = []
    mapping = {}

    while True:
        # If there's nothing left to match, then we're done
        if not filenames and not ambiguous_filenames:
            break
        elif not filenames and ambiguous_filenames:
            filenames = ambiguous_filenames
            ambiguous_filenames = []
            attempt_count += 1

            if attempt_count > 3:
                for f in filenames:
                    available_tracks = {tr["trackName"]: tr for tr in tracks}
                    questions = [
                        inquirer.List(
                            "track",
                            message=f"What track is {f!r}?",
                            choices=sorted(available_tracks.keys())
                            + ["(none of the above)"],
                        )
                    ]
                    answers = inquirer.prompt(questions)

                    track_name = answers["track"]

                    if track_name == "(none of the above)":
                        filenames.remove(f)
                        continue
                    else:
                        selected_track = available_tracks[track_name]
                        filenames.remove(f)
                        mapping[f] = selected_track
        else:
            # Pick a filename, and see if there's an unambiguously matching track.
            # If so, we can add it straight to the mapping.
            selected_filename = random.choice(filenames)

            matching_tracks = [
                tr
                for tr in tracks
                if tr["trackName"].lower() in selected_filename.lower()
            ]

            if len(matching_tracks) == 1:
                track = matching_tracks[0]
                mapping[selected_filename] = track
                filenames.remove(selected_filename)
                tracks.remove(track)
            else:
                # If the filename is ambiguous, add it to the list of ambiguous
                # filenames.  Hope that after we've checked the other files, at least
                # one of the tracks it matches against will have been removed.
                ambiguous_filenames.append(selected_filename)
                filenames.remove(selected_filename)

    return mapping


if __name__ == "__main__":
    front_url = (
        subprocess.check_output(
            [
                "osascript",
                "-e",
                """
        tell application "Safari" to get URL of document 1
        """,
            ]
        )
        .decode("utf8")
        .strip()
    )

    url = hyperlink.URL.from_text(front_url)
    if url.host != "music.apple.com":
        sys.exit(f"Not an iTunes URL: {url}")

    print("*** Fetching metadata from iTunes API")
    album_id = url.path[-1]
    album, tracks = get_itunes_metadata(album_id=album_id)

    print("*** Identified album and tracks")

    print("*** Matching filenames to tracks")
    mapping = match_filenames_to_tracks(
        filenames=list(glob.glob("*.mp3")), tracks=tracks
    )

    print(f"*** Matched every file to a track")
    for filename, track in mapping.items():
        audiofile = eyed3.load(filename)
        audiofile.tag.artist = track["artistName"]
        audiofile.tag.album = album["collectionName"]
        audiofile.tag.album_artist = album["artistName"]
        audiofile.tag.title = track["trackName"]
        audiofile.tag.track_num = (track["trackNumber"], album["trackCount"])
        audiofile.tag.genre = album["primaryGenreName"]
        audiofile.tag.save()

        os.rename(filename, track["trackName"].replace("/", "_") + ".mp3")

    artwork_url = album["artworkUrl100"].replace("100x100", "600x600")
    print(f"*** Artwork URL: {artwork_url}")
    webbrowser.open(artwork_url)

    print(f"*** Release year: {album['releaseDate'].split('-')[0]}")

    os.system("open *.mp3")
