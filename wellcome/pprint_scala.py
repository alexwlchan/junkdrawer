#!/usr/bin/env python
# -*- encoding: utf-8

import math
import sys


if __name__ == "__main__":
    try:
        scala_src = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <SCALA_SRC>")

    indent = 0

    while scala_src:
        try:
            opening = scala_src.index("(")
        except ValueError:
            opening = math.inf

        try:
            closing = scala_src.index(")")
        except ValueError:
            closing = math.inf

        try:
            comma = scala_src.index(",")
        except ValueError:
            comma = math.inf

        if comma < opening and comma < closing:
            print(" " * indent + scala_src[:comma + 1], end="")
            scala_src = scala_src[comma + 1:]

        elif opening < closing:
            print(" " * indent + scala_src[:opening + 1], end="")
            scala_src = scala_src[opening + 1:]
            indent += 2
        else:
            if scala_src[:closing]:
                print(" " * indent + scala_src[:closing])
            indent -= 2
            print(" " * indent + ")", end="")
            scala_src = scala_src[closing + 1:]

        try:
            if scala_src[0] == ",":
                print(",", end="")
                scala_src = scala_src[1:]
        except IndexError:
            pass

        print()
