#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Usage: save_single_tweet.py --id=<ID> --dst=<DST>
"""

import os
import subprocess
import sys

import docopt


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    subprocess.check_call([
        sys.executable, os.path.join(SCRIPT_DIR, 'backup_twitter.py'),
        '--credentials', os.path.join(SCRIPT_DIR, 'auth.json'),
        f'--dir=/Users/alexwlchan/Dropbox/twitter/{args["--dst"]}',
        '--method=statuses_lookup', f'--args=[[{args["--id"]}]]'
    ])
