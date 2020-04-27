#!/usr/bin/env python
"""
Search for a programme in BBC iPlayer and download all the episodes with youtube-dl.

See https://github.com/MikeRalphson/bbcparse/blob/master/iblApi/ibl_openapi_header.yaml
"""

import subprocess
import sys

import httpx
import inquirer


def find_programme_id(search_query):
    resp = httpx.get(
        "https://ibl.api.bbci.co.uk/ibl/v1/search", params={"q": search_query}
    )
    resp.raise_for_status()

    choices = [
        (programme["title"], programme)
        for programme in resp.json()["search"]["results"]
    ]

    if len(choices) == 1:
        return choices[0][1]
    elif not choices:
        sys.exit(f"No programmes found that matched {search_query!r}")
    else:
        questions = [
            inquirer.List(
                "programme",
                message="What programme do you want to download?",
                choices=[title for title, _ in choices]
            )
        ]

        answers = inquirer.prompt(questions)
        programme_title = answers["programme"]

        return dict(choices)[programme_title]


def get_episodes(programme_id):
    resp = httpx.get(
        f"http://ibl.api.bbci.co.uk/ibl/v1/programmes/{programme_id}/episodes"
    )
    resp.raise_for_status()

    yield from resp.json()["programme_episodes"]["elements"]


if __name__ == "__main__":
    programme = find_programme_id(sys.argv[1])

    for episode in get_episodes(programme["id"]):
        subprocess.check_call([
            "youtube-dl",
            "--write-sub", "--convert-subs", "srt",
            f"https://www.bbc.co.uk/iplayer/episode/{episode['id']}",
        ])
