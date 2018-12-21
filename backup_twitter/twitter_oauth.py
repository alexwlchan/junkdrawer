# -*- encoding: utf-8

from requests_oauthlib import OAuth1Session


API_URL = "https://api.twitter.com/1.1"


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
            self.cache[u["id_str"]] = u
