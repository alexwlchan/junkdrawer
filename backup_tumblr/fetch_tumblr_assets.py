#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os
import subprocess
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlparse
from urllib.request import urlretrieve

from bs4 import BeautifulSoup

from backup_tumblr_likes import BACKUP_DIR


def _download_asset(post_dir, url, suffix=""):
    name = os.path.basename(url) + suffix
    out_path = os.path.join(post_dir, name)
    if os.path.exists(out_path):
        return
    try:
        urlretrieve(url, out_path)
    except HTTPError:
        print(url)
        return
    print(".", end="", flush=True)


def _download_with_youtube_dl(post_dir, url):
    """
    Download a video using youtube-dl.
    """

    # The purpose of this marker is to check "have we run youtube_dl before?"
    #
    # Although youtube_dl is smart about not re-downloading files, it has to make
    # a network request before it does that, which is slow and mostly unnecessary.
    # This is a crude way to avoid unnecessary shell-outs/network requests.
    #
    marker = os.path.join(post_dir, ".youtube_dl")
    if os.path.exists(marker):
        return

    try:
        subprocess.check_call(
            ["youtube-dl", url],
            stdout=subprocess.DEVNULL,
            cwd=post_dir
        )
    except subprocess.CalledProcessError:
        print(url)
    else:
        open(marker, "wb").write(b"")
        print(".", end="", flush=True)


if __name__ == '__main__':
    for root, _, filenames in os.walk(BACKUP_DIR):
        if "info.json" not in filenames:
            continue

        post_dir = root
        post_data = json.load(open(os.path.join(post_dir, "info.json")))

        if post_data["type"] == "photo":
            for photo in post_data["photos"]:
                _download_asset(post_dir=post_dir, url=photo["original_size"]["url"])

        elif post_data["type"] in ("answer", "chat", "link", "quote", "text"):
            continue

        elif post_data["type"] == "video":
            players = [p for p in post_data["player"] if p["embed_code"]]

            if post_data["video_type"] == "tumblr":
                _download_asset(post_dir=post_dir, url=post_data["video_url"])
                continue

            elif post_data["video_type"] == "youtube":
                if all(not p["embed_code"] for p in post_data["player"]):
                    continue

                try:
                    if post_data["source_url"].startswith("https://www.youtube.com/embed"):
                        source_url = post_data["source_url"]
                    else:
                        source_url = parse_qs(urlparse(post_data["source_url"]).query)["z"][0]
                except KeyError:
                    best_player = max(players, key=lambda p: p["width"])
                    soup = BeautifulSoup(best_player["embed_code"], "html.parser")
                    iframe_matches = soup.find_all("iframe", attrs={"id": "youtube_iframe"})
                    assert len(iframe_matches) == 1

                    source_url = iframe_matches[0].attrs["src"]

                _download_with_youtube_dl(post_dir=post_dir, url=source_url)
                continue

            elif post_data["video_type"] in ("vimeo", "youtube"):
                best_player = max(players, key=lambda p: p["width"])
                soup = BeautifulSoup(best_player["embed_code"], "html.parser")
                iframe_matches = soup.find_all("iframe")
                assert len(iframe_matches) == 1

                embed_url = iframe_matches[0].attrs["src"]

                _download_with_youtube_dl(post_dir=post_dir, url=embed_url)
                continue

            elif (
                post_data["video_type"] == "unknown" and
                post_data.get("source_url").startswith("https://t.umblr.com/redirect?z=http%3A%2F%2Fwww.youtube.com")
            ):
                source_url = parse_qs(urlparse(post_data["source_url"]).query)["z"][0]
                _download_with_youtube_dl(post_dir=post_dir, url=source_url)
                continue

            elif post_data["video_type"] == "instagram":
                source_url = post_data["permalink_url"]
                print(source_url)
                continue

            elif post_data["video_type"] == "flickr":
                source_url = parse_qs(urlparse(post_data["source_url"]).query)["z"][0]
                print(source_url)
                continue

            print(post_data)

        elif post_data["type"] == "audio":

            # Exammple contents of the "player" field:
            #
            #     <iframe
            #       class="tumblr_audio_player tumblr_audio_player_76004518890"
            #       src="http://example.tumblr.com/post/1234/audio_player_iframe/example/tumblr_1234?audio_file=https%3A%2F%2Fwww.tumblr.com%2Faudio_file%2Fexample%2F1234%2Ftumblr_1234"
            #       frameborder="0"
            #       allowtransparency="true"
            #       scrolling="no"
            #       width="540"
            #       height="169"></iframe>
            #
            if post_data["audio_type"] == "tumblr":
                player_soup = BeautifulSoup(post_data["player"], "html.parser")
                player_matches = player_soup.find_all(
                    "iframe", attrs={"class": "tumblr_audio_player"}
                )
                assert len(player_matches) == 1

                src_url = player_matches[0]["src"]
                query_string = parse_qs(urlparse(src_url).query)
                assert len(query_string["audio_file"]) == 1
                audio_file = query_string["audio_file"][0]
                print(audio_file)
                continue

            elif post_data["audio_type"] == "spotify":
                source_url = post_data["audio_source_url"]
                print(source_url)
                continue

            elif post_data["audio_type"] == "soundcloud":
                source_url = post_data["audio_source_url"]
                print(source_url)
                continue

            # TODO: Something useful!
            print(post_data)

        else:
            print(post_data)
            assert False
