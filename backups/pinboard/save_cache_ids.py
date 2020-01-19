#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os

import bs4
import click
import requests

from save_bookmarks_list import BACKUP_ROOT

CACHE_ID_PATH = os.path.join(BACKUP_ROOT, "cache_ids.json")


def get_cache_ids(soup):
    bookmarks_div = soup.find("div", attrs={"id": "bookmarks"})
    bookmarks = bookmarks_div.find_all("div", attrs={"class": "bookmark"})

    for b in bookmarks:
        href = b.find("a", attrs={"class": "bookmark_title"}).attrs["href"]
        cache_link = b.find("a", attrs={"class": "cached"})

        if cache_link is None:
            continue

        cache_id = cache_link.attrs["href"].split("/")[-2]

        yield (href, cache_id)


@click.command()
@click.option("--username", required=True)
@click.option("--password", required=True)
def save_archive_copies(username, password):

    # Start by logging in to Pinboard, so we have the appropriate cookies.
    sess = requests.Session()
    resp = sess.post(
        "https://pinboard.in/auth/", data={"username": username, "password": password}
    )
    resp.raise_for_status()

    cache_ids = {}

    url = f"https://pinboard.in/u:{username}"

    while True:
        print(f"Making request to {url}")
        resp = sess.get(url, params={"per_page": 160})
        resp.raise_for_status()

        soup = bs4.BeautifulSoup(resp.text, "html.parser")

        cache_ids.update(get_cache_ids(soup))

        prev_link = soup.find("a", attrs={"class": "next_prev"})
        if "earlier" not in prev_link.text:
            break

        url = f"https://pinboard.in" + prev_link.attrs["href"]

    print(len(cache_ids))

    with open(CACHE_ID_PATH, "w") as outfile:
        outfile.write(json.dumps(cache_ids, indent=2, sort_keys=True))


if __name__ == "__main__":
    save_archive_copies()
