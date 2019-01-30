#!/usr/bin/env python
# -*- encoding: utf-8

import collections
from urllib.parse import quote_plus

import requests


class TravisSession:

    def __init__(self, token, user_agent):
        self.sess = requests.Session()

        # https://developer.travis-ci.com/gettingstarted
        self.sess.headers = {
            'Travis-API-Version': '3',
            'User-Agent': user_agent,
            'Authorization': f'token {token}',
        }

        def check_for_error(resp, *args, **kwargs):
            resp.raise_for_status()

        self.sess.hooks['response'].append(check_for_error)

    def get(self, endpoint, *args, **kwargs):
        url = f'https://api.travis-ci.org/{endpoint.lstrip("/")}'
        return self.sess.get(url, *args, **kwargs).json()

    def all_builds(self, repo_name):
        params = {}
        while True:
            resp = self.get(f'/repo/{quote_plus(repo_name)}/builds', params=params)
            yield from resp['builds']
            params['offset'] = params.get('offset', 0) + len(resp['builds'])
            if resp['@pagination']['is_last']:
                break


def draw_ascii_chart(data):
    max_value = max(count for _, count in data)
    increment = max_value / 25

    longest_label_length = max(len(label) for label, _ in data)

    for label, count in data:

        # The ASCII block elements come in chunks of 8, so we work out how
        # many fractions of 8 we need.
        # https://en.wikipedia.org/wiki/Block_Elements
        bar_chunks, remainder = divmod(int(count * 8 / increment), 8)

        # First draw the full width chunks
        bar = '█' * bar_chunks

        # Then add the fractional part.  The Unicode code points for
        # block elements are (8/8), (7/8), (6/8), ... , so we need to
        # work backwards.
        if remainder > 0:
            bar += chr(ord('█') + (8 - remainder))

        # If the bar is empty, add a left one-eighth block
        bar = bar or  '▏'

        minutes = int(count / 60)
        if minutes > 60:
            hours = int(minutes / 60)
            minutes %= 60
            count_label = "%dh %2dm" % (hours, minutes)
        else:
            count_label = "%2dm" % minutes

        print(f'{label.ljust(longest_label_length + 1)}  {count_label.rjust(7)} {bar}')


if __name__ == "__main__":
    sess = TravisSession(
        token=open("token.txt").read().strip(),
        user_agent=f"{__file__} by alexwlchan"
    )

    build_durations = {}
    for i, build in enumerate(sess.all_builds("wellcometrust/platform")):
        # If the duration isn't set, the build is still in progress
        if build["duration"] is None:
            continue

        if i > 100:
            break

        build_durations[build["id"]] = build["duration"]

    c = collections.Counter({
        f"https://travis-ci.org/wellcometrust/platform/builds/{key}": value
        for key, value in build_durations.items()
    })

    draw_ascii_chart(c.most_common(10))
