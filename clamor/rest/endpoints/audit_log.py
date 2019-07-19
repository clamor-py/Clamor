# -*- coding: utf-8 -*-

from enum import IntEnum
from typing import Union

from ..routes import Routes
from .base import *

__all__ = (
    'AuditLogAction',
    'AuditLogWrapper',
)


class AuditLogAction(IntEnum):
    """Enum that holds the various Audit Log event types."""

    #: Unknown event.
    UNKNOWN = 0

    #: Guild updated.
    GUILD_UPDATE = 1

    #: Channel created.
    CHANNEL_CREATE = 10
    #: Channel updated.
    CHANNEL_UPDATE = 11
    #: Channel deleted.
    CHANNEL_DELETE = 12
    #: Channel overwrite created.
    CHANNEL_OVERWRITE_CREATE = 13
    #: Channel overwrite updated.
    CHANNEL_OVERWRITE_UPDATE = 14
    #: Channel overwrite removed.
    CHANNEL_OVERWRITE_DELETE = 15

    #: Member kicked.
    MEMBER_KICK = 20
    #: Member pruned.
    MEMBER_PRUNE = 21
    #: Member banned.
    MEMBER_BAN_ADD = 22
    #: Member unbanned.
    MEMBER_BAN_REMOVE = 23
    #: Member updated.
    MEMBER_UPDATE = 24
    #: Member role updated.
    MEMBER_ROLE_UPDATE = 25

    #: Role created.
    ROLE_CREATE = 30
    #: Role updated.
    ROLE_UPDATE = 31
    #: Role deleted.
    ROLE_DELETE = 32

    #: Guild invite created.
    INVITE_CREATE = 40
    #: Guild invite updated.
    INVITE_UPDATE = 41
    #: Guild invite deleted.
    INVITE_DELETE = 42

    #: Webhook created.
    WEBHOOK_CREATE = 50
    #: Webhook updated.
    WEBHOOK_UPDATE = 51
    #: Webhook deleted.
    WEBHOOK_DELETE = 52

    #: Emoji added.
    EMOJI_CREATE = 60
    #: Emoji updated.
    EMOJI_UPDATE = 61
    #: Emoji deleted.
    EMOJI_DELETE = 62

    #: Message deleted.
    MESSAGE_DELETE = 72


class AuditLogWrapper(EndpointsWrapper):
    """"""

    def __init__(self, token: str, guild_id: Snowflake):
        super().__init__(token)

        self.guild_id = guild_id

    async def get_guild_audit_log(self,
                                  user_id: Snowflake,
                                  action_type: Union[AuditLogAction, int] = None,
                                  before: Snowflake = None,
                                  limit: int = 50) -> dict:
        """"""

        params = optional(**{
            'user_id': user_id,
            'action_type': action_type if isinstance(action_type, int) else action_type.value,
            'before': before,
            'limit': limit,
        })

        return await self.http.make_request(Routes.GET_GUILD_AUDIT_LOG,
                                            dict(guild=self.guild_id),
                                            params=params)
