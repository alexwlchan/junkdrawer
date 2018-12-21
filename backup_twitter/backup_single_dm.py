#!/usr/bin/env python
# -*- encoding: utf-8

import sys

from backup_dms import save_individual_dm
from twitter_oauth import TwitterSession


if __name__ == '__main__':
    try:
        direct_message_id = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <DM_ID>")

    sess = TwitterSession.from_credentials_path("auth.json")
    event = sess.show_dm_event(event_id=direct_message_id)

    save_individual_dm(event=event, sess=sess)
