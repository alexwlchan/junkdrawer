#!/usr/bin/env python
# -*- encoding: utf-8

import gzip
import json
import os

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


if not os.path.exists("works2.json.gz"):
    urlretrieve(
        url="https://data.wellcomecollection.org/catalogue/v2/works.json.gz",
        filename="works2.json.gz.tmp")

    os.rename("works2.json.gz.tmp", "works2.json.gz")

for line in gzip.GzipFile("works2.json.gz"):
    work = json.loads(line)

    keys = work.keys()
    if "extent" not in keys:
        continue
    if "physicalDescription" not in keys:
        continue
    if "description" not in keys:
        continue
    if "dimensions" not in keys:
        continue
    if "lettering" not in keys:
        continue
    if "language" not in keys:
        continue

    print(work["id"])
