#!/usr/bin/env python
# -*- encoding: utf-8

import os
import shutil
import subprocess
import sys
import tempfile

BACKUP_ROOT = os.path.join(os.environ["HOME"], "Documents", "backups", "twitter")


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <TARFILE_PATH>")

    # tmp_dir = tempfile.mkdtemp()
    # subprocess.check_call(["tar", "-xf", path, "-C", tmp_dir])
    tmp_dir = "/var/folders/tq/m5sckx6j72q9xr115j1fkhz00000gn/T/tmpi9nv0ryk"

    os.chdir(os.path.join(tmp_dir, "twitter"))

    try:
        os.unlink(".DS_Store")
    except FileNotFoundError:
        pass

    for transfer_dir, _, filenames in os.walk("."):
        if not filenames:
            continue

        backup_dir = os.path.join(BACKUP_ROOT, transfer_dir)
        for f in filenames:
            transfer_path = os.path.join(transfer_dir, f)
            backup_path = os.path.join(backup_dir, f)

            if os.path.exists(backup_path):
                print(".", end="", flush=True)
                continue
            else:
                print("c", end="", flush=True)
                os.makedirs(backup_dir, exist_ok=True)
                shutil.copyfile(transfer_path, backup_path)

    print("")

    subprocess.check_call([
        "python",
        "/Users/alexwlchan/repos/junkdrawer/backups/twitter/create_dm_threads.py",
        "/Users/alexwlchan/Documents/backups/twitter/direct_messages"
    ])
