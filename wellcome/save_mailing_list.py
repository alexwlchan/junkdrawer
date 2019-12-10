#!/usr/bin/env python
# -*- encoding: utf-8

import csv
import datetime as dt
import getpass
import os
import sys

import bs4
import requests
import tqdm


def raise_for_status(resp, *args, **kwargs):
    resp.raise_for_status()


def login_to_trustnet(sess, *, username, password):
    resp = sess.get(
        "https://trustnet.wellcome.ac.uk/user/login",
        params={"destination": "node/62"}
    )

    soup = bs4.BeautifulSoup(resp.text, "html.parser")

    hidden_input = soup.find("input", attrs={"type": "hidden", "name": "form_build_id"})
    form_build_id = hidden_input.attrs["value"]

    resp = sess.post(
        "https://trustnet.wellcome.ac.uk/user/login",
        data={
            "name": username,
            "pass": password,
            "persistent_login": "1",
            "form_build_id": form_build_id,
            "form_id": "user_login",
            "op": "Log in",
        },
        params={"destination": "node/62"}
    )

    assert "<title>Log in | Trustnet</title>" not in resp.text, resp.text


def get_members(html_string):
    soup = bs4.BeautifulSoup(html_string, "html.parser")

    sections = [
        soup.find("section", attrs={"id": "owners"}),
        soup.find("section", attrs={"id": "members"}),
    ]

    for sec in sections:
        for li_element in sec.find_all("li", attrs={"class": "list-members--item"}):
            yield (
                li_element.find("a").attrs["href"],
                li_element.find("h3", attrs={"class": "title"}).text
            )


def get_followers(html_string):
    soup = bs4.BeautifulSoup(html_string, "html.parser")

    for li_element in soup.find_all("li", attrs={"class": "list-members--item"}):
        yield (
            li_element.find("a").attrs["href"],
            li_element.find("h3", attrs={"class": "title"}).text
        )


def get_email_address(sess, user_link):
    resp = sess.get("https://trustnet.wellcome.ac.uk/" + user_link)
    soup = bs4.BeautifulSoup(resp.text, "html.parser")

    profile = soup.find("div", attrs={"class": "profile__contact"})
    return profile.find("a", attrs={"itemprop": "email"}).text


if __name__ == "__main__":
    GROUP_ID = "13207"

    username = getpass.getuser()
    print(f"Logging in as {username}", file=sys.stderr)
    password = getpass.getpass()

    sess = requests.Session()
    sess.hooks["response"].append(raise_for_status)

    login_to_trustnet(sess, username=username, password=password)

    resp_members = sess.get(f"https://trustnet.wellcome.ac.uk/members-listing/{GROUP_ID}")
    resp_followers = sess.get(f"https://trustnet.wellcome.ac.uk/node/{GROUP_ID}/followers")

    all_users = set()

    for member in get_members(resp_members.text):
        all_users.add(member)

    # for follower in get_followers(resp_followers.text):
    #     all_users.add(follower)

    email_addresses = set()

    date_string = dt.datetime.now().strftime("%Y-%m-%d_%H-%M")
    out_path = f"members_{GROUP_ID}_{date_string}.csv"

    with open(out_path + ".tmp", "w") as csvfile:
        fieldnames = ["link", "name", "email_address"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for user_link, name in tqdm.tqdm(all_users):
            row = {
                # TODO: Use hyperlink for this
                "link": ("https://trustnet.wellcome.ac.uk/" + user_link).replace("//", "/"),

                "name": name,
                "email_address": get_email_address(sess, user_link),
            }

            writer.writerow(row)

    os.rename(out_path + ".tmp", out_path)
