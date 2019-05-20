#!/usr/bin/env python
# -*- encoding: utf-8

import os
import pathlib
import subprocess
import sys

import boto3


sts = boto3.client("sts")


def get_ec2_client(account_id):
    resp = sts.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/developer",
        RoleSessionName=f"alexwlchan_{os.path.basename(__file__)}"
    )
    sess = boto3.Session(
        aws_access_key_id=resp["Credentials"]["AccessKeyId"],
        aws_secret_access_key=resp["Credentials"]["SecretAccessKey"],
        aws_session_token=resp["Credentials"]["SessionToken"],
    )

    return sess.client("ec2")


if __name__ == "__main__":
    try:
        instance_dns = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <INSTANCE_DNS>")

    for account_id, key_name in [
        ("975596993436", "wellcomedigitalstorage"),
        ("299497370133", "wellcomedigitalworkflow"),
        ("760097843905", "wellcomedigitalplatform"),
    ]:
        client = get_ec2_client(account_id)
        resp = client.describe_instances(
            Filters=[
                {
                    "Name": "dns-name",
                    "Values": [instance_dns],
                }
            ]
        )

        if resp["Reservations"]:
            print(f"Attempting to use key {key_name}")
            try:
                subprocess.check_call([
                    "ssh",
                    "-i", pathlib.Path.home() / ".ssh" / key_name,
                    f"ec2-user@{instance_dns}"
                ])
            except subprocess.CalledProcessError as err:
                sys.exit(err.returncode)

    else:
        sys.exit(f"Could not find the AWS account with {instance_dns}")
