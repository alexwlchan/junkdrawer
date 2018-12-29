#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os
import sys
from twitter_oauth import download_profile_image

seen = set()

for root, _, filenames in os.walk(f"/Users/alexwlchan/Documents/backups/twitter/{sys.argv[1]}"):
    for f in filenames:
        if not f.endswith(".json"):
            continue
        data = json.load(open(os.path.join(root, f)))

        if data["user"]["profile_image_url_https"] in seen:
            continue

        seen.add(data["user"]["profile_image_url_https"])

        print(f'{data["user"]["screen_name"]} / {os.path.join(root, f).replace("/Users/alexwlchan/Documents/backups/twitter", "")}')
        try:
            download_profile_image(data["user"])
        except Exception:
            continue
