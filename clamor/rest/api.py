import json
from functools import wraps
from typing import Union, Type, List, Optional

from clamor.models.audit_log import AuditLog, AuditLogAction
from clamor.models.base import Base
from clamor.models.channel import Channel
from clamor.models.emoji import Emoji
from clamor.models.guild import Ban, Integration, Guild, GuildEmbed, Member, Role
from clamor.models.invite import Invite
from clamor.models.message import Message
from clamor.models.snowflake import Snowflake
from clamor.models.user import User
from clamor.models.voice import VoiceRegion
from clamor.utils.parse import parse_emoji
from .http import HTTP
from .routes import Routes


def optional(**kwargs) -> dict:
    """Given a dictionary, this filters out all values that are ``None``.

    Useful for routes where certain parameters are optional.
    """

    return {
        key: value for key, value in kwargs.items()
        if value is not None
    }


def cast_to(model: Type[Base]):
    def func_wrap(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            result = await func(self, *args, **kwargs)
            if isinstance(result, list):
                return [model(r, self.client) for r in result]
            if isinstance(result, dict):
                return model(result, self.client)
        return wrapper
    return func_wrap


class ClamorAPI:

    def __init__(self, client, **kwargs):
        self.client = client
        self._http = kwargs

    @property
    def http(self) -> HTTP:
        if isinstance(self._http, dict) and self.client.token is None:
            raise AttributeError("Token has not been provided yet")
        elif isinstance(self._http, dict):
            self._http = HTTP(self.client.token, **self._http)
        return self._http

    @cast_to(AuditLog)
    async def get_guild_audit_log(self,
                                  guild_id: Snowflake,
                                  user_id: Snowflake,
                                  action_type: Union[AuditLogAction, int] = None,
                                  before: Snowflake = None,
                                  limit: int = 50) -> AuditLog:
        params = optional(**{
            'user_id': user_id,
            'action_type': action_type if isinstance(action_type, int) else action_type.value,
            'before': before,
            'limit': limit,
        })

        return await self.http.make_request(Routes.GET_GUILD_AUDIT_LOG,
                                            dict(guild=guild_id),
                                            params=params)

    @cast_to(Channel)
    async def get_channel(self, channel_id: Snowflake) -> Channel:
        return await self.http.make_request(Routes.GET_CHANNEL, dict(channel=channel_id))

    @cast_to(Channel)
    async def modify_channel(self,
                             channel_id: Snowflake,
                             name: str = None,
                             position: int = None,
                             topic: str = None,
                             nsfw: bool = None,
                             rate_limit_per_user: int = None,
                             bitrate: int = None,
                             user_limit: int = None,
                             permission_overwrites: list = None,
                             parent_id: Snowflake = None,
                             reason: str = None) -> Channel:

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
                                            dict(channel=channel_id),
                                            json=params,
                                            reason=reason)

    @cast_to(Channel)
    async def delete_channel(self, channel_id: Snowflake, reason: str = None) -> Channel:
        return await self.http.make_request(Routes.DELETE_CHANNEL,
                                            dict(channel=channel_id),
                                            reason=reason)

    @cast_to(Message)
    async def get_channel_messages(self,
                                   channel_id: Snowflake,
                                   around: Snowflake = None,
                                   before: Snowflake = None,
                                   after: Snowflake = None,
                                   limit: int = 50) -> List[Message]:
        params = optional(**{
            'around': around,
            'before': before,
            'after': after,
            'limit': limit
        })

        return await self.http.make_request(Routes.GET_CHANNEL_MESSAGES,
                                            dict(channel=channel_id),
                                            params=params)

    @cast_to(Message)
    async def get_channel_message(self, channel_id: Snowflake, message_id: Snowflake) -> Message:
        return await self.http.make_request(Routes.GET_CHANNEL_MESSAGE,
                                            dict(channel=channel_id, message=message_id))

    @cast_to(Message)
    async def create_message(self,
                             channel_id: Snowflake,
                             content: str = None,
                             nonce: Snowflake = None,
                             tts: bool = False,
                             files: list = None,
                             embed: dict = None) -> Message:
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
                                                dict(channel=channel_id),
                                                files=attachments,
                                                data={'payload_json': json.dumps(payload)})

        return await self.http.make_request(Routes.CREATE_MESSAGE,
                                            dict(channel=channel_id),
                                            json=payload)

    async def create_reaction(self, channel_id: Snowflake, message_id: Snowflake, emoji: str):
        return await self.http.make_request(Routes.CREATE_REACTION,
                                            dict(channel=channel_id,
                                                 message=message_id,
                                                 emoji=parse_emoji(emoji)))

    async def delete_own_reaction(self, channel_id: Snowflake, message_id: Snowflake, emoji: str):
        return await self.http.make_request(Routes.DELETE_OWN_REACTION,
                                            dict(channel=channel_id,
                                                 message=message_id,
                                                 emoji=parse_emoji(emoji)))

    async def delete_user_reaction(self,
                                   channel_id: Snowflake,
                                   message_id: Snowflake,
                                   user_id: Snowflake,
                                   emoji: str):
        return await self.http.make_request(Routes.DELETE_USER_REACTION,
                                            dict(channel=channel_id,
                                                 message=message_id,
                                                 emoji=parse_emoji(emoji),
                                                 user=user_id))

    @cast_to(User)
    async def get_reactions(self,
                            channel_id: Snowflake,
                            message_id: Snowflake,
                            emoji: str,
                            before: Snowflake = None,
                            after: Snowflake = None,
                            limit: int = 25) -> dict:
        params = optional(**{
            'before': before,
            'after': after,
            'limit': limit
        })

        return await self.http.make_request(Routes.GET_REACTIONS,
                                            dict(channel=channel_id,
                                                 message=message_id,
                                                 emoji=parse_emoji(emoji)),
                                            params=params)

    async def delete_all_reactions(self, channel_id: Snowflake, message_id: Snowflake):
        return await self.http.make_request(Routes.DELETE_ALL_REACTIONS,
                                            dict(channel=channel_id, message=message_id))

    @cast_to(Message)
    async def edit_message(self,
                           channel_id: Snowflake,
                           message_id: Snowflake,
                           content: str = None,
                           embed: dict = None) -> Message:
        params = optional(**{
            'content': content,
            'embed': embed,
        })

        return await self.http.make_request(Routes.EDIT_MESSAGE,
                                            dict(channel=channel_id, message=message_id),
                                            json=params)

    async def delete_message(self, channel_id: Snowflake,
                             message_id: Snowflake,
                             reason: str = None):
        return await self.http.make_request(Routes.DELETE_MESSAGE,
                                            dict(channel=channel_id, message=message_id),
                                            reason=reason)

    async def bulk_delete_messages(self, channel_id: Snowflake,
                                   messages: List[Snowflake],
                                   reason: str = None):
        if 2 <= len(messages) <= 100:
            raise ValueError('Bulk delete requires a message count between 2 and 100')

        return await self.http.make_request(Routes.BULK_DELETE_MESSAGES,
                                            dict(channel=channel_id),
                                            json={'messages': messages},
                                            reason=reason)

    async def edit_channel_permissions(self,
                                       channel_id: Snowflake,
                                       overwrite_id: Snowflake,
                                       allow: int = None,
                                       deny: int = None,
                                       type: str = None,
                                       reason: str = None):
        params = optional(**{
            'allow': allow,
            'deny': deny,
            'type': type
        })

        if params.get('type', 'member') not in ('member', 'role'):
            raise ValueError('Argument for type must be either "member" or "role"')

        return await self.http.make_request(Routes.EDIT_CHANNEL_PERMISSIONS,
                                            dict(channel=channel_id, overwrite=overwrite_id),
                                            json=params,
                                            reason=reason)

    @cast_to(Invite)
    async def get_channel_invites(self, channel_id: Snowflake) -> List[Snowflake]:
        return await self.http.make_request(Routes.GET_CHANNEL_INVITES,
                                            dict(channel=channel_id))

    @cast_to(Invite)
    async def create_channel_invite(self,
                                    channel_id: Snowflake,
                                    max_age: int = 86400,
                                    max_uses: int = 0,
                                    temporary: bool = False,
                                    unique: bool = False,
                                    reason: str = None) -> dict:
        params = optional(**{
            'max_age': max_age,
            'max_uses': max_uses,
            'temporary': temporary,
            'unique': unique
        })

        return await self.http.make_request(Routes.CREATE_CHANNEL_INVITE,
                                            dict(channel=channel_id),
                                            json=params,
                                            reason=reason)

    async def delete_channel_permission(self,
                                        channel_id: Snowflake,
                                        overwrite_id: Snowflake,
                                        reason: str = None):
        return await self.http.make_request(Routes.DELETE_CHANNEL_PERMISSION,
                                            dict(channel=channel_id, overwrite=overwrite_id),
                                            reason=reason)

    async def trigger_typing_indicator(self, channel_id: Snowflake):
        return await self.http.make_request(Routes.TRIGGER_TYPING_INDICATOR,
                                            dict(channel=channel_id))

    @cast_to(Message)
    async def get_pinned_messages(self, channel_id: Snowflake) -> Message:
        return await self.http.make_request(Routes.GET_PINNED_MESSAGES,
                                            dict(channel=channel_id))

    async def add_pinned_channel_message(self, channel_id: Snowflake, message_id: Snowflake):
        return await self.http.make_request(Routes.ADD_PINNED_CHANNEL_MESSAGE,
                                            dict(channel=channel_id, message=message_id))

    async def delete_pinned_channel_message(self,
                                            channel_id: Snowflake,
                                            message_id: Snowflake,
                                            reason: str = None):
        return await self.http.make_request(Routes.DELETE_PINNED_CHANNEL_MESSAGE,
                                            dict(channel=channel_id, message=message_id),
                                            reason=reason)

    async def group_dm_add_recipient(self,
                                     channel_id: Snowflake,
                                     user_id: Snowflake,
                                     access_token: str = None,
                                     nick: str = None):
        params = optional(**{
            'access_token': access_token,
            'nick': nick
        })

        return await self.http.make_request(Routes.GROUP_DM_ADD_RECIPIENT,
                                            dict(channel=channel_id, user=user_id),
                                            json=params)

    async def group_dm_remove_recipient(self, channel_id: Snowflake, user_id: Snowflake):
        return await self.http.make_request(Routes.GROUP_DM_REMOVE_RECIPIENT,
                                            dict(channel=channel_id, user=user_id))

    @cast_to(Emoji)
    async def list_guild_emojis(self, guild_id: Snowflake) -> List[Emoji]:
        return await self.http.make_request(Routes.LIST_GUILD_EMOJIS,
                                            dict(guild=guild_id))

    @cast_to(Emoji)
    async def get_guild_emoji(self, guild_id: Snowflake, emoji_id: Snowflake) -> Emoji:
        return await self.http.make_request(Routes.GET_GUILD_EMOJI,
                                            dict(guild=guild_id, emoji=emoji_id))

    @cast_to(Emoji)
    async def create_guild_emoji(self,
                                 guild_id: Snowflake,
                                 name: str,
                                 image: str,
                                 roles: list,
                                 reason: str = None) -> Emoji:
        params = {
            'name': name,
            'image': image,
            'roles': roles
        }

        return await self.http.make_request(Routes.CREATE_GUILD_EMOJI,
                                            dict(guild=guild_id),
                                            json=params,
                                            reason=reason)

    @cast_to(Emoji)
    async def modify_guild_emoji(self,
                                 guild_id: Snowflake,
                                 emoji_id: Snowflake,
                                 name: str = None,
                                 roles: list = None,
                                 reason: str = None) -> Emoji:
        params = optional(**{
            'name': name,
            'roles': roles
        })

        return await self.http.make_request(Routes.MODIFY_GUILD_EMOJI,
                                            dict(guild=guild_id, emoji=emoji_id),
                                            json=params,
                                            reason=reason)

    async def delete_guild_emoji(self,
                                 guild_id: Snowflake,
                                 emoji_id: Snowflake,
                                 reason: str = None):
        return await self.http.make_request(Routes.DELETE_GUILD_EMOJI,
                                            dict(guild=guild_id, emoji=emoji_id),
                                            reason=reason)

    async def get_gateway(self) -> dict:
        return await self.http.make_request(Routes.GET_GATEWAY)

    async def get_gateway_bot(self) -> dict:
        return await self.http.make_request(Routes.GET_GATEWAY_BOT)

    @cast_to(Guild)
    async def create_guild(self,
                           name: str,
                           region: str,
                           icon: str,
                           verification_level: int,
                           default_message_notifications: int,
                           explicit_content_filter: int,
                           roles: list,
                           channels: list) -> Guild:
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

    @cast_to(Guild)
    async def get_guild(self, guild_id: Snowflake) -> Guild:
        return await self.http.make_request(Routes.GET_GUILD,
                                            dict(guild=guild_id))

    @cast_to(Guild)
    async def modify_guild(self,
                           guild_id: Snowflake,
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
                           reason: str = None) -> Guild:
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
                                            dict(guild=guild_id),
                                            json=params,
                                            reason=reason)

    async def delete_guild(self, guild_id: Snowflake):
        return await self.http.make_request(Routes.DELETE_GUILD,
                                            dict(guild=guild_id))

    @cast_to(Channel)
    async def get_guild_channels(self, guild_id: Snowflake) -> list:
        return await self.http.make_request(Routes.GET_GUILD_CHANNELS,
                                            dict(guild=guild_id))

    @cast_to(Channel)
    async def create_guild_channel(self,
                                   guild_id: Snowflake,
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
                                            dict(guild=guild_id),
                                            json=params,
                                            reason=reason)

    async def modify_guild_channel_positions(self, guild_id: Snowflake, channels: List[dict]):
        return await self.http.make_request(Routes.MODIFY_GUILD_CHANNEL_POSITIONS,
                                            dict(guild=guild_id),
                                            json=channels)

    @cast_to(Member)
    async def get_guild_member(self, guild_id: Snowflake, user_id: Snowflake) -> Member:
        return await self.http.make_request(Routes.GET_GUILD_MEMBER,
                                            dict(guild=guild_id, member=user_id))

    @cast_to(Member)
    async def list_guild_members(self,
                                 guild_id: Snowflake,
                                 limit: int = None,
                                 after: Snowflake = None) -> List[Member]:
        params = optional(**{
            "limit": limit,
            "after": after
        })

        return await self.http.make_request(Routes.LIST_GUILD_MEMBERS,
                                            dict(guild=guild_id),
                                            json=params)

    @cast_to(Member)
    async def add_guild_member(self,
                               guild_id: Snowflake,
                               user_id: Snowflake,
                               access_token: str,
                               nick: str = None,
                               roles: list = None,
                               mute: bool = None,
                               deaf: bool = None) -> Member:
        params = optional(**{
            "access_token": access_token,
            "nick": nick,
            "roles": roles,
            "mute": mute,
            "deaf": deaf
        })

        return await self.http.make_request(Routes.ADD_GUILD_MEMBER,
                                            dict(guild=guild_id, member=user_id),
                                            json=params)

    async def modify_guild_member(self,
                                  guild_id: Snowflake,
                                  user_id: Snowflake,
                                  nick: str = None,
                                  roles: list = None,
                                  mute: bool = None,
                                  deaf: bool = None,
                                  channel_id: Snowflake = None,
                                  reason: str = None):
        params = optional(**{
            "nick": nick,
            "roles": roles,
            "mute": mute,
            "deaf": deaf,
            "channel_id": channel_id
        })

        return await self.http.make_request(Routes.MODIFY_GUILD_MEMBER,
                                            dict(guild=guild_id, member=user_id),
                                            json=params,
                                            reason=reason)

    async def modify_current_user_nick(self, guild_id: Snowflake,
                                       nick: str, reason: str = None) -> str:
        params = {
            "nick": nick
        }

        resp = await self.http.make_request(Routes.MODIFY_CURRENT_USER_NICK,
                                            dict(guild=guild_id),
                                            json=params,
                                            reason=reason)
        return resp['nick']

    async def add_guild_member_role(self,
                                    guild_id: Snowflake,
                                    user_id: Snowflake,
                                    role_id: Snowflake,
                                    reason: str = None):
        return await self.http.make_request(Routes.ADD_GUILD_MEMBER_ROLE,
                                            dict(guild=guild_id, member=user_id, role=role_id),
                                            reason=reason)

    async def remove_guild_member_role(self,
                                       guild_id: Snowflake,
                                       user_id: Snowflake,
                                       role_id: Snowflake,
                                       reason: str = None):
        return await self.http.make_request(Routes.REMOVE_GUILD_MEMBER_ROLE,
                                            dict(guild=guild_id, member=user_id, role=role_id),
                                            reason=reason)

    async def remove_guild_member(self, guild_id: Snowflake,
                                  user_id: Snowflake, reason: str = None):
        return await self.http.make_request(Routes.REMOVE_GUILD_MEMBER,
                                            dict(guild=guild_id, member=user_id),
                                            reason=reason)

    @cast_to(Ban)
    async def get_guild_bans(self, guild_id: Snowflake) -> List[Ban]:
        return await self.http.make_request(Routes.GET_GUILD_BANS,
                                            dict(guild=guild_id))

    @cast_to(Ban)
    async def get_guild_ban(self, guild_id: Snowflake, user_id: Snowflake) -> Ban:
        return await self.http.make_request(Routes.GET_GUILD_BAN,
                                            dict(guild=guild_id, user=user_id))

    async def create_guild_ban(self,
                               guild_id: Snowflake,
                               user_id: Snowflake,
                               delete_message_days: int = None,
                               reason: str = None):
        params = optional(**{
            "delete_message_days": delete_message_days,
            "reason": reason
        })

        return await self.http.make_request(Routes.CREATE_GUILD_BAN,
                                            dict(guild=guild_id, user=user_id),
                                            json=params)

    async def remove_guild_ban(self, guild_id: Snowflake, user_id: Snowflake, reason: str = None):
        return await self.http.make_request(Routes.REMOVE_GUILD_BAN,
                                            dict(guild=guild_id, user=user_id),
                                            reason=reason)

    @cast_to(Role)
    async def get_guild_roles(self, guild_id: Snowflake) -> Role:
        return await self.http.make_request(Routes.GET_GUILD_ROLES,
                                            dict(guild=guild_id))

    @cast_to(Role)
    async def create_guild_role(self,
                                guild_id: Snowflake,
                                name: str = None,
                                permissions: int = None,
                                color: int = None,
                                hoist: bool = None,
                                mentionable: bool = None,
                                reason: str = None) -> Role:
        params = optional(**{
            "name": name,
            "permissions": permissions,
            "color": color,
            "hoist": hoist,
            "mentionable": mentionable
        })

        return await self.http.make_request(Routes.CREATE_GUILD_ROLE,
                                            dict(guild=guild_id),
                                            json=params,
                                            reason=reason)

    @cast_to(Role)
    async def modify_guild_role_positions(self, guild_id: Snowflake,
                                          roles: List[dict], reason: str = None) -> List[Role]:
        return await self.http.make_request(Routes.MODIFY_GUILD_ROLE_POSITIONS,
                                            dict(guild=guild_id),
                                            json=roles,
                                            reason=reason)

    @cast_to(Role)
    async def modify_guild_role(self,
                                guild_id: Snowflake,
                                role_id: Snowflake,
                                name: str = None,
                                permissions: int = None,
                                color: int = None,
                                hoist: bool = None,
                                mentionable: bool = None,
                                reason: str = None) -> Role:
        params = optional(**{
            "name": name,
            "permissions": permissions,
            "color": color,
            "hoist": hoist,
            "mentionable": mentionable
        })

        return await self.http.make_request(Routes.MODIFY_GUILD_ROLE,
                                            dict(guild=guild_id, role=role_id),
                                            json=params,
                                            reason=reason)

    async def delete_guild_role(self, guild_id: Snowflake, role_id: Snowflake, reason: str = None):
        return await self.http.make_request(Routes.DELETE_GUILD_ROLE,
                                            dict(guild=guild_id, role=role_id),
                                            reason=reason)

    async def get_guild_prune_count(self, guild_id: Snowflake, days: int = None) -> int:
        params = optional(**{"days": days})
        resp = await self.http.make_request(Routes.GET_GUILD_PRUNE_COUNT,
                                            dict(guild=guild_id),
                                            json=params)
        return resp['pruned']

    async def begin_guild_prune(self,
                                guild_id: Snowflake,
                                days: int = None,
                                compute_prune_count: bool = None) -> Optional[int]:
        params = {
            "days": days,
            "compute_prune_count": compute_prune_count
        }

        resp = await self.http.make_request(Routes.BEGIN_GUILD_PRUNE,
                                            dict(guild=guild_id),
                                            json=params)
        return resp['pruned']

    @cast_to(VoiceRegion)
    async def get_guild_voice_regions(self, guild_id: Snowflake) -> List[VoiceRegion]:
        return await self.http.make_request(Routes.GET_GUILD_VOICE_REGIONS,
                                            dict(guild=guild_id))

    @cast_to(Invite)
    async def get_guild_invites(self, guild_id: Snowflake) -> List[Invite]:
        return await self.http.make_request(Routes.GET_GUILD_INVITES,
                                            dict(guild=guild_id))

    @cast_to(Integration)
    async def get_guild_integrations(self, guild_id: Snowflake) -> List[Integration]:
        return await self.http.make_request(Routes.GET_GUILD_INTEGRATIONS,
                                            dict(guild=guild_id))

    async def create_guild_integration(self,
                                       guild_id: Snowflake,
                                       int_type: str,
                                       int_id: Snowflake,
                                       reason: str = None):
        params = {
            "type": int_type,
            "id": int_id
        }

        return await self.http.make_request(Routes.CREATE_GUILD_INTEGRATION,
                                            dict(guild=guild_id),
                                            json=params,
                                            reason=reason)

    async def modify_guild_integration(self,
                                       guild_id: Snowflake,
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
                                            dict(guild=guild_id, integration=integration_id),
                                            json=params,
                                            reason=reason)

    async def delete_guild_integration(self, guild_id: Snowflake,
                                       integration_id: Snowflake, reason: str = None):
        return await self.http.make_request(Routes.DELETE_GUILD_INTEGRATION,
                                            dict(guild=guild_id, integration=integration_id),
                                            reason=reason)

    async def sync_guild_integration(self, guild_id: Snowflake, integration_id: Snowflake):
        return await self.http.make_request(Routes.SYNC_GUILD_INTEGRATION,
                                            dict(guild=guild_id, integration=integration_id))

    @cast_to(GuildEmbed)
    async def get_guild_embed(self, guild_id: Snowflake) -> GuildEmbed:
        return await self.http.make_request(Routes.GET_GUILD_EMBED,
                                            dict(guild=guild_id))

    @cast_to(GuildEmbed)
    async def modify_guild_embed(self,
                                 guild_id: Snowflake,
                                 enabled: bool,
                                 channel_id: Snowflake,
                                 reason: str = None) -> GuildEmbed:
        params = {
            "enabled": enabled,
            "channel_id": channel_id
        }

        return await self.http.make_request(Routes.MODIFY_GUILD_EMBED,
                                            dict(guild=guild_id),
                                            json=params,
                                            reason=reason)

    async def get_guild_vanity_url(self, guild_id: Snowflake) -> bytes:
        return await self.http.make_request(Routes.GET_GUILD_VANITY_URL,
                                            dict(guild=guild_id))

    @cast_to(Invite)
    async def get_invite(self, invite_code: str, with_counts: bool = False) -> Invite:
        return await self.http.make_request(Routes.GET_INVITE,
                                            dict(invite=invite_code),
                                            params=optional(**{'with_counts': with_counts}))

    @cast_to(Invite)
    async def delete_invite(self, invite_code: str, reason: str = None) -> Invite:
        return await self.http.make_request(Routes.DELETE_INVITE,
                                            dict(invite=invite_code),
                                            reason=reason)

    async def get_current_application_info(self) -> dict:
        return await self.http.make_request(Routes.GET_CURRENT_APPLICATION_INFO)


