set -x BACKUP_TWITTER $DIR/../backups/twitter

set TW_PYTHON /Users/alexwlchan/.virtualenvs/twitter/bin/python


function fave --argument-names url
  if test -z "$url"
    set url (furl)
  end

  eval $TW_PYTHON "$BACKUP_TWITTER/backup_single_tweet.py" --dirname=favorites --url="$url"
end


function selfie --argument-names url
  if test -z "$url"
    set url (furl)
  end

  eval $TW_PYTHON "$BACKUP_TWITTER/backup_single_tweet.py" --dirname=selfies --url="$url"
end


function trans-happy --argument-names url
  if test -z "$url"
    set url (furl)
  end

  eval $TW_PYTHON "$BACKUP_TWITTER/backup_single_tweet.py" --dirname=trans-happy --url="$url"
end


function backup_twitter
  bash $BACKUP_TWITTER/backup_twitter.sh
end


function rollup_thread --argument-names url
  if test -z "$url"
    set url (furl)
  end

  eval $TW_PYTHON "$BACKUP_TWITTER/rollup_thread.py" "$url"
end
