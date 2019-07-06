# -*- coding: utf-8 -*-

from collections import namedtuple

__all__ = (
    '__author__',
    '__copyright__',
    '__license__',
    '__title__',
    '__url__',
    '__version__',
    'version_info'
)

__author__ = 'Valentin B.'
__copyright__ = 'Copyright 2019 Valentin B.'
__license__ = 'MIT'
__title__ = 'Clamor',
__url__ = 'https://github.com/clamor-py/Clamor'
__version__ = '0.1.0'

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(0, 1, 0, 'beta', 0)
