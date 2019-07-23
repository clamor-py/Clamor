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

            gw_one = gateway.DiscordWebsocketClient(url['url'], shard_id=0, shard_count=2)
            gw_two = gateway.DiscordWebsocketClient(url['url'], shard_id=1, shard_count=2)

            self.assertIsInstance(gw_one, gateway.DiscordWebsocketClient)
            self.assertIsInstance(gw_two, gateway.DiscordWebsocketClient)

            async def stop_gatways(after):
                await anyio.sleep(after)
                await gw_one.close()
                await gw_two.close()

            async with anyio.create_task_group() as tg:
                await tg.spawn(gw_one.start, os.environ['TEST_BOT_TOKEN'])
                await tg.spawn(gw_two.start, os.environ['TEST_BOT_TOKEN'])
                await tg.spawn(stop_gatways, 10)

        anyio.run(main)
