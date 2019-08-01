#!/usr/bin/env python
# -*- encoding: utf-8

import json
import logging
import os
import sys

import daiquiri
from wellcome_storage_service import IngestNotFound, StorageServiceClient


daiquiri.setup(
    level=logging.INFO,
    outputs=[
        daiquiri.output.Stream(formatter=daiquiri.formatter.ColorFormatter(
            fmt="%(asctime)s.%(msecs)03d %(color)s[%(levelname)s] %(name)s -> %(message)s%(color_stop)s",
            datefmt="%H:%M:%S"
        ))
    ]
)

logger = daiquiri.getLogger(__name__)


if __name__ == "__main__":
    try:
        ingest_id = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <INGEST_ID>")

    logger.debug("Looking up ingest ID %s", ingest_id)

    creds_path = os.path.join(
        os.environ["HOME"], ".wellcome-storage", "oauth-credentials.json"
    )
    oauth_creds = json.load(open(creds_path))

    api_variants = {
        "stage": "api-stage",
        "prod": "api",
    }

    for name, host in api_variants.items():
        logging.debug("Checking %s API", name)

        api_url = f"https://{host}.wellcomecollection.org/storage/v1"

        sess = StorageServiceClient(
            api_url=api_url,
            client_id=oauth_creds["client_id"],
            client_secret=oauth_creds["client_secret"],
            token_url=oauth_creds["token_url"],
        )

        try:
            ingest = sess.get_ingest(ingest_id)
        except IngestNotFound:
            logging.debug("Not found in %s API", name)
        else:
            logging.debug("Found ingest in %s API:", name)
            print(json.dumps(ingest, indent=2, sort_keys=True))
            sys.exit(0)

    logging.error("Could not find %s in either API!", ingest_id)
    sys.exit(1)

