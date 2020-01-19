#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os
import re
import shutil

import hyperlink
import tqdm
from unidecode import unidecode

from runner import process_concurrent, wget
from save_bookmarks_list import BACKUP_ROOT


EXPORT_ROOT = os.path.join(os.environ["HOME"], "Documents", "backups", "ao3")


def slugify(u):
    "Convert Unicode string into blog slug."
    # https://leancrew.com/all-this/2014/10/asciifying/
    u = re.sub("[–—/:;,.]", "-", u)  # replace separating punctuation
    a = unidecode(u).lower()  # best ASCII substitutions, lowercased
    a = re.sub(r"[^a-z0-9 -]", "", a)  # delete any other characters
    a = a.replace(" ", "-")  # spaces to hyphens
    a = re.sub(r"-+", "-", a)  # condense repeated hyphens
    return a


def save_ao3_exports():
    all_bookmarks = json.load(open(os.path.join(BACKUP_ROOT, "bookmarks.json")))

    bookmark_urls = [
        hyperlink.URL.from_text(bookmark["href"]) for bookmark in all_bookmarks
    ]

    ao3_ids = [
        url.path[-1] for url in bookmark_urls if url.host == "archiveofourown.org"
    ]

    assert all(id_.isnumeric() for id_ in ao3_ids)

    for result in tqdm.tqdm(
        process_concurrent(save_ao3_id, iter(ao3_ids)), total=len(ao3_ids)
    ):
        pass


def save_ao3_id(ao3_id):
    download_dir = os.path.join(EXPORT_ROOT, ao3_id)

    if os.path.isdir(download_dir):
        return

    tmp_dir = download_dir + ".tmp"

    try:
        shutil.rmtree(tmp_dir)
    except FileNotFoundError:
        pass

    for ext in ["azw", "epub", "mobi", "pdf", "html"]:
        wget(
            "--no-verbose",
            "--output-file",
            "-",
            # The Content-Disposition header is sent by the server to say
            # what the file "should" be called.  By telling wget to respect this,
            # it means we can request "a.html", the header from AO3 will specify
            # the correct filename (including the fic title), and the file will
            # be named correctly.
            "--content-disposition",
            "--directory-prefix",
            tmp_dir,
            f"https://archiveofourown.org/downloads/{ao3_id}/a.{ext}",
        )

    os.rename(tmp_dir, download_dir)


if __name__ == "__main__":
    save_ao3_exports()
