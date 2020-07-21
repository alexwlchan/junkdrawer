#!/usr/bin/env python

import collections
import concurrent.futures

import boto3
from flask import Flask, render_template
import humanize


app = Flask(__name__)

sqs_client = boto3.client("sqs")


@app.template_filter("intcomma")
def intcomma(s):
    return humanize.intcomma(s)


def get_queue_urls():
    paginator = sqs_client.get_paginator("list_queues")

    for page in paginator.paginate():
        yield from page["QueueUrls"]


def get_queue_stats(queue_url):
    return sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=["All"])


def message_count(queue_attributes):
    return (
        int(queue_attributes["Attributes"]["ApproximateNumberOfMessages"]) +
        int(queue_attributes["Attributes"]["ApproximateNumberOfMessagesDelayed"]) +
        int(queue_attributes["Attributes"]["ApproximateNumberOfMessagesNotVisible"])
    )


def dashboard_url(queue_attributes):
    queue_arn = queue_attributes["Attributes"]["QueueArn"]
    _, _, _, region, account_id, name = queue_arn.split(":")
    return f"https://{region}.console.aws.amazon.com/sqs/v2/home?region={region}#/queues/https%3A%2F%2Fsqs.{region}.amazonaws.com%2F{account_id}%2F{name}"


@app.template_filter("is_empty")
def is_empty(queue_data):
    return (not queue_data["queue"]) and (not queue_data["dlq"])


@app.route("/")
def index():
    queue_urls = list(get_queue_urls())

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(get_queue_stats, queue_urls))

    display_results = collections.defaultdict(
        lambda: {"url": None, "dlq_url": None, "queue": None, "dlq": None}
    )

    for q_attributes in results:
        queue_name = q_attributes["Attributes"]["QueueArn"].split(":")[-1]

        if queue_name.endswith("_dlq"):
            display_results[queue_name.replace("_dlq", "")]["dlq"] = message_count(q_attributes)
            display_results[queue_name.replace("_dlq", "")]["dlq_url"] = dashboard_url(q_attributes)
        else:
            display_results[queue_name]["queue"] = message_count(q_attributes)
            display_results[queue_name]["url"] = dashboard_url(q_attributes)

    return render_template(
        "sqs_dashboard.html",
        display_results=display_results,
        results=sorted(results, key=lambda r: r["Attributes"]["QueueArn"])
    )


if __name__ == "__main__":
    app.run(port=3552, debug=True)
