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


BACKUP_ROOT = pathlib.Path.home() / "Documents" / "backups" / "deviantart"


def build_url(base, params):
    u = hyperlink.URL.from_text(base)
    for k, v in params.items():
        u = u.set(k, v)
    return u


def get_canonical_url(url):
    http = urllib3.PoolManager()

    seen_urls = set(url)

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


def get_backup_dir(canonical_url):
    page_url = hyperlink.URL.from_text(canonical_url)

    artist = page_url.path[0]
    deviantart_id = page_url.path[-1].split("-")[-1]
    assert deviantart_id.isnumeric(), deviantart_id

    return BACKUP_ROOT / f"{artist}-{deviantart_id}"


def get_oembed_data(canonical_url):
    http = urllib3.PoolManager()

    request_url = build_url(
        "https://backend.deviantart.com/oembed",
        params={"url": url}
    )

    oembed_resp = http.request("GET", str(request_url))
    assert oembed_resp.status == 200, oembed_resp
    return json.loads(oembed_resp.data)


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


def get_page_state(canonical_url):
    http = urllib3.PoolManager()

    resp = http.request("GET", canonical_url, headers={"User-Agent": "urllib3"})
    assert resp.status == 200, resp.status

    # We're looking for a line that goes
    #
    #       window.__INITIAL_STATE__ = JSON.parse(…);
    #
    # which contains a heap of useful data.
    soup = bs4.BeautifulSoup(resp.data, "html.parser")
    js_lines = soup.find("body").find("script").text.splitlines()

    initial_state = next(
        line.strip()
        for line in js_lines
        if line.strip().startswith("window.__INITIAL_STATE__")
    )
    json_string = initial_state[len('window.__INITIAL_STATE__ = JSON.parse('):-len(');')]

    return json.loads(json.loads(json_string))


if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <DEVIANTART_URL>")

    canonical_url = get_canonical_url(url)

    backup_dir = get_backup_dir(canonical_url)
    backup_dir.parent.mkdir(exist_ok=True)

    page_state = get_page_state(canonical_url)

    if backup_dir.exists():
        print("Already saved!")
        sys.exit(0)

    oembed_data = get_oembed_data(canonical_url)

    extended_deviation = page_state["@@entities"]["deviationExtended"]
    assert len(extended_deviation) == 1
    extended_deviation = list(extended_deviation.values())[0]
    del extended_deviation["relatedStreams"]

    deviation_info = {
        "url": url,
        "canonical_url": canonical_url,
        "saved_at": dt.datetime.now().isoformat(),
        "extended_deviation": extended_deviation,
        "oembed_data": oembed_data
    }

    json_string = json.dumps(deviation_info, indent=2, sort_keys=True)

    tmp_dir = pathlib.Path(tempfile.mkdtemp())
    (tmp_dir / "info.json").write_text(json_string)

    save_image(tmp_dir, oembed_data)

    tmp_dir.rename(backup_dir)
    print(backup_dir)
