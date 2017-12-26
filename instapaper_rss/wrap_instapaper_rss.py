#!/usr/bin/env python3
# -*- encoding: utf-8
"""
I make heavy use of Twitter.  Interesting tweets are sent to Instapaper,
then I use the private RSS feed to send them to a feed reader, which is
where I actually read them.

    [Twitter] -> [Instapaper] -> [RSS]

Instapaper's default title for Twitter links is simply "Twitter", which isn't
very good for distinguishing multiple feed entries.

This script pulls down the original RSS feed, replaces tweet titles with
"Twitter: Tweet from @username", then saves the result.  I republish this
on my web server, and subscribe to that feed.

This polls periodically; it's not driven by push or anything fancy.
"""

import os
import re
from urllib.request import urlopen


# I'm using urllib for two reasons:
#
#  1. So I can run this script in a vanilla Python environment
#  2. urllib makes it easier to get an encoding-free version of the RSS feed,
#     which is really what I want --- trying to manage encodings is more
#     likely to break something.
#
url = os.environ['URL']
original_rss = urlopen(url).read()

# If we split on ``<item>``, we'll get every feed entry as an individual string
items = original_rss.split(b'<item>')

for idx, it in enumerate(items):

    # In Instapaper feeds, the ``<link>`` always points to the page being
    # displayed, so we check that for Twitter links.
    if b'<link>https://twitter.com' in it:

        match = re.search(
            rb'<link>https://twitter.com/(?P<username>[^/]+)', it
        )
        assert match is not None
        username = match.group('username')

        items[idx] = it.replace(
            b'<title>Twitter</title>',
            b'<title>Tweet from @%s</title>' % username
        )


new_rss = b'<item>'.join(items)
new_rss = new_rss.replace(
    b'<title>Instapaper: Unread</title>',
    b'<title>Instapaper</title>'
)

outdir = os.environ.get('OUTDIR', '')
path = os.path.join(outdir, 'instapaper.rss')
os.makedirs(os.path.dirname(path), exist_ok=True)
open(path, 'wb').write(new_rss)
