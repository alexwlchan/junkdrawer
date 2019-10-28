#!/usr/bin/env python
# -*- encoding: utf-8

import click

from url_resolver import resolve_url
from twitter_oauth import TwitterSession, save_tweet


@click.command()
@click.option("--id", "tweet_id")
@click.option("--url")
def get_single_tweet_as_md(tweet_id, url):
    if tweet_id is None and url is None:
        raise click.UsageError("You must supply one of --id or --url")

    if tweet_id is not None and url is not None:
        raise click.UsageError("You must supply at most one of --id or --url")

    if url is not None:
        components = url.split("/")

        if url.endswith('/photo/1'):
            assert components[-4] == "status"
            tweet_id = components[-3]
        else:
            assert components[-2] == "status"
            tweet_id = components[-1]

    sess = TwitterSession()
    tweet = sess.lookup_status(tweet_id)

    screen_name = tweet["user"]["screen_name"]
    id_str = tweet["id_str"]
    display_url = f"https://twitter.com/{screen_name}/status/{id_str}"

    print(f"{display_url}:\n")

    full_text = tweet["full_text"]
    for entity in tweet["entities"].get("media", []):
        full_text = full_text.replace(
            entity["url"],
            entity["expanded_url"]
        )

    for entity in tweet["entities"]["urls"]:
        full_text = full_text.replace(
            entity["url"],
            resolve_url(entity["expanded_url"])
        )

    for line in full_text.splitlines():
        print(f"> {line}")


if __name__ == '__main__':
    get_single_tweet_as_md()
