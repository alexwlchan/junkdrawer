# -*- encoding: utf-8

import requests
from requests.auth import AuthBase


class PinboardAuth(AuthBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, req):
        req.prepare_url(req.url, params={"auth_token": self.api_key, "format": "json"})
        return req


def create_session(api_key):
    sess = requests.Session()

    def raise_for_status(resp, *args, **kwargs):
        resp.raise_for_status()

    sess.hooks["response"].append(raise_for_status)

    sess.auth = PinboardAuth(api_key=api_key)

    return sess
