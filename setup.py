#!/usr/bin/env python
"""Command line interface for translation workflow"""

import os
from setuptools import setup, find_packages
from twcli import APP_VERSION


with open(
        os.path.join(os.path.dirname(__file__), "requirements.txt"), 'rb'
) as require:
    REQUIRE = require.read().decode('utf-8').splitlines() + ['setuptools']


setup(
    name='workflow-cli',
    version=APP_VERSION,
    description="Command line interface for translation workflow",
    platforms=["Linux"],
    packages=find_packages(),
    author="Sundeep Anand",
    author_email="suanand@fedoraproject.org",
    maintainer="pnemade@fedoraproject.org",
    url="https://transtats.org",
    license="Apache License 2.0",
    install_requires=REQUIRE,
    scripts=["transtats"],
    entry_points='''
        [console_scripts]
        transtats=twcli:entry_point
    ''',
    classifiers=[
        'License :: OSI Approved :: Apache License 2.0 (Apache-2.0)',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.11',
    ],
)
