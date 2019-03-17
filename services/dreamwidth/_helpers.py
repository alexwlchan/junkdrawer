# -*- encoding: utf-8

import datetime as dt
import re

import pytest


def parse_date(date_s, time_s):
    amended_date_s = re.sub(
        r'(1st|2nd|3rd|\dth)',
        lambda m: m.group()[:-2],
        date_s
    )

    return dt.datetime.strptime(
        amended_date_s + ' ' + time_s,
        '%b. %d, %Y %H:%M %p'
    )


@pytest.mark.parametrize('date_s, time_s, expected_dt', [
    ('Mar. 17, 2019', '12:14 am', dt.datetime(2019, 3, 17, 12, 14, 0))
])
def test_parse_date(date_s, time_s, expected_dt):
    assert parse_date(date_s, time_s) == expected_dt
