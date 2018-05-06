#!/usr/bin/env python
# -*- encoding: utf-8

import collections
import datetime as dt
import json
import math
import os
import re
import sys


ROOT = os.path.join(os.environ['HOME'], 'Dropbox', 'spending')

if len(sys.argv) >= 2:
    DAYS_TO_GET = int(sys.argv[1])
else:
    DAYS_TO_GET = 14


if __name__ == '__main__':
    spending = {
        (dt.datetime.now() - dt.timedelta(days=x)).date(): []
        for x in range(DAYS_TO_GET + 1)
    }

    tagged_spending = collections.Counter()

    for root, _, filenames in os.walk(ROOT):

        # Check we're in a YYYY/MM/DD directory
        if not re.search(r'\d{4}/\d{2}/\d{2}$', root):
            continue

        date_string = root[-len('DDDD/DD/DD'):]
        date = dt.datetime.strptime(date_string, '%Y/%m/%d').date()

        if (dt.datetime.now().date() - date).days > DAYS_TO_GET:
            continue

        for f in filenames:
            path = os.path.join(root, f)
            data = json.load(open(path))
            spending[date].append(data['amount'])
            for t in data['tags']:
                tagged_spending[t] += data['amount']


    print('')
    print('## Spending by day ##')
    print('')
    max_spend = max(sum(v) for v in spending.values())
    increment = max_spend / 20

    for d, expenses in sorted(spending.items()):
        total = '%3.2f' % sum(expenses)
        units = int(math.floor(sum(expenses) / increment))
        print('%s\t%s\t%s' % (
            d.strftime('%Y-%m-%d'),
            total.rjust(6),
            u'█' * units or '▏'))

    print(
        ' ' * 16 +
        ('%.2f' % sum(sum(v) for v in spending.values())).rjust(6)
    )

    print('\n')

    print('## Spending by tag ##')
    print('')
    max_spend = max(sum(v) for v in spending.values())
    increment = max_spend / 20

    for t, value in tagged_spending.most_common(20):
        total = '%.2f' % value
        units = int(math.floor(value / increment))
        print('%s\t%s\t%s' % (
            t.ljust(20),
            total.rjust(6),
            u'█' * units or u'▏'))
