#!/usr/bin/env python3
# -*- encoding: utf-8
"""
This is a script I wrote for Alice W to create a list of items in Prismic
and their publication date.

"""

import codecs
import csv
import json

try:
    from urllib.request import urlretrieve
except ImportError:  # Python 2
    from urllib import urlretrieve


def get_repo_base(url):
    filename, _ = urlretrieve(url)
    return json.load(open(filename))


def get_master(base_info):
    """Returns the current master reference."""
    try:
        master_ref = next(ref for ref in base_info["refs"] if ref["id"] == "master")
    except StopIteration:
        return None
    else:
        return master_ref["ref"]


def get_documents(search_url, master_ref):
    """Generates all the documents in our Prismic repository."""
    url = "%s?ref=%s#format=json&pageSize=100" % (search_url, master_ref)

    while True:
        filename, _ = urlretrieve(url)
        payload = json.load(open(filename))

        for res in payload["results"]:
            yield res

        url = payload["next_page"]
        if url is None:
            break


if __name__ == "__main__":
    base_info = get_repo_base(url="https://wellcomecollection.prismic.io/api/v2")

    master_ref = get_master(base_info)
    search_url = base_info["forms"]["everything"]["action"]

    with codecs.open("prismic_stories.csv", "w") as csvfile:
        fieldnames=[
            "id",
            "type",
            "title",
            "published",
            "last updated",
            "URL"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for doc in get_documents(search_url=search_url, master_ref=master_ref):

            # These are probably uninteresting to Alice.  If she's interested
            # in seeing what's appear in analytics, seeing Prismic documents
            # that don't appear on the web is unhelpful.
            if doc["type"] in {
                "access-statements",
                "article-formats",
                "background-textures",
                "books",
                "collection-venue",
                "editorial-contributor-roles",
                "event-formats",
                "featureflag",
                "featurescohort",
                "iframe",
                "iframes",
                "interpretation-types",
                "organisations",
                "people",
            }:
                continue

            # This title doesn't have to be there (you can still look up the
            # item by Prismic ID on the website), but it makes the spreadsheet
            # easier to skim than our Prismic IDs.
            try:
                title = doc["data"]["title"][0]["text"]
            except (KeyError, IndexError):
                title = None

            if title is None:
                from pprint import pprint
                pprint(doc)

            # The URL doesn't have to be there, but it's most of the point!
            if doc["type"] in {
                "articles",
                "events",
                "event-series",
                "exhibitions",
                "pages",
                "series"
            }:
                url = "https://wellcomecollection.org/%s/%s" % (doc["type"], doc["id"])
            elif doc["type"] in {"articles", "webcomics"}:
                url = "https://wellcomecollection.org/articles/%s" % doc["id"]
            else:
                url = ""

            # Only show a "last updated" date if it's meaningfully different.
            if doc["first_publication_date"] == doc["last_publication_date"]:
                last_updated = ""
            else:
                last_updated = doc["last_publication_date"]

            # Assemble the row, write it to the CSV.
            row = {
                "id": doc["id"],
                # "type": base_info["types"][doc["type"]],
                "type": doc["type"],
                "title": title,
                "published": doc["first_publication_date"],
                "last updated": last_updated,
                "URL": url,
            }

            writer.writerow(row)
