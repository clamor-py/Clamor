# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import NewType, Union

from ..http import HTTP

__all__ = (
    'Snowflake',
    'optional',
    'EndpointsWrapper',
)

#: A type for denoting raw snowflake parameters.
Snowflake = NewType('Snowflake', Union[int, str])


def optional(**kwargs) -> dict:
    """Given a dictionary, this filters out all values that are ``None``.

    Useful for routes where certain parameters are optional.
    """

    return {
        key: value for key, value in kwargs.items()
        if value is not None
    }


class EndpointsWrapper:
    """Base class for higher-level wrappers for API endpoints."""

    __slots__ = ('http',)

    def __init__(self, token: str):
        self.http = HTTP(token)

    @property
    def token(self) -> str:
        """The token that is used for API authorization."""

        return self.http.token

    @contextmanager
    def raw_responses(self):
        """A contextmanager that yields all raw responses this instance holds.

        .. warning::

            Do not use this if you don't know what you're doing.
        """

        try:
            yield self.http.responses
        finally:
            self.http.responses.clear()
