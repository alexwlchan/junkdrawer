#!/usr/bin/env python

import datetime
import os
import math
import secrets
import string
import subprocess
import tempfile

import eyed3
import httpx
import iterfzf
import jinja2


ROOT = "/Users/alexwlchan/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books/Audiobooks"


def find_audiobook_folders():
    for d in os.listdir(ROOT):
        path = os.path.join(ROOT, d)

        if os.path.isdir(path) and any(p.endswith(".mp3") for p in os.listdir(path)):
            yield path


def format_duration(duration: int) -> str:
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60

    return "%0d:%02d:%02d" % (hours, minutes, seconds)


def format_chart(proportion: float) -> str:
    width = 8
    chars = []

    percentage = int(round(proportion * width * 8))
    max_value = 1 * width * 8

    # The ASCII block elements come in chunks of 8, so we work out how
    # many fractions of 8 we need.
    # https://en.wikipedia.org/wiki/Block_Elements
    bar_chunks, remainder = divmod(percentage, 8)

    # First draw the full width chunks
    bar = '█' * bar_chunks

    # Then add the fractional part.  The Unicode code points for
    # block elements are (8/8), (7/8), (6/8), ... , so we need to
    # work backwards.
    if remainder > 0:
        bar += chr(ord('█') + (8 - remainder))

    # If the bar is empty, add a left one-eighth block
    bar = bar or  '▏'

    if len(bar) < width:
        return bar + (width - len(bar)) * '▁'
    else:
        return bar


def create_identifier(length: int = 8) -> str:
    """
    Creates an identifier with ``length`` alphanumeric characters.

    This identifier is designed to be:

    - easy for a human to read/copy
    - unambiguous in a sans-serif font
    - safe for use in a variety of contexts

    """
    letters = list(set(string.ascii_lowercase) - {"o", "i", "l"})
    numbers = list(set(string.digits) - {"0", "1"})

    return secrets.choice(letters) + "".join(
        secrets.choice(letters + numbers) for _ in range(length - 1)
    )


if __name__ == "__main__":
    audiobooks = {}

    for dirpath in find_audiobook_folders():
        mp3_filename = next(p for p in os.listdir(dirpath) if p.endswith(".mp3"))
        mp3_path = os.path.join(dirpath, mp3_filename)
        mp3_metadata = eyed3.load(mp3_path)

        audiobooks[mp3_metadata.tag.album] = dirpath

    title = iterfzf.iterfzf(sorted(audiobooks))
    dirpath = audiobooks[title]

    files = [
        os.path.join(dirpath, p) for p in os.listdir(dirpath) if p.endswith(".mp3")
    ]

    tmp_dir = tempfile.mkdtemp()

    audiobook_id = create_identifier()

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("."), autoescape=jinja2.select_autoescape()
    )
    env.filters["duration"] = format_duration
    env.filters["chart"] = format_chart

    episodes = []

    start = datetime.datetime.now() - datetime.timedelta(days=365)

    for f in files:
        mp3_metadata = eyed3.load(f)
        track_title = mp3_metadata.tag.title
        author = mp3_metadata.tag.artist
        seconds = int(math.ceil(mp3_metadata.info.time_secs))
        episodes.append(
            {
                "title": track_title,
                "filename": os.path.basename(f),
                "length": os.stat(f).st_size,
                "track_num": mp3_metadata.tag.track_num,
                "pub_date": (start + datetime.timedelta(days=mp3_metadata.tag.track_num[0])),
                "duration": seconds,
            }
        )

    episodes = sorted(episodes, key=lambda ep: ep["track_num"])

    total_duration = sum(ep["duration"] for ep in episodes)
    cumulative_duration = 0
    for ep in episodes:
        ep["cumulative_duration"] = cumulative_duration
        cumulative_duration += ep["duration"]

    episodes.reverse()

    template = env.get_template("create_audiobook_rss_feed.xml.template")
    with open("audiobook.xml", "w") as outfile:
        outfile.write(
            template.render(
                author=author,
                book_title=title,
                now=datetime.datetime.now(),
                audiobook_id=audiobook_id,
                episodes=episodes,
                total_duration=total_duration,
            )
        )

    subprocess.check_call(
        f"ssh alexwlchan@helene.linode mkdir -p /home/alexwlchan/sites/alexwlchan.net/files/audiobooks/{audiobook_id}",
        shell=True,
    )
    subprocess.check_call(
        f"scp audiobook.xml alexwlchan@helene.linode:/home/alexwlchan/sites/alexwlchan.net/files/audiobooks/{audiobook_id}/audiobook.xml",
        shell=True,
    )

    subprocess.check_call([
        "ffmpeg", "-i", files[0], "cover.jpg",
    ])
    subprocess.check_call(
        f"scp cover.jpg alexwlchan@helene.linode:/home/alexwlchan/sites/alexwlchan.net/files/audiobooks/{audiobook_id}/cover.jpg",
        shell=True,
    )


    for f in files:
        subprocess.check_call(
            [
                "scp",
                f,
                f"alexwlchan@helene.linode:/home/alexwlchan/sites/alexwlchan.net/files/audiobooks/{audiobook_id}/{os.path.basename(f)}",
            ]
        )

    r = httpx.get(
        "https://overcast.fm/ping",
        params={
            "urlprefix": f"https://alexwlchan.net/files/audiobooks/{audiobook_id}/"
        }
    )
    print(r)
    r.raise_for_status()

    print(f"https://alexwlchan.net/files/audiobooks/{audiobook_id}/audiobook.xml")
