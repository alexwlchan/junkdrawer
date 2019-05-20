#!/usr/bin/env python
# -*- encoding: utf-8

import os

import requests.exceptions
import toml

from twitter_oauth import TwitterSession, save_tweet


if __name__ == '__main__':
    sess = TwitterSession()

    tweet_urls = toml.load(open(
        os.path.join(os.environ["HOME"], "repos", "linode-infra", "analytics", "referrers.toml")
    ))["twitter"].values()

    for url in tweet_urls:
        tweet_id = url.split("/")[-1]
        try:
            tweet = sess.lookup_status(tweet_id)
        except requests.exceptions.HTTPError as err:
            if err.args[0].startswith("404 Client Error"):
                continue
            else:
                raise
        save_tweet(tweet, dirname="referrers")
