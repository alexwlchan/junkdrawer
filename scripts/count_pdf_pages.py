#!/usr/bin/env python
# -*- encoding: utf-8

import os
import sys

import PyPDF2
import tqdm


def get_pdfs(search_root):
    for root, _, filenames in os.walk(search_root):
        for f in filenames:
            if not f.lower().endswith(".pdf"):
                continue
            yield os.path.join(search_root, root, f)


if __name__ == "__main__":
    try:
        search_root = os.path.realpath(sys.argv[1])
    except IndexError:
        sys.exit(f"Usage: {__file__} <ROOT>")

    page_count = 0

    pdf_paths = list(get_pdfs(search_root))

    for pdf_path in tqdm.tqdm(pdf_paths):
        with open(pdf_path, "rb") as pdf:
            reader = PyPDF2.PdfFileReader(pdf)
            page_count += reader.getNumPages()

    print(f"{page_count} pages across {len(pdf_paths)} files")
