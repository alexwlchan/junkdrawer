#!/usr/bin/env python
# -*- encoding: utf-8

import os
import sys


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit("%s <PATH>" % __file__)

    filenames = os.listdir(path)
    common_prefix = os.path.commonprefix(filenames)

    for f in sorted(filenames):
        name, ext = os.path.splitext(f)
        new_f = name[len(common_prefix):-12] + ext
        print(new_f)
        os.rename(
            os.path.join(path, f),
            os.path.join(path, new_f)
        )
