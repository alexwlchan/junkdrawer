# -*- encoding: utf-8

import re


BLOCKQUOTE_WHITESPACE_RE = re.compile(
    r"((?P<opening_tag><blockquote>)\s*|\s*(?P<closing_tag></blockquote>))"
)


def cleanup_blockquote_whitespace(description):
    """
    Remove any leading/trailing whitespace from <blockquote> tags.
    """
    if (
        ("<blockquote>\n" in description) or
        ("\n</blockquote>" in description)
    ):
        return BLOCKQUOTE_WHITESPACE_RE.sub(r"\g<opening_tag>\g<closing_tag>", description)
    else:
        return description
