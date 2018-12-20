#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os
import sys

from backup_dms import (
    API_URL, BACKUP_DIR, create_session, enrich_dm, save_individual_dm
)
from birdsite import TwitterCredentials


if __name__ == '__main__':
    try:
        direct_message_id = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <DM_ID>")

    credentials = TwitterCredentials.from_path("auth.json")

    sess = create_session(credentials)

    resp = sess.get(
        API_URL + "/direct_messages/events/show.json",
        params={"id": direct_message_id}
    )

    # data = resp.json()
    # with open("dm_single.json", "w") as f:
    #     json.dump(data, f)
    #
    # users_by_id = {}

    data = json.load(open("dm_single.json"))

    enriched_direct_message = enrich_dm(data["event"], apps=data["apps"])
    print(enriched_direct_message)

    user_resp = sess.post(
        API_URL + "/users/lookup.json",
        data={"user_id": ",".join(enriched_direct_message["user_ids"])}
    )

    users_by_id = {}
    for u in user_resp.json():
        del u["status"]
        users_by_id[u["id_str"]] = u

    save_individual_dm(
        dm_user_ids=enriched_direct_message["user_ids"],
        dm_metadata=enriched_direct_message["metadata"],
        users_by_id=users_by_id
    )
