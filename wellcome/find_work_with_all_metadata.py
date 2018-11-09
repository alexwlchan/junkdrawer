#!/usr/bin/env python
# -*- encoding: utf-8

import gzip
import json
import os

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

import tqdm


if not os.path.exists("works2.json.gz"):
    urlretrieve(
        url="https://data.wellcomecollection.org/catalogue/v2/works.json.gz",
        filename="works2.json.gz.tmp")

    os.rename("works2.json.gz.tmp", "works2.json.gz")

with gzip.GzipFile("works2.json.gz") as gz:
    for line in tqdm.tqdm(gz, total=1300000):
        work = json.loads(line)

        keys = set(work.keys())
        if "extent" not in keys:
            continue
        if "physicalDescription" not in keys:
            continue
        if "description" not in keys:
            continue
        if "dimensions" not in keys:
            continue

        print(work)
