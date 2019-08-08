# -*- coding: utf-8 -*-

import logging
import sys
from random import randint
from typing import Optional, Union
from urllib.parse import quote

import anyio
import asks
from asks.response_objects import Response

from ..exceptions import RequestFailed, Unauthorized, Forbidden, NotFound
from ..meta import __url__ as clamor_url, __version__ as clamor_version
from .rate_limit import Bucket, RateLimiter, InMemoryBucketStore
from .routes import APIRoute

__all__ = (
    'HTTP',
)

logger = logging.getLogger(__name__)


class _ReattemptRequest(Exception):
    def __init__(self, status_code: int, data: Optional[Union[dict, list, str]], *args):
        self.status_code = status_code
        self.data = data

        super().__init__(*args)


class HTTP:
    r"""An interface to perform requests to the Discord API.

    Parameters
    ----------
    token : str
        The token to use for API authorization.
    \**kwargs : dict
        See below.

    Keyword Arguments
    -----------------
    session : :class:`asks.Session<asks:asks.Session>`, optional
        The session to use. If none provided, a new one is created.
    app : str
        The application type for the ``Authorization`` header.
        Either ``Bot`` or ``Bearer``, defaults to ``Bot``.
    bucket_store: :class:`~clamor.rest.rate_limit.BucketStore`
        The bucket store which will be used by the RateLimiter.
        If no bucket store is provided, the RateLimiter will store the buckets in memory.

    Attributes
    ----------
    rate_limiter : :class:`~clamor.rest.rate_limit.RateLimiter`
        The rate limiter to use for requests.
    headers : dict
        The default headers included in every request.
    """

    #: The API version to use.
    API_VERSION = 7
    #: The Discord API URL.
    BASE_URL = 'https://discordapp.com/api/v{}'.format(API_VERSION)
    #: The total amount of allowed retries for failed requests.
    MAX_RETRIES = 5

    #: The log message format for successful requests.
    LOG_SUCCESSS = 'Success, {bucket} has received {text}!'
    #: The log message format for failed requests.
    LOG_FAILURE = 'Request to {bucket} failed with {code}: {error}'

    def __init__(self, token: str, **kwargs):
        self._token = token
        self._session = kwargs.get('session', asks.Session())
        self.rate_limiter = RateLimiter(kwargs.get('bucket_store'))

        self._responses = []
        self.headers = {
            'User-Agent': self.user_agent,
            'Authorization': kwargs.get('app', 'Bot') + ' ' + self._token,
        }

    @property
    def token(self) -> str:
        """The token used for API authorization."""

        return self._token

    @property
    def user_agent(self) -> str:
        """The ``User-Agent`` header sent in every request."""

        fmt = 'DiscordBot ({0}, v{1}) / Python {2[0]}.{2[1]}.{2[2]}'
        return fmt.format(clamor_url, clamor_version, sys.version_info)

    @property
    def responses(self):
        """All API responses this instance has received."""

        return self._responses

    @staticmethod
    def _parse_response(response: Response) -> Optional[Union[dict, list, str, bytes]]:
        if response.headers['Content-Type'] == 'application/json':
            return response.json(encoding='utf-8')
        if response.headers['Content-Type'].startswith("image"):
            return response.content
        return response.text.encode('utf-8')

    async def make_request(self,
                           route: APIRoute,
                           fmt: dict = None,
                           **kwargs) -> Optional[Union[dict, list, str, bytes]]:
        r"""Makes a request to a given route with a set of arguments.

        It also handles rate limits, non-success status codes and
        safely parses the response with :meth:`HTTP.parse_response`.

        Parameters
        ----------
        route : Tuple[:class:`~clamor.rest.routes.Method`, str]
            A tuple containing HTTP method and the route to make the request to.
        fmt : dict
            A dictionary holding endpoint parameters to dynamically format a route.
        \**kwargs : dict
            See below.

        Keyword Arguments
        -----------------
        headers : dict, optional
            Optional HTTP headers to include in the request.
        retries : int, optional
            The amount of retries that have yet been attempted.
        reason : str, optional
            Additional reason string for the ``X-Audit-Log-Reason``
            header.

        Returns
        -------
        Union[dict, list, str], optional
            The parsed response.

        Raises
        ------
        :exc:`clamor.exceptions.Unauthorized`
            Raised for status code ``401`` and means your token is invalid.
        :exc:`clamor.exceptions.Forbidden`
            Raised for status code ``403`` and means that your token
            doesn't have permissions for a certain action.
        :exc:`clamor.exceptions.NotFound`
            Raised for status code ``404`` and means that the passed API
            route doesn't exist.
        :exc:`clamor.exceptions.RequestFailed`
            Generic exception raised when either retries are exceeded
            or a non-success status code not listed above occurred.
        """

        fmt = fmt or {}
        retries = kwargs.pop('retries', 0)
        # The API shares rate limits with minor routes of guild, channel
        # and webhook endpoints. To make our lives easier through preparing
        # the buckets so that they share the same rate limit buckets by
        # default. Therefore no need to deal with X-RateLimit-Bucket.
        bucket_fmt = {
            key: value
            if key in ('guild', 'channel', 'webhook') else ''
            for key, value in fmt.items()
        }

        # Prepare the headers.
        if 'headers' in kwargs:
            kwargs['headers'].update(self.headers)
        else:
            kwargs['headers'] = self.headers

        # The additional header for audit logs.
        if 'reason' in kwargs and kwargs['reason'] is not None:
            kwargs['headers']['X-Audit-Log-Reason'] = quote(kwargs['reason'], '/ ')

        method = route[0].value
        url = self.BASE_URL + route[1].format(**fmt)
        bucket = (method, route[1].format(**bucket_fmt))
        logger.debug('Performing request to bucket %s', bucket)

        async with self.rate_limiter(bucket):
            response = await self._session.request(method, url, **kwargs)

            await self.rate_limiter.update_bucket(bucket, response)
            self._responses.append(response)

        try:
            result = await self.parse_response(bucket, response)
        except _ReattemptRequest as error:
            logger.debug(self.LOG_FAILURE.format(
                bucket=bucket, code=error.status_code, error=response.content))

            retries += 1
            if retries > self.MAX_RETRIES:
                raise RequestFailed(response, error.data)

            retry_after = randint(1000, 50000) / 1000.0
            await anyio.sleep(retry_after)

            return await self.make_request(route, fmt, **kwargs)
        else:
            return result

    async def parse_response(self,
                             bucket: Bucket,
                             response: Response) -> Optional[Union[dict, list, str, bytes]]:
        """Parses a given response and handles non-success status codes.

        Parameters
        ----------
        bucket : Union[Tuple[str, str], str]
            The request bucket.
        response : :class:`Response<asks:asks.response_objects.Response>`
            The response to parse.

        Returns
        -------
        Union[dict, list, str], optional
            The extracted response content.

        Raises
        ------
        :exc:`clamor.exceptions.Unauthorized`
            Raised for status code ``401`` and means your token is invalid.
        :exc:`clamor.exceptions.Forbidden`
            Raised for status code ``403`` and means that your token
            doesn't have permissions for a certain action.
        :exc:`clamor.exceptions.NotFound`
            Raised for status code ``404`` and means that the passed API
            route doesn't exist.
        :exc:`clamor.exceptions.RequestFailed`
            Generic exception raised when either retries are exceeded
            or a non-success status code not listed above occurred.
        """

        data = self._parse_response(response)
        status = response.status_code

        if 200 <= status < 300:
            # These status codes indicate successful requests.
            # Therefore we can return the JSON response body.
            logger.debug(self.LOG_SUCCESSS.format(bucket=bucket, text=data))
            return data

        elif status != 429 and 400 <= status < 500:
            # These status codes are user errors and won't disappear
            # with another request. In this case, we'll throw an
            # exception.
            if status == 401:
                raise Unauthorized(response, data)

            elif status == 403:
                raise Forbidden(response, data)

            elif status == 404:
                raise NotFound(response, data)

            else:
                raise RequestFailed(response, data)

        else:
            # Something weird happened here...Let's reattempt the request.
            raise _ReattemptRequest(status, data)

    async def close(self):
        """Closes the underlying :class:`Session<asks:asks.Session>`."""

        await self._session.close()
