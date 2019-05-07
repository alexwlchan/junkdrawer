#!/usr/bin/env python
# -*- encoding: utf-8
"""
Print a URL to every post which is "original content" on Tumblr.
"""

import itertools
import sys

import requests


def get_all_posts(host, api_key):
    params = {
        "api_key": api_key,
        "reblog_info": "true",
    }
    url = "https://api.tumblr.com/v2/blog/%s/posts" % host

    for offset in itertools.count(start=0, step=20):
        params["offset"] = offset
        resp = requests.get(url, params=params)
        posts = resp.json()["response"]["posts"]
        if not posts:
            break
        yield from posts


def is_original_post(p):
    return "reblogged_from_name" not in p


if __name__ == "__main__":
    try:
        host = sys.argv[1]
        api_key = sys.argv[2]
    except IndexError:
        sys.exit("Usage: %s <HOST> <API_KEY>" % __file__)

    for p in get_all_posts(host=host, api_key=api_key):
        if is_original_post(p):
            if "op" in p["tags"]:
                continue
            print(p["post_url"])
