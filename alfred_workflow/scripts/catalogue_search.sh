#!/usr/bin/env bash

set -o errexit
set -o nounset

open /Applications/Google\ Chrome.app/ \
  --new --args --new-window \
    "https://api.wellcomecollection.org/catalogue/v2/works?query=$1"
