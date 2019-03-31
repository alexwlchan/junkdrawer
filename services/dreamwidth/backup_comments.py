#!/usr/bin/env python
# -*- encoding: utf-8

import datetime as dt
import os
import sys

from _api import DreamwidthSession


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip().splitlines()[0])

    username = sys.argv[1]
    password = sys.argv[2]

    backup_dir = os.path.join(os.environ["HOME"], "Documents", "backups", "dreamwidth_comments")
    os.makedirs(backup_dir, exist_ok=True)

    sess = DreamwidthSession(username, password)

    resp = sess.get("https://www.dreamwidth.org/comments/recent", params={"show": 100})
    open(os.path.join(backup_dir, "recent_" + dt.datetime.now().isoformat() + ".html"), "w").write(resp.text)

    resp = sess.get("https://www.dreamwidth.org/comments/posted", params={"show": 100})
    open(os.path.join(backup_dir, "posted_" + dt.datetime.now().isoformat() + ".html"), "w").write(resp.text)
