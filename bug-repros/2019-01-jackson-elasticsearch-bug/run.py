#!/usr/bin/env python
# -*- encoding: utf-8

import secrets

import requests


INDEX_NAME = secrets.token_hex(8)
print("Index name is %s" % INDEX_NAME)


requests.put("http://localhost:9200/%s" % INDEX_NAME).raise_for_status()

resp = requests.get(
    "http://localhost:9200/%s/_search" % INDEX_NAME,
    json={"from": -10}
)
print(resp.text)
