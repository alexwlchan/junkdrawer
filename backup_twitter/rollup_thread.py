#!/usr/bin/env python
# -*- encoding: utf-8
"""
This allows me to save the contents of a thread to a local backup.
The script

*   Takes complete backups of all the tweets in the thread to a single
    ".twitter" directory
*   Creates a Markdown file that summarises the text of the thread

"""

import datetime as dt
import json
import os
import sys
from urllib.parse import urlparse

from twitter_oauth import TwitterSession, save_tweet


BACKUP_ROOT = ".twitter"


if __name__ == '__main__':
    sess = TwitterSession(backup_root=BACKUP_ROOT)

    try:
        url = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <URL>")

    parts = urlparse(url)
    assert parts.netloc == "twitter.com"

    _, username, status, tweet_id, *_ = parts.path.split("/")
    assert status == "status"

    thread = []
    while True:
        print(f"Saving {tweet_id}")
        tweet = sess.lookup_status(tweet_id)
        save_tweet(tweet, backup_root=BACKUP_ROOT, dirname="threads")

        thread.insert(0, tweet)

        in_reply_to_status_id_str = tweet["in_reply_to_status_id_str"]
        if in_reply_to_status_id_str is None:
            break

        tweet_id = in_reply_to_status_id_str

    out_path = f"thread_{username}_{tweet_id}.md"

    now = dt.datetime.now()

    # Often I'm saving these to my 'txt' repository or notebooks, in which
    # case I really want pretty JSON to make the diffs look nice.
    # So unless I've explicitly said don't do that, prettify the JSON.
    if "--nopretty" not in sys.argv:
        for root, _, filenames in os.walk(BACKUP_ROOT):
            for f in filenames:
                if not f.endswith(".json"):
                    continue

                path = os.path.join(root, f)
                d = json.load(open(path))
                new_json = json.dumps(d, indent=2, sort_keys=True)
                open(path, "w").write(new_json)

    with open(out_path, "w") as outfile:
        outfile.write("\n".join([
            f'url: "{url}"',
            f'retrieved: "{now}"',
            "---\n",
            "",
        ]))

        for tweet in thread:
            screen_name = tweet["user"]["screen_name"]
            text = tweet["full_text"]

            # Render URLs as their raw form and not the t.co link in the
            # Markdown thread.
            for u in tweet.get("entities", {}).get("urls", []):
                text = text.replace(u["url"], "<%s>" % u["expanded_url"])

            outfile.write(f"@{screen_name}: {text}\n\n")

    print(out_path)
