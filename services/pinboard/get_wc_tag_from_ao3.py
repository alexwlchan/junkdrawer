#!/usr/bin/env python
# -*- encoding: utf-8

from __future__ import division, print_function

import re
import subprocess

try:
    from urllib.request import urlretrieve
except ImportError:  # Python 2:
    from urllib import urlretrieve

from tag_counts import get_pinboard_tag


if __name__ == "__main__":
    ao3_url = (
        subprocess.check_output(
            ["osascript", "-e", 'tell application "Safari" to get URL of document 2']
        )
        .decode("utf8")
        .strip()
    )

    filename, _ = urlretrieve(ao3_url)
    html = open(filename).read()
    wc = int(html.split('<dd class="words">')[1].split("</dd>")[0].replace(",", ""))

    tag = get_pinboard_tag(wc)
    print(tag, end=" ")
