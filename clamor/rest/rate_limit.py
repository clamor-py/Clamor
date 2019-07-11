# -*- coding: utf-8 -*-

import logging
from typing import NewType, Tuple, Union

__all__ = (
    'Bucket',
)

logger = logging.getLogger(__name__)

#: A type to denote rate limit buckets.
Bucket = NewType('Bucket', Union[Tuple[str, str], str])

# TODO: Rate limiting
