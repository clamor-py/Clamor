# -*- coding: utf-8 -*-

import unittest
import os

import anyio

from clamor import gateway, HTTP, Routes


class GatewayTests(unittest.TestCase):
    def gateway_connect(self, compressed: bool):
        async def main():
            http = HTTP(os.environ['TEST_BOT_TOKEN'])
            url = await http.make_request(Routes.GET_GATEWAY)

            gw = gateway.DiscordWebsocketClient(url['url'], zlib_compressed=compressed)
            connected = False
            self.assertIsInstance(gw, gateway.DiscordWebsocketClient)

            async def set_connected(data):
                nonlocal connected
                connected = True

            gw.emitter.add_listener("READY", set_connected)

            async def stop_gatway(after):
                await anyio.sleep(after)
                await gw.close()

            async with anyio.create_task_group() as tg:
                await tg.spawn(gw.start, os.environ['TEST_BOT_TOKEN'])
                await tg.spawn(stop_gatway, 10)

            self.assertTrue(connected)

        anyio.run(main)

    def test_normal_gateway_connect(self):
        self.gateway_connect(False)

    def test_compressed_gateway_connect(self):
        self.gateway_connect(True)
