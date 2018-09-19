# -*- encoding: utf-8

import attr
import hcl


@attr.s
class TwitterCredentials:
    consumer_key = attr.ib()
    consumer_secret = attr.ib(repr=False)
    access_token = attr.ib()
    access_token_secret = attr.ib(repr=False)

    @classmethod
    def from_path(cls, path):
        data = hcl.load(open(path))
        return cls(**data)
