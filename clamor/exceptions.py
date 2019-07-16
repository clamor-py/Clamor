# -*- coding: utf-8 -*-

import logging
from enum import IntEnum
from itertools import starmap
from typing import Optional, Union

from asks.response_objects import Response

__all__ = (
    'JSONErrorCodes',
    'ClamorError',
    'RequestFailed',
    'Unauthorized',
    'Forbidden',
    'NotFound',
    'Hierarchied',
)

logger = logging.getLogger(__name__)


class JSONErrorCodes(IntEnum):
    """Enum that holds the REST API JSON error codes."""

    #: Unknown opcode.
    UNKNOWN = 0

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

    @property
    def name(self):
        return ' '.join(part.capitalize() for part in self._name_.split('_'))


class ClamorError(Exception):
    """Base exception class for any exceptions raised by this library.

    Therefore, catching :class:`~clamor.exceptions.ClamorException` may
    be used to handle **any** exceptions raised by this library.
    """
    pass


class RequestFailed(ClamorError):
    """Exception that will be raised for failed HTTP requests to the REST API.

    This extracts important components from the failed response
    and presents them to the user in a readable way.

    Parameters
    ----------
    response : :class:`Response<asks:asks.response_objects.Response>`
        The response for the failed request.
    data : Optional[dict, str]
        The parsed response body.

    Attributes
    ----------
    response : :class:`Response<asks:asks.response_objects.Response>`
        The response for the failed request.
    status_code : int
        The HTTP status code for the request.
    bucket : Tuple[str, str]
        A tuple containing request method and URL for debugging purposes.
    error : :class:`~clamor.exceptions.JSONErrorCodes`
        The JSON error code returned by the API.
    errors : dict
        The unflattened JSON error dict.
    message : str
        The error message returned by the API.
    """

    def __init__(self, response: Response, data: Optional[Union[dict, str]]):
        self.response = response
        self.status_code = response.status_code
        self.bucket = (self.response.method.upper(), self.response.url)

        self.error = None
        self.errors = None
        self.message = None

        failed = 'Request to {0.bucket} failed with {0.error.value} {0.error.name}: {0.message}'

        # Try to get any useful data from the dict
        error_code = data.get('code', 0)
        if isinstance(data, dict):
            try:
                self.error = JSONErrorCodes(error_code)
            except ValueError:
                logger.warning('Unknown error code %d', error_code)
                self.error = JSONErrorCodes.UNKNOWN

            self.errors = data.get('errors', {})
            self.message = data.get('message', '')

        else:
            self.message = data
            self.status_code = JSONErrorCodes.UNKNOWN

        if self.errors:
            errors = self._flatten_errors(self.errors)
            error_list = '\n'.join(
                starmap('code: {1[0][code]}, message: {1[0][message]}'.format, errors.items()))
            failed += '\nAdditional errors: {}'.format(error_list)

        super().__init__(failed.format(self))

    def _flatten_errors(self, errors: dict, key: str = '') -> dict:
        messages = []

        for k, v in errors.items():
            if k == 'message':
                continue

            new_key = k
            if key:
                if key.isdigit():
                    new_key = '{}.{}'.format(key, k)
                else:
                    new_key = '{}.[{}]'.format(key, k)

            if isinstance(v, dict):
                try:
                    _errors = v['_errors']
                except KeyError:
                    messages.extend(self._flatten_errors(v, new_key).items())
                else:
                    messages.append(
                        (new_key, ' '.join(error.get('message', '') for error in _errors)))
            else:
                messages.append((new_key, v))

        return dict(messages)


class Unauthorized(RequestFailed):
    """Raised for HTTP status code ``401: Unauthorized``.

    Essentially denoting that the user's token is wrong.
    """
    pass


class Forbidden(RequestFailed):
    """Raised for HTTP status code ``403: Forbidden``.

    Essentially denoting that your token is not permitted
    to access a specific resource.
    """
    pass


class NotFound(RequestFailed):
    """Raised for HTTP status code ``404: Not Found``.

    Essentially denoting that the specified resource
    does not exist.
    """
    pass


class Hierarchied(ClamorError):
    """Raised when an action fails due to hierarchy.

    This error is occurring when your bot tries to
    edit someone with a higher role than their own
    regardless of permissions.

    Common examples:
    ----------------

    - The bot is trying to edit the guild owner.

    - The bot is trying to kick/ban members with
      a higher role than their own.
      *Even occurs if the bot has ``Kick/Ban Members``.*
    """
    pass
