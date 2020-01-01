#!/usr/bin/env python
# -*- encoding: utf-8

import glob
import json
import os
import subprocess
import sys
import webbrowser

import eyed3
import hyperlink
import inquirer
import urllib3


if __name__ == "__main__":
    front_url = subprocess.check_output([
        "osascript", "-e",
        """
        tell application "Safari" to get URL of document 1
        """
    ]).decode("utf8").strip()

    url = hyperlink.URL.from_text(front_url)
    if url.host != "music.apple.com":
        sys.exit(f"Not an iTunes URL: {url}")

    print(f"*** Looking up URL {url}")

    album_id = url.path[-1]

    http = urllib3.PoolManager()

    print("*** Fetching metadata from iTunes API")
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
    assert len(tracks) == album["trackCount"]
    print("*** Identified album and tracks")

    print(f"*** Track names:")
    print("\n".join(sorted(t["trackName"] for t in tracks)))

    track_matches = {}

    for f in sorted(glob.glob("*.mp3")):
        matching_tracks = [
            t for t in tracks if t["trackName"].lower() in f.lower()
        ]

        if len(matching_tracks) != 1:
            choices = {
                t["trackName"]: t
                for t in matching_tracks
            }

            # If there are no matching tracks, anything left might be a candidate
            if not choices:
                choices = {t["trackName"]: t for t in tracks}

            questions = [
                inquirer.List(
                    "track",
                    message=f"Which track is {f!r}?",
                    choices=choices.keys()
                )
            ]

            answers = inquirer.prompt(questions)

            track_matches[f] = choices[answers["track"]]
        else:
            track_matches[f] = matching_tracks[0]

        tracks.remove(track_matches[f])

    print(f"*** Matched every file to a track")

    for f in sorted(glob.glob("*.mp3")):
        matching_track = track_matches[f]

        audiofile = eyed3.load(f)
        audiofile.tag.artist = matching_track["artistName"]
        audiofile.tag.album = album["collectionName"]
        audiofile.tag.album_artist = album["artistName"]
        audiofile.tag.title = matching_track["trackName"]
        audiofile.tag.track_num = (matching_track["trackNumber"], album["trackCount"])
        audiofile.tag.genre = album["primaryGenreName"]
        # audiofile.tag.best_release_date = matching_track["releaseDate"].split("-")[0]
        audiofile.tag.save()

        os.rename(f, matching_track["trackName"].replace("/", "_") + ".mp3")

    artwork_url = album["artworkUrl100"].replace("100x100", "400x400")
    print(f"*** Artwork URL: {artwork_url}")
    webbrowser.open(artwork_url)

    print(f"*** Track count: {album['trackCount']}")
    print(f"*** Release year: {album['releaseDate'].split('-')[0]}")

    os.system("open *.mp3")
