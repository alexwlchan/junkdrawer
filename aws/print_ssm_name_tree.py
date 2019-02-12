#!/usr/bin/env python
# -*- encoding: utf-8

import os

import boto3

ssm_client = boto3.client("ssm")


def all_parameters(ssm_client):
    paginator = ssm_client.get_paginator("describe_parameters")

    for page in paginator.paginate():
        yield from page["Parameters"]


def pprint_nested_tree(tree, is_root=True):
    lines = []

    if is_root:
        lines.append(".")

    entries = sorted(tree.items())

    for i, (key, nested_tree) in enumerate(entries, start=1):
        if i == len(entries):
            lines.append("└── " + key)
            lines.extend([
                "    " + l for l in pprint_nested_tree(nested_tree, is_root=False)
            ])
        else:
            lines.append("├── " + key)
            lines.extend([
                "│   " + l for l in pprint_nested_tree(nested_tree, is_root=False)
            ])

    return lines


if __name__ == "__main__":
    ssm_client = boto3.client("ssm")

    all_names = [param["Name"] for param in all_parameters(ssm_client)]

    tree = {}

    for name in all_names:
        d = tree
        for component in name.strip("/").split("/"):
            try:
                d = d[component]
            except KeyError:
                d[component] = {}
                d = d[component]

    print("\n".join(pprint_nested_tree(tree)))
