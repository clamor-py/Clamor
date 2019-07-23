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
            reconnected = False

            async def got_reconnect(data):
                nonlocal reconnected
                reconnected = True

            async def trigger_resume(data):
                await gw.resume()

            async def stop_gatway(after):
                await anyio.sleep(after)
                await gw.close()

            gw.emitter.add_listener("RECONNECTED", got_reconnect)
            gw.emitter.add_listener("READY", trigger_resume)

            async with anyio.create_task_group() as tg:
                await tg.spawn(gw.start, os.environ['TEST_BOT_TOKEN'])
                await tg.spawn(stop_gatway, 10)

            self.assertTrue(reconnected)

        anyio.run(main)
