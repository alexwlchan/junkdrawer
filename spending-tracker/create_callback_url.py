#!/usr/bin/env python
# -*- encoding: utf-8

import datetime as dt
import json
from urllib.parse import urlparse, urlencode, urlunparse


action_steps = [
    {
        'actionStepType': 'Script',
        'scriptText': open('prepare_entry.js').read(),
    },
    {
        'fileTemplate': '[[draft]]',
        'fileExtTemplate': 'json',
        'fileNameTemplate': '[[uuid]]',
        'folderTemplate': '/spending/[[date|%Y]]/[[date|%m]]/[[date|%d]]',
        'writeType': 'create',
        'actionStepType': 'Dropbox',
    },
]


parts = [
    'x-drafts4',
    'x-callback-url',
    '/import_action',

    # params
    '',

    urlencode({
        'actionSteps': [json.dumps(action_steps)],
        'shouldConfirm': ['0'],
        'uuid': ['5F62BCA9-A01D-4804-82D3-2DF126ACED8E'],
        'logLevel': ['1'],
        'name': ['Record spending'],
        'tintColor': [
            json.dumps([0.27500000596046448, 0.75700002908706665, 0.21600000560283661])
        ],
        'modifiedAt': [dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0000')],
        'disposition': ['2'],
        'v': ['2'],
        'iconImageName': ['454-pounds2'],
        'description': ['Take a spending entry, convert it into a JSON file, and save it to Dropbox.']
    }),

    # fragment
    '',
]

print(urlunparse(parts))
