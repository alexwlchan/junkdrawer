#!/usr/bin/env python
# -*- encoding: utf-8

import datetime as dt
import json

import bs4
import feedgenerator
import requests


def create_session():
    sess = requests.Session()

    def raise_for_status(resp, *args, **kwargs):
        resp.raise_for_status()

    sess.hooks["response"].append(raise_for_status)

    return sess


if __name__ == "__main__":
    sess = create_session()

    # Get the front page of /stories/
    resp = sess.get("https://wellcomecollection.org/stories")
    soup = bs4.BeautifulSoup(resp.text, "html.parser")

    # Crawl the entire page, looking for any <a> tags that link to a
    # page that starts with /articles/
    article_hrefs = set()
    for a_tag in soup.find_all("a"):
        try:
            href = a_tag.attrs["href"]
        except KeyError:
            continue

        if not href.startswith("/articles/"):
            continue

        article_hrefs.add(href)

    # Now let's go through and fetch every one of those articles, and save
    # the corresponding soup.
    #
    # Next, go through the soups, and extract the metadata we need to put
    # an article in the RSS feed.  We get this from a mixture of <meta> tags
    # and a nice block of JSON-LD provided in the <head>.
    #
    feed = feedgenerator.Rss201rev2Feed(
        title="Stories from Wellcome Collection",
        link="https://wellcomecollection.org/stories/",
        language="en",
        description="A homebrew feed for stories from Wellcome Collection"
    )

    for href in article_hrefs:
        resp = sess.get("https://wellcomecollection.org" + href)
        soup = bs4.BeautifulSoup(resp.text, "html.parser")

        json_ld_tag = soup.find("script", attrs={"type": "application/ld+json"})
        json_ld = json.loads(json_ld_tag.text)

        title = json_ld["headline"]
        link = json_ld["url"]
        pubdate = dt.datetime.strptime(
            json_ld["datePublished"],
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        author_name = ", ".join(
            contributor["name"] for contributor in json_ld["contributor"]
        )
        description = soup.find(
            "meta", attrs={"property": "og:description"}).attrs["content"]

        feed.add_item(
            title=title,
            link=link,
            pubdate=pubdate,
            author_name=author_name,
            description=description
        )

    with open("stories.xml", "w") as outfile:
        feed.write(outfile, "utf-8")
