# -*- encoding: utf-8

import json
import logging
import os

import daiquiri
from wellcome_storage_service import StorageServiceClient


def get_logger(name):
    daiquiri.setup(
        level=logging.INFO,
        outputs=[
            daiquiri.output.Stream(formatter=daiquiri.formatter.ColorFormatter(
                fmt="%(asctime)s.%(msecs)03d %(color)s[%(levelname)s] %(message)s%(color_stop)s",
                datefmt="%H:%M:%S"
            ))
        ]
    )

    return daiquiri.getLogger(name)


def get_storage_client(api_url):
    creds_path = os.path.join(
        os.environ["HOME"], ".wellcome-storage", "oauth-credentials.json"
    )
    oauth_creds = json.load(open(creds_path))

    return StorageServiceClient(
        api_url=api_url,
        client_id=oauth_creds["client_id"],
        client_secret=oauth_creds["client_secret"],
        token_url=oauth_creds["token_url"],
    )
