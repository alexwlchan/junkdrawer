# -*- encoding: utf-8
"""
Usage: yaffle index <PATH> [--date=<DATE>] [--subject=<SUBJECT>] [--from=<FROM>]
       yaffle report
       yaffle -h | --help
"""

import dateutil.parser as dp
import docopt

from yaffle.indexer import index_document
from yaffle.models import Document
from yaffle.reporter import print_report


def main():
    args = docopt.docopt(__doc__)

    if args['index']:
        path = args['<PATH>']
        date = dp.parse(args['--date']).date()
        subject = args['--subject']
        sender = args['--from']

        document = Document(
            path=None,
            date=date,
            subject=subject,
            sender=sender
        )
        index_document(path=path, document=document)
        print(f'Successfully indexed {path}!')
    elif args['report']:
        print_report()
