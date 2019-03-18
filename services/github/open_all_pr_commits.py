#!/usr/bin/env python
# -*- encoding: utf-8
"""
Given a path to a pull request on GitHub, e.g.

    https://github.com/HypothesisWorks/hypothesis/pull/1712

open a new web browser tab for every commit in the pull request.

"""

import sys
from urllib.parse import urlparse
import webbrowser

import requests


if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <URL>")

    parts = urlparse(url)

    if parts.netloc != "github.com":
        sys.exit("Can only be used with a GitHub URL!")

    _, owner, repo, pull, number = parts.path.split("/")
    if pull != "pull":
        sys.exit("Can only be used with a pull request!")

    resp = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/pulls/{number}/commits",
        headers={"Accept": "application/vnd.github.v3+json"}
    )

    try:
        resp.raise_for_status()
    except Exception:
        print(resp.json())
        raise

    for commit in resp.json():
        webbrowser.open(commit["html_url"])
