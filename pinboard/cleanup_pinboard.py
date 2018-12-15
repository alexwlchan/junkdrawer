#!/usr/bin/env python
# -*- encoding: utf-8
"""
A script for applying various "cleanup rules" to my Pinboard account.
"""

import copy
import sys

from pinboard import create_session
from text_transforms import cleanup_blockquote_whitespace



if __name__ == '__main__':
    # try:
    #     api_key = sys.argv[1]
    # except IndexError:
    #     sys.exit(f"Usage: {__file__} <API_KEY>")
    #
    # sess = create_session(api_key)
    # resp = sess.get("https://api.pinboard.in/v1/posts/all")
    # print(resp.text)
    import json; bookmarks = json.load(open("all_bookmarks.json"))

    for b in bookmarks:
        original_b = copy.deepcopy(b)

        b["extended"] = cleanup_blockquote_whitespace(b["extended"])

        print(b)
        break
