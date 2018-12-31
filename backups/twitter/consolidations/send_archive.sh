#!/usr/bin/env bash

set -o errexit
set -o nounset

outfile=twitter_$(date +"%Y-%m-%d_%H-%M-%S").tar.gz

pushd ~/Documents/backups
  tar -zcvf "$outfile" twitter
  scp "$outfile" alexwlchan@alexs-imac.local:Documents/backups/twitter
popd
