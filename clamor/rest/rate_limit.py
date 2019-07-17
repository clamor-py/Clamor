# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import NewType, Tuple, Union

import anyio
from async_generator import async_generator, asynccontextmanager, yield_
from asks.response_objects import Response

__all__ = (
    'Bucket',
    'CooldownBucket',
    'RateLimiter'
)

logger = logging.getLogger(__name__)

#: A type to denote rate limit buckets.
Bucket = NewType('Bucket', Union[Tuple[str, str], str])


class CooldownBucket:
    """"""

    __slots__ = ('bucket', '_date', '_remaining', '_reset', 'lock')

    def __init__(self, bucket: Bucket, response: Response):
        self.bucket = bucket

        # These values will be set later.
        self._date = None
        self._remaining = 0
        self._reset = None

        self.lock = anyio.create_lock()

        self.update(response)

    def __repr__(self) -> str:
        return '<CooldownBucket bucket={}>'.format(
            ' '.join((self.bucket,) if isinstance(self.bucket, str) else self.bucket)
        )

    @property
    def will_rate_limit(self) -> bool:
        """Whether the next request is going to exhaust a rate limit or not."""

        return self._remaining == 0

    def update(self, response: Response):
        """"""

        headers = response.headers

        # Rate limit headers is basically all or nothing.
        # If one of the headers is missing, this applies
        # to the other headers as well.
        # Therefore it is sufficient to check for one header.
        if 'X-RateLimit-Remaining' not in headers:
            return

        self._date = parsedate_to_datetime(headers.get('Date'))
        self._remaining = int(headers.get('X-RateLimit-Remaining'))
        self._reset = datetime.fromtimestamp(int(headers.get('X-RateLimit-Reset')), timezone.utc)

    async def wait(self) -> float:
        """"""

        start = datetime.utcnow()
        async with self.lock:
            pass

        return (datetime.utcnow() - start).total_seconds()

    async def cooldown(self) -> float:
        """"""

        delay = (self._reset - self._date).total_seconds() + .5
        logger.debug('Cooling bucket %s for %d seconds', self, delay)
        await anyio.sleep(delay)

        return delay


class RateLimiter:
    """"""

    def __init__(self):
        self._buckets = {}
        self.global_lock = anyio.create_lock()

    @asynccontextmanager
    @async_generator
    async def __call__(self, bucket: Bucket):
        # If a global rate limit occurred, this is going to block
        # until the lock has been released after a cooldown.
        # If no global limit is exhausted, the lock will be
        # released immediately.
        async with self.global_lock:
            pass

        try:
            if await self.cooldown_bucket(bucket) > 0:
                logger.debug('Bucket %s cooled down', bucket)

            await yield_(self)
        finally:
            pass

    @property
    def buckets(self) -> dict:
        """"""

        return self._buckets

    async def cooldown_bucket(self, bucket: Bucket) -> float:
        """"""

        if bucket in self._buckets:
            async with self._buckets[bucket].lock:
                if self._buckets[bucket].will_rate_limit:
                    return await self._buckets[bucket].cooldown()

        return 0.0

    async def update_bucket(self, bucket: Bucket, response: Response):
        """"""

        if 'X-RateLimit-Global' in response.headers:
            async with self.global_lock:
                await anyio.sleep(
                    int(response.headers.get('Retry-After')) / 1000.0
                )

        if bucket in self._buckets:
            self._buckets[bucket].update(response)
        else:
            self._buckets[bucket] = CooldownBucket(bucket, response)
