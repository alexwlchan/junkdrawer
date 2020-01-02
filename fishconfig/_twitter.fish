function fave --argument-names url
  if test -z "$url"
    set url (furl)
  end

  python3 ~/repos/backup_twitter/scripts/save_single_tweet.py "$url" --dirname=likes
end


function selfie --argument-names url
  if test -z "$url"
    set url (furl)
  end

  python3 ~/repos/backup_twitter/scripts/save_single_tweet.py "$url" --dirname=selfies
end


function trans-happy --argument-names url
  if test -z "$url"
    set url (furl)
  end

  python3 ~/repos/backup_twitter/scripts/save_single_tweet.py "$url" --dirname=trans-happy
end
