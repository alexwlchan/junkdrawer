#!/usr/bin/env python
# -*- encoding: utf-8

import collections
import datetime as dt
import json
import os
import re
import sys


ROOT = os.path.join(os.environ['HOME'], 'Dropbox', 'spending')

if len(sys.argv) >= 2:
    DAYS_TO_GET = int(sys.argv[1])
else:
    DAYS_TO_GET = 7


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
    for d, expenses in sorted(spending.items()):
        total = '%.2f' % sum(expenses)
        print('%s\t%s' % (d.strftime('%Y-%m-%d'), total.rjust(6)))

    print('\n')

    print('## Spending by tag ##')
    print('')
    for t, value in tagged_spending.most_common():
        total = '%.2f' % value
        print('%s\t%s' % (t.ljust(20), total.rjust(6)))
