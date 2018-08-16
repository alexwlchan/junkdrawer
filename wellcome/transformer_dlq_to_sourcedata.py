#!/usr/bin/env python
# -*- encoding: utf-8
"""
Usage: transformer_dlq_to_sourcedata.py <PATH>
"""

import json

import boto3
import docopt


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    path = args['<PATH>']

    jl = json.loads

    s3 = boto3.client('s3')

    for line in open(path):
        message = jl(jl(jl(line)['Body'])['Message'])

        if message['sourceName'] == 'sierra':
            bucket = 'wellcomecollection-vhs-sourcedata-sierra'
        else:
            assert False, message

        body = s3.get_object(Bucket=bucket, Key=message['s3key'])['Body']
        contents = body.read().decode('utf8')
        print(contents)
