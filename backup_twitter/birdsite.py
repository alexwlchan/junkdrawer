# -*- encoding: utf-8

from collections.abc import MutableMapping
import json
import os
from urllib.parse import urlparse
from urllib.request import urlretrieve

import attr
import hcl
import tweepy


@attr.s
class TwitterCredentials:
    consumer_key = attr.ib()
    consumer_secret = attr.ib(repr=False)
    access_token = attr.ib()
    access_token_secret = attr.ib(repr=False)

    @classmethod
    def from_path(cls, path):
        data = hcl.load(open(path))
        return cls(**data)


@attr.s
class TweetStore(MutableMapping):
    path = attr.ib()
    tweet_data = attr.ib()

    @classmethod
    def from_path(cls, path):
        os.makedirs(path, exist_ok=True)

        try:
            tweet_data = json.load(open(os.path.join(path, 'tweets.json')))
        except FileNotFoundError:
            tweet_data = {}

        return cls(path=path, tweet_data=tweet_data)

    def save(self, tweet, reindex=False):
        if reindex or (str(tweet.id) not in self):
            self[str(tweet.id)] = tweet
        else:
            print('.', end='')

    def __getitem__(self, tweet_id):
        return self.tweet_data[tweet_id]

    def __setitem__(self, tweet_id, tweet):
        print(f'Storing {tweet_id}')
        path = os.path.join(self.path, tweet_id[:2], tweet_id)
        os.makedirs(path, exist_ok=True)

        json_data = json.dumps(tweet._json, indent=2, sort_keys=True)
        with open(os.path.join(path, 'info.json'), 'w') as outfile:
            outfile.write(json_data)

        try:
            extended_entities = tweet.extended_entities
        except AttributeError:
            extended_entities = tweet.entities

        else:
            media = extended_entities.pop('media')

            for m in media:
                url = m['media_url_https']
                filename = os.path.join(
                    path, os.path.basename(urlparse(url).path)
                )
                urlretrieve(url=url, filename=filename)

            assert not extended_entities

        self.tweet_data[tweet_id] = {
            'dir': os.path.relpath(path, start=self.path),
            '_text': tweet.full_text,
            '_user': tweet.user.screen_name,
            '_date': tweet.created_at.isoformat(),
        }
        json_data = json.dumps(self.tweet_data, indent=2, sort_keys=True)
        with open(os.path.join(self.path, 'tweets.json'), 'w') as outfile:
            outfile.write(json_data)

    def __delitem__(self, tweet_id):
        raise NotImplementedError

    def __iter__(self):
        return iter(self.tweet_data)

    def __len__(self):
        return len(self.tweet_data)


def setup_api(credentials):
    """Authorise the use of the Twitter API.

    :param credentials: An instance of TwitterCredentials.

    """
    auth = tweepy.OAuthHandler(
        consumer_key=credentials.consumer_key,
        consumer_secret=credentials.consumer_secret)
    auth.set_access_token(
        key=credentials.access_token,
        secret=credentials.access_token_secret
    )
    return tweepy.API(auth)
