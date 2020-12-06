#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os
import re
import shutil
import tarfile

import tqdm
from unidecode import unidecode

from runner import process_concurrent, wget


BACKUP_ROOT = "/Volumes/Media (Sapphire)/backups/pinboard"


def slugify(u):
    "Convert Unicode string into blog slug."
    # https://leancrew.com/all-this/2014/10/asciifying/
    u = re.sub(u"[–—/:;,.]", "-", u)  # replace separating punctuation
    a = unidecode(u).lower()  # best ASCII substitutions, lowercased
    a = re.sub(r"[^a-z0-9 -]", "", a)  # delete any other characters
    a = a.replace(" ", "-")  # spaces to hyphens
    a = re.sub(r"-+", "-", a)  # condense repeated hyphens
    return a


def save_wget_copies():
    all_bookmarks = json.load(open(os.path.join(BACKUP_ROOT, "bookmarks.json")))

    urls = [bookmark["href"] for bookmark in all_bookmarks]

    for result in tqdm.tqdm(
        process_concurrent(save_wget_archive, urls), total=len(all_bookmarks)
    ):
        pass


def save_wget_archive(url):
    download_id = slugify(
        url.replace("http://", "").replace("https://", "").replace("www.", "")
    )

    download_dir = os.path.join(
        BACKUP_ROOT, "wget_archive", download_id[0], download_id
    )

    if os.path.exists(download_dir + ".tar.gz"):
        return

    os.makedirs(os.path.dirname(download_dir), exist_ok=True)

    tmp_dir = download_dir + ".tmp"

    try:
        shutil.rmtree(tmp_dir)
    except FileNotFoundError:
        pass

    wget(
        "--adjust-extension",
        "--span-hosts",
        "--no-verbose",
        "--convert-links",
        "--page-requisites",
        "--no-directories",
        "-e",
        "robots=off",
        "--output-file",
        "-",
        "-U",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "--directory-prefix",
        tmp_dir,
        url,
    )

    with tarfile.open(download_dir + ".tar.gz", "w:gz") as tf:
        tf.add(tmp_dir, arcname=download_id)
    
    shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    save_wget_copies()
