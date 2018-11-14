#!/usr/bin/env bash

set -o errexit
set -o nounset

ROOT="$(git rev-parse --show-toplevel)"
AWS="$ROOT"/aws

NAME=$(echo "$1" | tr "." " " | awk '{print $1}')

make "$NAME.out"
make "$ROOT"/.docker/gorunner

docker run --rm \
  --volume "$AWS":/bin \
  --volume ~/.aws:/root/.aws \
  alexwlchan/gorunner /bin/"$NAME".out
