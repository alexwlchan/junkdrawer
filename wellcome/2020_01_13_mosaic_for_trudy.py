#!/usr/bin/env python
"""
A script I wrote for Trudy on 13 Jan 2020 to extract a particular set of folders
from a hierarchy, as part of bringing in files from Mosaic.
"""

import os
import shutil
import subprocess

import tqdm


# Path to the original Mosaic files
SOURCE_DIR = "/Volumes/Publishing/Editorial/Editorial projects/MOSAIC/04 Content/02 Published"

# Path to save the export in
EXPORT_DIR = "mosaic"


os.makedirs(EXPORT_DIR, exist_ok=True)

for numbered_dir in tqdm.tqdm(os.listdir(SOURCE_DIR)):
    # print(f"Working on {numbered_dir}")
    source_path = os.path.join(SOURCE_DIR, numbered_dir)

    if not os.path.isdir(source_path):  # e.g. .DS_Store
        continue

    export_dir = os.path.join(EXPORT_DIR, numbered_dir)
    os.makedirs(export_dir, exist_ok=True)

    for name in ["00 Contracts and invoices", "05 Final article and extras"]:
        if not os.path.isdir(os.path.join(source_path, name)):
            continue

        export_name = os.path.join(export_dir, name)

        cmd = [
            "rsync", "--recursive",
            os.path.join(source_path, name),
            export_dir
        ]

        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Delete empty directories
        if os.path.isdir(export_name) and os.listdir(export_name) == []:
            shutil.rmtree(export_name)

    if os.listdir(export_dir) == []:
        shutil.rmtree(export_dir)
