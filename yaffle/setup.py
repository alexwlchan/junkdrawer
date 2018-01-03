#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import os

from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import find_packages, setup


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


SOURCE = local_file('src')
README = local_file('README.rst')
long_description = codecs.open(README, encoding='utf-8').read()

install_reqs = parse_requirements(
    local_file('requirements.txt'), session=PipSession()
)


setup(
    name='yaffle',
    version='1.0.0',
    description='A tool for managing a library of PDF documents',
    long_description=long_description,
    url='https://github.com/alexwlchan/homeconfig',
    author='Alex Chan',
    author_email='alex@alexwlchan.net',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(SOURCE),
    package_dir={'': SOURCE},
    install_requires=[str(ir.req) for ir in install_reqs],
    entry_points={
        'console_scripts': [
            'yaffle-index=yaffle:index_document',
            'yaffle-reindex=yaffle:reindex_all',
        ],
    },
)
