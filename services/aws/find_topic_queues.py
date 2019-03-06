#!/usr/bin/env python
# -*- encoding: utf-8

import boto3

sns = boto3.client("sns")


def get_all_subscriptions():
    paginator = sns.get_paginator("list_subscriptions")

    for page in paginator.paginate():
        yield from page["Subscriptions"]


if __name__ == "__main__":
    for sub in get_all_subscriptions():
        print(("%s ~> %s" % (
            sub["TopicArn"].replace("arn:aws:sns:eu-west-1:975596993436:", ""),
            sub["Endpoint"].replace("arn:aws:sqs:eu-west-1:975596993436:", "")
        )).replace("_colbert", "").replace("_stewart", ""))
