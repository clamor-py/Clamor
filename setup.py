#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
from pathlib import Path
from setuptools import find_packages, setup

ROOT = Path(__file__).parent

if sys.version_info < (3, 5):
    raise SystemExit('Clamor requires Python 3.5+, consider upgrading.')

with open(str(ROOT / 'clamor' / 'meta.py'), encoding='utf-8') as f:
    VERSION = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open(str(ROOT / 'README.rst'), encoding='utf-8') as f:
    README = f.read()

with open(str(ROOT / 'requirements.txt'), encoding='utf-8') as f:
    REQUIREMENTS = f.read().splitlines()

EXTRAS_REQUIRE = {}


setup(
    name='clamor',
    author='Valentin B.',
    author_email='valentin.be@protonmail.com',
    url='https://github.com/clamor-py/Clamor',
    license='MIT',
    description='The Python Discord API Framework',
    long_description=README,
    long_description_content_type='text/x-rst',
    project_urls={
        'Documentation': 'https://clamor.readthedocs.io/en/latest',
        'Source': 'https://github.com/clamor-py/Clamor',
        'Issue tracker': 'https://github.com/clamor-py/Clamor/issues'
    },
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    extras_require=EXTRAS_REQUIRE,
    python_requires='>=3.5.0',
    keywords='discord discord-api rest-api api wrapper websocket api-client library framework',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    test_suite='tests.suite',
)
