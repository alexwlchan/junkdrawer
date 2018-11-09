#!/usr/bin/env python
# -*- encoding: utf-8

import datetime as dt
import webbrowser

try:
    from urllib import urlencode
    from urlparse import urlparse, urlunparse
except ImportError:  # Python 3
    from urllib.parse import urlencode, urlparse, urlunparse


query_dict = {
    "startDate": (dt.datetime.now() - dt.timedelta(days=30)).strftime("%Y-%m-%d"),
    "endDate": dt.datetime.now().strftime("%Y-%m-%d"),
    "timeRangeOption": "Custom",

    "chartStyle": "Line",
    "excludeCredit": "false",
    "excludeOtherSubscriptionCosts": "false",
    "excludeRIRecurringCharges": "false",
    "excludeRIUpfrontFees": "false",
    "excludeRefund": "false",
    "excludeSupportCharges": "false",
    "excludeTaggedResources": "false",
    "excludeTax": "false",
    "filter": "[]",
    "forecastTimeRangeOption": "None",
    "granularity": "Daily",
    "groupBy": "Operation",
    "hasAmortized": "false",
    "hasBlended": "false",
    "isTemplate": "true",
    "reportName": "Daily API operation costs",
    "reportType": "CostUsage",
}

parts = [
    # scheme
    "https",

    # netloc
    "console.aws.amazon.com",

    # path
    "/cost-reports/home",

    # params
    "",

    # query
    "",

    # fragment
    "/custom?%s" % urlencode(query_dict)
]

webbrowser.open(urlunparse(parts))
