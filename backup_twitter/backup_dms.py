#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os

from birdsite import TwitterCredentials
from twitter_oauth import API_URL, UserInfo, create_session

BACKUP_DIR = os.path.join(os.environ["HOME"], "Dropbox", "twitter", "direct_messages")


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


def dms_for_saving(response_data):
    for direct_message in response_data["events"]:
        yield enrich_dm(direct_message, apps=response_data["apps"])


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

    out_dir = os.path.join(BACKUP_DIR, conversation_id)
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


def get_all_dms(sess):
    params = {"count": 50}
    while True:
        resp = sess.get(API_URL + "/direct_messages/events/list.json", params=params)
        yield resp.json()

        try:
            params["cursor"] = resp.json()["next_cursor"]
        except KeyError:
            break


def lookup_users(sess, user_ids):
    resp = sess.post(
        API_URL + "/users/lookup.json",
        data={"user_id": ",".join(user_ids)}
    )
    for u in resp.json():
        try:
            del u["status"]
        except KeyError:
            pass
        yield u


if __name__ == '__main__':
    credentials = TwitterCredentials.from_path("auth.json")

    sess = create_session(credentials)

    user_info = UserInfo(sess=sess)

    for response_data in get_all_dms(sess):
        dms_to_save = list(dms_for_saving(response_data))

        # Now we want to turn all the user IDs into user objects!
        # First gather a list of all the user IDs.
        unique_user_ids = set(
            uid
            for uid in flatten([dm["user_ids"] for dm in dms_to_save])
        )

        # You can get up to 100 users from this API at once; I just don't want to deal
        # with batching requests unless I actually have to.
        assert len(unique_user_ids) < 100

        # Now go through the collection of DMs again, this time turning the conversation
        # ID into a human-readable string and adding user info into the DM body.
        for dm_data in dms_to_save:
            save_individual_dm(
                dm_user_ids=dm_data["user_ids"],
                dm_metadata=dm_data["metadata"],
                user_info=user_info
            )
