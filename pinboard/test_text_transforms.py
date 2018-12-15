#!/usr/bin/env python
# -*- encoding: utf-8

import pytest

from text_transforms import apply_markdown_blockquotes, cleanup_blockquote_whitespace


@pytest.mark.parametrize('description, expected', [
    ("hello world", "hello world"),
    ("<blockquote>hello world</blockquote>", "<blockquote>hello world</blockquote>"),
    ("<blockquote>\nhello world</blockquote>", "<blockquote>hello world</blockquote>"),
    ("<blockquote>\n hello world</blockquote>", "<blockquote>hello world</blockquote>"),
    ("<blockquote>\r\nhello world</blockquote>", "<blockquote>hello world</blockquote>"),
    ("<blockquote>hello world\n</blockquote>", "<blockquote>hello world</blockquote>"),
    ("<blockquote>hello world\r\n</blockquote>", "<blockquote>hello world</blockquote>"),
    ("<blockquote>hello world\n\n</blockquote>", "<blockquote>hello world</blockquote>"),
])
def test_cleanup_blockquote_whitespace(description, expected):
    assert cleanup_blockquote_whitespace(description) == expected


@pytest.mark.parametrize('description, expected', [
    ("hello world", "hello world"),
    ("> hello world", "<blockquote>hello world</blockquote>"),
    ("> hello world\n\nfoo bar", "<blockquote>hello world</blockquote>\n\nfoo bar"),
    ("foo bar\n\n> hello world", "foo bar\n\n<blockquote>hello world</blockquote>"),
    ("foo bar\n\n> hello world\n\nbar baz", "foo bar\n\n<blockquote>hello world</blockquote>\n\nbar baz"),
    ("> hello world\n\n> howdy friend", "<blockquote>hello world\n\nhowdy friend</blockquote>"),
    ("> hello world\n\n> howdy friend\n\nfoo bar", "<blockquote>hello world\n\nhowdy friend</blockquote>\n\nfoo bar"),
    ("foo bar\n\n> hello world\n\n> howdy friend", "foo bar\n\n<blockquote>hello world\n\nhowdy friend</blockquote>"),
])
def test_apply_markdown_blockquotes(description, expected):
    assert apply_markdown_blockquotes(description) == expected
