#!/usr/bin/env bash

set -o errexit
set -o nounset

ROOT="$(git rev-parse --show-toplevel)"
AWS="$ROOT"/aws

make "$1.out"
make "$ROOT"/.docker/gorunner

docker run --rm \
  --volume "$AWS":/bin \
  --volume ~/.aws:/root/.aws \
  alexwlchan/gorunner /bin/"$1".out
