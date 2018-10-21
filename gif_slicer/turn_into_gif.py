#!/usr/bin/env python
# -*- encoding: utf-8
"""
Usage: turn_into_gif.py <PATH> --rows=<ROWS> --columns=<COLUMNS> [--reversed]
"""

import os
import subprocess
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


def create_frames(im, **kwargs):
    tmp_dir = tempfile.mkdtemp()

    areas = crop_areas(**kwargs)

    for idx, area in enumerate(areas):
        frame = im.crop(area)
        frame_path = os.path.join(tmp_dir, 'frame%d.jpg' % idx)
        frame.save(frame_path)
        yield frame_path


if __name__ == "__main__":
    args = docopt.docopt(__doc__)

    path = args["<PATH>"]
    row_count = int(args["--rows"])
    column_count = int(args["--columns"])

    im = Image.open(path)

    cmd = ["convert"]

    for frame in create_frames(im, rows=row_count, columns=column_count):
        cmd.append(frame)

    gif_path = path.replace(".jpg", ".gif")
    cmd.append(gif_path)
    subprocess.check_call(cmd)
    print(gif_path)
