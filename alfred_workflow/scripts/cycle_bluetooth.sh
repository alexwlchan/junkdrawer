#!/usr/bin/env bash

set -o errexit
set -o nounset

PATH=/usr/local/bin:$PATH

if [[ $(blueutil status) == "Status: on" ]]; then
    blueutil off
    blueutil on
elif [[ $(blueutil status) == "Status: off" ]]; then
    blueutil on
    blueutil off
else
    echo $(blueutil status)
    exit 1
fi
