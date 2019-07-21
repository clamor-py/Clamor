# -*- coding: utf-8 -*-

import logging
from typing import Optional, Union

from ..exceptions import ClamorError

__all__= (
    'GatewayError',
    'EncodingError',
    'InvalidListener',
)

logger = logging.getLogger(__name__)


class GatewayError(ClamorError):
    """Base class for every error raised by the gateway

    Catching this error is not recommended as it mostly
    indicates a critical client or server failure.
    """
    pass


class EncodingError(GatewayError):
    """Raised when the encoding or decoding of a message fails

    Parameters
    ----------
    error : Optional[str]
        Error message returned by the encoder
    data : Optional[Union[dict, str]]
        Raw data of the message

    Attributes
    ----------
    error : Optional[Union[dict, str]]

    """

    def __init__(self, err: Optional[str], data: Optional[Union[dict, str]] = None):
        if data:
            error = "Encoding of message {} failed".format(str(data))
        else:
            error = "Decoding of gateway message failed"
        if error:
            error += " with exception {}".format(err)
        super().__init__(error)


class InvalidListener(GatewayError):
    """Raised by the emitter when a listener is not a coroutine

    """
