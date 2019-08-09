# -*- coding: utf-8 -*-

import logging
import abc
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import NewType, Tuple, Union

import anyio
from async_generator import async_generator, asynccontextmanager, yield_
from asks.response_objects import Response

try:
    import redis
    INCLUDE_REDIS = True
except ModuleNotFoundError:
    INCLUDE_REDIS = False

__all__ = (
    'Bucket',
    'CooldownBucket',
    'RateLimiter',
)

logger = logging.getLogger(__name__)

#: A type to denote rate limit buckets.
Bucket = NewType('Bucket', Union[Tuple[str, str], str])


class CooldownBucket:
    """Wraps around a request bucket to handle rate limits.

    Instances of this class should be handled by :class:`~clamor.rest.rate_limit.RateLimiter`.
    They are constantly updated updated by :meth:`~CooldownBucket.update` given
    :class:`Response<asks:asks.response_objects.Response>` objects.

    CooldownBuckets extract rate limit information from headers and provide
    properties and methods that make it easy to deal with them.

    Parameters
    ----------
    bucket : Union[Tuple[str, str], str]
        The bucket for the route that should be covered.
    response : :class:`Response<asks:asks.response_objects.Response>`
        The initial response object to initialize this class with.

    Attributes
    ----------
    bucket : Union[Tuple[str, str], str]
        The bucket for the route that should be covered.
    lock : :class:`~Lock<anyio:anyio.abc.Lock>`
        The lock that is used when cooling down a route.
    """

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
        """Updates this instance given a response that holds rate limit headers.

        Parameters
        ----------
        response : :class:`Response<asks:asks.response_objects.Response>`
            The response object for the most recent request to the bucket
            this instance holds.
        """

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

    async def cooldown(self) -> float:
        """Cools down the bucket this instance holds.

        Returns
        -------
        float
            The duration the bucket has been cooled down for.
        """

        delay = (self._reset - self._date).total_seconds() + .5
        logger.debug('Cooling bucket %s for %d seconds', self, delay)
        await anyio.sleep(delay)

        return delay


class BucketStore(abc.ABC):
    """A bucket store to store buckets.

    This class is used to store RateLimiting buckets.
    This makes it possible to store buckets in other ways.
    For example in Redis.
    """

    @abc.abstractmethod
    def store_bucket(self, key: Bucket, value: CooldownBucket):
        pass

    @abc.abstractmethod
    def get_bucket(self, bucket: Bucket) -> CooldownBucket:
        pass

    @abc.abstractmethod
    def delete_bucket(self, bucket: Bucket):
        pass

    @abc.abstractmethod
    def has_bucket(self, bucket: Bucket) -> bool:
        pass

    def __getitem__(self, bucket: Bucket) -> CooldownBucket:
        return self.get_bucket(bucket)

    def __setitem__(self, key: Bucket, value: CooldownBucket):
        self.store_bucket(key, value)

    def __delitem__(self, bucket: Bucket):
        self.delete_bucket(bucket)

    def __contains__(self, bucket: Bucket) -> bool:
        return self.has_bucket(bucket)


class InMemoryBucketStore(BucketStore):
    """A BucketStore which stores the bucket in-memory via a dict

    This bucket store is the default store which will be used by the
    RateLimiter to store buckets.

    """

    def __init__(self):
        self._buckets = {}

    def store_bucket(self, key: Bucket, value: CooldownBucket):
        self._buckets[key] = value

    def get_bucket(self, bucket: Bucket) -> CooldownBucket:
        return self._buckets[bucket]

    def delete_bucket(self, bucket: Bucket):
        del self._buckets[bucket]

    def has_bucket(self, bucket: Bucket) -> bool:
        return bucket in self._buckets


if INCLUDE_REDIS:
    class RedisBucketStore(BucketStore):
        """A bucket store which stores the bucket in a redis database.

        This class is only available if you have [redis-py](https://pypi.org/project/redis/)
        installed.

        Parameters
        ----------
        **kwargs : dict
            Look at the [redis-py](https://pypi.org/project/redis/)
            documentation to see all Keyowrd arguments
        """

        def __init__(self, **kwargs):
            self.redis_client = redis.Redis(**kwargs)

        def store_bucket(self, key: Bucket, value: CooldownBucket):
            pass

        def get_bucket(self, bucket: Bucket) -> CooldownBucket:
            pass

        def delete_bucket(self, bucket: Bucket):
            pass

        def has_bucket(self, bucket: Bucket) -> bool:
            pass


class RateLimiter:
    """A rate limiter to keep track of per-bucket rate limits.

    This is responsible for updating and cooling down buckets
    before another request is made.
    :meth:`RateLimiter.update_bucket` and :meth:`RateLimiter.cooldown_bucket`
    can be used for that. It can also be used as an async
    contextmanager.

    Buckets are stored in the bucket store passed in the constructor.
    If no bucket store is specified, the buckets are stored in memory.
    :class:`~clamor.rest.rate_limit.CooldownBucket` objects.

    .. code-block:: python3

        buckets = {
            ('GET', '/channels/1234'): <CooldownBucket bucket=GET /channels/1234>,
            ('PATCH', '/users/@me'): <CooldownBucket bucket=PATCH /users/@me>,
            ...
        }

    Example
    -------

    .. code-block:: python3

        limiter = RateLimiter()

        ...

        # Option 1:

        # Make sure no global rate limit is exhausted.
        async with limiter.global_lock:
            pass

        await limiter.cooldown_bucket(bucket)  # Blocks if rate limit is exhausted.
        response = await asks.request(bucket[0],
                                      'https://discordapp.com/api/' + bucket[1], ...)
        await limiter.update_bucket(bucket, response)

        # Option 2:

        async with limiter(bucket):
            response = await asks.request(bucket[0],
                                          'https://discordapp.com/api/' + bucket[1], ...)
            await limiter.update_bucket(bucket, response)

    Attributes
    ----------
    global_lock : :class:`Lock<anyio:anyio.abc.Lock>`
        Separate lock for global rate limits.
    """

    def __init__(self, bucket_store=None):
        self._buckets = bucket_store or InMemoryBucketStore()
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
        """The buckets this instance holds."""

        return self._buckets

    async def cooldown_bucket(self, bucket: Bucket) -> float:
        """Cools down a given bucket.

        If no rate limit is exhausted, this returns immediately.

        .. note::

            This acquires the lock the bucket holds.

        Parameters
        ----------
        bucket : Union[Tuple[str, str], str]
            The bucket to cool down.

        Returns
        -------
        float
            The duration this bucket has been cooled down for.
        """

        if bucket in self._buckets:
            async with self._buckets[bucket].lock:
                if self._buckets[bucket].will_rate_limit:
                    return await self._buckets[bucket].cooldown()

        return 0.0

    async def update_bucket(self, bucket: Bucket, response: Response):
        """Updates a bucket by a given response.

        .. note::

            This also checks for global rate limits
            and handles them if necessary.

        Parameters
        ----------
        bucket : Union[Tuple[str, str], str]
            The bucket to update.
        response : :class:`Response<asks:asks.response_objects.Response>`
            The response object to extract rate limit headers from.
        """

        if 'X-RateLimit-Global' in response.headers:
            async with self.global_lock:
                await anyio.sleep(
                    int(response.headers.get('Retry-After')) / 1000.0
                )

        if bucket in self._buckets:
            self._buckets[bucket].update(response)
        else:
            self._buckets[bucket] = CooldownBucket(bucket, response)
