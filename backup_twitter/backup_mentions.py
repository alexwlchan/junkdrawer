#!/usr/bin/env python
# -*- encoding: utf-8

import os

from twitter_oauth import DEFAULT_BACKUP_ROOT, TwitterSession, save_tweet


if __name__ == '__main__':
    sess = TwitterSession()

    for tweet in sess.mentions_timeline():
        save_tweet(tweet, backup_dir=os.path.join(DEFAULT_BACKUP_ROOT, "mentions"))
