#!/usr/bin/env python
# -*- encoding: utf-8
"""
On sites where I don't want to use my standard username (@alexwlchan) --
for example, if I'm starring content but not creating anything -- I create
alliterative usernames from the names provided by Docker.

e.g. on GitHub I might use "goofy_galileo"

This script generates an alliterative username for me.

Usage: pass a single letter as first argument, and it offers five suggestions:

    $ ./usernames.py a
    angry_almeida
    admiring_ardinghelli
    admiring_austin
    amazing_aryabhata
    admiring_albattani

"""

import os
import random
import sys
import tempfile

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


def main():
    os.chdir(tempfile.mkdtemp())
    urlretrieve(
        'https://raw.githubusercontent.com/moby/moby/master/pkg/namesgenerator/names-generator.go',
        'names-generator.go')

    go_src = open('names-generator.go').read()

    # The adjectives are an array of strings:
    #
    #       var (
    #           left = [...]string{
    #               "admiring",
    #               "adoring",
    #               ...
    #               "zen",
    #           }
    #
    adjectives_src = go_src.split('left = [...]string{')[1].split('}')[0]

    # The names are another array of strings, but with comments on names
    # to explain their significance:
    #
    #           right = [...]string{
    #               // Muhammad ibn Jābir ...
    #               "albattani",
    #
    #               ...
    #
    #               "zhukovsky",
    #           }
    #
    names_src = go_src.split('right = [...]string{')[1].split('\n)')[0]

    adjectives = [
        line.strip('\t",')
        for line in adjectives_src.splitlines()
        if line.strip('\t",')
    ]

    names = [
        line.strip('\t",}')
        for line in names_src.splitlines()
        if not line.strip().startswith('//') and line.strip('\t",}')
    ]

    char = sys.argv[1].lower()

    for _ in range(5):
        print('%s_%s' % (
            random.choice([a for a in adjectives if a.startswith(char)]),
            random.choice([n for n in names if n.startswith(char)]),
        ))


if __name__ == '__main__':
    main()
