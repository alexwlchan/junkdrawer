#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Usage: save_single_tweet.py --url=<URL> --dst=<DST>
"""

import os
import subprocess
import sys

import docopt


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    tweet_url = args['--url']
    components = tweet_url.split('/')

    if tweet_url.endswith('/photo/1'):
        assert components[-4] == 'status'
        tweet_id = components[-3]
    else:
        assert components[-2] == 'status'
        tweet_id = components[-1]

    subprocess.check_call([
        sys.executable, os.path.join(SCRIPT_DIR, 'backup_twitter.py'),
        '--credentials', os.path.join(SCRIPT_DIR, 'auth.json'),
        f'--dir=/Users/alexwlchan/Dropbox/twitter/{args["--dst"]}',
        '--method=statuses_lookup', '--args', f'[[{tweet_id}]]'
    ])
