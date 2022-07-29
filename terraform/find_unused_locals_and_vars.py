#!/usr/bin/env python
# -*- encoding: utf-8

import os
import sys

import hcl


rc = 0

for root, _, filenames in os.walk("."):
    if not any(f.endswith(".tf") for f in filenames):
        continue

    if ".terraform" in root:
        continue

    defined_locals = set()
    defined_variables = set()

    for f in filenames:
        if not f.endswith(".tf"):
            continue

        # print(f)
        try:
            tf_data = hcl.load(open(os.path.join(root, f)))
        except (ValueError, TypeError):
            print("!!!", os.path.join(root, f))
            continue
        for k in ("module", "resource", "terraform", "provider", "data"):
            try:
                del tf_data[k]
            except KeyError:
                pass

        defined_locals ^= set(tf_data.get("locals", {}).keys())
        defined_variables ^= set(tf_data.get("variable", {}).keys())

    unseen_locals = defined_locals.copy()
    unseen_variables = defined_variables.copy()

    for f in filenames:

        # We've seen everything, so we can skip to the next directory
        if not unseen_locals and not unseen_variables:
            break

        if not f.endswith(".tf"):
            continue

        contents = open(os.path.join(root, f)).read()

        print(os.path.join(root, f))
        for varname in list(unseen_variables):
            if "var." + varname in contents:
                unseen_variables.remove(varname)

        for locname in list(unseen_locals):
            if "local." + locname in contents:
                unseen_locals.remove(locname)

    if unseen_locals or unseen_variables:
        print(f"*** {root}")

        if unseen_locals:
            print("*** Unused locals:")
            for locname in unseen_locals:
                print(f"    - {locname}")

        if unseen_variables:
            print("*** Unused variables:")
            for locname in unseen_variables:
                print(f"    - {locname}")

        print("\n")
        rc = 1

sys.exit(rc)
