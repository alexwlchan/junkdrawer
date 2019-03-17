#!/usr/bin/env python
# -*- encoding: utf-8

import datetime as dt
import json
import sys
import webbrowser

import click

from _api import DreamwidthAPI
from markdownify import md_to_dreamwidth_html


# First get the post source and convert to HTML
try:
    path = sys.argv[1]
except IndexError:
    sys.exit("Usage: %s <PATH>" % __file__)

md_src = open(path).read()
html_src = md_to_dreamwidth_html(md_src)


api = DreamwidthAPI(**json.load(open("auth.json")))


# Work out what the access groups are, and where this post should
# be shared.
choices = [
    ("public", {"security": "public"}),
    ("private", {"security": "private"}),
]

for access_group in api.get_custom_access_groups():
    choices.append(
        (access_group["name"] + " [filter]",
        {
            "security": "usemask",

            # I'm a bit iffy about this code, because the description isn't great.
            # What if you have more than 30 trust groups??
            #
            #   A 32-bit unsigned integer representing which of the user's
            #   trust groups are allowed to view this post. Turn bit 0 on to
            #   allow anyone with basic access to read it. Otherwise, turn
            #   bit 1-30 on for every trust group that should be allowed to
            #   read it. Bit 31 is reserved.
            #
            "allowmask": 2 ** access_group["id"]
        })
    )

numbered_choices = {
    i: (name, data)
    for (i, (name, data)) in enumerate(choices, start=1)
}


prompt_suffix = "\n".join(
    "%2d. %s" % (i, name)
    for (i, (name, _)) in numbered_choices.items()
)

group_id = click.prompt(
    "Where should this be posted?",
    type=click.Choice([str(key) for key in sorted(numbered_choices)]),
    value_proc=lambda t: int(t),
    prompt_suffix=":\n" + prompt_suffix + "\n"
)

group_name, security_data = numbered_choices[group_id]


# Now construct the post data.
now = dt.datetime.now()

title = click.prompt("What is the post title?")
tags = click.prompt("What are the post tags?", default="").split(",")

print("\n=== About to post: ===")
print("title:    %s" % title)
print("tags:     %s" % ", ".join(tags))
print("to group: %s" % group_name)
print("")
print(md_src[:95] + "...")
print("")

resp = click.confirm("Ready to post?", abort=True)

data = {
    "event": html_src,
    "subject": title,
    "year": now.strftime("%Y"),
    "mon": now.strftime("%m"),
    "day": now.strftime("%d"),
    "hour": now.strftime("%H"),
    "min": now.strftime("%M"),
    "props": {
        "taglist": ",".join(tags)
    }
}

data.update(**security_data)

resp = api.call_endpoint("postevent", data=data)
print(resp["url"])
webbrowser.open(resp["url"])
