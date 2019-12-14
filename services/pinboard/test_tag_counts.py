# -*- encoding: utf-8

from hypothesis import given
from hypothesis.strategies import integers
import pytest

from tag_counts import get_pinboard_tag


@pytest.mark.parametrize("wc, tag", [
    (1, "wc:<1k"),
    (100, "wc:<1k"),
    (999, "wc:<1k"),
    (1000, "wc:1k–5k"),
    (1200, "wc:1k–5k"),
    (4999, "wc:1k–5k"),
    (5000, "wc:5k–10k"),
    (7500, "wc:5k–10k"),
    (9999, "wc:5k–10k"),
    (10000, "wc:10k–25k"),
    (15025, "wc:10k–25k"),
    (20000, "wc:10k–25k"),
    (24999, "wc:10k–25k"),
    (25000, "wc:25k–50k"),
    (49999, "wc:25k–50k"),
])
def test_get_pinboard_tag(wc, tag):
    assert get_pinboard_tag(wc) == tag


@given(integers(min_value=1))
def test_get_pinboard_tag_big_integers(wc):
    tag = get_pinboard_tag(wc)
    assert tag.startswith("wc:")
