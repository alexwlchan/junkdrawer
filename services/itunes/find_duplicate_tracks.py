#!/usr/bin/env python3
"""
This is a script I wrote to help me find duplicate tracks in my iTunes library.

Something something… a bunch of tracks had multiple copies.  This goes through
and looks for any albums where there are multiple tracks for a given (track number).

It also highlighted some other issues, e.g. albums with wrong numbering.

Probably the most useful long-term thing to take from this code
is the `get_tracks()` function, which trakes an ElementTree-parsed version of
the iTunes Library XML file, and generating the individual tracks.

See https://osxdaily.com/2018/05/23/itunes-library-xml-file-missing-fix/

"""

import collections
import datetime
from urllib.parse import unquote
import xml.etree.ElementTree as ET


def get_tracks(root):
    top_level_dict = root[0]

    for child in top_level_dict:
        if child.tag != 'dict':
            continue

        for grandchild in child:
            if grandchild.tag != 'dict':
                continue

            track = {}

            key = None

            for track_data in grandchild:
                if track_data.tag == 'key':
                    key = track_data.text
                    continue
                elif track_data.tag == 'integer':
                    assert key is not None
                    track[key] = int(track_data.text)
                    key = None
                    continue
                elif track_data.tag == 'date':
                    assert key is not None
                    track[key] = datetime.datetime.strptime(
                        track_data.text, '%Y-%m-%dT%H:%M:%SZ'
                    )
                    key = None
                    continue
                elif track_data.tag == 'string':
                    assert key is not None
                    track[key] = track_data.text
                    key = None
                    continue
                elif track_data.tag == 'true':
                    assert key is not None
                    track[key] = True
                    key = None
                    continue
                else:
                    raise ValueError(f"Unrecognised track_data: {track_data!r}")

            yield track


if __name__ == "__main__":
    tree = ET.parse("/Users/alexwlchan/Music/iTunes/iTunes Library.xml")
    root = tree.getroot()

    albums = collections.defaultdict(lambda: collections.defaultdict(list))

    for track in get_tracks(root):
        if track.get('Has Video'):
            continue

        album_name = track['Album']
        track_number = track.get('Track Number')

        albums[album_name][track_number].append(track)


    for album_name, tracks in albums.items():
        if all(len(v) == 1 or k is None for k, v in tracks.items()):
            continue
        print(f"== Album: {album_name} ==")

        for track_num, dupe_tracks in sorted(tracks.items()):
            if track_num is None:
                continue

            if len(dupe_tracks) == 1:
                continue
            for t in dupe_tracks:
                print(t["Name"], '/', unquote(t["Location"].split("/")[-1]))

        print("")
