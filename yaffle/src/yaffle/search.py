# -*- encoding: utf-8
"""Search for matching Yaffle-indexed documents.

Usage: {PROG} <SEARCH>
       {PROG} -h | --help
       {PROG} --version
"""

import os
import sys
import tempfile

import docopt
from elasticsearch import Elasticsearch

from yaffle.version import __version__


def search_documents():
    args = docopt.docopt(
        __doc__.format(PROG=os.path.basename(sys.argv[0])),
        version=__version__
    )

    query = args['<SEARCH>']

    es = Elasticsearch(hosts=['http://localhost:9200'])
    resp = es.search(
        index='yaffle',
        doc_type='yaffle',
        body={
            'query': {
                'simple_query_string': {'query': query}
            },
            'highlight': {
                'fields': {
                    'text': {}
                }
            }
        })

    f = tempfile.mktemp()
    with open(f, 'w') as fp:
        for i, hit in enumerate(resp['hits']['hits'], start=1):
            src = hit['_source']
            fp.write(f'subject: {src["subject"]}\n')
            fp.write(f'sender:  {src["sender"]}\n')
            fp.write(f'date:    {src["date"]}\n')
            fp.write(f'path:    {src["path"]}\n')

            try:
                fp.write('\n')
                fp.write(
                    (' ... '.join(hit['highlight']['text']))
                    .replace('<em>', '\033[91m')
                    .replace('</em>', '\033[0m') + '\n'
                )
            except KeyError:
                pass

            if i != len(resp['hits']['hits']):
                fp.write('\n~ ~ ~\n\n')

    os.system(f'cat {f} | less -R')
