import json
from functools import wraps
from typing import Union, Type, List

from clamor.models.audit_log import AuditLog, AuditLogAction
from clamor.models.base import Base
from clamor.models.channel import Channel
from clamor.models.invite import Invite
from clamor.models.message import Message
from clamor.models.snowflake import Snowflake
from clamor.models.user import User
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
