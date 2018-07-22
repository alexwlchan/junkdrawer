#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o xtrace

for dirname in scrapbook pinboard
do
  ssh alexwlchan@helene.linode tar -czf "$dirname".tar.gz "$dirname"
  scp alexwlchan@helene.linode:"$dirname".tar.gz ~/"$dirname".tar.gz
  ssh alexwlchan@helene.linode rm "$dirname".tar.gz
done
