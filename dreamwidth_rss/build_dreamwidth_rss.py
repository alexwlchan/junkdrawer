#!/usr/bin/env python
# -*- encoding: utf-8
"""
Usage: build_dreamwidth_rss.py --username=<USERNAME> --password=<PASSWORD>
"""

import hashlib
import os

import bs4
import docopt
import feedgenerator
import maya
import requests


def md5(s):
    h = hashlib.md5()
    h.update(s.encode('ascii'))
    return h.hexdigest()


args = docopt.docopt(__doc__)

username = args['--username']
password = args['--password']


# First we have to log in to Dreamwidth.  This is a bit more complicated
# than a standard username/password form.
#
# Possibly because the LiveJournal/Dreamwidth codebase predates widespread
# adoption/support for HTTPS, the login page doesn't just send an encrypted
# username/password.  Instead, the login page includes an auth and a challenge.
#
# The challenge is prepended to an MD5 hash of the password, all of which is
# in turn MD5-hashed.  The resulting string is sent to the server, and the
# plaintext password omitted.
#
# You can see the browser-side implementation in question in login.js:
# https://github.com/dreamwidth/dw-free/blob/3467339cd823c6d71b8a235bf76409d5dab93b85/htdocs/js/login.js
#
# This bit definitely works, btu it's probably fragile.
sess = requests.Session()

resp = sess.get('https://www.dreamwidth.org/login')
login_soup = bs4.BeautifulSoup(resp.text, 'html.parser')
lj_form_auth = login_soup.find(
    'input', attrs={'name': 'lj_form_auth'}).attrs['value']
chal = login_soup.find('input', attrs={'name': 'chal'}).attrs['value']

response_field = md5(chal + md5(password))

resp = sess.post(
    'https://www.dreamwidth.org/login',
    data={
        'user': username,
        'password': '',
        'lj_form_auth': lj_form_auth,
        'chal': chal,
        'action:login': 'Log in',
        'response': response_field,
    }
)
resp.raise_for_status()

# Dreamwidth always returns an HTTP 200, even if login fails.  This is a
# better way to check if login succeeded.
assert 'Welcome back to Dreamwidth!' in resp.text

# Okay, now get the reading page.  This should contain the most recent
# 1000 entries from the last 14 days, which is plenty.
resp = sess.get(f'https://{username}.dreamwidth.org/read')
assert "You're viewing your Reading Page." in resp.text

reading_soup = bs4.BeautifulSoup(resp.text, 'html.parser')
entries = reading_soup.find('div', attrs={'id': 'entries'})
entry_wrappers = entries.findAll('div', attrs={'class': 'entry-wrapper'})

# Now get the feed items.  This is just a pile of messy HTML parsing.
#
# Important note: because this RSS feed may be exposed outside Dreamwidth
# (and thus outside the Dreamwidth access controls), it shouldn't include
# overly sensitive information.  In particular, NO POST CONTENT.  This is
# just some metadata I'm hoping isn't too secret -- in particular, the same
# stuff you get from notification emails.
#
feed = feedgenerator.Rss201rev2Feed(
    title="alexwlchan's Dreamwidth reading page",
    link='https://alexwlchan.dreamwidth.org/',
    description="Entries on alexwlchan's reading page",
    language='en'
)

for e in entry_wrappers:
    h3_title = e.find('h3', attrs={'class': 'entry-title'})
    title = h3_title.find('a').text
    url = h3_title.find('a').attrs['href']

    datetime_span = e.find('span', attrs={'class': 'datetime'})
    date_span = datetime_span.find('span', attrs={'class': 'date'}).text
    time_span = datetime_span.find('span', attrs={'class': 'time'}).text
    pubdate = maya.parse(date_span + ' ' + time_span)

    poster = e.find('span', attrs={'class': 'poster'}).text

    try:
        tags = [
            li.find('a').text for li in
            e.find('div', attrs={'class': 'tag'}).find('ul').findAll('li')
        ]
        description = 'This post is tagged with %s' % ', '.join(
            repr(t) for t in tags)
    except AttributeError:
        tags = []
        description = '(This post is untagged)'

    feed.add_item(
        title=title,
        link=url,
        pubdate=pubdate,
        author_name=poster,
        description=description
    )

with open('dreamwidth.rss', 'w') as fp:
    feed.write(fp, 'utf-8')
