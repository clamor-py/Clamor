# -*- coding: utf-8 -*-

import clamor
# RequestFailed executes an error on importing it. Please look after it..
# from clamor.exceptions import RequestFailed

import logging
import sys
from random import randint
from urllib.parse import quote

import anyio
import asks


logger = logging.getLogger(__name__)


class HTTP:
    """Represents the HTTP client that uses the asks library to perform requests to the Discord API."""

    BASE_URL = 'https://discordapp.com/api/v7'
    MAX_RETRIES = 5

    LOG_SUCCESS = 'Successful! {bucket} ({url}) has received {text}!'
    LOG_FAILED = 'Request to {bucket} failed with status code {code}: {error}. Retrying after {seconds} seconds.'

    def __init__(self, token, **kwargs):
        self._token = token
        self._session = kwargs.get('session', asks.Session())

        self.headers = {
            'User-Agent': self.create_user_agent(),
            'Authorization': kwargs.get('application_type', 'Bot').strip() + ' ' + self._token
        }

    async def make_request(self, route, fmt=None, **kwargs) -> dict:
        """Makes a request to a given endpoint with a set of arguments.

           This makes an request for you and retries non-success status
           codes up to 5 times.

           Parameters
           ----------
           route : tuple
                A tuple containing the HTTP Method to use as well as the route to make the request to.
           fmt: dict
                The necessary keys and values to dynamically format the route.
           headers : dict, optional
                The headers to use for the request.
           retires : int, optional
                The amount of retires that have been made yet.

           Returns
           --------
           dict
                The API's JSON response.

           Raises
           --------
           RequestFailed
                Will be raised on request failure or when the total amount of retries was exceeded.
        """

        fmt = fmt or {}
        retries = kwargs.pop('retires', 0)
        bucket_fmt = {key: value if key in ('guild', 'channel', 'webhook') else '' for key, value in fmt.items()}

        # Prepare the headers
        if 'headers' in kwargs:
            kwargs['headers'].update(self.headers)
        else:
            kwargs['headers'] = self.headers

        if kwargs.get('reason'):
            kwargs['headers']['X-Audit-Log-Reason'] = quote(kwargs['reason'], '/ ')

        method = route[0].value
        bucket_endpoint = route[1].format(**bucket_fmt)
        bucket = (method, bucket_endpoint)
        url = self.BASE_URL + route[1].format(**fmt)

        logger.debug('Performing request to bucket %s with headers %s', bucket, kwargs['headers'])

        response = await self._session.request(method, url, **kwargs)
        data = response._actual_response = self.parse_response(response)
        status = response.status_code

        if 200 <= status < 300:
            # These status codes indicate successful requests. So just return the JSON response.
            logger.debug(self.LOG_SUCCESS.format(bucket=bucket, url=url, text=data))
            return data

        elif status != 429 and 400 <= status < 500:
            # These status codes are only caused by the user and won't disappear with another request.
            # It'd be just a waste of performance to attempt sending another request.
            raise Exception('Something went wrong..\nData: ' + data)  # TODO change Exception
            # raise RequestFailed(response, data)

        else:
            # Something happened wrong... Let's try that again.
            retries += 1
            if retries > self.MAX_RETRIES:
                raise Exception('Something went wrong..\nData: ' + data)  # TODO change Exception
                # raise RequestFailed(response, data)

            retrying = randint(100, 50000) / 1000.0
            logger.debug(self.LOG_FAILED.format(bucket=bucket, code=status, error=response.content, seconds=retrying))
            await anyio.sleep(retrying)

            return await self.make_request(route, fmt, retries=retries, **kwargs)

    @staticmethod
    def parse_response(response):
        if response.headers['Content-Type'] == 'application/json':
            return response.json()
        return response.text.encode('utf-8')

    @staticmethod
    def create_user_agent():
        fmt = 'DiscordBot ({0.__url__}, v{0.__version__}) / Python {1[0]}.{1[1]}.{1[2]}'
        return fmt.format(clamor, sys.version_info)
