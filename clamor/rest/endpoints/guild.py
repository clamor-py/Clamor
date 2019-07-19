# -*- coding: utf-8 -*-

from ..routes import Routes
from .base import *

__all__ = (
    'GuildWrapper',
)


class GuildWrapper(EndpointsWrapper):
    """"""

    def __init__(self, token: str, guild_id: Snowflake):
        super().__init__(token)

        self.guild_id = guild_id

    async def create_guild(self,
                           name: str,
                           region: str,
                           icon: str,
                           verification_level: int,
                           default_message_notifications: int,
                           explicit_content_filter: int,
                           roles: list,
                           channels: list) -> dict:
        """"""

        params = {
            "name": name,
            "region": region,
            "icon": icon,
            "verification_level": verification_level,
            "default_message_notifications": default_message_notifications,
            "explicit_content_filter": explicit_content_filter,
            "roles": roles,
            "channels": channels
        }

        return await self.http.make_request(Routes.CREATE_GUILD,
                                            json=params)

    async def get_guild(self) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_GUILD,
                                            dict(guild=self.guild_id))

    async def modify_guild(self,
                           name: str = None,
                           region: str = None,
                           verification_level: int = None,
                           default_message_notifications: int = None,
                           explicit_content_filter: int = None,
                           afk_channel_id: Snowflake = None,
                           afk_timout: int = None,
                           icon: str = None,
                           owner_id: Snowflake = None,
                           splash: str = None,
                           system_channel_id: Snowflake = None,
                           reason: str = None) -> dict:
        """"""

        params = optional(**{
            "name": name,
            "region": region,
            "verification_level": verification_level,
            "default_message_notifications": default_message_notifications,
            "explicit_content_filter": explicit_content_filter,
            "afk_channel_id": afk_channel_id,
            "afk_timeout": afk_timout,
            "icon": icon,
            "owner_id": owner_id,
            "splash": splash,
            "system_channel_id": system_channel_id
        })

        return await self.http.make_request(Routes.MODIFY_GUILD,
                                            dict(guild=self.guild_id),
                                            json=params,
                                            reason=reason)

    async def delete_guild(self):
        """"""

        return await self.http.make_request(Routes.DELETE_GUILD,
                                            dict(guild=self.guild_id))

    async def get_guild_channels(self) -> list:
        """"""

        return await self.http.make_request(Routes.GET_GUILD_CHANNELS,
                                            dict(guild=self.guild_id))

    async def create_guild_channel(self,
                                   name: str,
                                   channel_type: int = None,
                                   topic: str = None,
                                   bitrate: int = None,
                                   user_limit: int = None,
                                   rate_limit_per_user: int = None,
                                   position: int = None,
                                   permission_overwrites: list = None,
                                   parent_id: Snowflake = None,
                                   reason: str = None) -> dict:
        """"""

        params = optional(**{
            "name": name,
            "channel_type": channel_type,
            "topic": topic,
            "bitrate": bitrate,
            "user_limit": user_limit,
            "rate_limit_per_user": rate_limit_per_user,
            "position": position,
            "permission_overwrites": permission_overwrites,
            "parent_id": parent_id
        })

        return await self.http.make_request(Routes.CREATE_GUILD_CHANNEL,
                                            dict(guild=self.guild_id),
                                            json=params,
                                            reason=reason)

    async def modify_guild_channel_positions(self, channels: list):
        """"""

        return await self.http.make_request(Routes.MODIFY_GUILD_CHANNEL_POSITIONS,
                                            dict(guild=self.guild_id),
                                            json=channels)

    async def get_guild_member(self, user_id: Snowflake) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_GUILD_MEMBER,
                                            dict(guild=self.guild_id, member=user_id))

    async def list_guild_members(self,
                                 limit: int = None,
                                 after: Snowflake = None) -> list:
        """"""

        params = optional(**{
            "limit": limit,
            "after": after
        })

        return await self.http.make_request(Routes.LIST_GUILD_MEMBERS,
                                            dict(guild=self.guild_id),
                                            json=params)

    async def add_guild_member(self,
                               user_id: Snowflake,
                               access_token: str,
                               nick: str = None,
                               roles: list = None,
                               mute: bool = None,
                               deaf: bool = None) -> dict:
        """"""

        params = optional(**{
            "access_token": access_token,
            "nick": nick,
            "roles": roles,
            "mute": mute,
            "deaf": deaf
        })

        return await self.http.make_request(Routes.ADD_GUILD_MEMBER,
                                            dict(guild=self.guild_id, member=user_id),
                                            json=params)

    async def modify_guild_member(self,
                                  user_id: Snowflake,
                                  nick: str = None,
                                  roles: list = None,
                                  mute: bool = None,
                                  deaf: bool = None,
                                  channel_id: Snowflake = None,
                                  reason: str = None):
        """"""

        params = optional(**{
            "nick": nick,
            "roles": roles,
            "mute": mute,
            "deaf": deaf,
            "channel_id": channel_id
        })

        return await self.http.make_request(Routes.MODIFY_GUILD_MEMBER,
                                            dict(guild=self.guild_id, member=user_id),
                                            json=params,
                                            reason=reason)

    async def modify_current_user_nick(self, nick: str, reason: str = None) -> str:
        """"""

        params = {
            "nick": nick
        }

        return await self.http.make_request(Routes.MODIFY_CURRENT_USER_NICK,
                                            dict(guild=self.guild_id),
                                            json=params,
                                            reason=reason)

    async def add_guild_member_role(self,
                                    user_id: Snowflake,
                                    role_id: Snowflake,
                                    reason: str = None):
        """"""

        return await self.http.make_request(Routes.ADD_GUILD_MEMBER_ROLE,
                                            dict(guild=self.guild_id, member=user_id, role=role_id),
                                            reason=reason)

    async def remove_guild_member_role(self,
                                       user_id: Snowflake,
                                       role_id: Snowflake,
                                       reason: str = None):
        """"""

        return await self.http.make_request(Routes.REMOVE_GUILD_MEMBER_ROLE,
                                            dict(guild=self.guild_id, member=user_id, role=role_id),
                                            reason=reason)

    async def remove_guild_member(self, user_id: Snowflake, reason: str = None):
        """"""

        return await self.http.make_request(Routes.REMOVE_GUILD_MEMBER,
                                            dict(guild=self.guild_id, member=user_id),
                                            reason=reason)

    async def get_guild_bans(self) -> list:
        """"""

        return await self.http.make_request(Routes.GET_GUILD_BANS,
                                            dict(guild=self.guild_id))

    async def get_guild_ban(self, user_id: Snowflake) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_GUILD_BAN,
                                            dict(guild=self.guild_id, user=user_id))

    async def create_guild_ban(self,
                               user_id: Snowflake,
                               delete_message_days: int = None,
                               reason: str = None):
        """"""

        params = optional(**{
            "delete_message_days": delete_message_days,
            "reason": reason
        })

        return await self.http.make_request(Routes.CREATE_GUILD_BAN,
                                            dict(guild=self.guild_id, user=user_id),
                                            json=params)

    async def remove_guild_ban(self, user_id: Snowflake, reason: str = None):
        """"""

        return await self.http.make_request(Routes.REMOVE_GUILD_BAN,
                                            dict(guild=self.guild_id, user=user_id),
                                            reason=reason)

    async def get_guild_roles(self):
        """"""

        return await self.http.make_request(Routes.GET_GUILD_ROLES,
                                            dict(guild=self.guild_id))

    async def create_guild_role(self,
                                name: str = None,
                                permissions: int = None,
                                color: int = None,
                                hoist: bool = None,
                                mentionable: bool = None,
                                reason: str = None) -> dict:
        """"""

        params = optional(**{
            "name": name,
            "permissions": permissions,
            "color": color,
            "hoist": hoist,
            "mentionable": mentionable
        })

        return await self.http.make_request(Routes.CREATE_GUILD_ROLE,
                                            dict(guild=self.guild_id),
                                            json=params,
                                            reason=reason)

    async def modify_guild_role_positions(self, roles: list, reason: str = None) -> list:
        """"""

        return await self.http.make_request(Routes.MODIFY_GUILD_ROLE_POSITIONS,
                                            dict(guild=self.guild_id),
                                            json=roles,
                                            reason=reason)

    async def modify_guild_role(self,
                                role_id: Snowflake,
                                name: str = None,
                                permissions: int = None,
                                color: int = None,
                                hoist: bool = None,
                                mentionable: bool = None,
                                reason: str = None) -> dict:
        """"""

        params = optional(**{
            "name": name,
            "permissions": permissions,
            "color": color,
            "hoist": hoist,
            "mentionable": mentionable
        })

        return await self.http.make_request(Routes.MODIFY_GUILD_ROLE,
                                            dict(guild=self.guild_id, role=role_id),
                                            json=params,
                                            reason=reason)

    async def delete_guild_role(self, role_id: Snowflake, reason: str = None):
        """"""

        return await self.http.make_request(Routes.DELETE_GUILD_ROLE,
                                            dict(guild=self.guild_id, role=role_id),
                                            reason=reason)

    async def get_guild_prune_count(self) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_GUILD_PRUNE_COUNT,
                                            dict(guild=self.guild_id))

    async def begin_guild_prune(self,
                                days: int,
                                compute_prune_count: bool) -> dict:
        """"""

        params = {
            "days": days,
            "compute_prune_count": compute_prune_count
        }

        return await self.http.make_request(Routes.BEGIN_GUILD_PRUNE,
                                            dict(guild=self.guild_id),
                                            json=params)

    async def get_guild_voice_regions(self) -> list:
        """"""

        return await self.http.make_request(Routes.GET_GUILD_VOICE_REGIONS,
                                            dict(guild=self.guild_id))

    async def get_guild_invites(self) -> list:
        """"""

        return await self.http.make_request(Routes.GET_GUILD_INVITES,
                                            dict(guild=self.guild_id))

    async def get_guild_integrations(self) -> list:
        """"""

        return await self.http.make_request(Routes.GET_GUILD_INTEGRATIONS,
                                            dict(guild=self.guild_id))

    async def create_guild_integration(self,
                                       int_type: str,
                                       int_id: Snowflake,
                                       reason: str = None):
        """"""

        params = {
            "type": int_type,
            "id": int_id
        }

        return await self.http.make_request(Routes.CREATE_GUILD_INTEGRATION,
                                            dict(guild=self.guild_id),
                                            json=params,
                                            reason=reason)

    async def modify_guild_integration(self,
                                       integration_id: Snowflake,
                                       expire_behavior: int,
                                       expire_grace_period: int,
                                       enable_emoticons: bool,
                                       reason: str = None):
        params = {
            "expire_behavior": expire_behavior,
            "expire_grace_period": expire_grace_period,
            "enable_emoticons": enable_emoticons
        }

        return await self.http.make_request(Routes.MODIFY_GUILD_INTEGRATION,
                                            dict(guild=self.guild_id, integration=integration_id),
                                            json=params,
                                            reason=reason)

    async def delete_guild_integration(self, integration_id: Snowflake, reason: str = None):
        """"""

        return await self.http.make_request(Routes.DELETE_GUILD_INTEGRATION,
                                            dict(guild=self.guild_id, integration=integration_id),
                                            reason=reason)

    async def sync_guild_integration(self, integration_id: Snowflake):
        """"""

        return await self.http.make_request(Routes.SYNC_GUILD_INTEGRATION,
                                            dict(guild=self.guild_id, integration=integration_id))

    async def get_guild_embed(self) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_GUILD_EMBED,
                                            dict(guild=self.guild_id))

    async def modify_guild_embed(self,
                                 enabled: bool,
                                 channel_id: Snowflake,
                                 reason: str = None):
        """"""

        params = {
            "enabled": enabled,
            "channel_id": channel_id
        }

        return await self.http.make_request(Routes.MODIFY_GUILD_EMBED,
                                            dict(guild=self.guild_id),
                                            json=params,
                                            reason=reason)

    async def get_guild_vanity_url(self):
        """"""

        return await self.http.make_request(Routes.GET_GUILD_VANITY_URL,
                                            dict(guild=self.guild_id))

    async def get_guild_widget_image(self, style: str):
        """"""

        return await self.http.make_request(Routes.GET_GUILD_WIDGET_IMAGE,
                                            dict(guild=self.guild_id),
                                            json={"style": style})
