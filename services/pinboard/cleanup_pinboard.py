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


def fix_word_count_tags(tag_str):
    tag_str = tag_str.replace("wc:5k-10k", "wc:5k–10k")
    tag_str = tag_str.replace("wc:100k-125k", "wc:100k–125k")
    tag_str = tag_str.replace("wc:175k-200k", "wc:175k–200k")

    return tag_str


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

        b["tags"] = fix_word_count_tags(b["tags"])

        tags = b["tags"].split()
        if "!fic" in tags and not any(t.startswith("wc:") for t in tags):
            logger.warning("%s is a fic with no word count", b["href"])

        bad_word_count_tags = [t.startswith("wc:") and "-" in t for t in tags]
        if bad_word_count_tags:
            sys.exit("Bad word count tags: %s" % ", ".join(bad_word_count_tags))

        if b != original_b:
            logger.info("Updating %s", b["href"])

            # We need to replace 'href' with 'URL' for the Pinboard API to accept
            # this as a bookmark.
            b["url"] = b.pop("href")

            resp = sess.get("https://api.pinboard.in/v1/posts/add", params=b)

            assert resp.json()["result_code"] == "done", resp.text
