# -*- encoding: utf-8
"""Give a report of documents in the Pince database."""

import json

from tabulate import tabulate

from yaffle.models import Document


def print_report():
    data = json.load(open('documents.json'))
    documents = [Document(**d) for d in data]
    documents.sort(key=lambda d: d.date)
    rows = [
        [d.subject, d.sender, d.date, d.path]
        for d in documents
    ]
    print(tabulate(rows))
