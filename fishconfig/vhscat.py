#!/usr/bin/env python
# -*- encoding: utf-8

import json
import pprint
import subprocess
import sys

import boto3


def hostname():
    return subprocess.check_output(['hostname']).strip().decode('utf8')


if __name__ == '__main__':
    if hostname() in ('Alexs-iMac.local',):
        import os
        os.environ.update({'AWS_PROFILE': 'wellcome'})

    try:
        vhs_id = sys.argv[1]
    except IndexError:
        sys.exit(f'Usage: {__file__} <VHS_ID>')

    dynamodb = boto3.client('dynamodb')
    item = dynamodb.get_item(
        TableName='SourceData',
        Key={
            'id': {'S': vhs_id}
        }
    )
    s3key = item['Item']['s3key']['S']

    s3 = boto3.client('s3')
    body = s3.get_object(
        Bucket='wellcomecollection-vhs-sourcedata',
        Key=s3key
    )['Body']

    payload = json.loads(body.read())
    if payload.get('sourceName') == 'sierra':
        payload['maybeBibData']['data'] = json.loads(payload['maybeBibData']['data'])
        payload['itemData'] = {
            k: json.loads(v) for k, v in payload['itemData'].items()
        }

    print(json.dumps(payload, indent=2, sort_keys=True))
