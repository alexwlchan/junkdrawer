#!/usr/bin/env python
# -*- encoding: utf-8

import pytest

from text_transforms import cleanup_blockquote_whitespace


@pytest.mark.parametrize('description, expected', [
    ("hello world", "hello world"),
    ("<blockquote>hello world</blockquote>", "<blockquote>hello world</blockquote>"),
    ("<blockquote>\nhello world</blockquote>", "<blockquote>hello world</blockquote>"),
    ("<blockquote>\n hello world</blockquote>", "<blockquote>hello world</blockquote>"),
    ("<blockquote>hello world\n</blockquote>", "<blockquote>hello world</blockquote>"),
    ("<blockquote>hello world\n\n</blockquote>", "<blockquote>hello world</blockquote>"),
])
def test_cleanup_blockquote_whitespace(description, expected):
    assert cleanup_blockquote_whitespace(description) == expected
