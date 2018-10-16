#!/usr/bin/env python
# -*- encoding: utf-8

import datetime as dt
import itertools
import json
import os

import requests


BACKUP_DIR = os.path.join(os.environ["HOME"], "Documents", "backups", "tumblr_likes")


def all_likes(*, blog_identifier, api_key):
    sess = requests.Session()

    last_page_fetched = None

    for offset in itertools.count(start=0, step=20):
        resp = sess.get(
            f"https://api.tumblr.com/v2/blog/{blog_identifier}/likes",
            params={
                "api_key": api_key,
                "offset": offset,
            }
        )

        now = dt.datetime.now()
        if last_page_fetched is None:
            print(f"Page received at {now}")
        else:
            print(f"Page received at {now} ({(now - last_page_fetched).seconds} seconds ago)")
        last_page_fetched = now

        print([p["id"] for p in resp.json()["response"]["liked_posts"]])

        for post in resp.json()["response"]["liked_posts"]:
            yield post


if __name__ == '__main__':
    os.makedirs(BACKUP_DIR, exist_ok=True)

    for post_info in all_likes(
        blog_identifier="alexwlchan.tumblr.com",
        api_key="ii4TLRjfMoszcoDkrxBKUk5isHgx0ezQnJ8JWGntYIboVVigez"
    ):
        post_id = str(post_info["id"])
        post_dir = os.path.join(BACKUP_DIR, post_id[:2], post_id)
        os.makedirs(post_dir, exist_ok=True)

        info_path = os.path.join(post_dir, "info.json")

        # The Tumblr API only returns the first 1000 or so responses via pagination.
        # After that, you have to get a bit cheaty.  If we found something we've
        # already seen, give up.
        if os.path.exists(info_path):
            break

        json_string = json.dumps(post_info, indent=2, sort_keys=True)
        with open(info_path, "w") as outfile:
            outfile.write(json_string)
        print(".", end="", flush=True)
