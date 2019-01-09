#!/usr/bin/env python
# -*- encoding: utf-8

import json
import sys

import boto3

client = boto3.client("route53")

paginator = client.get_paginator("list_resource_record_sets")

for page in paginator.paginate(HostedZoneId=sys.argv[1]):
    for record_set in page["ResourceRecordSets"]:
        print(json.dumps(record_set))
