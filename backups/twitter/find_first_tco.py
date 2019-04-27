#!/usr/bin/env python
# -*- encoding: utf-8

import sys

from twitter_oauth import TwitterSession


if __name__ == '__main__':
    sess = TwitterSession()

    try:
        tco_url = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <TCO_URL>")

    searches = list(sess.search(query=tco_url))

    if not searches:
        sys.exit("Could not find any tweets with that URL!")

    # Check that filtering out retweeted statuses still leaves us with something
    searches = [s for s in searches if "retweeted_status" not in s]
    if not searches:
        sys.exit("Could only find retweets with that URL?")

    for s in searches:
        assert any(u["url"] == tco_url for u in s["entities"]["urls"])

    candidates = [
        "https://twitter.com/%s/status/%s" % (s["user"]["screen_name"], s["id_str"])
        for s in searches
    ]

    if len(searches) > 1:
        sys.exit("Found multiple tweets:\n%s" % "\n".join(candidates))
    else:
        print(candidates[0])
