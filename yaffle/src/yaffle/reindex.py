# -*- encoding: utf-8
"""Reindex the Yaffle database in Elasticsearch.

Usage: {PROG}
       {PROG} -h | --help
       {PROG} --version
"""

import os
import sys

import docopt
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import requests

from yaffle import db
from yaffle.models import Document
from yaffle.version import __version__


def reindex_all():
    args = docopt.docopt(
        __doc__.format(PROG=os.path.basename(sys.argv[0])),
        version=__version__
    )

    resp = requests.delete('http://localhost:9200/yaffle')
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        if resp.status_code != 404:
            raise

    documents = db.read_db()

    def _actions():
        for d_id, d_data in documents.items():
            doc = Document(**d_data)
            data = {
                '_op_type': 'index',
                '_index': 'yaffle',
                '_type': 'yaffle',
                '_id': d_id,
            }
            data.update(**d_data)
            data['text'] = doc.text()
            yield data

    resp = bulk(
        client=Elasticsearch(hosts=['http://localhost:9200']),
        actions=_actions()
    )
    assert resp[0] == len(documents)
