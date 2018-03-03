#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Usage: backup_twitter.py --credentials=<CREDENTIALS_FILE>
       backup_twitter.py -h --help

Options:
    --credentials=<CREDENTIALS_FILE>
        Path to an HCL or JSON file containing Twitter API credentials.
        The file should be a dict with four keys:
        * consumer_key
        * consumer_secret
        * access_token
        * access_token_secret

"""

import attr
import docopt
import hcl
import tenacity
import tweepy


@attr.s
class TwitterCredentials:
    consumer_key = attr.ib()
    consumer_secret = attr.ib(repr=False)
    access_token = attr.ib()
    access_token_secret = attr.ib(repr=False)

    @classmethod
    def from_path(cls, path):
        data = hcl.load(open(path))
        return cls(**data)


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
    kwargs['tweet_mode'] = 'extended'

    @tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, max=10))
    def _get_next_tweets():
        return method(*args, **kwargs)

    # Keep going until we've exhausted all the tweets from the API, or
    # something else causes us to break.
    while True:
        new_tweets = _get_next_tweets()
        yield from new_tweets

        # What is the earliest ID of the tweets we've seen?  We'll want
        # to get everything up to that point on the next call.
        earliest_id = min(tweet.id for tweet in new_tweets)
        kwargs['max_id'] = earliest_id - 1


if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    credentials = TwitterCredentials.from_path(args['--credentials'])
    api = setup_api(credentials=credentials)

    for t in get_tweets(api.user_timeline):
        print(t)
