# -*- coding: utf-8 -*-

import abc


class BaseEncoder(abc.ABC):
    """An Abstract Base Class for implementing encoders to communicate with the Discord Gateway."""

    TYPE = None
    OPCODE = None

    @staticmethod
    @abc.abstractmethod
    def decode(data):
        pass

    @staticmethod
    @abc.abstractmethod
    def encode(data):
        pass
