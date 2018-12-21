#!/usr/bin/env python
# -*- encoding: utf-8

import sys

from backup_dms import enrich_dm, save_individual_dm
from birdsite import TwitterCredentials
from twitter_oauth import API_URL, UserInfo, create_session


if __name__ == '__main__':
    try:
        direct_message_id = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <DM_ID>")

    credentials = TwitterCredentials.from_path("auth.json")

    sess = create_session(credentials)
    user_info = UserInfo(sess=sess)

    resp = sess.get(
        API_URL + "/direct_messages/events/show.json",
        params={"id": direct_message_id}
    )

    data = resp.json()

    enriched_direct_message = enrich_dm(data["event"], apps=data["apps"])

    save_individual_dm(
        dm_user_ids=enriched_direct_message["user_ids"],
        dm_metadata=enriched_direct_message["metadata"],
        user_info=user_info
    )
