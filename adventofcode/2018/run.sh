#!/usr/bin/env bash

set -o errexit
set -o nounset

docker run --rm --tty --volume $(pwd):/data --workdir /data ruby:alpine ruby "day$1.rb"
