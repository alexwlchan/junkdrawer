#!/usr/bin/env python
# -*- encoding: utf-8

import boto3
import termcolor


def draw_chart(data):
    max_value = max(count for _, count in data)
    increment = max_value / 25

    longest_label_length = max(len(label) for label, _ in data)

    for label, count in data:

        # The ASCII block elements come in chunks of 8, so we work out how
        # many fractions of 8 we need.
        # https://en.wikipedia.org/wiki/Block_Elements
        bar_chunks, remainder = divmod(int(count * 8 / increment), 8)

        # First draw the full width chunks
        bar = '█' * bar_chunks

        # Then add the fractional part.  The Unicode code points for
        # block elements are (8/8), (7/8), (6/8), ... , so we need to
        # work backwards.
        if remainder > 0:
            bar += chr(ord('█') + (8 - remainder))

        # If the bar is empty, add a left one-eighth block
        bar = bar or  '▏'

        color = {
            "Accepted": "yellow",
            "Failed": "red",
            "Completed": "green",
            "Processing": "yellow",
        }[label]

        if count == 0:
            color = "grey"

        print(
            termcolor.colored(
                f'{label.ljust(longest_label_length).lower()}  {count:#4d} {bar}',
                color
            )
        )


data = {
    "Accepted": 0,
    "Failed": 0,
    "Completed": 0,
    "Processing": 0,
}

dynamodb = boto3.client("dynamodb")
paginator = dynamodb.get_paginator("scan")

for page in paginator.paginate(TableName="storage-ingests"):
    for item in page["Items"]:
        status = item["payload"]["M"]["status"]["S"]
        if status == "Failed":
            print(item["id"]["S"])
        data[status] += 1


if all(v == 0 for v in data.values()):
    print("No ingests!")
else:
    draw_chart(
        [(label, data[label]) for label in ["Accepted", "Processing", "Completed", "Failed"]]
    )
