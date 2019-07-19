# -*- coding: utf-8 -*-

from ..routes import Routes
from .base import *

__all__ = (
    'EmojiWrapper',
)


class EmojiWrapper(EndpointsWrapper):
    """"""

    def __init__(self, token: str, guild_id: Snowflake):
        super().__init__(token)

        self.guild_id = guild_id

    async def list_guild_emojis(self) -> list:
        """"""

        return await self.http.make_request(Routes.LIST_GUILD_EMOJIS,
                                            dict(guild=self.guild_id))

    async def get_guild_emoji(self, emoji_id: Snowflake) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_GUILD_EMOJI,
                                            dict(guild=self.guild_id, emoji=emoji_id))

    async def create_guild_emoji(self,
                                 name: str,
                                 image: str,
                                 roles: list) -> dict:
        """"""

        params = {
            'name': name,
            'image': image,
            'roles': roles
        }

        return await self.http.make_request(Routes.CREATE_GUILD_EMOJI,
                                            dict(guild=self.guild_id),
                                            json=params)

    async def modify_guild_emoji(self,
                                 emoji_id: Snowflake,
                                 name: str = None,
                                 roles: list = None) -> dict:
        """"""

        params = optional(**{
            'name': name,
            'roles': roles
        })

        return await self.http.make_request(Routes.MODIFY_GUILD_EMOJI,
                                            dict(guild=self.guild_id, emoji=emoji_id),
                                            json=params)

    async def delete_guild_emoji(self, emoji_id: Snowflake):
        """"""

        return await self.http.make_request(Routes.DELETE_GUILD_EMOJI,
                                            dict(guild=self.guild_id, emoji=emoji_id))
