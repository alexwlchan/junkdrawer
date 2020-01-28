#!/usr/bin/env python
"""
Whenever Homebrew upgrades Python, a lot of my virtualenvs created by virtualfish
stop working, spitting out an error like:

    dyld: Library not loaded: @executable_path/../.Python
      Referenced from: /Users/alexwlchan/.virtualenvs/venv_name/bin/python3
      Reason: image not found
    fish: 'python3' terminated by signal SIGABRT (Abort)

This is pretty annoying, and I have to debug it a lot, so this script goes and
checks every virtualfish-created virtualenv, and removes the broken ones.

"""

import os
import shutil
import subprocess

try:
    import termcolor
except ImportError:
    def print_green(s):
        print(s)

    def print_red(s):
        print(s)
else:
    def print_green(s):
        print(termcolor.colored(s, "green"))

    def print_red(s):
        print(termcolor.colored(s, "red"))


if __name__ == "__main__":
    VENVS_DIR = os.path.join(os.environ["HOME"], ".virtualenvs")

    for venv_name in os.listdir(VENVS_DIR):
        # e.g. .DS_Store
        if not os.path.isdir(os.path.join(VENVS_DIR, venv_name)):
            continue

        python_path = os.path.join(VENVS_DIR, venv_name, "bin/python")

        print(f"Checking {venv_name}... ".ljust(35, " "), end="")

        result = subprocess.call(
            [python_path, "-c", "print('hello world')"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result == 0:
            print_green("ok")
        else:
            print_red("broken")
            shutil.rmtree(os.path.join(VENVS_DIR, venv_name))
