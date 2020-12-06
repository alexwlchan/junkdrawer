#!/usr/bin/env bash

set -o errexit
set -o nounset

USERNAME="alexwlchan"
PASSWORD=$(keyring get pinboard password)

mkdir -p ~/Documents/backups/pinboard

for script in save_bookmarks_list.py save_cache_ids.py save_archive_copies.py save_wget_copies.py save_ao3_exports.py
do
  python3 "$script" --username="$USERNAME" --password="$PASSWORD"
done
