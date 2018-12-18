#!/usr/bin/env python
# -*- encoding: utf-8

from requests_oauthlib import OAuth1Session

from birdsite import TwitterCredentials

credentials = TwitterCredentials.from_path("auth.json")

auth = OAuth1Session(
    client_key=credentials.consumer_key,
    client_secret=credentials.consumer_secret,
    resource_owner_key=credentials.access_token,
    resource_owner_secret=credentials.access_token_secret
)

sess = requests.Session()
sess.auth = auth

print(dir(auth))
