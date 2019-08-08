# -*- coding: utf-8 -*-

import logging
import zlib
from random import randint
from time import perf_counter
from typing import Any, Union

import anyio
import anysocks

from ..exceptions import *
from ..utils import Emitter
from .encoding import ENCODERS
from .opcodes import Opcode
from .serialization import *

logger = logging.getLogger(__name__)


class DiscordWebsocketClient:
    """Implements version 6 of the Discord WebSocket Gateway protocol.

    Todo: Add sharding.

    Parameters
    ----------
    url : str
        URL of the gateway, usually 'wss://gateway.discord.gg``
    encoding : str
        Either 'json' or 'etf'; the encoding used in the connection. Defaults to 'json'
    zlib_compressed : bool
        Indicates if the communication should be compressed. Defaults to false

    Attributes
    ----------
    url : str
        URL of the gateway
    encoder : :class:`clamor.gateway.BaseEncoder`
        Used to en-/decode the messages from the gateway.
    zlib_compressed : bool
        Indicates if the communication should be compressed.
    """

    #: The gateway version to use.
    VERSION = 6
    #: Necessary bytes to detect zlib-compressed payloads.
    ZLIB_SUFFIX = b'\x00\x00\xff\xff'

    def __init__(self, url: str, **kwargs):
        self.encoder = ENCODERS[kwargs.get('encoding', 'json')]
        self.zlib_compressed = kwargs.get('zlib_compressed', True)
        self._token = None
        self.url = self.format_url(url)

        # Sharding
        self.shard_id = kwargs.get('shard_id')
        self.shard_count = kwargs.get('shard_count')

        # Compression
        if self.zlib_compressed:
            self.buffer = bytearray()
            self.inflator = zlib.decompressobj()

        # WebSocket connection
        self._con = None
        self._running = False
        self._should_reconnect = True
        self._task_group = None

        # Connection state
        self._session_id = None
        self.reconnects = 0
        self._last_sent = perf_counter()
        self._last_ack = perf_counter()
        self.latency = float('inf')

        # Heartbeat stuff
        self.sequence = None
        self._interval = 0
        self._heartbeat_acknowledged = True

        # TODO: Rate limiting

        # Event dispatching
        self.emitter = Emitter()
        self.emitter.add_listener(Opcode.DISPATCH, self._on_dispatch)
        self.emitter.add_listener(Opcode.HEARTBEAT, self._on_heartbeat)
        self.emitter.add_listener(Opcode.RECONNECT, self._on_reconnect)
        self.emitter.add_listener(Opcode.INVALID_SESSION, self._on_invalid_session)
        self.emitter.add_listener(Opcode.HELLO, self._on_hello)
        self.emitter.add_listener(Opcode.HEARTBEAT_ACK, self._on_heartbeat_ack)

    def format_url(self, url: str) -> str:
        url += '?v={}&encoding={}'.format(self.VERSION, self.encoder.TYPE)
        if self.zlib_compressed:
            url += '&compress=zlib-stream'

        return url

    async def _heartbeat_task(self):
        while not self._con.closed and self._running:
            await self._do_heartbeat()
            await anyio.sleep(self._interval)

    async def _do_heartbeat(self):
        if self._heartbeat_acknowledged:
            logger.debug('Sending Heartbeat with sequence %s', self.sequence)
            await self._send(Opcode.HEARTBEAT, self.sequence)
            self._last_sent = perf_counter()
            self._heartbeat_acknowledged = False
        else:
            logger.error('Gateway hasn\'t responded with HEARTBEAT_ACK. Forcing a reconnect.')
            await self._con.close(4000, 'Zombied connection!')

    async def _send(self, opcode: Union[Opcode, int, str], data: Any):
        logger.debug('Sending %s', data)
        payload = {
            'op': opcode.value if isinstance(opcode, Opcode) else int(opcode),
            'd': data,
        }

        await self._con.send(self.encoder.encode(payload))

    async def _on_dispatch(self, event: str, data: dict):
        logger.debug('Received Opcode 0 Dispatch for event %s with data %s', event, data)

        # Ready is special and contains critical state information,
        # that's why it needs to be handled separately.
        if event == 'READY':
            if data['v'] != self.VERSION:
                raise RuntimeError('Gateway protocol versions do not match')

            if 'shard' in data and data['shard'] != [self.shard_id, self.shard_count]:
                raise RuntimeError('Running on wrong shard')

            self._session_id = data['session_id']

        # TODO: Do actual event dispatching.

    async def _on_heartbeat(self, _):
        logger.debug('Heartbeat requested by the Discord gateway')
        await self._do_heartbeat()
        self._last_sent = perf_counter()

    async def _on_reconnect(self, _):
        logger.debug('Received Opcode 7 Reconnect, forcing a reconnect.')
        self._session_id = None
        self.sequence = None
        await self._con.close(1000)

    async def _on_invalid_session(self, _):
        logger.debug('Received Opcode 9 Invalid Session, forcing a reconnect.')
        self._session_id = None
        self.sequence = None
        await self._con.close(1000)

    async def _on_hello(self, data: dict):
        self._interval = data['heartbeat_interval'] / 1000
        logger.debug('Received Opcode 10 Hello with heartbeat interval %s', self._interval)
        await self._task_group.spawn(self._heartbeat_task)
        await self._identify_or_resume()

    async def _on_heartbeat_ack(self, _):
        logger.debug('Received Opcode 11 Heartbeat ACK')
        self._last_ack = ack_time = perf_counter()
        self.latency = ack_time - self._last_sent
        self._heartbeat_acknowledged = True

    async def _process_message(self, message: Union[bytes, str]):
        logger.debug('Received %s', message)

        # Decompress zlib stream if given.
        if self.zlib_compressed:
            self.buffer.extend(message)

            # The WebSocket protocol supports entire payloads being
            # split across multiple messages. Though there are no
            # known cases where Discord does that, it is still
            # possible and we handle that for convenience.
            if len(message) < 4 or message[-4:] != self.ZLIB_SUFFIX:
                return

            message = self.inflator.decompress(self.buffer).decode('utf-8')
            self.buffer = bytearray()
        elif message[0] not in ('{', 131):  # Neither JSON nor ETF.
            # In special cases, the gateway may also send
            # zlib-compressed payloads even without the
            # compress URL parameter being set.
            message = zlib.decompress(message, 15).decode('utf-8')

        # Decode ETF/JSON payload.
        try:
            message = self.encoder.decode(message)
        except Exception as e:
            raise EncodingFailed(str(e))

        if 's' in message:
            self.sequence = message['s']

        opcode = Opcode(message['op'])
        event_data = message['d']

        if opcode is Opcode.DISPATCH:
            await self.emitter.emit(opcode, message['t'].upper(), event_data)
        else:
            await self.emitter.emit(opcode, event_data)

    async def _identify_or_resume(self):
        if self._session_id and self.sequence:
            # Since session_id and sequence are set,
            # we attempt to resume the connection.
            logger.debug('Attempting to resume connection with Session ID %s and Sequence %s',
                         self._session_id, self.sequence)
            await self._send(Opcode.RESUME, resume(self._token, self._session_id, self.sequence))
        else:
            logger.debug('Performing identify handshake')
            await self._send(
                Opcode.IDENTIFY,
                identify(self._token, shard=[self.shard_id, self.shard_count])
            )

    async def _handle_closure(self, code: GatewayCloseCode, reason: str):
        logger.info('Connection was closed with %s (%s): %s', code.value, code.name, reason)

        # Clean up old data
        self._con = None
        self._running = False
        if self.zlib_compressed:
            self.buffer = bytearray()
            self.inflator = zlib.decompressobj()

        if not self._should_reconnect:
            return

        # These codes denote errors. In such cases
        # we don't want to resume connections, but
        # restart them.
        if 4000 <= code.value <= 4011:
            self._session_id = None
            self._interval = None

        action = 'resume' if self._session_id else 'reconnect'
        delay = randint(10, 20)
        logger.debug('Attempting to %s after %s seconds', action, delay)

        await anyio.sleep(delay)
        await self._connect()

    async def _connect(self):
        logger.debug('Opening WebSocket connection to %s', self.url)

        async with anysocks.open_connection(self.url) as con:
            self._con = con
            self._running = True

            while not self._con.closed and self._running:
                try:
                    message = await self._con.get_message()
                except anysocks.exceptions.ConnectionClosed:
                    break

                await self._process_message(message)

        close_code = GatewayCloseCode(self._con.close_code.value)
        close_reason = self._con.close_reason or ''

        await self._handle_closure(close_code, close_reason)

    async def start(self, token: str):
        self._token = token
        async with anyio.create_task_group() as task_group:
            self._task_group = task_group
            await self._task_group.spawn(self._connect)

    async def close(self):
        self._should_reconnect = False
        await self._con.close(1000)
