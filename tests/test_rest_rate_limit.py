# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timezone
from email.utils import format_datetime
from random import randint

import anyio

from clamor import RateLimiter


class HTTPTests(unittest.TestCase):
    def test_rate_limiter(self):
        async def main():
            limiter = RateLimiter()
            self.assertIsInstance(limiter, RateLimiter)

            # Hack a fake response object.
            response = object()
            response.headers = {
                'Date': format_datetime(datetime.now(timezone.utc)),
                'X-RateLimit-Remaining': randint(1, 10),
                # 2 minutes in the future.
                'X-RateLimit-Reset': datetime.now(timezone.utc).timestamp() + (2 * 60),
            }

            bucket = ('POST', '/random')

            while True:
                if await limiter.cooldown_bucket(bucket) > 0:
                    break

                # The loop is supposed to be interrupted
                # before this is no longer true.
                self.assertGreaterEqual(limiter.buckets[bucket]._remaining, 0)

                # Update headers
                response.headers['Date'] = format_datetime(datetime.now(timezone.utc))
                response.headers['X-RateLimit-Remaining'] -= 1

                # Update the limiter
                await limiter.update_bucket(bucket, response)

            anyio.run(main)
