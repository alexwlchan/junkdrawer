#!/usr/bin/env python
# -*- encoding: utf-8
"""
Some snippets for analysing queues when we were trying to identify leaks
in the pipeline.

We'd use an SQS freezeray to dump the entire contents of a queue to a
series of files (multiple files -- multiple freezerays running in parallel),
then try to ID unique keys.

These snippets are intended for copy/pasting into a Jupyter notebook.
"""


def get_messages(dir_path):
    """
    Given a directory of freezeray outputs, generate a dict for every
    SQS message.
    """
    import os, json

    jl = json.loads

    for f in os.listdir(dir_path):
        if f.startswith('.'):
            continue
        for line in open(os.path.join(dir_path, f)):
            # Unpacking several levels because our SQS messages are really
            # SNS notifications, and we care about the 'inner' message.
            yield jl(jl(jl(line)['Body'])['Message'])


def uniq_id_minter_messages(dir_path):
    """
    Return a set of unique ID minter messages.  These are S3 keys for
    merged works, so we can only get the S3 keys, not individual IDs.

    Example message:

        {
          'src': {
            'namespace': 'wellcomecollection-platform-messages',
            'key': 'catalogue_pipeline_merged_works/2018/07/23/8270db1b'
          }
        }

    """
    return {
        m['src']['key'] for m in get_messages(dir_path)
    }


def uniq_merger_messages(dir_path):
    """
    Return a set of unique merger queue identifiers.  Output comes from
    the matcher:

        {
          'works': [
            {
              'identifiers': [
                {
                  'identifier': 'miro-image-number/L0043794',
                  'version': 50
                }
              ]
            }
          ]
        }

    We were working with Miro works, which never get merged, so we didn't
    have to do anything fiddly to iterate over works/identifiers.

    """
    return {
        m['works'][0]['identifiers'][0]['identifier'].split('/')[1]
        for m in get_messages(dir_path)
    }


def uniq_recorder_messages(dir_path):
    """
    Return a set of unique recorder S3 keys.  Output comes from
    the transformer:

        {
          'src': {
            'namespace': 'wellcomecollection-platform-messages',
            'key': 'catalogue_pipeline_transformed_works/2018/07/23/8270db1b'
          }
        }

    We were working with Miro works, which never get merged, so we didn't
    have to do anything fiddly to iterate over works/identifiers.

    """
    return {
        m['src']['key'] for m in get_messages(dir_path)
    }


def uniq_transformer_messages(dir_path):
    """
    Return a set of unique transformer messages.  Output comes from
    Dynamo to SNS for SourceData:

        {
          'sourceId': 'V0019832',
          's3key': 'miro/23/V0019832/0.json',
          'reindexVersion': 1532350967,
          'id': 'miro/V0019832',
          'sourceName': 'miro',
          'version': 51,
          'reindexShard': 'miro/50'
        }

    """
    return {
        m['sourceId'] for m in get_messages(dir_path)
    }


def record_dynamodb_ids(table_name='vhs-catalogue-pipeline-Recorder'):
    """
    Return a set of unique IDs in the recorder table.
    """
    import boto3

    ddb = boto3.client('dynamodb')

    paginator = ddb.get_paginator('scan')

    ids = set()
    for page in paginator.paginate(TableName=table_name):
        for item in page['Items']:
            ids.add(item['id']['S'])
    return ids
