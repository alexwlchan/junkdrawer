# -*- encoding: utf-8

import copy
import json
import os
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import urlretrieve

from requests_oauthlib import OAuth1Session


API_URL = "https://api.twitter.com/1.1"

BACKUP_DIR = os.path.join(os.environ["HOME"], "Documents", "backups", "twitter")
BACKUP_DIR_PROFILE_IMAGES = os.path.join(BACKUP_DIR, "profile_images")
BACKUP_DIR_DMS = os.path.join(BACKUP_DIR, "direct_messages")


def create_session(credentials):
    sess = OAuth1Session(
        client_key=credentials["consumer_key"],
        client_secret=credentials["consumer_secret"],
        resource_owner_key=credentials["access_token"],
        resource_owner_secret=credentials["access_token_secret"]
    )

    # Raise an exception on any responses that don't return a 200 OK.

    def raise_for_status(resp, *args, **kwargs):
        resp.raise_for_status()

    sess.hooks["response"].append(raise_for_status)

    return sess


class TwitterSession:

    def __init__(self):
        credentials_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "auth.json"
        )
        credentials = json.load(open(credentials_path))
        self.oauth_session = create_session(credentials)
        self.user_info = UserInfo(self.oauth_session)

    def list_dm_events(self):
        initial_params = {"count": 50}
        for resp in self._cursored_response(
            path="/direct_messages/events/list.json",
            initial_params=initial_params
        ):
            for event in resp["events"]:

                # Denormalise the "source_app_id" field, which can only be
                # retrieved if you also have the "apps" field from the response.
                try:
                    event["message_create"]["_source_app"] = (
                        resp["apps"][event["message_create"]["source_app_id"]]
                    )
                except KeyError:
                    pass

                # Denormalise the sender/recipient information, where you normally
                # just get their ID.
                event["message_create"]["_sender"] = self.user_info.lookup_user(
                    event["message_create"]["sender_id"]
                )

                event["message_create"]["target"]["_recipient"] = self.user_info.lookup_user(
                    event["message_create"]["target"]["recipient_id"]
                )

                yield event

    def show_dm_event(self, event_id):
        resp = self.oauth_session.get(
            API_URL + "/direct_messages/events/show.json",
            params={"id": event_id}
        )

        event = resp.json()["event"]
        event["message_create"]["_source_app"] = (
            resp.json()["apps"][event["message_create"]["source_app_id"]]
        )

        return event

    def list_favorites(self):
        initial_params = {
            "count": 200,
            "include_entities": True,
            "tweet_mode": "extended"
        }
        yield from self._tweet_id_response(
            path="/favorites/list.json",
            initial_params=initial_params
        )

    def mentions_timeline(self):
        initial_params = {
            "count": 200,
            "include_entities": True,
            "tweet_mode": "extended"
        }
        yield from self._tweet_id_response(
            path="/statuses/mentions_timeline.json",
            initial_params=initial_params
        )

    def user_timeline(self):
        initial_params = {
            "count": 200,
            "exclude_replies": False,
            "include_rts": True,
            "tweet_mode": "extended",
            "include_entities": True,
        }
        yield from self._tweet_id_response(
            path="/statuses/user_timeline.json",
            initial_params=initial_params
        )

    def lookup_users(self, user_ids):
        return self.user_info.lookup_users(user_ids=user_ids)

    def lookup_user(self, user_id):
        return self.user_info.lookup_user(user_id=user_id)

    def lookup_status(self, tweet_id):
        params = {
            "id": tweet_id,
            "include_entities": True,
            "trim_user": False,
            "include_ext_alt_text": True,
            "tweet_mode": "extended",
        }
        resp = self.oauth_session.get(
            API_URL + "/statuses/show.json",
            params=params, timeout=1)
        assert resp.json()["id_str"] == tweet_id
        return resp.json()

    def _cursored_response(self, path, initial_params):
        params = copy.deepcopy(initial_params)
        while True:
            resp = self.oauth_session.get(API_URL + path, params=params, timeout=5)
            yield resp.json()

            try:
                params["cursor"] = resp.json()["next_cursor"]
            except KeyError:
                break

    def _tweet_id_response(self, path, initial_params):
        params = copy.deepcopy(initial_params)
        while True:
            print(f"Making request to {path} with {params}")
            resp = self.oauth_session.get(API_URL + path, params=params, timeout=5)
            yield from resp.json()

            for tweet in resp.json():
                download_profile_image(tweet["user"])

            try:
                params["max_id"] = min(tweet["id"] for tweet in resp.json())
            except ValueError:
                # Empty response; nothing more to do
                break


class UserInfo:

    def __init__(self, oauth_session):
        self.oauth_session = oauth_session
        self.cache = {}

    def lookup_users(self, user_ids):
        missing = [uid for uid in user_ids if uid not in self.cache]
        if missing:
            self._lookup_api_user(missing)
        return {uid: self.cache[uid] for uid in user_ids}

    def lookup_user(self, user_id):
        return self.lookup_users(user_ids=[user_id])[user_id]

    def _lookup_api_user(self, user_ids):
        resp = self.oauth_session.post(
            API_URL + "/users/lookup.json",
            data={"user_id": ",".join(user_ids)}
        )
        for u in resp.json():
            try:
                del u["status"]
            except KeyError:
                pass
            download_profile_image(u)
            self.cache[u["id_str"]] = u


def download_profile_image(user_object):
    _download_profile_image_raw(
        screen_name=user_object["screen_name"],
        profile_image_url=user_object["profile_image_url_https"]
    )

def _download_profile_image_raw(screen_name, profile_image_url):
    out_dir = os.path.join(
        BACKUP_DIR_PROFILE_IMAGES,
        screen_name[0].lower(),
        screen_name
    )
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(
        out_dir,
        os.path.basename(profile_image_url).replace("_normal", ""))

    if os.path.exists(out_path):
        return

    try:
        atomic_urlretrieve(
            url=profile_image_url.replace("_normal", "_400x400"),
            filename=out_path)
    except HTTPError:
        atomic_urlretrieve(url=profile_image_url, filename=out_path)


def atomic_urlretrieve(url, filename):
    tmp_filename = filename + ".tmp"
    try:
        urlretrieve(url, tmp_filename)
    except HTTPError:
        try:
            os.unlink(tmp_filename)
        except FileNotFoundError:
            pass
        raise
    else:
        os.rename(tmp_filename, filename)


def save_tweet(tweet, dirname):
    tweet_id = tweet["id_str"]
    path = os.path.join(BACKUP_DIR, dirname, tweet_id[:2], tweet_id)

    if os.path.exists(path):
        return

    tmp_path = path + ".tmp"

    os.makedirs(tmp_path, exist_ok=True)
    with open(os.path.join(tmp_path, "info.json"), "w") as outfile:
        outfile.write(json.dumps(tweet))

    download_profile_image(tweet["user"])

    try:
        extended_entities = tweet["extended_entities"]
    except KeyError:
        extended_entities = tweet["entities"]

    else:
        media = extended_entities.pop("media")

        for m in media:
            url = m["media_url_https"]
            filename = os.path.join(
                tmp_path, os.path.basename(urlparse(url).path)
            )
            urlretrieve(url=url, filename=filename)

            assert not extended_entities

    os.rename(tmp_path, path)
