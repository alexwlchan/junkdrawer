#!/usr/bin/env python
# -*- encoding: utf-8
"""
Run inside a directory, and it moves every non-trivial file up to the
top-level.
"""

import filecmp
import os
import secrets
import shutil
import sys


def mv(src, dst):
    print(f'mv {src} ~> {dst}')
    if '--run' in sys.argv:
        os.rename(src, dst)


def rm(path):
    print(f'rm {path}')
    if '--run' in sys.argv:
        os.unlink(path)


if __name__ == '__main__':
    for root, _, filenames in os.walk('.'):
        if root == '.':
            continue

        for f in filenames:
            f_src = os.path.join(root, f)

            if f == '.DS_Store':
                rm(f_src)
                continue

            f_dst = f

            if os.path.exists(f_dst) and filecmp.cmp(f_src, f_dst):
                rm(f_src)
                continue

            # Add a bit of noise to filenames to avoid duplication
            while os.path.exists(f_dst):
                name, ext = os.path.splitext(f)
                f_dst = name + '__' + secrets.token_hex(3) + ext

            mv(src=f_src, dst=f_dst)

    # Clean up empty directories
    while True:
        is_finished = True
        for root, dirnames, filenames in os.walk('.'):
            if not dirnames and not filenames:
                shutil.rmtree(root)
                is_finished = False

        if is_finished:
            break
