#!/usr/bin/env python
# -*- encoding: utf-8
"""
Given a URL to a file on GitHub, e.g.

    https://github.com/alexwlchan/junkdrawer/blob/master/github_permalink.py

rewrite that into a URL that refers to a commit -- specifically, the last
commit that changed this file.  Ensures that the content/line references in
a link don't change later.

This API doesn't require auth for public repos (yay!), but it might hit
rate limits.  If you get 403 errors, that's probably why.

"""

import sys
from urllib.parse import urlparse, urlunparse

import requests


if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <URL>")

    parts = urlparse(url)

    if parts.netloc != "github.com":
        sys.exit("Can only be used with a GitHub URL!")

    _, owner, repo, _, ref, path = parts.path.split("/", maxsplit=5)

    # Workaround for artefactual/archivematica, who use slashes in their
    # release tags.
    if ref == "stable" and path.startswith("1.8.x/"):
        ref = "stable/1.8.x"
        _, path = path.split("/", maxsplit=1)

    resp = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/commits",
        params={"sha": ref, "path": path},
        headers={"Accept": "application/vnd.github.v3+json"}
    )

    try:
        resp.raise_for_status()
    except Exception:
        print(resp.json())
        raise

    commits = resp.json()
    assert len(commits) > 1

    sha = commits[0]["sha"]

    new_path = "/".join(["", owner, repo, "blob", sha, path])

    print(urlunparse((
        parts.scheme,
        parts.netloc,
        new_path,
        parts.params,
        parts.query,
        parts.fragment
    )))
