#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Prints the name, description, and follower/following count
of followers with unusually high numbers of followers or
following.

This is a crude heuristic for finding the source of
"pile-ons" -- when a popular account retweets or quote-tweets
something, and sends their followers against the account.

Note: Twitter rate limits for the /followers/list API call are
quite restrictive, so this script will take a while to run.

"""

import sys

import tweepy


def setup_api():
    from secrets import (
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
    )
    auth = tweepy.OAuthHandler(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET)
    auth.set_access_token(
        key=ACCESS_TOKEN,
        secret=ACCESS_TOKEN_SECRET
    )
    return tweepy.API(auth)


def all_followers(api, username):
    cursor = tweepy.Cursor(
        api.followers,
        screen_name=username,
        
        # The max allowed by this API call.  We only get 15 requests
        # every fifteen minutes, so make them count!
        # https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-followers-list.html
        count=200,

        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True
    )
    for page in cursor.pages():
        for follower in page:
            yield follower


if __name__ == "__main__":
    api = setup_api()
    for follower in all_followers(api, username=sys.argv[1]):
        follower_count = follower.followers_count
        following_count = follower.friends_count

        if follower_count > 5000 or following_count > 5000:
            print("%5d\t%5d\t%s (%s)" % (
                follower_count,
                following_count,
                follower.screen_name,
                follower.description
            ))

