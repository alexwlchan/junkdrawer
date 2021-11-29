#!/usr/bin/env python3
# -*- encoding: utf-8

import os
import subprocess
import sys

filename = sys.argv[1]
border = sys.argv[2]

new_name = os.path.splitext(filename)[0] + "_reborder" + os.path.splitext(filename)[1]

subprocess.check_call([
    "convert",
    "-background", "none",
    "-trim", filename, "-bordercolor", "white", "-border", f"{border}x{border}",
    new_name
])
