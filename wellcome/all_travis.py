#!/usr/bin/env python
# -*- encoding: utf-8

import subprocess
import sys

import yaml


travis_yml = yaml.load(open('.travis.yml'))

from pprint import pprint

for j in travis_yml['jobs']['include']:
    env = j['env']
    if isinstance(env, list):
        continue
    task = env.replace('TASK=', '')

    if task == 'travis-format':
        continue

    print(    f'=== STARTING: {task} ===')
    try:
        subprocess.check_call(['make', task])
    except subprocess.CalledProcessError:
        print(f'=== FAILED:   {task} ===')
        sys.exit(1)
    else:
        print(f'=== PASSED:   {task} ===')
