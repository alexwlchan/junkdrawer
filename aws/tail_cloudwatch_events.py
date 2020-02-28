#!/usr/bin/env python
"""
The Archivematica CloudWatch logs are very chatty until something breaks, at
which point you get a traceback and then all output stops.

This script acts as like "tail" for CloudWatch -- just shows you the last 10 seconds
of events, which usually has enough detail to debug the issue.

"""

import datetime
import sys

import boto3
import humanize
import inquirer
import iterfzf


def get_log_group_names(client):
    paginator = client.get_paginator("describe_log_groups")

    for page in paginator.paginate():
        for log_group in page["logGroups"]:
            yield log_group["logGroupName"]


def get_log_streams(client, *, log_group_name):
    paginator = client.get_paginator("describe_log_streams")

    for page in paginator.paginate(
        logGroupName=log_group_name, orderBy="LastEventTime", descending=True
    ):
        yield from page["logStreams"]


def get_last_ten_seconds_from_stream(client, *, log_group_name, log_stream):
    # This timestamp is milliseconds since the epoch, so to wind back 10 seconds
    # is 10 * 1000 milliseconds.
    start_time = log_stream["lastEventTimestamp"] - 10 * 1000

    paginator = client.get_paginator("filter_log_events")

    for page in paginator.paginate(
        logGroupName=log_group_name,
        logStreamNames=[log_stream["logStreamName"]],
        startTime=start_time,
    ):
        yield from page["events"]


if __name__ == "__main__":
    client = boto3.client("logs")

    try:
        log_group_name = sys.argv[1]
    except IndexError:
        log_group_name = iterfzf.iterfzf(
            get_log_group_names(client), prompt="What log group do you want to tail? "
        )

    all_streams = get_log_streams(client, log_group_name=log_group_name)

    choices = {}
    for _ in range(5):
        stream = next(all_streams)
        dt = datetime.datetime.fromtimestamp(stream["lastEventTimestamp"] / 1000)
        name = stream["logStreamName"]
        choices[f"{name} ({humanize.naturaltime(dt)})"] = stream

    questions = [
        inquirer.List(
            "log_stream_id",
            message="Which log stream would you like to tail?",
            choices=choices,
        )
    ]

    answers = inquirer.prompt(questions)

    log_stream = choices[answers["log_stream_id"]]

    for event in get_last_ten_seconds_from_stream(
        client, log_group_name=log_group_name, log_stream=log_stream
    ):
        print(event["message"])
