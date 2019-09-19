#!/usr/bin/env python
# -*- encoding: utf-8

import collections
import datetime
import itertools
import json
import os
import sys

import PyPDF2
import tqdm


try:
    CACHE = json.load(open("_pdf_cache.json"))
except FileNotFoundError:
    CACHE = {}


def draw_bar_chart(data):
    # https://alexwlchan.net/2018/05/ascii-bar-charts/
    max_value = max(count for _, count in data)
    increment = max_value / 25

    longest_label_length = max(len(label) for label, _ in data)

    for label, count in data:

        # The ASCII block elements come in chunks of 8, so we work out how
        # many fractions of 8 we need.
        # https://en.wikipedia.org/wiki/Block_Elements
        bar_chunks, remainder = divmod(int(count * 8 / increment), 8)

        # First draw the full width chunks
        bar = '█' * bar_chunks

        # Then add the fractional part.  The Unicode code points for
        # block elements are (8/8), (7/8), (6/8), ... , so we need to
        # work backwards.
        if remainder > 0:
            bar += chr(ord('█') + (8 - remainder))

        # If the bar is empty, add a left one-eighth block
        bar = bar or  '▏'

        print(f'{label.rjust(longest_label_length)} ▏ {count:#5d} {bar}')


def get_pdfs(search_root):
    for root, _, filenames in os.walk(search_root):
        for f in filenames:
            if not f.lower().endswith(".pdf"):
                continue
            yield os.path.join(search_root, root, f)


if __name__ == "__main__":
    search_roots = [os.path.realpath(p) for p in sys.argv[1:]]

    if not search_roots:
        sys.exit(f"Usage: {__file__} <ROOT> ...")

    counts = collections.defaultdict(int)

    pdf_paths = list(itertools.chain(
        *(get_pdfs(root) for root in search_roots)
    ))

    for pdf_path in tqdm.tqdm(pdf_paths):
        if pdf_path not in CACHE:
            date = datetime.datetime.fromtimestamp(os.stat(pdf_path).st_mtime)
            with open(pdf_path, "rb") as pdf:
                reader = PyPDF2.PdfFileReader(pdf)
                page_count = reader.getNumPages()

            CACHE[pdf_path] = {
                "date": date.strftime("%Y-%m-%d"),
                "page_count": page_count
            }

        data = CACHE[pdf_path]
        counts[data["date"]] += data["page_count"]

    print("")

    draw_bar_chart(sorted(counts.items()))
    print("─" * 40)
    print(f"TOTAL      ▏ {sum(counts.values()):#5d}")

    with open("_pdf_cache.json", "w") as f:
        f.write(json.dumps(CACHE))
