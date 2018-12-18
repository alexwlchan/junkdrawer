#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Usage: rollup_thread.py --credentials=<CREDENTIALS_FILE> --url=<URL>
       rollup_thread.py -h --help

Options:
    --credentials=<CREDENTIALS_FILE>
        Path to an HCL or JSON file containing Twitter API credentials.
        The file should be a dict with four keys:
        * consumer_key
        * consumer_secret
        * access_token
        * access_token_secret

    --url=<URL>
        URL of the final tweet in the thread.

"""

import docopt

from birdsite import setup_api, TwitterCredentials


if __name__ == '__main__':
    docopt_args = docopt.docopt(__doc__)

    credentials = TwitterCredentials.from_path(docopt_args['--credentials'])
    api = setup_api(credentials=credentials)

    status_id = docopt_args['--url'].split('/')[-1]

    thread = []

    while True:
        resp = api.statuses_lookup([status_id])
        assert len(resp) == 1
        tweet = resp[0]

        thread.insert(0, tweet)

        status_id = tweet.in_reply_to_status_id_str
        if status_id is None:
            break

    print(f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}')
    print('---\n')
    print('\n\n'.join(t.full_text for t in thread))
