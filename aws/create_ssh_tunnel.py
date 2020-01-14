#!/usr/bin/env python
# -*- encoding: utf-8
"""
Slightly ropey script for creating SSH tunnels into AWS.

We run our EC2 instances behind a bastion host.  If you want to SSH into
an instance, you have to SSH into the bastion host first.  Only the bastion
is accessible to the outside world, not the inner instances:

                       +-----------------------------+
                       |                             |
    (user) ~~~> (bastion hosts) ~~~> (ec2 instances) |
                       |                             |
                       +-----------------------------+

In slightly more detail:

*   The bastion host is in a security group that only allows SSH access
    from certain IP addresses (e.g. the Wellcome office building)

*   The EC2 instances are in a security group that only allows SSH access
    from other instances inside the same security group (which includes the bastion)

This script:

1.  Asks me what instances I want to access

2.  Adds my current IP address to the bastion security group, so I can SSH in
    [Note: these security groups are managed by Terraform, so this will be
    rolled back the next time we make a TF change.]

3.  Works out the IP address of the bastion/instance hosts

4.  Sets up an SSH connection into the instance host

It saves me a small amount of fiddling inside the EC2 console.

"""

import ipaddress
import os
import re
import subprocess

import boto3
import inquirer
import urllib3


def get_my_ip():
    """What's my current IP address?  Assumes IPv4."""
    http = urllib3.PoolManager()

    resp = http.request(
        "GET", "https://bot.whatismyipaddress.com/",
        headers={"User-Agent": "A script by @alexwlchan"}
    )

    ip = resp.data.decode("utf-8").strip()
    assert re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip)
    return ip


def get_aws_client(resource, *, role_arn):
    # Taken from https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-api.html
    sts_client = boto3.client("sts")
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn, RoleSessionName="AssumeRoleSession1"
    )
    credentials = assumed_role_object["Credentials"]

    return boto3.client(
        resource,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )


def get_security_groups(ec2):
    paginator = ec2.get_paginator("describe_security_groups")

    for page in paginator.paginate():
        yield from page["SecurityGroups"]


def get_instances(ec2):
    paginator = ec2.get_paginator("describe_instances")

    for page in paginator.paginate():
        for res in page["Reservations"]:
            yield from res["Instances"]


def get_running_instances(instances, *, prefix):
    for ec2_inst in instances:
        name_tag = next(t for t in ec2_inst["Tags"] if t["Key"] == "Name")
        name = name_tag["Value"]

        if not name.startswith(ec2_instance_prefix):
            continue

        if ec2_inst["State"]["Name"] == "terminated":
            continue

        yield (name, ec2_inst)


if __name__ == "__main__":
    ip_address = get_my_ip()
    print(f"*** The current IP address is {ip_address}")

    questions = [
        inquirer.List(
            "cluster",
            message="Which EC2 cluster do you want to access?",
            choices=[
                "archivematica-staging",
                "archivematica-prod",
            ],
        )
    ]

    answers = inquirer.prompt(questions)

    if answers["cluster"] in {"archivematica-staging", "archivematica-prod"}:
        ec2 = get_aws_client(
            "ec2", role_arn="arn:aws:iam::299497370133:role/workflow-developer"
        )

        ec2_instance_prefix = answers["cluster"]
        security_group_prefix = f"{answers['cluster']}-bastion_ssh_controlled_ingress"
    else:
        sys.exit(f"Unrecognised cluster: {answers['cluster']}")

    for sg in get_security_groups(ec2):
        if not sg["GroupName"].startswith(security_group_prefix):
            continue

        permissions = sg["IpPermissions"]

        existing_networks = [
            ipaddress.ip_network(rng["CidrIp"]) for rng in permissions[0]["IpRanges"]
        ]

        if any(ipaddress.ip_address(ip_address) in net for net in existing_networks):
            print(f"*** Already authorised to SSH to {sg['GroupName']}")
        else:
            print(f"*** Adding this IP address to security group {sg['GroupName']}")
            new_rule = {
                "CidrIp": ip_address + "/32",
                "Description": "Alex working remotely",
            }

            permissions[0]["IpRanges"] = [new_rule]

            ec2.authorize_security_group_ingress(
                GroupId=sg["GroupId"],
                IpPermissions=permissions,
            )

    bastion_host = None
    instances = []

    print("*** Looking up EC2 instances")
    ec2_instances = get_instances(ec2)
    running_instances = list(
        get_running_instances(ec2_instances, prefix=ec2_instance_prefix)
    )

    bastion_host = next(
        ec2_inst
        for name, ec2_inst in running_instances
        if name.endswith("-bastion")
    )

    container_hosts = [
        ec2_inst
        for name, ec2_inst in running_instances
        if not name.endswith("-bastion")
    ]

    if bastion_host is None:
        print("*** Unable to find bastion host?")
    else:
        print("*** Found the bastion host!")

    if not container_hosts:
        print("*** Unable to find any container hosts?")
    elif len(container_hosts) == 1:
        print("*** Found 1 container hosts!")
    else:
        print(f"*** Found {len(container_hosts)} container hosts!")

    print("*** Copying the key to ~/.ssh/authorized_keys on the bastion host")
    key_name = bastion_host["KeyName"]
    key_path = os.path.join(os.environ["HOME"], ".ssh", key_name)
    bastion_dns = bastion_host['PublicDnsName']
    copy_cmd = [
        "scp",
        "-i", key_path,
        key_path, f"ec2-user@{bastion_dns}:.ssh/{key_name}"
    ]
    subprocess.check_call(copy_cmd, stdout=subprocess.DEVNULL)

    if len(container_hosts) == 1:
        selected_host = container_hosts[0]["PrivateDnsName"]
    else:
        questions = [
            inquirer.List(
                "instance",
                message="Which EC2 instance do you want to access?",
                choices=[host["PublicDnsName"] for host in container_hosts],
            )
        ]
        answers = inquirer.prompt(questions)
        selected_host = answers["instance"]

    print(f"*** SSH'ing into EC2 instance at {selected_host}")
    ssh_cmd = [
        "ssh", "-t", "-i", key_path, f"ec2-user@{bastion_dns}",
        f"ssh -t -i ~/.ssh/{key_name} {selected_host}"
    ]
    subprocess.check_call(ssh_cmd)
