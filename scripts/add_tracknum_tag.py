#!/usr/bin/env python
# -*- encoding: utf-8

import os

import eyed3


for f in list(os.listdir(".")):
    if not f.endswith(".mp3"):
        continue

    disc, track_num, *_ = f.split("-")
    disc = int(disc)
    track_num = int(track_num)
    if disc == 2:
        track_num += 21

    af = eyed3.load(f)
    af.tag.track_num = track_num
    af.tag.save()

    os.rename(f, f[9:])
