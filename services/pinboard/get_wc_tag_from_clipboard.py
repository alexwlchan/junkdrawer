#!/usr/bin/env python
# -*- encoding: utf-8

from __future__ import division, print_function

import subprocess

from tag_counts import get_pinboard_tag


if __name__ == "__main__":
    wc = int(subprocess.check_output("pbpaste | wc -w", shell=True))

    tag = get_pinboard_tag(wc)
    print(tag, end=" ")
