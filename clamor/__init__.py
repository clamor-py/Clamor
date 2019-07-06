# -*- coding: utf-8 -*-

"""
Clamor
~~~~~~

The Python Discord API Framework.

:copyright: (c) 2019 Valentin B.
:license: MIT, see LICENSE for more details.
"""

from . import meta
from .meta import *

import logging

fmt = '[%(levelname)s] %(asctime)s - %(name)s:%(lineno)d - %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO)
logging.getLogger(__name__).addHandler(logging.NullHandler())
