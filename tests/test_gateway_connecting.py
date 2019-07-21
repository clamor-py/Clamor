# -*- coding: utf-8 -*-

import unittest

import anyio

from clamor import gateway, HTTP, Routes

TOKEN = 'secret'


class GatewayTests(unittest.TestCase):
    def test_gateway_connect(self):
        async def main():
            http = HTTP(TOKEN)
            url = await http.make_request(Routes.GET_GATEWAY)

            gw = gateway.DiscordWebsocketClient(url['url'])
            self.assertIsInstance(gw, gateway.DiscordWebsocketClient)

            await gw.start(TOKEN)

        anyio.run(main, backend='trio')
