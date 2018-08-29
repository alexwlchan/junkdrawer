#!/usr/bin/env python
# -*- encoding: utf-8

import json
import sys

import boto3


if __name__ == '__main__':
    if len(sys.argv) == 2:
        table_name = sys.argv[1]
    else:
        print('Usage: dump_dynamodb_table.py <INDEX>', file=sys.stderr)
        sys.exit(1)

    dynamodb = boto3.client('dynamodb')
    paginator = dynamodb.get_paginator('scan')

    for page in paginator.paginate(TableName=table_name):
        for item in page['Items']:
            print(json.dumps(item))
