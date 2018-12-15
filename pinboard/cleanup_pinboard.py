#!/usr/bin/env python
# -*- encoding: utf-8
"""
A script for applying various "cleanup rules" to my Pinboard account.
"""

import sys

from pinboard import create_session


if __name__ == '__main__':
    try:
        api_key = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <API_KEY>")

    sess = create_session(api_key)
    resp = sess.get("https://api.pinboard.in/v1/user/secret", params={"foo": "bar"})
    print(resp.json())
