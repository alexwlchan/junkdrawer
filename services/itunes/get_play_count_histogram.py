#!/usr/bin/env python
"""
Since I have a way to get all the tracks from my iTunes library programatically,
why not have some fun with the stats?
"""

import collections
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt

from find_duplicate_tracks import get_tracks


if __name__ == "__main__":
    tree = ET.parse("/Users/alexwlchan/Music/iTunes/iTunes Library.xml")
    root = tree.getroot()

    play_counts = collections.Counter()

    for track in get_tracks(root):
        play_counts[track.get("Play Count", 0)] += 1

    print(play_counts)

    _, ax = plt.subplots()
    plt.bar(
        range(max(play_counts) + 1),
        [play_counts[count] for count in range(max(play_counts) + 1)]
    )
    ax.set_xlabel('# of plays')
    ax.set_ylabel('# of tracks')
    plt.show()
