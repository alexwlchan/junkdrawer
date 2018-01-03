# -*- encoding: utf-8
"""
Usage: yaffle index <PATH> --date=<DATE> --subject=<SUBJECT> --from=<FROM>
       yaffle report
       yaffle -h | --help
"""

import dateutil.parser as dp
import docopt

from pince.core import Document
from pince.indexer import index_document
from pince.reporter import print_report


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
