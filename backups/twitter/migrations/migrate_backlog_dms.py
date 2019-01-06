#!/usr/bin/env python
# -*- encoding: utf-8
"""
A script for migrating the HTML backlog into "synthetic" DM responses that
approximate the "pure" API responses from Twitter.

TODO:

*   Group conversations
*   Playable media
*   Tweet entities
*   Information about the sending app

It overrides existing synthetic responses, as it always goes back to the original
HTML dumps, which are expected to be more "pure".

"""

import json
import os

import bs4
import requests

import sys; sys.path.append("..")

from twitter_oauth import TwitterSession, DEFAULT_BACKUP_ROOT


sess = TwitterSession()

users_by_id = {}


for f in os.listdir("backlog"):
    if f.startswith((".", "_")):
        continue

    # I'd like to come back and do these eventually, but I want an example of
    # what a real group DM conversation API response looks like first.
    if f.startswith("group_"):
        continue

    print(f)

    path = os.path.join("backlog", f)

    soup = bs4.BeautifulSoup(open(path).read(), "html.parser")

    conversation_content_ol = soup.find_all(
        "ol", attrs={"class": "DMConversation-content"}
    )
    assert len(conversation_content_ol) == 1
    conversation_content = conversation_content_ol[0]

    direct_messages = conversation_content.find_all(
        "li", attrs={"class": "DirectMessage"}
    )

    thread_id = conversation_content.attrs["data-thread-id"]
    participants = thread_id.split("-")

    for p in participants:
        if p not in users_by_id:
            user_data = sess.lookup_users(user_ids=[p])[p]
            users_by_id[user_data["id_str"]] = user_data

    other_user = [p for p in participants if users_by_id[p]["screen_name"] != "alexwlchan"][0]
    other_screen_name = users_by_id[other_user]["screen_name"]

    for dm in direct_messages:
        timestamp = dm.find("span", attrs={"class": "_timestamp"}).attrs["data-time"]

        sender_id = dm.attrs["data-sender-id"]
        recipient_id = [p for p in participants if p != sender_id][0]

        dm_id = dm.attrs["data-item-id"]

        try:
            text = dm.find("div", attrs={"class": "DirectMessage-text"}).text.strip()
        except AttributeError:
            try:
                # In this case I'm quoting a tweet (e.g. croissantkatie's conversation),
                # so just stick in a link to the tweet.
                href = (dm
                    .find("div", attrs={"class": "DirectMessage-tweet"})
                    .find("a", attrs={"class": "QuoteTweet-link"})
                    .attrs["href"]
                )
                assert "/status/" in href
                text = "https://twitter.com" + href
            except AttributeError:
                try:
                    # Maybe the DM was an image?
                    img_src = (
                        dm
                            .find("div", attrs={"class": "Media-photo"})
                            .find("img")
                            .attrs["src"]
                    )
                    assert img_src.startswith(
                        ("https://ton.twitter.com/", "https://ton.twimg.com/")), img_src
                    text = img_src
                except AttributeError:
                    try:
                        # Or a card?
                        card_url = (
                            dm
                                .find("div", attrs={"class": "DirectMessage-card"})
                                .find("div", attrs={"class": "card-type-summary"})
                                .attrs["data-card-url"]
                        )
                        assert card_url.startswith("https://t.co/")
                        text = requests.head(card_url).headers["Location"]
                    except AttributeError:
                        # Or a GIF/video?
                        if dm.find("div", attrs={"class": "PlayableMedia-player"}) is not None:
                            text = "<Playable media>"
                        else:
                            print(dm)
                            raise

        data = {
            "_synthetic": True,
            "type": "message_create",
            "id": dm_id,
            "created_timestamp": timestamp,
            "message_create": {
                "target": {
                    "recipient_id": recipient_id,
                    "_recipient": users_by_id[recipient_id]
                },
                "sender_id": sender_id,
                "_sender": users_by_id[sender_id],
                "message_data": {
                    "text": text
                }
            }
        }

        out_path = os.path.join(
            DEFAULT_BACKUP_ROOT, "direct_messages", other_screen_name, dm_id + ".json"
        )

        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        if (
            not os.path.exists(out_path) or
            (os.path.exists(out_path) and json.load(open(out_path)).get("_synthetic"))
        ):
            json_string = json.dumps(data)
            open(out_path, "w").write(json_string)
        else:
            continue
