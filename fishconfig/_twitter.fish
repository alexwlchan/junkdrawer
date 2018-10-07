set -x BACKUP_TWITTER $DIR/../backup_twitter


function fave --argument-names url
  if test -z "$url"
    set url (furl)
  end

  /Users/alexwlchan/.virtualenvs/twitter/bin/python "$BACKUP_TWITTER/save_single_tweet.py" --dst=favorites --url="$url"
end


function selfie --argument-names url
  if test -z "$url"
    set url (furl)
  end

  /Users/alexwlchan/.virtualenvs/twitter/bin/python "$BACKUP_TWITTER/save_single_tweet.py" --dst=selfies --url="$url"
end


function backup_twitter
  bash $BACKUP_TWITTER/backup_twitter.sh
  osascript -e '
    tell application "Things3"
      repeat with todayToDo in to dos of list "Today"
        if ((name of todayToDo) = "Run my tweet backup script") then
          set status of todayToDo to completed
        end if
      end repeat
    end tell
  '
end


function rollup_thread
  set dst ~/notes/"$argv[1].md"
  if [ -f "$dst" ]
    echo "$name already exists!" >&2
    return 1
  end

  bash $BACKUP_TWITTER/rollup_thread.sh (furl) > "$dst"
  open "$dst"
end
