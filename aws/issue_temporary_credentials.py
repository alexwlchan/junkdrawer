#!/usr/bin/env python
# -*- encoding: utf-8

import configparser
import os
import sys

import boto3
import click


def get_credentials(*, account_id, role_name):
    iam_client = boto3.client("iam")
    sts_client = boto3.client("sts")

    username = iam_client.get_user()["User"]["UserName"]

    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
    role_session_name = f"{username}@{role_name}.{account_id}"

    resp = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name
    )

    return resp["Credentials"]


def update_credentials_file(*, profile_name, credentials):
    aws_dir = os.path.join(os.environ["HOME"], ".aws")

    credentials_path = os.path.join(aws_dir, "credentials")
    config = configparser.ConfigParser()
    config.read(credentials_path)

    if profile_name not in config.sections():
        config.add_section(profile_name)

    assert profile_name in config.sections()

    config[profile_name]["aws_access_key_id"] = credentials["AccessKeyId"]
    config[profile_name]["aws_secret_access_key"] = credentials["SecretAccessKey"]
    config[profile_name]["aws_session_token"] = credentials["SessionToken"]

    config.write(open(credentials_path, "w"), space_around_delimiters=False)


@click.command()
@click.option("--account_id", required=True)
@click.option("--role_name", required=True)
@click.option("--profile_name")
def save_assumed_role_credentials(account_id, role_name, profile_name):
    if profile_name is None:
        profile_name = account_id

    credentials = get_credentials(
        account_id=account_id,
        role_name=role_name
    )

    update_credentials_file(profile_name=profile_name, credentials=credentials)


if __name__ == "__main__":
    save_assumed_role_credentials()
