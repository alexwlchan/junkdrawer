# -*- encoding: utf-8
"""Index a document in the Pince database."""

import datetime as dt
import json
import os
import re

import attr
from unidecode import unidecode

from pince.core import Document


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, dt.datetime):
            return obj.isoformat()
        if isinstance(obj, Document):
            return attr.asdict(obj)
        return json.JSONEncoder.default(self, obj)


def slugify(u):
    """Convert Unicode string into blog slug."""
    # Taken from http://www.leancrew.com/all-this/2014/10/asciifying/
    u = re.sub(u'[–—/:;,.]', '-', u)   # replace separating punctuation
    a = unidecode(u).lower()           # best ASCII substitutions, lowercased
    a = re.sub(r'[^a-z0-9 -]', '', a)  # delete any other characters
    a = a.replace(' ', '-')            # spaces to hyphens
    a = re.sub(r'-+', '-', a)          # condense repeated hyphens
    return a


def index_document(path, document):
    assert os.path.exists(path)
    document.path = os.path.join(
        str(document.date.year),
        document.date.strftime('%m-%d' + '_%s.pdf' % slugify(document.subject))
    )
    assert not os.path.exists(document.path)
    os.makedirs(os.path.dirname(document.path), exist_ok=True)
    os.rename(path, document.path)

    data = json.load(open('documents.json'))
    data.append(document)
    json_str = json.dumps(
        data, indent=2, sort_keys=True, cls=EnhancedJSONEncoder
    )
    open('documents.json', 'w').write(json_str)
