#!/usr/bin/env python
# -*- encoding: utf-8

# https://twitter.com/ticky/status/1141370988820480001

import warnings


def self_deprecating(*args, **kwargs):
    print("Called self_deprecating with %r, %r" % (args, kwargs))

    if not hasattr(globals()["self_deprecating"], "deprecated"):
        def original_self_deprecating():
            pass

        original_self_deprecating.__code__ = self_deprecating.__code__

        def new_self_deprecating(*args, **kwargs):
            warnings.warn(
                "The self_deprecating function is deprecated",
                DeprecationWarning)
            return original_self_deprecating(*args, **kwargs)

        globals()["self_deprecating"] = new_self_deprecating
        globals()["self_deprecating"].deprecated = True


self_deprecating("hello", "ticky")
self_deprecating("hello", "alex")
