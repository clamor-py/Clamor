# -*- coding: utf-8 -*-

"""
Clamor
~~~~~~

The Python Discord API Framework.

:copyright: (c) 2019 Valentin B.
:license: MIT, see LICENSE for more details.
"""

__title__ = 'Clamor'
__author__ = 'Valentin B.'
__version__ = '0.0.1a'
__license__ = 'MIT'
__copyright__ = '(c) 2019 Valentin B.'
__url__ = 'https://github.com/clamor-py/Clamor'

from . import meta
from .meta import *

import logging

fmt = '[%(levelname)s] %(asctime)s - %(name)s:%(lineno)d - %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO)
logging.getLogger(__name__).addHandler(logging.NullHandler())
