#!/bin/bash

set -o errexit

source ~/.virtualenvs/twitter/bin/activate

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

python $DIR/rollup_thread.py --credentials=$DIR/auth.json --url="$1"
