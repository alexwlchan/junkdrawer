# -*- encoding: utf-8

import datetime as dt

import attr


@attr.s
class Document:
    path = attr.ib()
    date = attr.ib()
    subject = attr.ib()
    sender = attr.ib()
    date_scanned = attr.ib(default=lambda: dt.datetime.now())
