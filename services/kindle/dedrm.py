#!/usr/bin/env python
# -*- encoding: utf-8

import contextlib
import os
import pathlib
import subprocess
import sys


@contextlib.contextmanager
def tmp_home_dir():
    outdir = pathlib.Path.home() / ".ebooks"
    outdir.mkdir()

    try:
        yield outdir
    finally:
        for f in os.listdir(outdir):
            (outdir / f).unlink()

        outdir.rmdir()


def check_call(cmd):
    if "--verbose" in sys.argv:
        subprocess.check_call(cmd)
    else:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    try:
        azw_path = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <PATH_TO_AZW>")

    root = pathlib.Path(__file__).parent.resolve()

    with tmp_home_dir() as outdir:
        print("*** Stripping DRM from file")
        check_call(
            [
                "python2.7",
                str(root / "kindle_dedrm" / "kindle_dedrm.py"),
                "--kindle=B00E 1510 1483 0G04",
                f"--outdir={outdir}",
                azw_path
            ]
        )
        print("*** Successfully stripped DRM from file")

        out_files = os.listdir(outdir)
        assert len(out_files) == 1, out_files
        mobi_filename = pathlib.Path(out_files[0])
        epub_filename = mobi_filename.with_suffix(".epub")

        print("*** Converting .azw file to .epub")
        check_call([
            "docker", "run",
            "--volume", f"{outdir}:/ebooks",
            "--entrypoint", "ebook-convert",
            "regueiro/calibre-server",
            f"/ebooks/{mobi_filename}", f"/ebooks/{epub_filename}"
        ])
        print("*** Successfully converted to .epub")

        check_call(["open", outdir])

        title = input("What is the name of the book? ")
        tags = input("How do you want to tag the book? ")
        source_url = input("What is the source of the book? (optional) ")

        # TODO: Upload to docstore
