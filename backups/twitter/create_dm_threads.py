#!/usr/bin/env python
# -*- encoding: utf-8
"""
Produce human-readable copies of my DM threads.
"""

import json
import os
import sys
import time


if __name__ == '__main__':
    try:
        dm_backup_dir = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <DM_DEFAULT_BACKUP_ROOT>")

    dm_backup_dir = os.path.abspath(dm_backup_dir)

    for root, _, filenames in os.walk(dm_backup_dir):
        if not any(f.endswith(".json") for f in filenames):
            continue

        print("Creating thread for %s..." % root)

        messages = [
            json.load(open(os.path.join(root, f)))
            for f in filenames
            if f.endswith(".json")
        ]

        message_metas = [
            {
                "date": time.gmtime(int(m["created_timestamp"]) / 1000),
                "screen_name": m["message_create"]["_sender"]["screen_name"],
                "text": m["message_create"]["message_data"]["text"]
            }
            for m in messages
        ]

        with open(os.path.join(root, "thread.txt"), "w") as f:
            for m in sorted(message_metas, key=lambda m: m["date"]):
                f.write(time.strftime("[%Y-%m-%d %H:%M:%S] ", m["date"]))
                f.write("<%s> " % m["screen_name"])
                f.write(m["text"] + "\n")
