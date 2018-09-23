set -x BACKUP_TWITTER $DIR/../backup_twitter


alias fave='/Users/alexwlchan/.virtualenvs/twitter/bin/python "$BACKUP_TWITTER/save_single_tweet.py" --dst=favorites --url=(furl)'
alias selfie='/Users/alexwlchan/.virtualenvs/twitter/bin/python "$BACKUP_TWITTER/save_single_tweet.py" --dst=selfies --url=(furl)'


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
