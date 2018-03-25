#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Usage: save_single_tweet.py --id=<ID> --dst=<DST>
"""

import subprocess

import docopt

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    subprocess.check_call([
        'python', 'backup_twitter.py', '--credentials=auth.json',
        f'--dir=/Users/alexwlchan/Dropbox/twitter/{args["--dst"]}',
        '--method=statuses_lookup', f'--args=[[{args["--id"]}]]'
    ])
