#!/usr/bin/env python
# -*- encoding: utf-8
"""
A script for applying various "cleanup rules" to my Pinboard account.
"""

import copy
import sys

from pinboard import create_session
from text_transforms import apply_markdown_blockquotes, cleanup_blockquote_whitespace



if __name__ == '__main__':
    try:
        api_key = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <API_KEY>")

    sess = create_session(api_key)
    resp = sess.get("https://api.pinboard.in/v1/posts/all")

    bookmarks = resp.json()

    for b in bookmarks:
        original_b = copy.deepcopy(b)

        b["extended"] = apply_markdown_blockquotes(b["extended"])
        b["extended"] = cleanup_blockquote_whitespace(b["extended"])

        if b != original_b:
            print(f"Updating {b['href']}")

            # We need to replace 'href' with 'URL' for the Pinboard API to accept
            # this as a bookmark.
            b["url"] = b.pop("href")

            resp = sess.get(
                "https://api.pinboard.in/v1/posts/add",
                params=b
            )

            assert resp.json()["result_code"] == "done", resp.text

        tags = b["tags"].split()
        if "!fic" in tags and not any(t.startswith("wc:") for t in tags):
            print(f"WARNING: {b['href']} is a fic with no word count")
