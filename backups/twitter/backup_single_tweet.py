#!/usr/bin/env python
# -*- encoding: utf-8

import click

from twitter_oauth import TwitterSession, save_tweet


@click.command()
@click.option("--id", "tweet_id")
@click.option("--url")
@click.option("--dirname", required=True)
def save_single_tweet(tweet_id, url, dirname):
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

    save_single_tweet_by_id(tweet_id=tweet_id, dirname=dirname)


def save_single_tweet_by_id(tweet_id, dirname):
    print(f"Saving {tweet_id} to {dirname}")
    sess = TwitterSession()
    tweet = sess.lookup_status(tweet_id)
    save_tweet(tweet, dirname=dirname)


if __name__ == '__main__':
    save_single_tweet()
