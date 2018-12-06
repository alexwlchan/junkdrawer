#!/usr/bin/env python3
# -*- encoding: utf-8

import os
import subprocess
import sys

filename = sys.argv[1]
border = sys.argv[2]

new_name = os.path.splitext(filename)[0] + "_reborder" + os.path.splitext(filename)[1]

subprocess.check_call([
    "docker", "run", "--rm", "--tty",
    "--volume", f"{os.path.abspath(os.curdir)}:/data", "--workdir", "/data",
    "alexwlchan/imagemagick", "convert",
    "-trim", filename, "-bordercolor", "white", "-border", f"{border}x{border}",
    new_name
])
