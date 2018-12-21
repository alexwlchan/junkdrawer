#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os

from birdsite import TwitterCredentials
from twitter_oauth import BACKUP_DIR_DMS, TwitterSession, UserInfo, create_session


def enrich_dm(event, apps):
    assert event["type"] == "message_create"

    # For now, assume a conversation is between two people, and then we'll
    # create a "conversation ID" by concatenating the sender/recipient.
    sender_id = event["message_create"]["sender_id"]
    recipient_id = event["message_create"]["target"]["recipient_id"]
    user_ids = [sender_id, recipient_id]

    # Denormalise the app data into the individual messages
    try:
        event["message_create"]["_source_app"] = (
            apps[event["message_create"]["source_app_id"]]
        )
    except KeyError:
        pass

    return {
        "user_ids": user_ids,
        "metadata": event
    }


def flatten(iterable):
    for sublist in iterable:
        for item in sublist:
            yield item


def save_individual_dm(dm_user_ids, dm_metadata, user_info):
    users = user_info.lookup_users(dm_user_ids)

    # Discard me!
    conversation_id = "__".join(sorted(
        u["screen_name"] for u in users.values() if u["screen_name"] != "alexwlchan"
    ))

    out_dir = os.path.join(BACKUP_DIR_DMS, conversation_id)
    os.makedirs(out_dir, exist_ok=True)

    sender_id = dm_metadata["message_create"]["sender_id"]
    dm_metadata["message_create"]["_sender"] = user_info.lookup_user(sender_id)

    recipient_id = dm_metadata["message_create"]["target"]["recipient_id"]
    dm_metadata["message_create"]["target"]["_recipient"] = user_info.lookup_user(recipient_id)

    dm_id = dm_metadata["id"]

    out_path = os.path.join(out_dir, f"{dm_id}.json")
    if os.path.exists(out_path):
        print(".", end="")
    else:
        print(dm_id)
        with open(out_path, "w") as outfile:
            outfile.write(json.dumps(dm_metadata))


if __name__ == '__main__':
    credentials = TwitterCredentials.from_path("auth.json")

    oauth_session = create_session(credentials)
    sess = TwitterSession(oauth_session)

    user_info = UserInfo(oauth_session)

    for event in sess.list_dm_events():

        sender_id = event["message_create"]["sender_id"]
        recipient_id = event["message_create"]["target"]["recipient_id"]
        user_ids = [sender_id, recipient_id]

        save_individual_dm(
            dm_user_ids=user_ids,
            dm_metadata=event,
            user_info=user_info
        )
