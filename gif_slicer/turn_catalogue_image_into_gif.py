#!/usr/bin/env python
# -*- encoding: utf-8
"""
Usage: turn_catalogue_image_into_gif.py <ID> --rows=<ROWS> --columns=<COLUMNS>
"""

import os
import re
import tempfile
from urllib.parse import urlparse

import docopt
import requests

from turn_into_gif import create_gif


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


def get_miro_id(catalogue_id):
    resp = requests.get(
        f"https://api.wellcomecollection.org/catalogue/v2/works/{catalogue_id}",
        params={"include": "identifiers"}
    )
    resp.raise_for_status()

    identifiers = resp.json()["identifiers"]
    miro_ids = [
        i
        for i in identifiers
        if i["identifierType"]["id"] == "miro-image-number"
    ]
    assert len(miro_ids) == 1
    return miro_ids[0]["value"]


def download_url(url):
    out_dir = tempfile.mkdtemp()
    out_path = os.path.join(out_dir, os.path.basename(url))

    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(out_path, "wb") as out_file:
        for chunk in resp.iter_content(chunk_size=512):
            if chunk:
                out_file.write(chunk)

    return out_path


if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    catalogue_id_arg = args["<ID>"]
    row_count = int(args["--rows"])
    column_count = int(args["--columns"])

    catalogue_id = parse_catalogue_id(catalogue_id_arg)
    miro_id = get_miro_id(catalogue_id)

    jpeg_path = download_url(
        f"https://iiif.wellcomecollection.org/image/{miro_id}.jpg/full/full/0/default.jpg"
    )

    gif_path = create_gif(
        path=jpeg_path,
        row_count=row_count,
        column_count=column_count
    )
    actual_gif_path = f"{miro_id}.gif"

    os.rename(gif_path, actual_gif_path)
    print(actual_gif_path)
