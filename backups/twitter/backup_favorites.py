#!/usr/bin/env python
# -*- encoding: utf-8

from twitter_oauth import TwitterSession, save_tweet


if __name__ == '__main__':
    sess = TwitterSession()

    for tweet in sess.list_favorites():
        save_tweet(tweet, dirname="favorites")
