#!/usr/bin/env python
"""
Tries to rename files in the working directory to match the numbering scheme
used by Plex, based on metadata from The TVDB.
"""

import itertools
import json
import os
import pathlib
from pprint import pprint
import sys

import httpx


def get_client():
    client = httpx.Client()

    auth_path = pathlib.Path(__file__).resolve().parent / "auth.json"

    resp = client.post(
        "https://api.thetvdb.com/login",
        json=json.load(auth_path.open())
    )
    resp.raise_for_status()

    client.headers = {"Authorization": f"Bearer {resp.json()['token']}"}

    return client


def get_series_episodes(series_id):
    for page in itertools.count(start=1):
        resp = client.get(
            f"https://api.thetvdb.com/series/{series_id}/episodes",
            params={"page": page}
        )

        yield from resp.json()["data"]

        if resp.json()["links"]["last"] == page:
            break


if __name__ == "__main__":
    client = get_client()

    series_name = sys.argv[1]

    resp = client.get(
        "https://api.thetvdb.com/search/series",
        params={"name": series_name}
    )

    if len(resp.json()["data"]) == 1:
        series_name = resp.json()["data"][0]["seriesName"]
        series_id = resp.json()["data"][0]["id"]
    else:
        # TODO: Implement a way to choose what episode I want using inquirer
        # or similar, but until it arises not worth writing.
        print("Can't work out what series this is!", file=sys.stderr)
        pprint(resp.json())

    for episode in get_series_episodes(series_id):
        matching = [
            f
            for f in os.listdir()
            if episode["episodeName"] in f
        ]

        target_name = "%s - s%02de%02d - %s" % (
            series_name,
            episode["airedSeason"],
            episode["airedEpisodeNumber"],
            episode["episodeName"]
        )

        print(target_name)

        for f in os.listdir():
            if f.startswith(target_name):
                continue

            if episode["episodeName"] in f:
                if f.endswith(".en.srt"):
                    new_name = f"{target_name}.en.srt"
                else:
                    ext = os.path.splitext(f)[1]
                    new_name = f"{target_name}{ext}"

                if not os.path.exists(new_name):
                    os.rename(f, new_name)
