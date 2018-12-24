#!/usr/bin/env python
# -*- encoding: utf-8

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

    resp = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/commits",
        params={"sha": ref, "path": path},
        headers={"Accept": "application/vnd.github.v3+json"}
    )
    resp.raise_for_status()

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
