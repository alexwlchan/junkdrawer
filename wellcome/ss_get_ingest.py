#!/usr/bin/env python
# -*- encoding: utf-8
"""
Look up an ingest.  Usage:

    python ss_get_ingest.py <INGEST_ID>

The script will check both APIs for the ingest ID.

"""

import logging
import sys

import termcolor
from wellcome_storage_service import IngestNotFound

from ss_ingests import get_logger, get_storage_client


logger = get_logger(__name__)


def lookup_ingest(ingest_id):
    logger.debug("Looking up ingest ID %s", ingest_id)

    api_variants = {
        "stage": "api-stage",
        "prod": "api",
    }

    for name, host in api_variants.items():
        logging.debug("Checking %s API", name)

        api_url = f"https://{host}.wellcomecollection.org/storage/v1"
        client = get_storage_client(api_url)

        try:
            ingest = client.get_ingest(ingest_id)
        except IngestNotFound:
            logging.debug("Not found in %s API", name)
        else:
            logging.debug("Found ingest in %s API:", name)
            return ingest

    logging.error("Could not find %s in either API!", ingest_id)
    sys.exit(1)


if __name__ == "__main__":
    try:
        ingest_id = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <INGEST_ID>")

    ingest = lookup_ingest(ingest_id)

    print("Source:      s3://%s/%s" % (
        ingest["sourceLocation"]["bucket"],
        ingest["sourceLocation"]["path"],
    ))
    print("Space:       %s" % ingest["space"]["id"])
    print("External ID: %s" % ingest["bag"]["info"]["externalIdentifier"])
    print("")

    print("Events:")

    for event in ingest["events"]:
        print(" * %s" % event["description"])

    print("")

    status = ingest["status"]["id"]
    colour = {
        "accepted": "yellow",
        "processing": "yellow",
        "succeeded": "green",
        "failed": "red",
    }[status]

    print("Status: %s" % termcolor.colored(status, colour))

    sys.exit(0)
