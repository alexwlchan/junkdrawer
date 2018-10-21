#!/usr/bin/env python
# -*- encoding: utf-8
"""
Usage: turn_into_gif.py <PATH> --rows=<ROWS> --columns=<COLUMNS> [--reversed]
"""

import math
import os
import subprocess
import sys
import tempfile

import docopt
from PIL import Image


def crop_areas(*, rows, columns):
    segment_width = im.width / columns
    segment_height = im.height / rows
    for row_idx in range(rows):
        for col_idx in range(columns):
            yield (
                col_idx * segment_width,
                row_idx * segment_height,
                (col_idx + 1) * segment_width,
                (row_idx + 1) * segment_height
            )


def create_frames(im, *, rows, columns):
    tmp_dir = tempfile.mkdtemp()

    for idx, area in enumerate(areas):
        frame = im.crop(area)
        frame_path = os.path.join(tmp_dir, 'frame%d.jpg' % idx)
        frame.save(frame_path)
        yield frame_path


if __name__ == "__main__":
    args = docopt.docopt(__doc__)

    path = args["<PATH>"]

    im = Image.open(path)
    im.convert('RGB')

    tmp_dir = tempfile.mkdtemp()

    areas = crop_areas(rows=int(args["--rows"]), columns=int(args["--columns"]))
    for i, area in enumerate(areas):
        frame = im.crop(area)
        frame.save(os.path.join(tmp_dir, 'frame%03d.jpg' % i))

    subprocess.check_call(
        ["convert", "-delay", "0", "-loop", "0", "*.jpg", "combined.gif"], cwd=tmp_dir
    )

    os.rename(os.path.join(tmp_dir, "combined.gif"), path.replace(".jpg", ".gif"))
