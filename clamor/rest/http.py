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
from .rate_limit import Bucket, RateLimiter
from .routes import APIRoute

__all__ = (
    'HTTP',
)

logger = logging.getLogger(__name__)


class HTTP:
    """"""

    BASE_URL = 'https://discordapp.com/api/v7'
    MAX_RETRIES = 5

    LOG_SUCCESSS = 'Success, {bucket} has received {text}!'
    LOG_FAILURE = 'Request to {bucket} failed with {code}: {error}'

    def __init__(self, token: str, **kwargs):
        self._token = token
        self._session = kwargs.get('session', asks.Session())
        self.rate_limiter = RateLimiter()

        self._responses = []
        self.headers = {
            'User-Agent': self.user_agent,
            'Authorization': 'Bot ' + self._token,
        }

    @property
    def token(self) -> str:
        """"""

        return self._token

    @property
    def user_agent(self) -> str:
        """"""

        fmt = 'DiscordBot ({0}, v{1}) / Python {2[0]}.{2[1]}.{2[2]}'
        return fmt.format(clamor_url, clamor_version, sys.version_info)

    @property
    def responses(self):
        """"""

        return self._responses

    @staticmethod
    def _parse_response(response: Response):
        if response.headers['Content-Type'] == 'application/json':
            return response.json(encoding='utf-8')
        return response.text.encode('utf-8')

    async def make_request(self,
                           route: APIRoute,
                           fmt: dict = None,
                           **kwargs) -> Optional[Union[dict, list, str]]:
        """"""

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
        if 'reason' in kwargs:
            kwargs['headers']['X-Audit-Log-Reason'] = quote(kwargs['reason'] or '', '/ ')

        method = route[0].value
        url = self.BASE_URL + route[1].format(**fmt)
        bucket = (method, route[1].format(**bucket_fmt))
        logger.debug('Performing request to bucket %s', bucket)

        async with self.rate_limiter(bucket):
            response = await self._session.request(method, url, **kwargs)
            response.route = route

            await self.rate_limiter.update_bucket(bucket, response)
            self._responses.append(response)

        return await self.parse_response(response,
                                         fmt,
                                         bucket=bucket,
                                         retries=retries,
                                         **kwargs)

    async def parse_response(self,
                             response: Response,
                             fmt: dict,
                             *,
                             bucket: Bucket,
                             retries: int = 0,
                             **kwargs) -> Optional[Union[dict, list, str]]:
        """"""

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
            # Something weird happened here...Let's try it again.
            logger.debug(
                self.LOG_FAILURE.format(bucket=bucket, code=status, error=response.content))

            retries += 1
            if retries > self.MAX_RETRIES:
                raise RequestFailed(response, data)

            retry_after = randint(1000, 50000) / 1000.0
            await anyio.sleep(retry_after)

            return await self.make_request(
                response.route, fmt, retries=retries, **kwargs)

    async def close(self):
        """"""

        await self._session.close()
