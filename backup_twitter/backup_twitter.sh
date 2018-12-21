#!/bin/bash

set -o errexit

source ~/.virtualenvs/twitter/bin/activate

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo ""
echo "*** user_timeline"
python $DIR/backup_twitter.py \
  --credentials=$DIR/auth.json \
  --dir=/Users/alexwlchan/Dropbox/twitter/user_timeline \
  --method=user_timeline

echo ""
echo "*** mentions"
python $DIR/backup_twitter.py \
  --credentials=$DIR/auth.json \
  --dir=/Users/alexwlchan/Dropbox/twitter/mentions \
  --method=mentions_timeline

echo ""
echo "*** favorites"
python $DIR/backup_twitter.py \
  --credentials=$DIR/auth.json \
  --dir=/Users/alexwlchan/Dropbox/twitter/favorites \
  --method=favorites

echo ""
echo "*** direct messages"
python $DIR/backup_dms.py
