#!/usr/bin/env python
# -*- encoding: utf-8

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

    adjectives_src = go_src.split('left = [...]string{')[1].split('}')[0]
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
