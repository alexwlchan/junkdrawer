#!/usr/bin/env bash

source ~/.virtualenvs/twitter/bin/activate

set -o errexit
set -o nounset
set -o verbose

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pushd "$DIR"
  python backup_user_timeline.py
  python backup_mentions.py
  python backup_favorites.py
  python $DIR/backup_dms.py
  python save_followers.py
  python save_friends.py

  osascript -e '
    tell application "Things3"
      repeat with todayToDo in to dos of list "Today"
        if ((name of todayToDo) = "Run my tweet backup script") then
          set status of todayToDo to completed
        end if
      end repeat
    end tell
  '
popd

pushd ~/Documents/backups/twitter
  find . -type d -empty
  find . -type d -empty | wc -l
  find . -type d -empty -delete
popd
