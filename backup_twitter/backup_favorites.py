#!/usr/bin/env python
# -*- encoding: utf-8

from twitter_oauth import TwitterSession, save_tweet


def save_favorite(tweet):
    return save_tweet(tweet, dirname="favorites")


if __name__ == '__main__':
    sess = TwitterSession.from_credentials_path("auth.json")

    for tweet in sess.list_favorites():
        save_favorite(tweet)
