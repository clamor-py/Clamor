# -*- coding: utf-8 -*-

import unittest
import os

import anyio

from clamor import gateway, HTTP, Routes


class GatewayTests(unittest.TestCase):
    def test_gateway_connect(self):
        async def main():
            http = HTTP(os.environ['TEST_BOT_TOKEN'])
            url = await http.make_request(Routes.GET_GATEWAY)

            gw = gateway.DiscordWebsocketClient(url['url'])
            self.assertIsInstance(gw, gateway.DiscordWebsocketClient)

            await gw.start(os.environ['TEST_BOT_TOKEN'])

        anyio.run(main)
