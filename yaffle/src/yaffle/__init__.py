# -*- encoding: utf-8
"""
Usage: yaffle report
       yaffle -h | --help
"""

import docopt

from yaffle.indexer import index_document
from yaffle.reporter import print_report


def main():
    args = docopt.docopt(__doc__)

    if args['report']:
        print_report()
