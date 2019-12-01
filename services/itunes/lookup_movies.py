#!/usr/bin/env python
# -*- encoding: utf-8
"""
Build a spreadsheet of iTunes movies and their HD rental/purchase prices.

When there's something I think I might like to watch, I save the iTunes URL
to a text file.  This script turns that into a spreadsheet showing me the
rental/purchase prices of everything I've saved.  Something like:

    id	        | title	                | rental price  | purchase price
    ------------+-----------------------+---------------+----------------
    966073356	| John Wick	            | 3.49	        | 7.99
    1203098946	| John Wick: Chapter 2	| 3.49	        | 7.99
    1462496695	| John Wick: Chapter 3  | 4.99	        | 13.99

This gives me a mini "shopping list" next time I have money to spend
on entertainment.

There is a wish list feature built into iTunes, but this lets me manage
the list with a text file instead.

Plus it was a chance to experiment with the iTunes API!

"""

import csv
import json
import os
import pprint
import sys

import hyperlink
import tqdm
import urllib3


def get_itunes_movie_ids(path):
    with open(path) as infile:
        for line in infile:
            if not line.startswith("http"):
                continue

            url = hyperlink.URL.from_text(line.strip())
            yield url.path[-1].replace("id", "")


def get_itunes_data(itunes_ids, country="gb"):
    http = urllib3.PoolManager()

    for it_id in itunes_ids:
        lookup_url = f"https://itunes.apple.com/lookup?id={it_id}&country={country}"
        resp = http.request("GET", lookup_url)

        itunes_data = json.loads(resp.data)
        yield from itunes_data["results"]


def _is_movie(itunes_entry):
    return itunes_entry.get("kind") == "feature-movie"


def _create_movie_row(movie):
    try:
        rental_price = movie["trackHdRentalPrice"]
    except KeyError:
        try:
            rental_price = movie["trackRentalPrice"]
        except KeyError:
            rental_price = ""

    try:
        itunes_url = hyperlink.URL.from_text(movie["collectionViewUrl"])
    except KeyError:
        itunes_url = hyperlink.URL.from_text(movie["trackViewUrl"])
    itunes_url = itunes_url.remove("uo")

    return {
        "id": movie["trackId"],
        "title": movie["trackName"],
        "rental price": rental_price,
        "purchase price": movie["trackHdPrice"],
        "URL": str(itunes_url)
    }


def _is_tv_show(itunes_entry):
    return itunes_entry.get("collectionType") == "TV Season"


def _create_tv_show_row(tv_show):
    itunes_url = hyperlink.URL.from_text(tv_show["collectionViewUrl"])
    itunes_url = itunes_url.remove("uo")

    return {
        "id": tv_show["collectionId"],
        "title": tv_show["collectionName"],
        "rental price": "",
        "purchase price": tv_show["collectionHdPrice"],
        "URL": str(itunes_url)
    }


def _is_movie_bundle(itunes_entry):
    return itunes_entry.get("collectionType") == "Movie Bundle"


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <MOVIES_TXT>")

    http = urllib3.PoolManager()

    movie_ids = get_itunes_movie_ids(path)
    itunes_movies = get_itunes_data(movie_ids)

    total = len([line for line in open(path) if line.startswith("http")])

    with open("itunes.csv", "w") as csvfile:
        fieldnames = ["id", "title", "rental price", "purchase price", "URL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for itunes_entry in tqdm.tqdm(itunes_movies, total=total):
            if _is_movie(itunes_entry):
                row = _create_movie_row(itunes_entry)
            elif _is_tv_show(itunes_entry) or _is_movie_bundle(itunes_entry):
                row = _create_tv_show_row(itunes_entry)
            else:
                pprint.pprint(itunes_entry)
                raise ValueError("Unrecognised type of iTunes entry!")

            writer.writerow(row)

    os.system("open itunes.csv")
