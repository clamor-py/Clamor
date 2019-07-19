# -*- coding: utf-8 -*-

from typing import List, Optional

from ..routes import Routes
from .base import *

__all__ = (
    'UserWrapper',
)


class UserWrapper(EndpointsWrapper):
    """"""

    @staticmethod
    def _check_username(username: str) -> Optional[str]:
        if not username:
            return None

        if 2 > len(username) > 32:
            raise ValueError('Usernames must be beween 2 and 32 characters long')

        if username in ('discordtag', 'everyone', 'here'):
            raise ValueError('Restricted username')

        if any(c in ('@', '#', ':', '```') for c in username):
            raise ValueError('Usernames must not contain "@", "#", ":" or "```"')

        return username.strip()

    async def get_current_user(self) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_CURRENT_USER)

    async def get_user(self, user_id: Snowflake) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_USER,
                                            dict(user=user_id))

    async def modify_current_user(self, username: str = None, avatar: str = None) -> dict:
        """"""

        params = optional(**{
            'username': self._check_username(username),
            'avatar': avatar
        })

        return await self.http.make_request(Routes.MODIFY_CURRENT_USER,
                                            json=params)

    async def get_current_user_guilds(self,
                                      before: Snowflake = None,
                                      after: Snowflake = None,
                                      limit: int = 100) -> list:
        """"""

        params = optional(**{
            'before': before,
            'after': after,
            'limit': limit
        })

        return await self.http.make_request(Routes.GET_CURRENT_USER_GUILDS,
                                            params=params)

    async def leave_guild(self, guild_id: Snowflake):
        """"""

        return await self.http.make_request(Routes.LEAVE_GUILD,
                                            dict(guild=guild_id))

    async def get_user_dms(self) -> list:
        """"""

        return await self.http.make_request(Routes.GET_USER_DMS)

    async def create_dm(self, recipient_id: Snowflake) -> dict:
        """"""

        return await self.http.make_request(Routes.CREATE_DM,
                                            json={'recipient_id': recipient_id})

    async def create_group_dm(self, access_tokens: List[str], nicks: dict) -> dict:
        """"""

        params = {
            'access_tokens': access_tokens,
            'nicks': nicks,
        }

        return await self.http.make_request(Routes.CREATE_GROUP_DM,
                                            json=params)

    async def get_user_connections(self) -> list:
        """"""

        return await self.http.make_request(Routes.GET_USER_CONNECTIONS)
