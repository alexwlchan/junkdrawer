#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o verbose

HOST="$1"

scp -i ~/.ssh/wellcomedigitalstorage -r ~/.aws ec2-user@"$HOST":aws
scp -i ~/.ssh/wellcomedigitalstorage -r ~/.ssh ec2-user@"$HOST":ssh

set +o verbose
RED='\033[0;31m'
NC='\033[0m'

echo -e "When you log in, run"
echo -e "${RED}sudo su${NC}"
echo ""
echo -e "Then run the following command:"
echo -e "${RED}yum install -y python3 make docker git; systemctl start docker; mv ssh/id_rsa ~/.ssh; mv aws ~/.aws; git clone git@github.com:wellcometrust/storage-service.git; cd storage-service${NC}"
set -o verbose

ssh -i ~/.ssh/wellcomedigitalstorage ec2-user@"$HOST"
