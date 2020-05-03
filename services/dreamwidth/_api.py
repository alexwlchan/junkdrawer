# -*- encoding: utf-8
"""
Dreamwidth API wrapper class.

Useful links:
    - https://dw-dev-training.dreamwidth.org/58924.html?thread=383532
    - https://github.com/ziarkaen/dreamwidth-gsoc/blob/2f73355b60d59288bc78671cebe901879121fe8a/dreamwidth-library/dreamwidth2.py
    - http://wiki.dwscoalition.org/wiki/index.php/XML-RPC_Protocol
    - https://www.livejournal.com/doc/server/ljp.csp.xml-rpc.protocol.html

"""

import json

try:
    from xmlrpclib import Binary, ServerProxy
except ImportError:  # Python 3
    from xmlrpc.client import Binary, ServerProxy

import requests


class DreamwidthAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.server = ServerProxy("https://www.dreamwidth.org/interface/xmlrpc")

    def call_endpoint(self, method_name, data=None):
        if data is None:
            data = {}

        # See http://wiki.dwscoalition.org/wiki/index.php/XML-RPC_Protocol_Method:_login
        data.update(
            {
                "username": self.username,
                "password": self.password,
                "auth_method": "clear",
                "ver": "1",
            }
        )

        method = getattr(self.server, "LJ.XMLRPC." + method_name)
        return method(data)

    def get_all_posts(self):
        data = {"selecttype": "lastn", "howmany": 50}

        # I'm doing my own book-keeping of event IDs to ensure that this function
        # never returns a duplicate item, even if we mess up the API call and
        # end up retrieving an item more than once.
        #
        # This will happen on the ``beforedate`` boundary, because I deliberately
        # fudge the date slightly to ensure we're getting everything before *or on*
        # the time specified by ``beforedate``.
        seen_event_ids = set()

        while True:
            resp = self.call_endpoint("getevents", data=data)

            # If we've seen every event in this array already, we must be at
            # the end of the journal.  Abort!
            if all(event["itemid"] in seen_event_ids for event in resp["events"]):
                break

            for event in resp["events"]:
                event_id = event["itemid"]
                if event_id not in seen_event_ids:
                    yield event
                    seen_event_ids.add(event_id)

            # This ensures that if there were multiple posts at the same time as
            # the earliest event in the response, we'll get all of them.
            sorted_logtimes = sorted(set(event["logtime"] for event in resp["events"]))
            data["beforedate"] = sorted_logtimes[1]

    def get_custom_access_groups(self):
        return self.call_endpoint("gettrustgroups")["trustgroups"]


class BinaryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Binary):
            return obj.data.decode("utf8")
        return super().default(obj)


class DreamwidthSession:
    def __init__(self, username, password):
        self.sess = requests.Session()

        resp = self.sess.post(
            "https://www.dreamwidth.org/login",
            data={"user": username, "password": password, "action:login": "Log in"},
        )
        resp.raise_for_status()

        # Dreamwidth always returns an HTTP 200, even if login fails.  This is a
        # better way to check if login succeeded.
        assert "Welcome back to Dreamwidth!" in resp.text

    def get(self, *args, **kwargs):
        return self.sess.get(*args, **kwargs)
