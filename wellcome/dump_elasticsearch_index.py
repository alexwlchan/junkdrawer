#!/usr/bin/env python
# -*- encoding: utf-8

import subprocess
import sys

import boto3
import hcl


if __name__ == '__main__':
    if len(sys.argv) == 2:
        index_name = sys.argv[1]
    else:
        print('Usage: dump_elasticsearch_index.py <INDEX>', file=sys.stderr)
        sys.exit(1)

    s3 = boto3.client('s3')
    tfvars_body = s3.get_object(
        Bucket='wellcomecollection-platform-infra',
        Key='terraform.tfvars'
    )['Body'].read()

    tfvars = hcl.loads(tfvars_body)

    es_credentials = tfvars['es_cluster_credentials']

    subprocess.check_call([
        'docker', 'run', '--rm',
        'taskrabbit/elasticsearch-dump',
        '--input', f'https://{es_credentials["username"]}:{es_credentials["password"]}@{es_credentials["name"]}.{es_credentials["region"]}.aws.found.io:{es_credentials["port"]}/',
        '--input-index', index_name,
        '--output', '$',
        '--limit', '1000',
    ])
