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


if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    credentials = TwitterCredentials.from_path(args['--credentials'])
    api = setup_api(credentials=credentials)
