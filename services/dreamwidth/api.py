# -*- encoding: utf-8
"""
Dreamwidth API wrapper class.

Useful links:
    - https://dw-dev-training.dreamwidth.org/58924.html?thread=383532
    - https://github.com/ziarkaen/dreamwidth-gsoc/blob/2f73355b60d59288bc78671cebe901879121fe8a/dreamwidth-library/dreamwidth2.py
    - http://wiki.dwscoalition.org/wiki/index.php/XML-RPC_Protocol
    - https://www.livejournal.com/doc/server/ljp.csp.xml-rpc.protocol.html

"""

import hashlib
import json
from xmlrpc.client import Binary, ServerProxy


def md5(s):
    h = hashlib.md5()
    h.update(s.encode("ascii"))
    return h.hexdigest()


class DreamwidthAPI:

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.server = ServerProxy("https://www.dreamwidth.org/interface/xmlrpc")

    def auth_info(self):
        # Invoke LJ.XMLRPC.getchallenge on the endpoint.
        # See https://dw-dev-training.dreamwidth.org/58924.html?thread=383532
        challenge_resp = self.server.LJ.XMLRPC.getchallenge()
        auth_challenge = challenge_resp["challenge"]

        auth_response = md5(auth_challenge + md5(self.password))
        return {
            "username": self.username,
            "auth_method": "challenge",
            "auth_challenge": auth_challenge,
            "auth_response": auth_response
        }

    def call_endpoint(self, method_name, data=None):
        if data is None:
            data = {}
        data.update(self.auth_info())
        data.update({"ver": "1"})

        method = getattr(self.server, "LJ.XMLRPC." + method_name)
        return method(data)

    def get_all_posts(self):
        data = {
            "selecttype": "lastn",
            "howmany": 50
        }

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
            sorted_logtimes = sorted(
                set(event["logtime"] for event in resp["events"])
            )
            data["beforedate"] = sorted_logtimes[1]

    def get_custom_access_groups(self):
        return self.call_endpoint("gettrustgroups")["trustgroups"]


class BinaryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Binary):
            return obj.data.decode("utf8")
        return super().default(obj)
