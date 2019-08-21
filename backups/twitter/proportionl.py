#!/usr/bin/env python
# -*- encoding: utf-8

import click
import collections
import glob
import json
import textwrap

import termcolor


latest_following_file = max(
    glob.glob("/Users/alexwlchan/Documents/backups/twitter/friends/*.txt"))


OPTIONS = {
    "M": "man",
    "F": "woman",
    "NB": "non-binary",
    "NP": "not a person",
    "U": "unknown"
}

try:
    recorded = json.load(open("gender_of_following.json"))
except FileNotFoundError:
    recorded = {}


with open(latest_following_file) as infile:
    for line in infile:
        following = json.loads(line)

        if following["screen_name"] in recorded and recorded[following["screen_name"]] != "U":
            continue

        print(
            termcolor.colored(
                textwrap.dedent(f"""
                @{following['screen_name']} ({following['name']})
                {following['description']}
                """).strip(),
                "blue"
            )
        )

        guessed_gender = None

        description = following["description"].lower()
        if (
            ("enby" in description) or
            ("they/them" in description) or
            ("non-binary" in description)
        ):
            guessed_gender = "NB"
        elif ("trans woman" in description) or ("she/her" in description):
            guessed_gender = "F"
        elif "he/him" in description:
            guessed_gender = "M"

        gender = click.prompt(
            "What is their gender?",
            type=click.Choice(OPTIONS),
            default=guessed_gender,
            value_proc=lambda char: char.upper()
        )

        print("")

        recorded[following["screen_name"]] = gender
        with open("gender_of_following.json", "w") as outfile:
            outfile.write(json.dumps(recorded))

    print(collections.Counter(recorded.values()))
