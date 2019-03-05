#!/usr/bin/env python
# -*- encoding: utf-8

import getpass
import sys

from api import DreamwidthAPI


if __name__ == "__main__":
    username = "alexwlchan"
    password = open("password.txt").read()

    tag = "daily journal"

    posts_start = "2019-02-20"
    posts_end   = "2019-03-20"

    api = DreamwidthAPI(username, password)

    for post in api.get_all_posts():
        if tag not in post["props"].get("taglist", "").split(", "):
            continue
        if posts_start < post["eventtime"] < posts_end:
            print(post["url"])
