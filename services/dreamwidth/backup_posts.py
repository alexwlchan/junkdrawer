#!/usr/bin/env python
# -*- encoding: utf-8
"""
Usage: backup_posts.py <USERNAME> <PASSWORD>

A script for backing up Dreamwidth posts using the XML-RPC API.

"""

import json
import os
import sys

from api import BinaryEncoder, DreamwidthAPI


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip().splitlines()[0])

    username = sys.argv[1]
    password = sys.argv[2]

    backup_dir = os.path.join(os.environ["HOME"], "Documents", "backups", "dreamwidth")
    json_backup_dir = os.path.join(backup_dir, "json")
    html_backup_dir = os.path.join(backup_dir, "html")

    os.makedirs(json_backup_dir, exist_ok=True)
    os.makedirs(html_backup_dir, exist_ok=True)

    api = DreamwidthAPI(username, password)

    for post in api.get_all_posts():
        post_id = post["itemid"]
        json_path = os.path.join(json_backup_dir, f"{post_id}.json")

        if os.path.exists(json_path):
            break

        html_path = os.path.join(html_backup_dir, f"{post_id}.html")
        try:
            open(html_path, "w").write(post["event"])
        except TypeError:
            open(html_path, "wb").write(post["event"].data)

        json_string = json.dumps(post, indent=2, sort_keys=True, cls=BinaryEncoder)
        open(json_path, "w").write(json_string)
