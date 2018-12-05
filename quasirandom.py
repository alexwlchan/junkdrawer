#!/usr/bin/env python
# -*- encoding: utf-8
"""
Used to generate data that looks a bit like the real thing, but is totally
meaningless.

e.g. example API keys for screenshots.

"""

import random
import string
import sys


def choice(xs):
    while True:
        r = random.choice(xs)
        if r not in {'0', 'o', 'O', '1', 'l', 'I'}:
            return r


def _randomize_char(c):
    if c.isupper():
        return choice(string.ascii_uppercase)
    elif c.islower():
        return choice(string.ascii_lowercase)
    elif c.isnumeric():
        return choice(string.digits[1:])


def randomize(s):
    return ''.join(_randomize_char(c) for c in s)


if __name__ == '__main__':
    print(randomize(sys.argv[1]))
