# -*- coding: utf-8 -*-

import json
import re
from typing import List

from ..routes import Routes
from .base import *

__all__ = (
    'ChannelWrapper',
)


class ChannelWrapper(EndpointsWrapper):
    """"""

    def __init__(self, token: str, channel_id: Snowflake):
        super().__init__(token)

        self.channel_id = channel_id

    @staticmethod
    def _parse_emoji(emoji: str) -> str:
        match = re.match(r'<a?(:\w+:\d+)>', emoji)
        if match:
            emoji = match.group(1)

        return emoji

    async def get_channel(self) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_CHANNEL, dict(channel=self.channel_id))

    async def modify_channel(self,
                             name: str = None,
                             position: int = None,
                             topic: str = None,
                             nsfw: bool = None,
                             rate_limit_per_user: int = None,
                             bitrate: int = None,
                             user_limit: int = None,
                             permission_overwrites: list = None,
                             parent_id: Snowflake = None,
                             reason: str = None) -> dict:
        """"""

        params = optional(**{
            'name': name,
            'position': position,
            'topic': topic,
            'nsfw': nsfw,
            'rate_limit_per_user': rate_limit_per_user,
            'bitrate': bitrate,
            'user_limit': user_limit,
            'permission_overwrites': permission_overwrites,
            'parent_id': parent_id
        })

        return await self.http.make_request(Routes.MODIFY_CHANNEL,
                                            dict(channel=self.channel_id),
                                            json=params,
                                            reason=reason)

    async def delete_channel(self, reason: str = None) -> dict:
        """"""

        return await self.http.make_request(Routes.DELETE_CHANNEL,
                                            dict(channel=self.channel_id),
                                            reason=reason)

    async def get_channel_messages(self,
                                   around: Snowflake = None,
                                   before: Snowflake = None,
                                   after: Snowflake = None,
                                   limit: int = 50) -> list:
        """"""

        params = optional(**{
            'around': around,
            'before': before,
            'after': after,
            'limit': limit
        })

        return await self.http.make_request(Routes.GET_CHANNEL_MESSAGES,
                                            dict(channel=self.channel_id),
                                            params=params)

    async def get_channel_message(self, message_id: Snowflake) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_CHANNEL_MESSAGE,
                                            dict(channel=self.channel_id, message=message_id))

    async def create_message(self,
                             content: str = None,
                             nonce: Snowflake = None,
                             tts: bool = False,
                             files: list = None,
                             embed: dict = None) -> dict:
        """"""

        payload = optional(**{
            'content': content,
            'nonce': nonce,
            'tts': tts,
            'embed': embed
        })

        if files:
            if len(files) == 1:
                attachments = {
                    'file': tuple(files[0]),
                }
            else:
                attachments = {
                    'file{}'.format(index): tuple(file) for index, file in enumerate(files)
                }

            return await self.http.make_request(Routes.CREATE_MESSAGE,
                                                dict(channel=self.channel_id),
                                                files=attachments,
                                                data={'payload_json': json.dumps(payload)})

        return await self.http.make_request(Routes.CREATE_MESSAGE,
                                            dict(channel=self.channel_id),
                                            json=payload)

    async def create_reaction(self, message_id: Snowflake, emoji: str):
        """"""

        return await self.http.make_request(Routes.CREATE_REACTION,
                                            dict(channel=self.channel_id,
                                                 message=message_id,
                                                 emoji=self._parse_emoji(emoji)))

    async def delete_own_reaction(self, message_id: Snowflake, emoji: str):
        """"""

        return await self.http.make_request(Routes.DELETE_OWN_REACTION,
                                            dict(channel=self.channel_id,
                                                 message=message_id,
                                                 emoji=self._parse_emoji(emoji)))

    async def delete_user_reaction(self,
                                   message_id: Snowflake,
                                   user_id: Snowflake,
                                   emoji: str):
        """"""

        return await self.http.make_request(Routes.DELETE_USER_REACTION,
                                            dict(channel=self.channel_id,
                                                 message=message_id,
                                                 emoji=self._parse_emoji(emoji),
                                                 user=user_id))

    async def get_reactions(self,
                            message_id: Snowflake,
                            emoji: str,
                            before: Snowflake = None,
                            after: Snowflake = None,
                            limit: int = 25) -> dict:
        """"""

        params = optional(**{
            'before': before,
            'after': after,
            'limit': limit
        })

        return await self.http.make_request(Routes.GET_REACTIONS,
                                            dict(channel=self.channel_id,
                                                 message=message_id,
                                                 emoji=self._parse_emoji(emoji)),
                                            params=params)

    async def delete_all_reactions(self, message_id: Snowflake):
        """"""

        return await self.http.make_request(Routes.DELETE_ALL_REACTIONS,
                                            dict(channel=self.channel_id, message=message_id))

    async def edit_message(self,
                           message_id: Snowflake,
                           content: str = None,
                           embed: dict = None) -> dict:
        """"""

        params = optional(**{
            'content': content,
            'embed': embed,
        })

        return await self.http.make_request(Routes.EDIT_MESSAGE,
                                            dict(channel=self.channel_id, message=message_id),
                                            json=params)

    async def delete_message(self, message_id: Snowflake, reason: str = None):
        """"""

        return await self.http.make_request(Routes.DELETE_MESSAGE,
                                            dict(channel=self.channel_id, message=message_id),
                                            reason=reason)

    async def bulk_delete_messages(self, messages: List[Snowflake], reason: str = None):
        """"""

        if 2 <= len(messages) <= 100:
            raise ValueError('Bulk delete requires a message count between 2 and 100')

        return await self.http.make_request(Routes.BULK_DELETE_MESSAGES,
                                            dict(channel=self.channel_id),
                                            json={'messages': messages},
                                            reason=reason)

    async def edit_channel_permissions(self,
                                       overwrite_id: Snowflake,
                                       allow: int = None,
                                       deny: int = None,
                                       type: str = None,
                                       reason: str = None):
        """"""

        params = optional(**{
            'allow': allow,
            'deny': deny,
            'type': type
        })

        if params.get('type', 'member') not in ('member', 'role'):
            raise ValueError('Argument for type must be either "member" or "role"')

        return await self.http.make_request(Routes.EDIT_CHANNEL_PERMISSIONS,
                                            dict(channel=self.channel_id, overwrite=overwrite_id),
                                            json=params,
                                            reason=reason)

    async def get_channel_invites(self) -> list:
        """"""

        return await self.http.make_request(Routes.GET_CHANNEL_INVITES,
                                            dict(channel=self.channel_id))

    async def create_channel_invite(self,
                                    max_age: int = 86400,
                                    max_uses: int = 0,
                                    temporary: bool = False,
                                    unique: bool = False,
                                    reason: str = None) -> dict:
        """"""

        params = optional(**{
            'max_age': max_age,
            'max_uses': max_uses,
            'temporary': temporary,
            'unique': unique
        })

        return await self.http.make_request(Routes.CREATE_CHANNEL_INVITE,
                                            dict(channel=self.channel_id),
                                            json=params,
                                            reason=reason)

    async def delete_channel_permission(self, overwrite_id: Snowflake, reason: str = None):
        """"""

        return await self.http.make_request(Routes.DELETE_CHANNEL_PERMISSION,
                                            dict(channel=self.channel_id, overwrite=overwrite_id),
                                            reason=reason)

    async def trigger_typing_indicator(self):
        """"""

        return await self.http.make_request(Routes.TRIGGER_TYPING_INDICATOR,
                                            dict(channel=self.channel_id))

    async def get_pinned_messages(self) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_PINNED_MESSAGES,
                                            dict(channel=self.channel_id))

    async def add_pinned_channel_message(self, message_id: Snowflake):
        """"""

        return await self.http.make_request(Routes.ADD_PINNED_CHANNEL_MESSAGE,
                                            dict(channel=self.channel_id, message=message_id))

    async def delete_pinned_channel_message(self, message_id: Snowflake, reason: str = None):
        """"""

        return await self.http.make_request(Routes.DELETE_PINNED_CHANNEL_MESSAGE,
                                            dict(channel=self.channel_id, message=message_id),
                                            reason=reason)

    async def group_dm_add_recipient(self,
                                     user_id: Snowflake,
                                     access_token: str = None,
                                     nick: str = None):
        """"""

        params = optional(**{
            'access_token': access_token,
            'nick': nick
        })

        return await self.http.make_request(Routes.GROUP_DM_ADD_RECIPIENT,
                                            dict(channel=self.channel_id, user=user_id),
                                            json=params)

    async def group_dm_remove_recipient(self, user_id: Snowflake):
        """"""

        return await self.http.make_request(Routes.GROUP_DM_REMOVE_RECIPIENT,
                                            dict(channel=self.channel_id, user=user_id))
