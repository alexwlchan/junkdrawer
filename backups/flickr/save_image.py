#!/usr/bin/env python
# -*- encoding: utf-8

import datetime as dt
import json
import pathlib
import sys
import tempfile

import bs4
import hyperlink
import urllib3
import xmltodict


BACKUP_ROOT = pathlib.Path.home() / "Documents" / "backups" / "flickr"


def get_canonical_url(url):
    http = urllib3.PoolManager()

    seen_urls = set(url)

    url = url.split("/in/")[0]

    while True:
        resp = http.request(
            "GET", url,
            redirect=False,
            headers={"User-Agent": "urllib3"}
        )

        try:
            url = resp.headers["Location"]
        except KeyError:
            return url

        if url in seen_urls:
            raise ValueError("Circular redirect: {url}")
        else:
            seen_urls.add(url)


def build_url(base, params):
    u = hyperlink.URL.from_text(base)
    for k, v in params.items():
        u = u.set(k, v)
    return u


def get_oembed_data(canonical_url):
    http = urllib3.PoolManager()

    request_url = build_url(
        "https://www.flickr.com/services/oembed/",
        params={"url": url}
    )

    oembed_resp = http.request("GET", str(request_url))
    assert oembed_resp.status == 200, oembed_resp.status
    return xmltodict.parse(oembed_resp.data)["oembed"]


def get_description(url):
    http = urllib3.PoolManager()

    resp = http.request("GET", url)
    assert resp.status == 200, resp.status

    soup = bs4.BeautifulSoup(resp.data, "html.parser")
    return soup.find("meta", attrs={"name": "description"}).attrs["content"]


def get_backup_dir(canonical_url, oembed_data):
    parsed_url = hyperlink.URL.from_text(canonical_url.strip("/"))

    assert parsed_url.path[0] == "photos", parsed_url

    flickr_id = parsed_url.path[-1]
    assert flickr_id.isnumeric()

    author_url = oembed_data["author_url"].strip("/")
    creator = hyperlink.URL.from_text(author_url).path[-1]

    return BACKUP_ROOT / f"{creator}-{flickr_id}"


def save_image(out_dir, oembed_data):
    http = urllib3.PoolManager()

    img_url = oembed_data["url"]
    filename = hyperlink.URL.from_text(img_url).path[-1]

    # See https://stackoverflow.com/q/17285464/1558022
    resp = http.request("GET", img_url, preload_content=False)

    with (out_dir / filename).open("wb") as out:
        while True:
            data = resp.read(1024)
            if not data:
                break
            out.write(data)

    resp.release_conn()


if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <FLICKR_URL>")

    canonical_url = get_canonical_url(url)
    oembed_data = get_oembed_data(canonical_url)

    backup_dir = get_backup_dir(canonical_url, oembed_data)
    backup_dir.parent.mkdir(exist_ok=True)

    if backup_dir.exists():
        print("Already saved!")
        sys.exit(0)

    description = get_description(canonical_url)

    flickr_info = {
        "url": url,
        "canonical_url": canonical_url,
        "saved_at": dt.datetime.now().isoformat(),
        "description": description,
        "oembed_data": oembed_data
    }

    json_string = json.dumps(flickr_info, indent=2, sort_keys=True)

    tmp_dir = pathlib.Path(tempfile.mkdtemp())
    (tmp_dir / "info.json").write_text(json_string)

    save_image(tmp_dir, oembed_data)

    tmp_dir.rename(backup_dir)
    print(backup_dir)
