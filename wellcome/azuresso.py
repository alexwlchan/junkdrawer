#!/usr/bin/env python
# -*- encoding: utf-8
"""
This script is for getting ~/.aws/credentials for the platform account.

We authenticate with AWS using Azure Active Directory and SSO.  To log into AWS,
the in-browser flow is:

1.  Visit wellcomecloud.org
2.  Click on "AWS - Digital Platform"
3.  Log in to Azure AD using your username/password/2FA key

This drops you into the AWS Console.

This script does a similar thing to get SDK credentials.  It kicks off a login
session in Chrome, then reads the Chrome cookies and uses them as the basis for
an HTTP session that's already authenticated, and can thus make SAML requests
against AWS.

"""

import base64
import configparser
import datetime as dt
import os
import subprocess
import sys
import time
import uuid
import zlib

try:
    from configparser import ConfigParser
    from urllib.parse import urlencode
except ImportError:  # Python 2
    from ConfigParser import ConfigParser
    from urllib import urlencode

import boto3
import browsercookie
import click
import bs4
import requests


try:
    input = safe_input
except NameError:
    pass


TENANT_ID = "3b7a675a-1fc8-4983-a100-cc52b7647737"


def deflate_and_base64_encode(value):
    try:
        compressor = zlib.compressobj(wbits=-15)
    except TypeError:  # Python 2
        compressor = zlib.compressobj(-1, zlib.DEFLATED, -15)

    return base64.b64encode(
        compressor.compress(value.encode("utf8")) + compressor.flush()
    )


def create_saml_request_url(tenant_id):
    saml_request = """
    <samlp:AuthnRequest
      xmlns="urn:oasis:names:tc:SAML:2.0:metadata"
      ID="id%s"
      Version="2.0"
      IssueInstant="%s.000Z"
      IsPassive="false"
      AssertionConsumerServiceURL="https://signin.aws.amazon.com/saml"
      xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
        <Issuer xmlns="urn:oasis:names:tc:SAML:2.0:assertion">https://signin.aws.amazon.com/saml#14</Issuer>
        <samlp:NameIDPolicy Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress">
        </samlp:NameIDPolicy>
    </samlp:AuthnRequest>
    """ % (
        uuid.uuid4(),
        dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

    saml_param = deflate_and_base64_encode(saml_request)

    params = urlencode({"SAMLRequest": saml_param})

    return "https://login.microsoftonline.com/%s/saml2?" % tenant_id + params



if __name__ == "__main__":
    is_chrome_running = subprocess.check_output([
        "osascript", "-e",
        """
        tell application "System Events" to (name of processes) contains "Google Chrome"
        """
    ]).strip().decode("utf8")

    print("*** Opening Chrome to ensure you're logged in")
    subprocess.check_call([
        "open", "-a", "Google Chrome", create_saml_request_url(TENANT_ID)
    ])

    print("*** Waiting for you to be logged in")

    while True:
        chrome_url = subprocess.check_output([
            "osascript", "-e",
            """
            tell application "Google Chrome" to get URL of active tab of first window
            """
        ]).strip().decode("utf8")

        if chrome_url == (
            "https://eu-west-1.console.aws.amazon.com/console/home?region=eu-west-1#"
        ):
            subprocess.check_call([
                "osascript", "-e",
                """
                tell application "Google Chrome" to close front window
                """
            ])

            if is_chrome_running == "false":
                subprocess.check_call([
                    "osascript", "-e", 'tell application "Google Chrome" to quit'
                ])

            break
        else:
            time.sleep(1)

    while True:
        print("*** Making SAML request with Chrome cookies")
        cookies = browsercookie.chrome()
        resp = requests.get(
            create_saml_request_url(tenant_id=TENANT_ID),
            cookies=cookies
        )

        print("*** Received SAML response")
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        saml_response = soup.find("input", attrs={"name": "SAMLResponse"}).attrs["value"]

        saml_xml = base64.b64decode(saml_response)
        saml_soup = bs4.BeautifulSoup(saml_xml, "xml")
        role_attrs = saml_soup.find_all(
            "Attribute",
            attrs={"Name": "https://aws.amazon.com/SAML/Attributes/Role"}
        )

        roles = []
        for r in role_attrs:
            value = r.find("AttributeValue").text
            iam1, iam2 = value.split(",")

            # Role/principal claims may be in either order
            if ":role/" in iam2:
                principal, role = iam1, iam2
            else:
                principal, role = iam2, iam1
            roles.append((principal, role))

        if not roles:
            sys.exit("Did not find any roles???")
        elif len(roles) == 1:
            selected_role = roles[0]
        else:
            subprocess.check_call([
                "osascript", "-e", 'tell application "iTerm 2" to activate'
            ])

            print("Which role would you like to assume?")
            numbered_roles = {
                str(i): role_set
                for (i, role_set) in enumerate(roles, start=1)
            }

            for i, role_set in sorted(numbered_roles.items()):
                print("%s) %s" % (i, role_set[0]))

            while True:
                choice = input().strip()
                try:
                    selected_role = numbered_roles[choice.strip()]
                except KeyError:
                    print("Unrecognised selection!")
                else:
                    break

        print("*** Assuming role %s" % selected_role[0])
        sts_client = boto3.client("sts")
        sts_resp = sts_client.assume_role_with_saml(
            RoleArn=selected_role[1],
            PrincipalArn=selected_role[0],
            SAMLAssertion=saml_response
        )

        print("*** Writing credentials to ~/.aws/credentials")
        config = ConfigParser()
        config.read(os.path.join(os.environ["HOME"], ".aws", "credentials"))

        config["default"] = {
            "aws_access_key_id": sts_resp["Credentials"]["AccessKeyId"],
            "aws_secret_access_key": sts_resp["Credentials"]["SecretAccessKey"],
            "aws_session_token": sts_resp["Credentials"]["SessionToken"],
            "aws_session_expiration": sts_resp["Credentials"]["Expiration"].isoformat()
        }

        with open(os.path.join(os.environ["HOME"], ".aws", "credentials"), "w") as cfgfile:
            config.write(cfgfile)

        for hostname in [
            "ec2-18-203-67-12.eu-west-1.compute.amazonaws.com",
        ]:
            try:
                subprocess.check_call([
                    "scp", "-i", "/Users/chana/.ssh/wellcomedigitalstorage",
                    "/Users/chana/.aws/credentials",
                    f"ec2-user@{hostname}:/home/ec2-user/.aws/credentials"
                ])
            except Exception:
                pass

        print("*** Sleeping for 45 minutes")
        time.sleep(60 * 45)
