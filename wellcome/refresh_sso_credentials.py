#!/usr/bin/env python
# -*- encoding: utf-8

import base64
import configparser
import datetime as dt
import io
import pathlib
import subprocess
import struct
import time
import uuid
import webbrowser
import zlib

try:
    from urllib.parse import urlencode
except ImportError:  # Python 2
    from urllib import urlencode

import boto3
import bs4
from lxml import etree
import requests


TENANT_ID = "3b7a675a-1fc8-4983-a100-cc52b7647737"

COOKIES_PATH = pathlib.Path.home() / "Library" / "Cookies" / "Cookies.binarycookies"


def deflate_and_base64_encode(value):
    try:
        compressor = zlib.compressobj(wbits=-15)
    except TypeError:  # Python 2
        compressor = zlib.compressobj(-1, zlib.DEFLATED, -15)

    return base64.b64encode(
        compressor.compress(value.encode("utf8")) + compressor.flush()
    )


def _read_to_null_terminator(buffer):
    result = b""

    while True:
        next_byte = buffer.read(1)
        if struct.unpack("<b", next_byte)[0] == 0:
            break
        result += next_byte

    return result


def read_cookies(binary_file):
    # Based on http://www.securitylearn.net/2012/10/27/cookies-binarycookies-reader/
    if binary_file.read(4) != b"cook":
        raise ValueError("Not a Cookies.binarycookies file?")

    num_pages=struct.unpack('>i',binary_file.read(4))[0]               #Number of pages in the binary file: 4 bytes

    page_sizes=[]
    for np in range(num_pages):
        page_sizes.append(struct.unpack('>i',binary_file.read(4))[0])  #Each page size: 4 bytes*number of pages

    pages=[]
    for ps in page_sizes:
        pages.append(binary_file.read(ps))                      #Grab individual pages and each page will contain >= one cookie

    for page in pages:
        page=io.BytesIO(page)                                     #Converts the string to a file. So that we can use read/write operations easily.
        page.read(4)                                            #page header: 4 bytes: Always 00000100
        num_cookies=struct.unpack('<i',page.read(4))[0]                #Number of cookies in each page, first 4 bytes after the page header in every page.

        cookie_offsets=[]
        for nc in range(num_cookies):
            cookie_offsets.append(struct.unpack('<i',page.read(4))[0]) #Every page contains >= one cookie. Fetch cookie starting point from page starting byte

        page.read(4)                                            #end of page header: Always 00000000

        cookie=''
        for offset in cookie_offsets:
            page.seek(offset)                                   #Move the page pointer to the cookie starting point
            cookiesize=struct.unpack('<i',page.read(4))[0]             #fetch cookie size
            cookie=io.BytesIO(page.read(cookiesize))              #read the complete cookie

            cookie.read(4)                                      #unknown

            flags=struct.unpack('<i',cookie.read(4))[0]                #Cookie flags:  1=secure, 4=httponly, 5=secure+httponly
            cookie_flags=''
            if flags==0:
                cookie_flags=''
            elif flags==1:
                cookie_flags='Secure'
            elif flags==4:
                cookie_flags='HttpOnly'
            elif flags==5:
                cookie_flags='Secure; HttpOnly'
            else:
                cookie_flags='Unknown'

            cookie.read(4)                                      #unknown

            urloffset=struct.unpack('<i',cookie.read(4))[0]            #cookie domain offset from cookie starting point
            nameoffset=struct.unpack('<i',cookie.read(4))[0]           #cookie name offset from cookie starting point
            pathoffset=struct.unpack('<i',cookie.read(4))[0]           #cookie path offset from cookie starting point
            valueoffset=struct.unpack('<i',cookie.read(4))[0]          #cookie value offset from cookie starting point

            endofcookie=cookie.read(8)                          #end of cookie

            expiry_date_epoch= struct.unpack('<d',cookie.read(8))[0]+978307200          #Expiry date is in Mac epoch format: Starts from 1/Jan/2001
            expiry_date=time.gmtime(expiry_date_epoch) #978307200 is unix epoch of  1/Jan/2001

            create_date_epoch=struct.unpack('<d',cookie.read(8))[0]+978307200           #Cookies creation time
            create_date = time.gmtime(create_date_epoch)

            cookie.seek(urloffset - 4)
            url = _read_to_null_terminator(cookie)

            cookie.seek(nameoffset - 4)
            name = _read_to_null_terminator(cookie)

            cookie.seek(pathoffset - 4)
            path = _read_to_null_terminator(cookie)

            cookie.seek(valueoffset - 4)
            value = _read_to_null_terminator(cookie)

            yield {
                "name": name,
                "value": value,
                "url": url,
                "path": path,
                "expires": expiry_date,
                "flags": cookie_flags,
            }


def create_saml_url():
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

    return "https://login.microsoftonline.com/%s/saml2?" % TENANT_ID + params


def osascript(cmd):
    return subprocess.check_output(["osascript", "-e", cmd]).strip().decode("utf8")


def get_safari_url():
    return osascript('tell application "Safari" to get URL of document 1')



if __name__ == "__main__":
    print("*** Sending you to log in with your web browser")

    url = create_saml_url()
    webbrowser.open(url)

    while "console.aws.amazon.com" not in get_safari_url():
        time.sleep(1)

    osascript('tell application "iTerm 2" to activate')

    print("*** Reading the Safari cookie jar")
    jar = requests.cookies.RequestsCookieJar()

    for cookie in read_cookies(COOKIES_PATH.open("rb")):
        if cookie["name"] == b"ESTSAUTHPERSISTENT":
            jar.set(
                name=cookie["name"].decode("utf8"),
                value=cookie["value"].decode("utf8"),
                domain=cookie["url"].decode("utf8"),
                path=cookie["path"].decode("utf8")
            )
            break

    sess = requests.Session()
    sess.cookies = jar

    url = create_saml_url()

    print("*** Making SAML request")
    resp = sess.get(url)

    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    saml_response = soup.find("input", attrs={"name": "SAMLResponse"}).attrs["value"]

    xml = base64.b64decode(saml_response)
    tree = bs4.BeautifulSoup(xml, "xml")

    role = tree.find(
        "Attribute",
        attrs={"Name": "https://aws.amazon.com/SAML/Attributes/Role"}
    )

    role_arn, principal_arn = role.find("AttributeValue").text.split(",")
    print(f"*** Assuming role {role_arn}")

    sts = boto3.client("sts")

    resp = sts.assume_role_with_saml(
        RoleArn=role_arn,
        PrincipalArn=principal_arn,
        SAMLAssertion=saml_response
    )

    print("*** Writing new credentials to ~/.aws/credentials")

    credentials = pathlib.Path.home() / ".aws" / "credentials"

    config = configparser.ConfigParser()
    config.read(credentials)

    config["default"] = {
        "aws_access_key_id": resp["Credentials"]["AccessKeyId"],
        "aws_secret_access_key": resp["Credentials"]["SecretAccessKey"],
        "aws_session_token": resp["Credentials"]["SessionToken"],
        "aws_session_expiration": resp["Credentials"]["Expiration"].isoformat(),
    }

    with credentials.open("w") as configfile:
        config.write(configfile)
