# -*- coding: utf-8 -*-

import earl

from wsproto.frame_protocol import Opcode

from .base import BaseEncoder


class ETFEncoder(BaseEncoder):
    """An encoder that will be used to handle received Gateway payloads.

    This will be used when communication should be done in Erlang's ETF format.
    """

    TYPE = 'etf'
    OPCODE = Opcode.BINARY

    @staticmethod
    def decode(data):
        return earl.unpack(data, encoding='utf-8', encode_binary_ext=True)

    @staticmethod
    def encode(data):
        return earl.pack(data)
