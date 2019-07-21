# -*- coding: utf-8 -*-

from enum import Enum
from typing import NewType, Tuple

__all__ = (
    'Method',
    'Routes',
    'APIRoute',
)


class Method(Enum):
    """Enum denoting valid HTTP methods for requests to the Discord API."""

    #: GET method.
    GET = 'GET'
    #: POST method.
    POST = 'POST'
    #: PUT method.
    PUT = 'PUT'
    #: PATCH method.
    PATCH = 'PATCH'
    #: DELETE method.
    DELETE = 'DELETE'


class Routes:
    """This acts as a namespace for API routes.

    Routes are denoted as tuples where the first index
    is a :class:`~clamor.rest.routes.Method` member and
    the second index a string denoting the actual endpoint.
    """

    # Guild
    GUILD = '/guilds'
    CREATE_GUILD = (Method.POST, GUILD)
    GET_GUILD = (Method.GET, GUILD + '/{guild}')
    MODIFY_GUILD = (Method.PATCH, GUILD + '/{guild}')
    DELETE_GUILD = (Method.DELETE, GUILD + '/{guild}')
    GET_GUILD_CHANNELS = (Method.GET, GUILD + '/{guild}/channels')
    CREATE_GUILD_CHANNEL = (Method.POST, GUILD + '/{guild}/channels')
    MODIFY_GUILD_CHANNEL_POSITIONS = (Method.PATCH, '/{guild}/channels')
    GET_GUILD_MEMBER = (Method.GET, GUILD + '/{guild}/members/{member}')
    LIST_GUILD_MEMBERS = (Method.GET, GUILD + '/{guild}/members')
    ADD_GUILD_MEMBER = (Method.PUT, GUILD + '/{guild}/members/{member}')
    MODIFY_GUILD_MEMBER = (Method.PATCH, GUILD + '/{guild}/members/{member}')
    MODIFY_CURRENT_USER_NICK = (Method.PATCH, GUILD + '/{guild}/members/@me/nick')
    ADD_GUILD_MEMBER_ROLE = (Method.PUT, GUILD + '/{guild}/members/{member}/roles/{role}')
    REMOVE_GUILD_MEMBER_ROLE = (Method.DELETE, GUILD + '/{guild}/members/{member}/roles/{role}')
    REMOVE_GUILD_MEMBER = (Method.DELETE, GUILD + '/{guild}/members/{member}')
    GET_GUILD_BANS = (Method.GET, GUILD + '/{guild}/bans')
    GET_GUILD_BAN = (Method.GET, GUILD + '/{guild}/bans/{user}')
    CREATE_GUILD_BAN = (Method.PUT, GUILD + '/{guild}/bans/{user}')
    REMOVE_GUILD_BAN = (Method.DELETE, GUILD + '/{guild}/bans/{user}')
    GET_GUILD_ROLES = (Method.GET, GUILD + '/{guild}/roles')
    CREATE_GUILD_ROLE = (Method.POST, GUILD + '/{guild}/roles')
    MODIFY_GUILD_ROLE_POSITIONS = (Method.PATCH, GUILD + '/{guild}/roles')
    MODIFY_GUILD_ROLE = (Method.PATCH, GUILD + '/{guild}/roles/{role}')
    DELETE_GUILD_ROLE = (Method.DELETE, GUILD + '/{guild}/roles/{role}')
    GET_GUILD_PRUNE_COUNT = (Method.GET, GUILD + '/{guild}/prune')
    BEGIN_GUILD_PRUNE = (Method.POST, GUILD + '/{guild}/prune')
    GET_GUILD_VOICE_REGIONS = (Method.GET, GUILD + '/{guild}/regions')
    GET_GUILD_INVITES = (Method.GET, GUILD + '/{guild}/invites')
    GET_GUILD_INTEGRATIONS = (Method.GET, GUILD + '/{guild}/integrations')
    CREATE_GUILD_INTEGRATION = (Method.POST, GUILD + '/{guild}/integrations')
    MODIFY_GUILD_INTEGRATION = (Method.PATCH, GUILD + '/{guild}/integrations/{integration}')
    DELETE_GUILD_INTEGRATION = (Method.DELETE, GUILD + '/{guild}/integrations/{integration}')
    SYNC_GUILD_INTEGRATION = (Method.POST, GUILD + '/{guild}/integrations/{integration}/sync')
    GET_GUILD_EMBED = (Method.GET, GUILD + '/{guild}/embed')
    MODIFY_GUILD_EMBED = (Method.PATCH, GUILD + '/{guild}/embed')
    GET_GUILD_VANITY_URL = (Method.GET, GUILD + '/{guild}/vanity-url')
    GET_GUILD_WIDGET_IMAGE = (Method.GET, GUILD + '/{guild}/widget.png')

    # Channel
    CHANNEL = '/channels/{channel}'
    GET_CHANNEL = (Method.GET, CHANNEL)
    MODIFY_CHANNEL = (Method.PATCH, CHANNEL)
    DELETE_CHANNEL = (Method.DELETE, CHANNEL)
    GET_CHANNEL_MESSAGES = (Method.GET, CHANNEL + '/messages')
    GET_CHANNEL_MESSAGE = (Method.GET, CHANNEL + '/messages/{message}')
    CREATE_MESSAGE = (Method.POST, CHANNEL + '/messages')
    CREATE_REACTION = (Method.PUT, CHANNEL + '/messages/{message}/reactions/{emoji}/@me')
    DELETE_OWN_REACTION = (Method.DELETE, CHANNEL + '/messages/{message}/reactions/{emoji}/@me')
    DELETE_USER_REACTION = (Method.DELETE, CHANNEL + '/messages/{message}/reactions/{emoji}/{user}')  # noqa
    GET_REACTIONS = (Method.GET, CHANNEL + '/messages/{message}/reactions/{emoji}')
    DELETE_ALL_REACTIONS = (Method.DELETE, CHANNEL + '/messages/{message}/reactions')
    EDIT_MESSAGE = (Method.PATCH, CHANNEL + '/messages/{message}')
    DELETE_MESSAGE = (Method.DELETE, CHANNEL + '/messages/{message}')
    BULK_DELETE_MESSAGES = (Method.POST, CHANNEL + '/messages/bulk-delete')
    EDIT_CHANNEL_PERMISSIONS = (Method.PUT, CHANNEL + '/permissions/{permission}')
    GET_CHANNEL_INVITES = (Method.GET, CHANNEL + '/invites')
    CREATE_CHANNEL_INVITE = (Method.POST, CHANNEL + '/invites')
    DELETE_CHANNEL_PERMISSION = (Method.DELETE, CHANNEL + '/permissions/{permission}')
    TRIGGER_TYPING_INDICATOR = (Method.POST, CHANNEL + '/typing')
    GET_PINNED_MESSAGES = (Method.GET, CHANNEL + '/pins')
    ADD_PINNED_CHANNEL_MESSAGE = (Method.PUT, CHANNEL + '/pins/{message}')
    DELETE_PINNED_CHANNEL_MESSAGE = (Method.DELETE, CHANNEL + '/pins/{message}')
    GROUP_DM_ADD_RECIPIENT = (Method.PUT, CHANNEL + '/recipients/{user}')
    GROUP_DM_REMOVE_RECIPIENT = (Method.DELETE, CHANNEL + '/recipients/{user}')

    # Audit Log
    GET_GUILD_AUDIT_LOG = (Method.GET, GUILD + '/{guild}/audit-logs')

    # Emoji
    EMOJI = '/emojis'  # noqa
    LIST_GUILD_EMOJIS = (Method.GET, GUILD + '/{guild}' + EMOJI)
    GET_GUILD_EMOJI = (Method.GET, GUILD + '/{guild}' + EMOJI + '/{emoji}')
    CREATE_GUILD_EMOJI = (Method.POST, GUILD + '/{guild}' + EMOJI)
    MODIFY_GUILD_EMOJI = (Method.PATCH, GUILD + '/{guild}' + EMOJI + '/{emoji}')
    DELETE_GUILD_EMOJI = (Method.DELETE, GUILD + '/{guild}' + EMOJI + '/{emoji}')

    # Invite
    INVITE = '/invites/{invite}'
    GET_INVITE = (Method.GET, INVITE)
    DELETE_INVITE = (Method.DELETE, INVITE)

    # User
    USER = '/users'
    GET_CURRENT_USER = (Method.GET, USER + '/@me')
    GET_USER = (Method.GET, USER + '/{user}')
    MODIFY_CURRENT_USER = (Method.PATCH, USER + '/@me')
    GET_CURRENT_USER_GUILDS = (Method.GET, USER + '/@me/guilds')
    LEAVE_GUILD = (Method.DELETE, USER + '/@me/guilds/{guild}')
    GET_USER_DMS = (Method.GET, USER + '/@me/channels')
    CREATE_DM = (Method.POST, USER + '/@me/channels')
    CREATE_GROUP_DM = (Method.POST, USER + '/@me/channels')
    GET_USER_CONNECTIONS = (Method.GET, USER + '/@me/connections')

    # Voice
    VOICE = '/voice/regions'
    LIST_VOICE_REGIONS = (Method.GET, VOICE)

    # Webhook
    WEBHOOK = '/webhooks'
    CREATE_WEBHOOK = (Method.POST, CHANNEL + WEBHOOK)
    GET_CHANNEL_WEBHOOKS = (Method.GET, CHANNEL + WEBHOOK)
    GET_GUILD_WEBHOOKS = (Method.GET, GUILD + '/{guild}' + WEBHOOK)
    GET_WEBHOOK = (Method.GET, WEBHOOK + '/{webhook}')  # noqa
    GET_WEBHOOK_WITH_TOKEN = (Method.GET, WEBHOOK + '/{webhook}/{token}')
    MODIFY_WEBHOOK = (Method.PATCH, WEBHOOK + '/{webhook}')
    MODIFY_WEBHOOK_WITH_TOKEN = (Method.PATCH, WEBHOOK + '/{webhook}/{token}')
    DELETE_WEBHOOK = (Method.DELETE, WEBHOOK + '/{webhook}')
    DELETE_WEBHOOK_WITH_TOKEN = (Method.DELETE, WEBHOOK + '/{webhook}/{token}')
    EXECUTE_WEBHOOK = (Method.POST, WEBHOOK + '/{webhook}/{token}')
    EXECUTE_SLACK_COMPATIBLE_WEBHOOK = (Method.POST, WEBHOOK + '/{webhook}/{token}/slack')
    EXECUTE_GITHUB_COMPATIBLE_WEBHOOK = (Method.POST, WEBHOOK + '/{webhook}/{token}/github')

    # OAuth2
    OAUTH = '/oauth2/applications'
    GET_CURRENT_APPLICATION_INFO = (Method.GET, OAUTH + '/@me')

    # Gateway
    GATEWAY = '/gateway'
    GET_GATEWAY = (Method.GET, GATEWAY)
    GET_GATEWAY_BOT = (Method.GET, GATEWAY + '/bot')


#: A type to denote Discord API routes.
APIRoute = NewType('Route', Tuple[Method, str])
