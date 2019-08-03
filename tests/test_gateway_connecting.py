# -*- coding: utf-8 -*-

import os
import unittest

import anyio

from clamor import gateway, HTTP, Routes


class GatewayTests(unittest.TestCase):
    def gateway_connect(self, compressed: bool):
        async def main():
            http = HTTP(os.environ['TEST_BOT_TOKEN'])
            url = await http.make_request(Routes.GET_GATEWAY_BOT)

            gw = gateway.DiscordWebsocketClient(url['url'], shard_id=0, shard_count=1,
                                                zlib_compressed=compressed)
            connected = False
            self.assertIsInstance(gw, gateway.DiscordWebsocketClient)

            async def set_connected(_):
                nonlocal connected
                connected = True

            gw.emitter.add_listener(gateway.Opcode.DISPATCH, set_connected)

            async def stop_gateway(after):
                await anyio.sleep(after)
                await gw.close()

            async with anyio.create_task_group() as tg:
                await tg.spawn(gw.start, os.environ['TEST_BOT_TOKEN'])
                await tg.spawn(stop_gateway, 10)

            self.assertTrue(connected)

        anyio.run(main)

    def test_normal_gateway_connect(self):
        self.gateway_connect(False)

    def test_compressed_gateway_connect(self):
        self.gateway_connect(True)
