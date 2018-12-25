#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os

from twitter_oauth import BACKUP_ROOT_DMS, TwitterSession


def save_individual_dm(event, sess):
    sender_id = event["message_create"]["sender_id"]
    recipient_id = event["message_create"]["target"]["recipient_id"]
    user_ids = [sender_id, recipient_id]

    users = sess.lookup_users(user_ids)

    # Discard me!
    conversation_id = "__".join(sorted(
        u["screen_name"] for u in users.values() if u["screen_name"] != "alexwlchan"
    ))

    out_dir = os.path.join(BACKUP_ROOT_DMS, conversation_id)
    os.makedirs(out_dir, exist_ok=True)

    dm_id = event["id"]

    out_path = os.path.join(out_dir, f"{dm_id}.json")
    if os.path.exists(out_path):
        print(".", end="")
    else:
        print(dm_id)
        with open(out_path, "w") as outfile:
            outfile.write(json.dumps(event))


if __name__ == '__main__':
    sess = TwitterSession()

    for event in sess.list_dm_events():
        save_individual_dm(event=event, sess=sess)
