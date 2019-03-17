#!/usr/bin/env python
# -*- encoding: utf-8
"""
Usage: build_reading_page_rss.py --username=<USERNAME> --password=<PASSWORD>
"""

import sys

import bs4
import click
import feedgenerator

from _api import DreamwidthSession
from _helpers import parse_date


@click.command()
@click.option("--username", required=True)
@click.option("--password", required=True)
def build_reading_page_rss(username, password):
    sess = DreamwidthSession(username, password)

    # Okay, now get the reading page.  This should contain the most recent
    # 1000 entries from the last 14 days, which is plenty.
    resp = sess.get('https://%s.dreamwidth.org/read' % username)
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
        title="%s's Dreamwidth reading page" % username,
        link='https://%s.dreamwidth.org/' % username,
        description="Entries on %s's reading page" % username,
        language='en'
    )

    for e in entry_wrappers:
        h3_title = e.find('h3', attrs={'class': 'entry-title'})
        title = h3_title.find('a').text
        url = h3_title.find('a').attrs['href']

        datetime_span = e.find('span', attrs={'class': 'datetime'})
        date_span = datetime_span.find('span', attrs={'class': 'date'}).text
        time_span = datetime_span.find('span', attrs={'class': 'time'}).text
        pubdate = parse_date(date_span, time_span)

        poster = e.find('span', attrs={'class': 'poster'}).text

        try:
            tags = [
                li.find('a').text for li in
                e.find('div', attrs={'class': 'tag'}).find('ul').findAll('li')
            ]
            description = 'This post is tagged with %s' % ', '.join(tags)
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

    feed.write(sys.stdout, 'utf-8')


if __name__ == '__main__':
    build_reading_page_rss()
