#!/usr/bin/env python
# -*- encoding: utf-8

import contextlib
import os
import tempfile
from urllib.request import urlretrieve
import zipfile


# https://aws.amazon.com/architecture/icons/
ZIP_URL = (
    'https://s3-us-west-2.amazonaws.com/awswebanddesign/Architecture+Icons/'
    'AWS-Arch-Icon-Sets_Feb-18/PNG%2C+SVG%2C+EPS_18.02.22.zip'
)


@contextlib.contextmanager
def working_directory(path):
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


tmpdir = tempfile.mkdtemp()

with working_directory(tempfile.mkdtemp()):
    urlretrieve(ZIP_URL, 'icons.zip')
    PATH = os.path.join(os.getcwd(), 'icons.zip')


with zipfile.ZipFile(PATH) as zf:
    for zip_info in zf.infolist():
        filename = zip_info.filename
        if filename.startswith(('.', '__MACOSX')):
            continue

        if not filename.endswith('_LARGE.png'):
            continue

        if ('GRAYSCALE_' in filename) or ('GRAYSCALE-' in filename):
            continue

        out_name = os.path.basename(filename.replace('_LARGE', ''))
        out_dirname, out_filename = out_name.split('_', 1)

        if out_filename.startswith('Amazon'):
            out_filename = out_filename[len('Amazon'):]
        if out_filename.startswith('AWS'):
            out_filename = out_filename[len('AWS'):]

        out_dir = os.path.join('aws_icons', out_dirname)
        os.makedirs(out_dir, exist_ok=True)

        path = zf.extract(zip_info, path=tmpdir)
        os.rename(path, os.path.join(out_dir, out_filename))
