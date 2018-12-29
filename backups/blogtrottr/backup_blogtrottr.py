# -*- encoding: utf-8

import datetime as dt
import os

import click
import requests


def fetch_blogtrottr_opml(*, username, password):
    """Fetch the subscriptions OPML for a Blogtrottr account."""
    sess = requests.Session()

    # TODO: Check this request succeeded
    sess.post(
        'https://blogtrottr.com/loginhandler/',
        data={
            'username': username,
            'password': password,
        }
    )

    return sess.get('https://blogtrottr.com/opml_export/').text


@click.command()
@click.option("--username", required=True, help="Blogtrottr account email address")
@click.option("--password", required=True)
def save_opml(username, password):
    opml = fetch_blogtrottr_opml(username=username, password=password)

    backup_dir = os.path.join(os.environ["HOME"], "Documents", "backups", "blogtrottr")
    os.makedirs(backup_dir, exist_ok=True)

    date_string = dt.datetime.now().strftime('%Y-%m-%d')
    out_path = os.path.join(backup_dir, f"{date_string}_subscriptions.opml")

    with open(out_path, "w") as outfile:
        outfile.write(opml)


if __name__ == '__main__':
    save_opml()
