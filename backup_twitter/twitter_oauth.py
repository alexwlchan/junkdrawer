# -*- encoding: utf-8

import os
from urllib.error import HTTPError
from urllib.request import urlretrieve

from requests_oauthlib import OAuth1Session


API_URL = "https://api.twitter.com/1.1"

BACKUP_DIR = os.path.join(os.environ["HOME"], "Documents", "backups", "twitter")
BACKUP_DIR_PROFILE_IMAGES = os.path.join(BACKUP_DIR, "profile_images")
BACKUP_DIR_DMS = os.path.join(BACKUP_DIR, "direct_messages")


def create_session(credentials):
    sess = OAuth1Session(
        client_key=credentials.consumer_key,
        client_secret=credentials.consumer_secret,
        resource_owner_key=credentials.access_token,
        resource_owner_secret=credentials.access_token_secret
    )

    # Raise an exception on any responses that don't return a 200 OK.

    def raise_for_status(resp, *args, **kwargs):
        resp.raise_for_status()

    sess.hooks["response"].append(raise_for_status)

    return sess


class UserInfo:

    def __init__(self, sess):
        self.sess = sess
        self.cache = {}

    def lookup_users(self, user_ids):
        missing = [uid for uid in user_ids if uid not in self.cache]
        if missing:
            self._api_lookup(missing)
        return {uid: self.cache[uid] for uid in user_ids}

    def lookup_user(self, user_id):
        return self.lookup_users(user_ids=[user_id])[user_id]

    def _api_lookup(self, user_ids):
        resp = self.sess.post(
            API_URL + "/users/lookup.json",
            data={"user_id": ",".join(user_ids)}
        )
        for u in resp.json():
            try:
                del u["status"]
            except KeyError:
                pass
            self._download_profile_image(u)
            self.cache[u["id_str"]] = u

    def _download_profile_image(self, user_object):
        self._download_profile_image_raw(
            screen_name=user_object["screen_name"],
            profile_image_url=user_object["profile_image_url_https"]
        )

    def _download_profile_image_raw(self, screen_name, profile_image_url):
        out_dir = os.path.join(BACKUP_DIR_PROFILE_IMAGES, screen_name)
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
