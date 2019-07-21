# -*- coding: utf-8 -*-

try:
    import ujson as json
except ImportError:
    import json

from wsproto.frame_protocol import Opcode

from .base import BaseEncoder


class JSONEncoder(BaseEncoder):
    """An encoder that will be used to handle received Gateway payloads.

    This will be used when communication should be done in JSON format.
    """

    TYPE = 'json'
    OPCODE = Opcode.TEXT

    @staticmethod
    def decode(data):
        return json.loads(data)

    @staticmethod
    def encode(data):
        return json.dumps(data)
