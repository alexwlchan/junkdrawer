#!/usr/bin/env python
# -*- encoding: utf-8
"""
Build a spreadsheet of iTunes movies and their HD rental/purchase prices.
"""

import csv
import json
import os
import pprint

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

    itunes_url = hyperlink.URL.from_text(movie["collectionViewUrl"])
    itunes_url = itunes_url.remove("uo")

    return {
        "id": movie["trackId"],
        "title": movie["trackName"],
        "rental price": rental_price,
        "buy price": movie["trackHdPrice"],
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
        "buy price": tv_show["collectionHdPrice"],
        "URL": str(itunes_url)
    }



if __name__ == "__main__":
    http = urllib3.PoolManager()

    movie_ids = get_itunes_movie_ids("movies.txt")
    itunes_movies = get_itunes_data(movie_ids)

    total = len([line for line in open("movies.txt") if line.startswith("http")])

    with open("itunes.csv", "w") as csvfile:
        fieldnames = ["id", "title", "rental price", "buy price", "URL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for itunes_entry in tqdm.tqdm(itunes_movies, total=total):
            if _is_movie(itunes_entry):
                row = _create_movie_row(itunes_entry)
            elif _is_tv_show(itunes_entry):
                row = _create_tv_show_row(itunes_entry)
            else:
                pprint.pprint(itunes_entry)
                raise ValueError("Unrecognised type of iTunes entry!")

            writer.writerow(row)

    os.system("open itunes.csv")
