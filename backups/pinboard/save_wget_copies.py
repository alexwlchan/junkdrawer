#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os
import re
import shutil
import subprocess

import click
import tqdm
from unidecode import unidecode

from save_bookmarks_list import BACKUP_ROOT
from save_cache_ids import CACHE_ID_PATH


def wget(*args):
    subprocess.call(["wget"] + list(args), stdout=subprocess.DEVNULL)


def slugify(u):
    "Convert Unicode string into blog slug."
    # https://leancrew.com/all-this/2014/10/asciifying/
    u = re.sub(u"[–—/:;,.]", "-", u)  # replace separating punctuation
    a = unidecode(u).lower()  # best ASCII substitutions, lowercased
    a = re.sub(r"[^a-z0-9 -]", "", a)  # delete any other characters
    a = a.replace(" ", "-")  # spaces to hyphens
    a = re.sub(r"-+", "-", a)  # condense repeated hyphens
    return a


@click.command()
def save_wget_copies():
    all_bookmarks = json.load(open(os.path.join(BACKUP_ROOT, "bookmarks.json")))

    for bookmark in tqdm.tqdm(all_bookmarks):
        download_id = slugify(
            bookmark["href"]
            .replace("http://", "")
            .replace("https://", "")
            .replace("www.", "")
        )

        download_dir = os.path.join(
            BACKUP_ROOT, "wget_archive", download_id[0], download_id
        )

        if os.path.isdir(download_dir):
            continue
        else:
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
            "--directory-prefix",
            tmp_dir,
            bookmark["href"],
        )

        os.rename(tmp_dir, download_dir)


if __name__ == "__main__":
    save_wget_copies()
