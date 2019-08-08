# -*- coding: utf-8 -*-

"""
Clamor
~~~~~~

The Python Discord API Framework.

:copyright: (c) 2019 Valentin B.
:license: MIT, see LICENSE for more details.
"""

from .gateway import *
from .meta import *
from .models import *
from .rest import *
from . import utils  # Preserve the namespace

import logging

fmt = '[%(levelname)s] %(asctime)s - %(name)s:%(lineno)d - %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO)
logging.getLogger(__name__).addHandler(logging.NullHandler())
