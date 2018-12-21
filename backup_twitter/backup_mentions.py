#!/usr/bin/env python
# -*- encoding: utf-8

from twitter_oauth import TwitterSession, save_tweet


if __name__ == '__main__':
    sess = TwitterSession.from_credentials_path("auth.json")

    for tweet in sess.mentions_timeline():
        save_tweet(tweet, dirname="mentions")
