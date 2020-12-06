#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os

import click
import requests

BACKUP_ROOTS = [
    os.path.join(os.environ["HOME"], "Documents", "backups", "pinboard"),
    "/Volumes/Media (Sapphire)/backups/pinboard",
]


@click.command()
@click.option("--username", required=True)
@click.option("--password", required=True)
def save_all_bookmarks(username, password):
    resp = requests.get(
        "https://api.pinboard.in/v1/posts/all",
        params={"format": "json"},
        auth=(username, password),
    )
    resp.raise_for_status()

    json_string = json.dumps(resp.json(), indent=2, sort_keys=True)

    for root in BACKUP_ROOTS:
        os.makedirs(root, exist_ok=True)

        with open(os.path.join(root, "bookmarks.json"), "w") as outfile:
            outfile.write(json_string)


if __name__ == "__main__":
    save_all_bookmarks()
