#!/usr/bin/env bash

set -o errexit
set -o nounset

ROOT="$(git rev-parse --show-toplevel)"
DIR="$ROOT"/2017

NAME=$(echo "$1" | tr "." " " | awk '{print $1}')

make --silent "$NAME.out"
make --silent "$DIR"/.docker/gorunner

docker run --rm \
  --volume "$DIR":/bin \
  --workdir /bin \
  alexwlchan/gorunner /bin/"$NAME".out
