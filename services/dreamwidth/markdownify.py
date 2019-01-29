#!/usr/bin/env python
# -*- encoding: utf-8

import sys

import markdown2


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit("Usage: %s <PATH>" % __file__)

    md_src = open(path).read()
    print(" ".join(markdown2.markdown(md_src).splitlines()).replace("</p>  <p>", "</p><p>"))
