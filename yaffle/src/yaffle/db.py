# -*- encoding: utf-8

import json

from yaffle.models import YaffleJSONEncoder

DB_NAME = 'yaffle_documents.json'


def read_db():
    try:
        return json.load(open(DB_NAME))
    except FileNotFoundError:
        return {}


def write_db(documents):
    json_str = json.dumps(
        documents, indent=2, sort_keys=True, cls=YaffleJSONEncoder
    )
    open(DB_NAME, 'w').write(json_str)
