#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os
import subprocess
from urllib.request import urlretrieve

from bs4 import BeautifulSoup

from backup_tumblr_likes import BACKUP_DIR


def _download_asset(post_dir, url, suffix=""):
    name = os.path.basename(url) + suffix
    out_path = os.path.join(post_dir, name)
    if os.path.exists(out_path):
        return
    urlretrieve(url, out_path)
    print(".", end="", flush=True)


if __name__ == '__main__':
    for root, _, filenames in os.walk(BACKUP_DIR):
        if "info.json" not in filenames:
            continue

        post_data = json.load(open(os.path.join(root, "info.json")))

        if post_data["type"] == "photo":
            for photo in post_data["photos"]:
                _download_asset(post_dir=root, url=photo["original_size"]["url"])

        elif post_data["type"] in ("answer", "chat", "link", "quote", "text"):
            continue

        elif post_data["type"] == "video":
            players = [p for p in post_data["player"] if p["embed_code"]]

            # TODO: Why does this happen?
            if not players:
                print(post_data)
                continue

            best_player = max(players, key=lambda p: p["width"])

            soup = BeautifulSoup(best_player["embed_code"], "html.parser")

            sources = soup.find_all("source")
            if len(sources) == 1:
                source = sources[0]

                assert source.attrs["type"] == "video/mp4"
                _download_asset(post_dir=root, url=source.attrs["src"], suffix=".mp4")
                continue

            iframes = soup.find_all("iframe", attrs={"id": "youtube_iframe"})
            if len(iframes) == 1:
                iframe = iframes[0]
                # TODO: Actually do the download here.
                continue

            a_flickrs = soup.find_all("a", attrs={"data-flickr-embed": "true"})
            if len(a_flickrs) == 1:
                assert len(a_flickrs[0].find_all("img")) == 1
                img = a_flickrs[0].find_all("img")[0]
                _download_asset(post_dir=root, url=img.attrs["src"])
                continue



            print(post_data)
            # assert False, soup

        elif post_data["type"] == "audio":
            # TODO: Something useful!
            print(post_data)

        else:
            print(post_data)
            assert False
