# -*- coding: utf-8 -*-

import platform
from typing import List

from ..meta import __title__ as name

__all__ = (
    'identify',
    'resume',
)


def identify(token: str, compress: bool = True, large_threshold: int = 50,
             *, shard: List[int] = None, presence: dict = None) -> dict:
    """Returns an identify payload to complete the client handshake."""

    presence = presence or {'since': None, 'game': None, 'status': 'online', 'afk': False}
    shard = shard or [0, 1]

    return {
        'token': token,
        'properties': {
            '$os': platform.system(),
            '$browser': name,
            '$device': name
        },
        'compress': compress,
        'large_threshold': large_threshold,
        'shard': shard,
        'presence': presence
    }


def resume(token: str, session_id: str, seq: int) -> dict:
    """Returns a resume payload to continue a closed connection."""

    return {
        'token': token,
        'session_id': session_id,
        'seq': seq
    }
