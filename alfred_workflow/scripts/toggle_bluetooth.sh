#!/usr/bin/env bash

set -o errexit
set -o nounset

PATH=/usr/local/bin:$PATH

if [[ $(blueutil status) == "Status: on" ]]; then
    blueutil off
elif [[ $(blueutil status) == "Status: off" ]]; then
    blueutil on
else
    exit 1
fi
