#!/usr/bin/env python
"""
Find the CPU/memory bottlenecks in an ECS cluster.

This script will look for ECS clusters in your AWS account, ask you to pick
one, then show you peak CPU/memory utilisation over the last 24 hours.
It's a good way to identify apps that might be under-provisioned, and benefit
from being given more resources.

Python 3.6+.
"""

import datetime
import os

import boto3
import inquirer
import termcolor


cloudwatch = boto3.client("cloudwatch")
ecs = boto3.client("ecs")


def _get_max_metric_value(
    *, metric_name, cluster_name, service_name, start_time, end_time
):
    """
    Look up the maximum value of an ECS metric over the last 24 hours.
    """
    resp = cloudwatch.get_metric_statistics(
        Namespace="AWS/ECS",
        MetricName=metric_name,
        Dimensions=[
            {"Name": "ClusterName", "Value": cluster_name},
            {"Name": "ServiceName", "Value": service_name},
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=["Maximum"],
    )

    try:
        return max(dp["Maximum"] for dp in resp["Datapoints"])
    except ValueError:
        return 0.0


def get_max_cpu_utilisation(**kwargs):
    return _get_max_metric_value(metric_name="CPUUtilization", **kwargs)


def get_max_memory_utilisation(**kwargs):
    return _get_max_metric_value(metric_name="MemoryUtilization", **kwargs)


def list_services(cluster):
    """Generates the ARN of every service in an ECS cluster."""
    paginator = ecs.get_paginator("list_services")

    for page in paginator.paginate(cluster=cluster):
        yield from page["serviceArns"]


def list_clusters():
    """Generates the ARN of every ECS cluster in an account."""
    paginator = ecs.get_paginator("list_clusters")

    for page in paginator.paginate():
        yield from page["clusterArns"]


def choose_cluster():
    """
    Get a list of the ECS clusters running in this account, and choose
    one to inspect – possibly asking the user to choose from a list.
    """
    all_clusters = list(list_clusters())

    if len(all_clusters) == 0:
        raise RuntimeException("No ECS clusters found in account!")
    elif len(all_clusters) == 1:
        return all_clusters[0]
    else:
        # AWS cluster ARNs are of the form
        #
        #       arn:aws:ecs:eu-west-1:{account_id}:cluster/{cluster_name}
        #
        # Although we'll use the full cluster ARN to list the services it
        # contains, we can ask the user to select a cluster based on the
        # names alone.
        clusters = {
            cluster_arn.split("/")[-1]: cluster_arn for cluster_arn in all_clusters
        }

        question = inquirer.List(
            "cluster_name",
            message="Which cluster do you want to inspect?",
            choices=sorted(clusters.keys()),
        )

        answers = inquirer.prompt([question])
        cluster_name = answers["cluster_name"]
        return clusters[cluster_name]


def draw_bar_chart(data):
    # A lot of our services have a common prefix in the name, e.g. everything
    # in the storage-prod cluster is called storage-prod_register,
    # storage-prod_replicator, and so on.
    #
    # While helpful for disambiguating in absolute terms, it's visual noise here.
    # Remove any common prefix.
    common_label_prefix = os.path.commonprefix([label for label, _ in data])
    data = [
        (label[len(common_label_prefix) :].lstrip("-").lstrip("_"), value)
        for label, value in data
    ]

    # The values are percentages so should max out at 100, but somewhere
    # in CloudWatch they occasionally come out as slightly over 100.
    # Treat the top value as 110 to allow a bit of slop.
    max_value = 110.0

    increment = max_value / 25

    longest_label_length = max(len(label) for label, _ in data)

    for label, count in sorted(data):

        # The ASCII block elements come in chunks of 8, so we work out how
        # many fractions of 8 we need.
        # https://en.wikipedia.org/wiki/Block_Elements
        bar_chunks, remainder = divmod(int(count * 8 / increment), 8)

        # First draw the full width chunks
        bar = "█" * bar_chunks

        # Then add the fractional part.  The Unicode code points for
        # block elements are (8/8), (7/8), (6/8), ... , so we need to
        # work backwards.
        if remainder > 0:
            bar += chr(ord("█") + (8 - remainder))

        # If the bar is empty, add a left one-eighth block
        bar = bar or "▏"

        line = f"{label.ljust(longest_label_length)} ▏ {count:#5.1f}% {bar}"

        if count > 95:
            print(termcolor.colored(line, "red"))
        else:
            print(line)


if __name__ == "__main__":
    cluster_arn = choose_cluster()

    cpu_stats = []
    memory_stats = []

    cluster_name = cluster_arn.split("/")[-1]

    now = datetime.datetime.now()
    start_time = now - datetime.timedelta(hours=1)

    for service_arn in list_services(cluster=cluster_name):
        # AWS service ARNs are of the form
        #
        #       arn:aws:ecs:eu-west-1:{account_id}:service/{service_name}
        #
        # We only want the service name for the CloudWatch metric.
        service_name = service_arn.split("/")[-1]

        max_cpu = get_max_cpu_utilisation(
            cluster_name=cluster_name,
            service_name=service_name,
            start_time=start_time,
            end_time=now,
        )
        cpu_stats.append((service_name, max_cpu))

        max_memory = get_max_memory_utilisation(
            cluster_name=cluster_name,
            service_name=service_name,
            start_time=start_time,
            end_time=now,
        )
        memory_stats.append((service_name, max_memory))

    print("=== CPU stats ===")
    draw_bar_chart(cpu_stats)

    print("")

    print("=== Memory stats ===")
    draw_bar_chart(memory_stats)
