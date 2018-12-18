#!/usr/bin/env python
# -*- encoding: utf-8

from requests_oauthlib import OAuth1Session

from birdsite import TwitterCredentials


def create_session(credentials):
    sess = OAuth1Session(
        client_key=credentials.consumer_key,
        client_secret=credentials.consumer_secret,
        resource_owner_key=credentials.access_token,
        resource_owner_secret=credentials.access_token_secret
    )

    # Raise an exception on any responses that don't return a 200 OK.

    def raise_for_status(resp, *args, **kwargs):
        resp.raise_for_status()

    sess.hooks["response"].append(raise_for_status)

    # Allow making GET requests without supplying the full API URL; just
    # the API endpoint path.

    orig_get = sess.get

    def get(path, *args, **kwargs):
        return orig_get("https://api.twitter.com/1.1" + path, *args, **kwargs)

    sess.get = get

    return sess


credentials = TwitterCredentials.from_path("auth.json")
sess = create_session(credentials)
print(sess.get("/account/settings.json"))