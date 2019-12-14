# -*- encoding: utf-8

from __future__ import division


def get_pinboard_tag(wc):
    if wc < 1000:
        return "wc:<1k"
    elif wc < 5000:
        return "wc:1k–5k"
    elif wc < 10000:
        return "wc:5k–10k"
    elif wc < 25000:
        return "wc:10k–25k"
    else:
        lower_bound = (wc // 25000) * 25000
        upper_bound = lower_bound + 25000
        return "wc:%dk–%dk" % (lower_bound // 1000, upper_bound // 1000)
