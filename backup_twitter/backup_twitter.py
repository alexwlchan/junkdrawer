#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Usage: backup_twitter.py --credentials=<CREDENTIALS_FILE> --dir=<DIR> --method=<METHOD> [--args=<ARGS>] [--kwargs=<KWARGS>]
       backup_twitter.py -h --help

Options:
    --credentials=<CREDENTIALS_FILE>
        Path to an HCL or JSON file containing Twitter API credentials.
        The file should be a dict with four keys:
        * consumer_key
        * consumer_secret
        * access_token
        * access_token_secret

    --dir=<DIR>
        Directory to store the backed-up tweet data.

"""

import json
import os

import docopt
import tenacity
import tweepy

from birdsite import TweetStore, TwitterCredentials


def setup_api(credentials):
    """Authorise the use of the Twitter API.

    :param credentials: An instance of TwitterCredentials.

    """
    auth = tweepy.OAuthHandler(
        consumer_key=credentials.consumer_key,
        consumer_secret=credentials.consumer_secret)
    auth.set_access_token(
        key=credentials.access_token,
        secret=credentials.access_token_secret
    )
    return tweepy.API(auth)


def get_tweets(method, *args, **kwargs):
    """Generates tweets for a given API method.

    :param method: The tweepy API method to call.
    :param args: args to pass to the API method.
    :param kwargs: kwargs to pass to the API method.

    """
    # We always want the extended mode: this includes the full text of tweets
    # that are >140 characters.
    # https://dev.twitter.com/overview/api/upcoming-changes-to-tweets
    if method.__name__ != 'statuses_lookup':
        kwargs['tweet_mode'] = 'extended'

    @tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, max=60))
    def _get_next_tweets():
        try:
            return method(*args, **kwargs)
        except Exception as exc:
            # Rate limit exceeded is common if you're running this script
            # a lot.  Record it in the output, but don't print the whole thing.
            if exc.reason == "[{'message': 'Rate limit exceeded', 'code': 88}]":
                print('r', end='')
            else:
                print(exc)
            raise

    # Keep going until we've exhausted all the tweets from the API, or
    # something else causes us to break.
    while True:
        new_tweets = _get_next_tweets()
        yield from new_tweets

        if method.__name__ == 'statuses_lookup':
            break

        if not new_tweets:
            break

        # What is the earliest ID of the tweets we've seen?  We'll want
        # to get everything up to that point on the next call.
        earliest_id = min(tweet.id for tweet in new_tweets)
        kwargs['max_id'] = earliest_id - 1


if __name__ == '__main__':
    docopt_args = docopt.docopt(__doc__)

    credentials = TwitterCredentials.from_path(docopt_args['--credentials'])
    api = setup_api(credentials=credentials)

    store = TweetStore.from_path(path=os.path.abspath(docopt_args['--dir']))

    method = docopt_args['--method']
    method = getattr(api, method)
    args = tuple(json.loads(docopt_args['--args'] or '[]'))
    kwargs = json.loads(docopt_args['--kwargs'] or '{}')

    for tweet in get_tweets(method, *args, **kwargs):
        store.save(tweet)
