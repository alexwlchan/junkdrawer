#!/usr/bin/env python
# -*- encoding: utf-8

import json
from urllib.parse import urlparse, urlencode, urlunparse


parts = [
    'x-drafts4',
    'x-callback-url',
    '/import_action',

    # params
    '',

    urlencode({
        'actionSteps': ['[\n  {\n    "scriptText" : "\\/\\/ The expected format of a spending\\n\\/\\/ entry is a three-line draft:\\n\\/\\/\\n\\/\\/     (amount)\\n\\/\\/     (tags, space separated)\\n\\/\\/     (description, may be multi-line)\\n\\/\\/\\ncomponents = draft\\n  .content\\n  .split(\\"\\\\n\\", limit = 3);\\n\\nif (components.length !== 3) {\\n  alert(\\"Not enough lines in the budget!\\");\\n  stopAction();\\n}\\n\\n\\/\\/ Build the JSON blob which is to be\\n\\/\\/ stored in Dropbox.\\namount = parseFloat(components[0]);\\ntags = components[1]\\n  .toLowerCase()\\n  .split(\\" \\")\\n  .sort();\\ndescription = components[2];\\n\\ndate_created = draft.createdDate;\\n\\ndata = {\\n  \\"amount\\": amount,\\n  \\"tags\\": tags,\\n  \\"description\\": description,\\n  \\"date_created\\": date_created,\\n}\\n\\ndraft.content = JSON.stringify(\\n  data, replace = null, space = 2\\n);\\ncommit(draft);",\n    "actionStepType" : "Script"\n  },\n  {\n    "writeType" : "create",\n    "fileTemplate" : "[[draft]]",\n    "actionStepType" : "Dropbox",\n    "folderTemplate" : "\\/spending\\/[[date|%Y]]\\/[[date|%m]]\\/[[date|%d]]",\n    "fileExtTemplate" : "json",\n    "fileNameTemplate" : "[[uuid]]"\n  }\n]'],
        'shouldConfirm': ['0'],
        'uuid': ['5F62BCA9-A01D-4804-82D3-2DF126ACED8E'],
        'logLevel': ['1'],
        'name': ['Record spending'],
        'tintColor': ['[\n  0.27500000596046448,\n  0.75700002908706665,\n  0.21600000560283661\n]'],
        'modifiedAt': ['2018-04-28 07:33:47 +0000'],
        'disposition': ['2'],
        'v': ['2'],
        'iconImageName': ['454-pounds2'],
        'description': ['Take a spending entry, convert it into a JSON file, and save it to Dropbox.']
    }),

    # fragment
    '',
]

print(urlunparse(parts))
