#!/usr/bin/env python
# -*- encoding: utf-8
"""
Build a spreadsheet of iTunes movies and their HD rental/purchase prices.
"""

import csv
import json
import os

import hyperlink
import tqdm
import urllib3


def get_itunes_movie_ids(path):
    with open(path) as infile:
        for line in infile:
            url = hyperlink.URL.from_text(line.strip())
            yield url.path[-1].replace("id", "")


def get_itunes_data(itunes_ids):
    http = urllib3.PoolManager()

    for it_id in itunes_ids:
        lookup_url = f"https://itunes.apple.com/lookup?id={it_id}&country=gb"
        resp = http.request("GET", lookup_url)

        itunes_data = json.loads(resp.data)
        yield from itunes_data["results"]



if __name__ == "__main__":
    http = urllib3.PoolManager()

    movie_ids = get_itunes_movie_ids("movies.txt")
    itunes_movies = get_itunes_data(movie_ids)

    total = len([line for line in open("movies.txt") if line.strip()])

    with open("movies.csv", "w") as csvfile:
        fieldnames = ["id", "title", "rental price", "buy price", "URL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for movie in tqdm.tqdm(itunes_movies, total=total):
            try:
                rental_price = movie["trackHdRentalPrice"]
            except KeyError:
                try:
                    rental_price = movie["trackRentalPrice"]
                except KeyError:
                    rental_price = ""

            itunes_url = hyperlink.URL.from_text(movie["collectionViewUrl"])
            itunes_url = itunes_url.remove("uo")

            row = {
                "id": movie["trackId"],
                "title": movie["trackName"],
                "rental price": rental_price,
                "buy price": movie["trackHdPrice"],
                "URL": str(itunes_url)
            }
            writer.writerow(row)

    os.system("open movies.csv")
