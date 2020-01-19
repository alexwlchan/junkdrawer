#!/usr/bin/env python
# -*- encoding: utf-8
"""
A script for applying various "cleanup rules" to my Pinboard account.
"""

import copy
import logging
import sys

import daiquiri

from pinboard import create_session
from text_transforms import (
    apply_markdown_blockquotes,
    cleanup_blockquote_whitespace,
    fix_encoding,
)

daiquiri.setup(level=logging.INFO)

logger = daiquiri.getLogger(__name__)


if __name__ == "__main__":
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
        b["extended"] = fix_encoding(b["extended"])

        tags = b["tags"].split()
        if "!fic" in tags and not any(t.startswith("wc:") for t in tags):
            logger.warning("%s is a fic with no word count", b["href"])

        if b != original_b:
            logger.info("Updating %s", b["href"])

            # We need to replace 'href' with 'URL' for the Pinboard API to accept
            # this as a bookmark.
            b["url"] = b.pop("href")

            resp = sess.get("https://api.pinboard.in/v1/posts/add", params=b)

            assert resp.json()["result_code"] == "done", resp.text
