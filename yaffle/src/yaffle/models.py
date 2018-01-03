# -*- encoding: utf-8

import datetime as dt
import json

import attr


@attr.s
class Document:
    path = attr.ib()
    date = attr.ib()
    subject = attr.ib()
    sender = attr.ib()
    date_scanned = attr.ib(default=dt.datetime.now())

    @property
    def text_path(self):
        return self.path + '.txt'

    def text(self):
        try:
            return open(self.text_path).read()
        except FileNotFoundError:
            return None


class YaffleJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (dt.datetime, dt.date)):
            return obj.isoformat()
        if isinstance(obj, Document):
            return attr.asdict(obj)
        return json.JSONEncoder.default(self, obj)
