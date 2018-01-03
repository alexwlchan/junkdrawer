# -*- encoding: utf-8
"""Index a document in the Yaffle database.

Usage: {PROG} <PATH> [--date=<DATE>] [--subject=<SUBJECT>] [--from=<FROM>]
       {PROG} -h | --help
       {PROG} --version
"""

import datetime as dt
import json
import os
import re
import sys

import attr
import dateutil.parser as dp
import docopt
from unidecode import unidecode

from yaffle import db
from yaffle.models import Document, YaffleJSONEncoder
from yaffle.version import __version__


def slugify(u):
    """Convert Unicode string into blog slug."""
    # Taken from http://www.leancrew.com/all-this/2014/10/asciifying/
    u = re.sub(u'[–—/:;,.]', '-', u)   # replace separating punctuation
    a = unidecode(u).lower()           # best ASCII substitutions, lowercased
    a = re.sub(r'[^a-z0-9 -]', '', a)  # delete any other characters
    a = a.replace(' ', '-')            # spaces to hyphens
    a = re.sub(r'-+', '-', a)          # condense repeated hyphens
    return a


def index_document():
    args = docopt.docopt(
        __doc__.format(PROG=os.path.basename(sys.argv[0])),
        version=__version__
    )

    path = args['<PATH>']

    if args['--date']:
        date_str = args['--date']
    else:
        date_str = input('\nWhen was this document sent?\n> ')
    date = dp.parse(date_str).date()

    if args['--subject']:
        subject = args['--subject']
    else:
        subject = input('\nWhat is the subject of this document?\n> ')

    if args['--from']:
        sender = args['--from']
    else:
        sender = input('\nWho sent this document?\n> ')

    slug = '__'.join([
        date.strftime('%Y-%m-%d'),
        slugify(sender),
        slugify(subject)
    ])
    doc = Document(
        path=os.path.join(str(date.year), slug),
        date=date,
        subject=subject,
        sender=sender
    )

    assert os.path.exists(path)
    assert not os.path.exists(doc.path)

    documents = db.read_db()
    assert slug not in documents
    documents[slug] = doc
    db.write_db(documents=documents)

    os.makedirs(os.path.dirname(doc.path), exist_ok=True)
    os.rename(path, doc.path)
