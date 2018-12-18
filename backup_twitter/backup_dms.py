#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os

from requests_oauthlib import OAuth1Session

from birdsite import TwitterCredentials


API_URL = "https://api.twitter.com/1.1"

BACKUP_DIR = os.path.join(os.environ["HOME"], "Dropbox", "twitter", "direct_messages")


def create_session(credentials):
    sess = OAuth1Session(
        client_key=credentials.consumer_key,
        client_secret=credentials.consumer_secret,
        resource_owner_key=credentials.access_token,
        resource_owner_secret=credentials.access_token_secret
    )

    # Raise an exception on any responses that don't return a 200 OK.

    def raise_for_status(resp, *args, **kwargs):
        resp.raise_for_status()

    sess.hooks["response"].append(raise_for_status)

    return sess


def dms_for_saving(response_data):
    for direct_message in response_data["events"]:
        assert direct_message["type"] == "message_create"

        # For now, assume a conversation is between two people, and then we'll
        # create a "conversation ID" by concatenating the sender/recipient.
        sender_id = direct_message["message_create"]["sender_id"]
        recipient_id = direct_message["message_create"]["target"]["recipient_id"]
        user_ids = [sender_id, recipient_id]

        # Denormalise the app data into the individual messages
        try:
            direct_message["message_create"]["_source_app"] = (
                response_data["apps"][direct_message["message_create"]["source_app_id"]]
            )
        except KeyError:
            pass

        yield {
            "user_ids": user_ids,
            "metadata": direct_message
        }


def flatten(iterable):
    for sublist in iterable:
        for item in sublist:
            yield item


def save_individual_dm(dm_user_ids, dm_metadata, users_by_id):
    users = [users_by_id[i] for i in dm_data["user_ids"]]

    # Discard me!
    conversation_id = "__".join(sorted(
        u["screen_name"] for u in users if u["screen_name"] != "alexwlchan"
    ))

    out_dir = os.path.join(BACKUP_DIR, conversation_id)
    os.makedirs(out_dir, exist_ok=True)

    sender_id = dm_metadata["message_create"]["sender_id"]
    dm_metadata["message_create"]["_sender"] = users_by_id[sender_id]

    recipient_id = dm_metadata["message_create"]["target"]["recipient_id"]
    dm_metadata["message_create"]["target"]["_recipient"] = users_by_id[recipient_id]

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


if __name__ == '__main__':
    credentials = TwitterCredentials.from_path("auth.json")

    sess = create_session(credentials)

    users_by_id = {}

    for response_data in get_all_dms(sess):
        dms_to_save = list(dms_for_saving(response_data))

        # Now we want to turn all the user IDs into user objects!
        # First gather a list of all the user IDs.
        unique_user_ids = set(
            uid
            for uid in flatten([dm["user_ids"] for dm in dms_to_save])
            if uid not in users_by_id
        )

        # You can get up to 100 users from this API at once; I just don't want to deal
        # with batching requests unless I actually have to.
        if unique_user_ids:
            assert len(unique_user_ids) < 100
            resp = sess.post(
                API_URL + "/users/lookup.json",
                data={"user_id": ",".join(unique_user_ids)}
            )
            users_by_id.update({u["id_str"]: u for u in resp.json()})

        # Now go through the collection of DMs again, this time turning the conversation
        # ID into a human-readable string and adding user info into the DM body.
        for dm_data in dms_to_save:
            save_individual_dm(
                dm_user_ids=dm_data["user_ids"],
                dm_metadata=dm_data["metadata"],
                users_by_id=users_by_id
            )
