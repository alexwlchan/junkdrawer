#!/usr/bin/env python
# -*- encoding: utf-8

import configparser
import os
import sys

import boto3
import click


iam_client = boto3.client("iam")
sts_client = boto3.client("sts")


def get_credentials(*, account_id, account_name, role_name):
    resp = sts_client.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
        RoleSessionName=f"{role_name}@{account_name}"
    )

    return resp["Credentials"]


def update_config(*, account_name, credentials):
    aws_dir = os.path.join(os.environ["HOME"], ".aws")

    credentials_path = os.path.join(aws_dir, "credentials")
    config = configparser.ConfigParser()
    config.read(credentials_path)

    if account_name not in config.sections():
        config.add_section(account_name)

    assert account_name in config.sections()

    config[account_name]["aws_access_key_id"] = credentials["AccessKeyId"]
    config[account_name]["aws_secret_access_key"] = credentials["SecretAccessKey"]
    config[account_name]["aws_session_token"] = credentials["SessionToken"]

    config.write(open(credentials_path, "w"), space_around_delimiters=False)


@click.command()
@click.option("--account_id", required=True)
@click.option("--account_name")
@click.option("--role_name", required=True)
def assume_role(account_id, account_name, role_name):
    if account_name is None:
        account_name = account_id

    credentials = get_credentials(
        account_id=account_id,
        account_name=account_name,
        role_name=role_name
    )

    update_config(account_name=account_name, credentials=credentials)


if __name__ == '__main__':
    assume_role()
#
# resp = sts_client.assume_role(
#     RoleArn=sys.argv[1],
#     RoleSessionName=sys.argv[2]
# )
#
# from pprint import pprint
# pprint(resp)