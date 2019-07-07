# -*- coding: utf-8 -*-

from enum import IntEnum


class ErrorCodes(IntEnum):
    #: Unknown status code.
    UNKNOWN = -1

    #: Internal server error.
    SERVER_ERROR = 0

    #: Unknown account.
    UNKNOWN_ACCOUNT = 10001
    #: Unknown application.
    UNKNOWN_APPLICATION = 10002
    #: Unknown channel.
    UNKNOWN_CHANNEL = 10003
    #: Unknown guild.
    UNKNOWN_GUILD = 10004
    #: Unknown integration.
    UNKNOWN_INTEGRATION = 10005
    #: Unknown invite.
    UNKNOWN_INVITE = 10006
    #: Unknown member.
    UNKNOWN_MEMBER = 10007
    #: Unknown message.
    UNKNOWN_MESSAGE = 10008
    #: Unknown overwrite.
    UNKNOWN_OVERWRITE = 10009
    #: Unknown provider.
    UNKNOWN_PROVIDER = 10010
    #: Unknown role.
    UNKNOWN_ROLE = 10011
    #: Unknown token.
    UNKNOWN_TOKEN = 10012
    #: Unknown user.
    UNKNOWN_USER = 10013
    #: Unknown emoji.
    UNKNOWN_EMOJI = 10014
    #: Unknown webhook.
    UNKNOWN_WEBHOOK = 10015
    #: Unknown ban.
    UNKNOWN_BAN = 10026

    #: Bots cannot use this endpoint.
    BOTS_NOT_ALLOWED = 20001
    #: Only bots can use this endpoint.
    ONLY_BOTS_ALLOWED = 20002

    #: Maximum number of guilds reached (100).
    MAX_GUILDS_LIMIT = 30001
    #: Maximum number of friends reached (1000).
    MAX_FRIENDS_LIMIT = 30002
    #: Maximum number of pinned messages reached (50).
    MAX_PINS_LIMIT = 30003
    #: Maximum number of recipients reached (10).
    MAX_USERS_PER_DM = 30004
    #: Maximum number of roles reached (250).
    MAX_ROLES_LIMIT = 30005
    #: Maximum number of reactions reached (20).
    MAX_REACTIONS_LIMIT = 30010
    #: Maximum number of guild channels reached (500).
    MAX_GUILD_CHANNELS_LIMIT = 30013

    #: Unauthorized.
    UNAUTHORIZED = 40001
    #: Missing access.
    MISSING_ACCESS = 50001
    #: Invalid account type.
    INVALID_ACCOUNT_TYPE = 50002
    #: Cannot execute action on DM channel.
    INVALID_DM_ACTION = 50003
    #: Widget disabled.
    WIDGET_DISABLED = 50004
    #: Cannot edit a message authored by another user.
    CANNOT_EDIT = 50005
    #: Cannot send an empty message.
    EMPTY_MESSAGE = 50006
    #: Cannot send messages to this user.
    CANNOT_SEND_TO_USER = 50007
    #: Cannot send messages in a voice channel.
    CANNOT_SEND_IN_VC = 50008
    #: Channel verification level is too high.
    VERIFICATION_LEVEL_TOO_HIGH = 50009
    #: OAuth2 application does not have a bot.
    OAUTH_WITHOUT_BOT = 50010
    #: OAuth2 application limit reached.
    MAX_OAUTH_APPS = 50011
    #: Invalid OAuth2 state.
    INVALID_OAUTH_STATE = 50012
    #: Missing permissions.
    MISSING_PERMISSIONS = 50013
    #: Invalid authentication token.
    INVALID_TOKEN = 50014
    #: Note is too long.
    NOTE_TOO_LONG = 50015
    #: Provided too few (at least 2) or too many (fewer than 100) messages to delete.
    INVALID_BULK_DELETE = 50016
    #: Invalid MFA level.
    INVALID_MFA_LEVEL = 50017
    #: Invalid password.
    INVALID_PASSWORD = 50018
    #: A message can only be pinned to the channel it was sent in.
    INVALID_PIN = 50019
    #: Invite code is either invalid or taken.
    INVALID_VANITY_URL = 50020
    #: Cannot execute action on a system message.
    INVALID_MESSAGE_TARGET = 50021
    #: Invalid OAuth2 access token.
    INVALID_OAUTH_TOKEN = 50025
    #: A message provided was too old to bulk delete.
    TOO_OLD_TO_BULK_DELETE = 50034
    #: Invalid form body.
    INVALID_FORM_BODY = 50035
    #: An invite was accepted to a guild the application's bot is not in.
    INVALID_INVITE_GUILD = 50036
    #: Invalid API version.
    INVALID_API_VERSION = 50041

    #: Reaction blocked.
    REACTION_BLOCKED = 90001

    #: Resource overloaded.
    RESOURCE_OVERLOADED = 130000
