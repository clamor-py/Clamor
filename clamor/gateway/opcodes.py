# -*- coding: utf-8 -*-

from enum import IntEnum

__all__ = (
    'Opcode',
)


class Opcode(IntEnum):
    """Gateway opcodes."""

    #: Dispatches an event.
    DISPATCH = 0
    #: Used for ping checking.
    HEARTBEAT = 1
    #: Used for client handshake.
    IDENTIFY = 2
    #: Used to update the client status.
    STATUS_UPDATE = 3
    #: Used to join/move/leave voice channels.
    VOICE_STATE_UPDATE = 4
    #: Used to check ping time to a voice channel.
    VOICE_PING = 5
    #: Used to resume a closed connection.
    RESUME = 6
    #: Used to tell clients to reconnect to the gateway.
    RECONNECT = 7
    #: Used to request guild members.
    REQUEST_GUILD_MEMBERS = 8
    #: Used to notify the client that they have an invalid session id.
    INVALID_SESSION = 9
    #: Sent immediately after connecting, contains heartbeat and server debug information.
    HELLO = 10
    #: Sent immediately following a client heartbeat that was received.
    HEARTBEAT_ACK = 11
    #: Used to request a client sync.
    GUILD_SYNC = 12
