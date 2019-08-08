# -*- coding: utf-8 -*-

from .json import JSONEncoder

ENCODERS = {
    'json': JSONEncoder,
}

try:
    from .etf import ETFEncoder
except ImportError:
    pass
else:
    ENCODERS['etf'] = ETFEncoder
