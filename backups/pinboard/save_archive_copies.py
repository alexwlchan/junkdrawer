#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os
import shutil
import tarfile

import click
import tqdm

from runner import process_concurrent, wget
from save_bookmarks_list import BACKUP_ROOT
from save_cache_ids import CACHE_ID_PATH


@click.command()
@click.option("--username", required=True)
@click.option("--password", required=True)
def save_archive_copies(username, password):
    wget(
        "--save-cookies",
        "pinboard-cookies.txt",
        "--keep-session-cookies",
        "--delete-after",
        "--output-file",
        "-",
        "--post-data",
        f"username={username}&password={password}",
        "https://pinboard.in/auth/",
    )

    cache_ids = json.load(open(CACHE_ID_PATH))

    for result in tqdm.tqdm(
        process_concurrent(download_archive, cache_ids.values()),
        total=len(cache_ids.values()),
    ):
        pass

    os.unlink("pinboard-cookies.txt")


def download_archive(cache_id):
    cache_dir = os.path.join(BACKUP_ROOT, "archive", cache_id[0], cache_id)
    
    if os.path.exists(cache_dir + ".tar.gz"):
        return

    tmp_dir = cache_dir + ".tmp"

    os.makedirs(os.path.dirname(cache_dir), exist_ok=True)

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
        "--load-cookies",
        "pinboard-cookies.txt",
        "--output-file",
        "-",
        "--directory-prefix",
        tmp_dir,
        f"https://pinboard.in/cached/{cache_id}/",
    )

    with tarfile.open(cache_dir + ".tar.gz", "w:gz") as tf:
        tf.add(tmp_dir, arcname=cache_id)
    
    shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    save_archive_copies()
