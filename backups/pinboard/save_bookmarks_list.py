#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os

import click
import requests

BACKUP_ROOT = os.path.join(os.environ["HOME"], "Documents", "backups", "pinboard")


@click.command()
@click.option("--username", required=True)
@click.option("--password", required=True)
def save_all_bookmarks(username, password):
    resp = requests.get(
        "https://api.pinboard.in/v1/posts/all",
        params={"format": "json"},
        auth=(username, password)
    )
    resp.raise_for_status()

    with open(os.path.join(BACKUP_ROOT, "bookmarks.json"), "w") as outfile:
        outfile.write(resp.text)


if __name__ == "__main__":
    save_all_bookmarks()
