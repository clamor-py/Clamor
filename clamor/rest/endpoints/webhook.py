# -*- coding: utf-8 -*-

import json
from typing import Optional

from ..routes import Routes
from .base import *

__all__ = (
    'WebhookWrapper',
)


class WebhookWrapper(EndpointsWrapper):
    """"""

    @staticmethod
    def _check_name(name: str) -> Optional[str]:
        """"""

        if 2 > len(name) > 32:
            raise ValueError('Name must be between 2 and 32 characters long')

        return name.strip()

    async def create_webhook(self, channel_id: Snowflake, name: str, avatar: str = None) -> dict:
        """"""

        params = {
            'name': self._check_name(name),
            'avatar': avatar,
        }

        return await self.http.make_request(Routes.CREATE_WEBHOOK,
                                            dict(channel=channel_id),
                                            json=params)

    async def get_channel_webhooks(self, channel_id: Snowflake) -> list:
        """"""

        return await self.http.make_request(Routes.GET_CHANNEL_WEBHOOKS,
                                            dict(channel=channel_id))

    async def get_guild_webhooks(self, guild_id: Snowflake) -> list:
        """"""

        return await self.http.make_request(Routes.GET_GUILD_WEBHOOKS,
                                            dict(guild=guild_id))

    async def get_webhook(self, webhook_id: Snowflake) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_WEBHOOK,
                                            dict(webhook=webhook_id))

    async def get_webhook_with_token(self, webhook_id: Snowflake, webhook_token: str) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_WEBHOOK_WITH_TOKEN,
                                            dict(webhook=webhook_id, token=webhook_token))

    async def modify_webhook(self,
                             webhook_id: Snowflake,
                             name: str = None,
                             avatar: str = None,
                             channel_id: Snowflake = None) -> dict:
        """"""

        params = optional(**{
            'name': self._check_name(name),
            'avatar': avatar,
            'channel_id': channel_id
        })

        return await self.http.make_request(Routes.MODIFY_WEBHOOK,
                                            dict(webhook=webhook_id),
                                            json=params)

    async def modify_webhook_with_token(self,
                                        webhook_id: Snowflake,
                                        webhook_token: str,
                                        name: str = None,
                                        avatar: str = None) -> dict:
        """"""

        params = optional(**{
            'name': self._check_name(name),
            'avatar': avatar
        })

        return await self.http.make_request(Routes.MODIFY_WEBHOOK_WITH_TOKEN,
                                            dict(webhook=webhook_id, token=webhook_token),
                                            json=params)

    async def delete_webhook(self, webhook_id: Snowflake):
        """"""

        return await self.http.make_request(Routes.DELETE_WEBHOOK,
                                            dict(webhook=webhook_id))

    async def delete_webhook_with_token(self, webhook_id: Snowflake, webhook_token: str):
        """"""

        return await self.http.make_request(Routes.DELETE_WEBHOOK_WITH_TOKEN,
                                            dict(webhook=webhook_id, token=webhook_token))

    async def execute_webhook(self,
                              webhook_id: Snowflake,
                              webhook_token: str,
                              content: str = None,
                              username: str = None,
                              avatar_url: str = None,
                              tts: bool = False,
                              files: list = None,
                              embeds: list = None,
                              wait: bool = False):
        """"""

        if not content and not files and not embeds:
            raise ValueError('At least one of content, files or embeds is required')

        payload = optional(**{
            'content': content,
            'username': username,
            'avatar_url': avatar_url,
            'tts': tts,
            'embeds': embeds
        })

        params = optional(**{
            'wait': wait
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

            return await self.http.make_request(Routes.EXECUTE_WEBHOOK,
                                                dict(webhook=webhook_id, token=webhook_token),
                                                files=attachments,
                                                data={'payload_json': json.dumps(payload)},
                                                params=params)

        return await self.http.make_request(Routes.EXECUTE_WEBHOOK,
                                            dict(webhook=webhook_id, token=webhook_token),
                                            json=payload,
                                            params=params)
