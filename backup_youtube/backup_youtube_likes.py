#!/usr/bin/env python
# -*- encoding: utf-8
"""
Usage: backup_youtube_likes.py <GOOGLE_TAKEOUT_ZIP>
"""

import json
import os
import subprocess
import sys
import zipfile


BACKUP_DIR = os.path.join(
    os.environ["HOME"], "Documents", "backups", "youtube_playlists"
)


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit(__doc__.strip())

    zf = zipfile.ZipFile(path)

    playlists = [
        name
        for name in zf.namelist()
        if name.startswith("Takeout/YouTube/playlists/")
        and not name.endswith(("uploads.json", "watch-later.json"))
    ]

    for playlist_name in playlists:
        data = json.load(zf.open(name=playlist_name))

        name = os.path.splitext(os.path.basename(playlist_name))[0]

        backup_dir = os.path.join(BACKUP_DIR, name)
        os.makedirs(backup_dir, exist_ok=True)

        with open(os.path.join(backup_dir, "info.json"), "w") as outfile:
            outfile.write(json.dumps(data, indent=2, sort_keys=True))

        for entry in data:
            video_id = entry["contentDetails"]["videoId"]
            video_url = f"https://youtube.com/watch?v={video_id}"
            try:
                subprocess.check_call(
                    ["youtube-dl", video_url],
                    cwd=backup_dir,
                    stdout=subprocess.DEVNULL
                )
            except subprocess.CalledProcessError as err:
                print(f"{video_url} ({err})")
            else:
                print(".", end="", flush=True)

    os.rename(path, os.path.join(BACKUP_DIR, os.path.basename(path)))
