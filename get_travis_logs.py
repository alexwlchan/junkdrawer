#!/usr/bin/env python
# -*- encoding: utf-8
"""
Usage: get_travis_logs.py <URL> --token=<TOKEN>
       get_travis_logs.py -h | --help

Options:
    <URL>   URL of a Travis CI build, for example
            https://travis-ci.org/wellcometrust/platform/builds/394971265
    --token=<TOKEN>
            Token for the Travis API.  Instructions for getting a token:
            https://developer.travis-ci.com/authentication
"""

import os
import tempfile
from urllib.parse import urlparse

import docopt
import requests


class TravisSession():

    def __init__(self, token):
        self.sess = requests.Session()

        # https://developer.travis-ci.com/gettingstarted
        self.sess.headers = {
            'Travis-API-Version': '3',
            'User-Agent': 'get_travis_logs.py from https://github.com/alexwlchan/homeconfig',
            'Authorization': f'token {token}',
        }

        def check_for_error(resp, *args, **kwargs):
            resp.raise_for_status()

        self.sess.hooks['response'].append(check_for_error)

    def get(self, endpoint, *args, **kwargs):
        url = f'https://api.travis-ci.org/{endpoint.lstrip("/")}'
        return self.sess.get(url, *args, **kwargs).json()


if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    build_id = os.path.basename(urlparse(args['<URL>']).path)

    sess = TravisSession(token=args['--token'])

    job_resp = sess.get(f'/build/{build_id}/jobs')

    out_dir = os.path.join(tempfile.mkdtemp(), f'travis-{build_id}')

    for job in job_resp['jobs']:

        # We can't get info for all jobs
        if job['finished_at'] is None:
            continue

        # Passing logs aren't interesting
        if job['state'] == 'passed':
            continue

        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, job['number'] + '.log')

        log_resp = sess.get(f'/job/{job["id"]}/log')
        with open(out_path, 'w') as outfile:
            outfile.write(log_resp['content'])

    if os.path.exists(out_dir):
        print(out_dir)
    else:
        print('No failed jobs?')
