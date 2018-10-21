#!/usr/bin/env python
# -*- encoding: utf-8
"""
Usage: turn_catalogue_image_into_gif.py <ID>
"""

import os
import re
from urllib.parse import urlparse

import docopt


def parse_catalogue_id(arg):
    if arg.startswith((
        "https://wellcomecollection.org/works",
        "https://api.wellcomecollection.org/catalogue",
    )):
        return os.path.basename(urlparse(arg).path)
    elif re.match(r"^[a-z0-9]{8}$", arg):
        return arg
    else:
        raise ValueError("Unrecognised catalogue ID: %r" % arg)


if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    catalogue_id = args["<ID>"]
    print(turn_catalogue_image_into_gif.py(catalogue_id))
