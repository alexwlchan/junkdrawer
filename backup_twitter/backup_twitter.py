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


if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    auth = TwitterCredentials.from_path(args['--credentials'])
