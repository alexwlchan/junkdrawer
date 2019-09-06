#!/usr/bin/env python
# -*- encoding: utf-8

import datetime as dt
import errno
import filecmp
import os
import shutil
import subprocess
import webbrowser

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


REPOS_DIR = os.path.join(os.environ["HOME"], "repos")


def gprint(s):
    """Print a message in green!"""
    print("\033[92m*** %s\033[0m" % s)


def mkdir_p(path):
    """Create a directory if it doesn't already exist."""
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def git_clone_or_update(repo_url, local_name):
    gprint("Updating repo %s" % local_name)
    repo_path = os.path.join(REPOS_DIR, local_name)

    if os.path.isdir(repo_path):
        subprocess.check_call(["git", "checkout", "master"], cwd=repo_path)
        subprocess.check_call(["git", "pull", "origin", "master"], cwd=repo_path)
    else:
        subprocess.check_call(["git", "clone", repo_url, repo_path])


if __name__ == "__main__":
    mkdir_p(REPOS_DIR)

    git_clone_or_update(
        "git@github.com:fihristorg/fihrist-mss.git",
        local_name="fihrist-mss"
    )

    git_clone_or_update(
        "git@github.com:wellcometrust/wellcome-collection-tei.git",
        local_name="wellcome-collection-tei"
    )
        #
    # fihrist_mss = os.path.join(REPOS_DIR, "fihrist-mss")
    # wellcome_tei = os.path.join(REPOS_DIR, "wellcome-collection-tei")
    #
    # fihrist_dir = os.path.join(fihrist_mss, "collections", "wellcome trust")
    # wellcome_dir = os.path.join(wellcome_tei, "Arabic")
    #
    # for name in os.listdir(fihrist_dir):
    #     fihrist_path = os.path.join(fihrist_dir, name)
    #     wellcome_path = os.path.join(wellcome_dir, name)
    #
    #     if (
    #         not os.path.exists(wellcome_path) or
    #         not filecmp.cmp(fihrist_path, wellcome_path)
    #     ):
    #         print("*** Updating %s" % name)
    #         shutil.copyfile(fihrist_path, wellcome_path)
    #         subprocess.check_call(["git", "add", wellcome_path], cwd=wellcome_tei)
    #
    # has_changes = subprocess.call(
    #     ["git", "diff", "--cached", "--exit-code", "--quiet"],
    #     cwd=wellcome_tei)
    #
    # if has_changes:
    #     branch = "arabic_ms_updates-%s" % dt.datetime.now().date()
    #     subprocess.check_call(["git", "checkout", "-b", branch], cwd=wellcome_tei)
    #     subprocess.check_call([
    #         "git", "commit", "-m", "Update Arabic manuscripts from fihrist-mss"],
    #         cwd=wellcome_tei
    #     )
    #     subprocess.check_call(["git", "push", "origin", branch], cwd=wellcome_tei)
    #
    #     webbrowser.open(
    #         "https://github.com/wellcometrust/wellcome-collection-tei/pull/new/%s" %
    #         branch
    #     )
