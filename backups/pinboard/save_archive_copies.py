#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os
import shutil
import subprocess

import click
import tqdm

from save_bookmarks_list import BACKUP_ROOT
from save_cache_ids import CACHE_ID_PATH


def wget(*args):
    subprocess.call(["wget"] + list(args), stdout=subprocess.DEVNULL)


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
    for c_id in tqdm.tqdm(cache_ids.values()):
        cache_dir = os.path.join(BACKUP_ROOT, "archive", c_id[0], c_id)
        if os.path.exists(cache_dir):
            continue

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
            f"https://pinboard.in/cached/{c_id}/",
        )

        os.rename(tmp_dir, cache_dir)


if __name__ == "__main__":
    save_archive_copies()
