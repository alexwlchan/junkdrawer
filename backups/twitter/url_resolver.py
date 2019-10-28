#!/usr/bin/env python
# -*- encoding: utf-8

import hyperlink
import requests


def resolve_url(url):
    parsed_url = hyperlink.URL.from_text(url)

    for key, _ in parsed_url.query:
        if key.startswith("utm_"):
            parsed_url = parsed_url.remove(key)

    if parsed_url.host not in {"bit.ly",}:
        return str(parsed_url)

    url = str(parsed_url)
    resp = requests.head(url)
    try:
        return resolve_url(resp.headers["Location"])
    except KeyError:
        return resolve_url(url)
