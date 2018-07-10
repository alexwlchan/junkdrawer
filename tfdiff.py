#!/usr/bin/env python
# -*- encoding: utf-8
"""
The output from 'terraform plan' sometimes includes a change in container
definitions, of the form:

    container_definitions: "<old definition>" => "<new definition>"

These definitions are large JSON blobs, which makes it hard to see what's
actually changed.

This script unpacks the change and pretty-prints a diff.

Pass the string '"<old definition>" => "<new definition>"' as a single
command-line argument.

"""

import difflib
import json
import shlex
import sys


parts = shlex.split(sys.argv[1])
old_definition, _, new_definition = parts

old_json = json.loads(old_definition)
new_json = json.loads(new_definition)

old_lines = json.dumps(old_json, indent=2, sort_keys=True).splitlines()
new_lines = json.dumps(new_json, indent=2, sort_keys=True).splitlines()

for line in difflib.context_diff(old_lines, new_lines):
    print(line)
