# -*- coding: utf-8 -*-

import sys
import unittest

import anyio

from clamor import __url__, __version__, HTTP, Routes


class HTTPTests(unittest.TestCase):
    def test_user_agent(self):
        async def main():
            http = HTTP('secret')
            self.assertIsInstance(http, HTTP)

            self.assertEqual(
                http.user_agent,
                'DiscordBot ({0}, v{1}) / Python {2[0]}.{2[1]}.{2[2]}'.format(
                    __url__, __version__, sys.version_info)
            )

        anyio.run(main)

    def test_authorization_header(self):
        async def main():
            http = HTTP('secret')
            self.assertIsInstance(http, HTTP)

            self.assertEqual(http.headers['Authorization'],
                             'Bot {}'.format(http.token))

        anyio.run(main)

    def test_route(self):
        route = Routes.CREATE_MESSAGE
        self.assertIsInstance(route[0].value, str)
        self.assertEqual(route[0].value.lower(), 'post')
        self.assertIsInstance(route[1], str)

    def test_http_request(self):
        async def main():
            http = HTTP('secret')
            self.assertIsInstance(http, HTTP)

            resp = await http.make_request(Routes.GET_GATEWAY)
            self.assertIsInstance(resp, dict)
            self.assertEqual(resp['url'], 'wss://gateway.discord.gg')

            await http.close()

        anyio.run(main)
