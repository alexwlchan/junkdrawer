# -*- encoding: utf-8

import pytest

from turn_catalogue_image_into_gif import parse_catalogue_id


@pytest.mark.parametrize('arg,expected_id', [
    ("https://wellcomecollection.org/works/rq48tke5", "rq48tke5"),
    ("https://wellcomecollection.org/works/rq48tke5?query=cabbage&page=1", "rq48tke5"),
    ("https://api.wellcomecollection.org/catalogue/v2/works/ecdebckk?include=identifiers,subjects", "ecdebckk"),
    ("https://api.wellcomecollection.org/catalogue/v1/works/ecdebckk", "ecdebckk"),
    ("a22au6yn", "a22au6yn"),
])
def test_parse_catalogue_id(arg, expected_id):
    assert parse_catalogue_id(arg) == expected_id
