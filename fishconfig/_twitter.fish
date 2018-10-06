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
