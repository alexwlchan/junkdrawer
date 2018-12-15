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
        ("\n</blockquote>" in description) or
        ("<blockquote>\r\n" in description) or
        ("\r\n</blockquote>" in description)
    ):
        return BLOCKQUOTE_WHITESPACE_RE.sub(r"\g<opening_tag>\g<closing_tag>", description)
    else:
        return description


CONTINUOUS_BLOCKQUOTE_RE = re.compile(r"</blockquote>(?P<whitespace>\s*)<blockquote>")


def apply_markdown_blockquotes(description):
    """
    Replace Markdown-style blockquotes with HTML <blockquote> tags.
    """
    lines = description.splitlines()
    for i, line in enumerate(lines):
        if line.lstrip().startswith(">"):
            inner_line = line.lstrip('>').strip()
            lines[i] = f"<blockquote>{inner_line}</blockquote>"

    new_description = "\n".join(lines)
    return CONTINUOUS_BLOCKQUOTE_RE.sub(r"\g<whitespace>", new_description)
