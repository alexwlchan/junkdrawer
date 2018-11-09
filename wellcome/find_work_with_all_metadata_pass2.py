#!/usr/bin/env python
# -*- encoding: utf-8

i = 0
for line in open("works2.txt"):
    work = eval(line.strip())

    keys = set(work.keys())

    if "lettering" not in keys:
        continue

    if "language" not in keys:
        continue

    if keys != {'id', 'subjects', 'lettering', 'genres', 'physicalDescription', 'production', 'identifiers', 'title', 'contributors', 'workType', 'extent', 'dimensions', 'items', 'language', 'type', 'description'}:
        print({'id', 'subjects', 'lettering', 'genres', 'physicalDescription', 'production', 'identifiers', 'title', 'contributors', 'workType', 'extent', 'dimensions', 'items', 'language', 'type', 'description'})
        print(keys)
        print("")

    print(work["id"])

    i += 1
    if i >= 10:
        break

#    # print(keys)