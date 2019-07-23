#!/usr/bin/env python
# -*- encoding: utf-8

import sys

from twitter_oauth import TwitterSession, save_tweet


if __name__ == '__main__':
    sess = TwitterSession()

    try:
        search_term = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <SEARCH_TERM>")

    for tweet in sess.search(search_term):
        save_tweet(tweet, dirname=f"searches/{search_term}")
