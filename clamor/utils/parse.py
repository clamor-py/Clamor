# -*- coding: utf-8 -*-

from typing import List, Optional

import re

__all__ = (
    'CHANNEL_REGEX',
    'check_username',
    'check_webhook_name',
    'CODEBLOCK_REGEX',
    'EMOJI_REGEX',
    'parse_react_emoji',
    'ROLE_REGEX',
    'strip_codeblocks',
    'USER_REGEX',
)

#: A regex to match channel mentions.
CHANNEL_REGEX = re.compile(r'<#(\d+)>')
#: A regex to match code blocks.
CODEBLOCK_REGEX = re.compile(r'(?:```([A-Za-z0-9\-.]*)\n)?(.+?)(?:```)?', re.S)
#: A regex to match custom emojis.
EMOJI_REGEX = re.compile(r'<a?(:\w+:\d+)>')
#: A regex to match role mentions.
ROLE_REGEX = re.compile(r'<@&(\d+)>')
#: A regex to match user mentions.
USER_REGEX = re.compile(r'<@!?(\d+)>')


def parse_react_emoji(emoji: str) -> str:
    """Parses an emoji for the ``Reaction Add`` endpoint.

    Since custom emojis must be in a ``:name:id`` format
    instead of the regular ``<:name:id>`` for messages,
    this ensures an emoji is in the correct format.

    Parameters
    ----------
    emoji : str
        The emoji to check.

    Returns
    -------
    str
        The correct emoji format for reacting.
    """

    match = EMOJI_REGEX.match(emoji)
    if match:
        emoji = match.group(1)

    return emoji


def check_username(username: str) -> Optional[str]:
    """Validates a username according to Discord's guidelines.

    Parameters
    ----------
    username : str
        The username to check.

    Returns
    -------
    str, optional
        The sanitized username.

    Raises
    ------
    ValueError
        Raised in case the username violates Discord's policy.
    """

    if not username:
        return None

    if 2 > len(username) > 32:
        raise ValueError('Usernames must be beween 2 and 32 characters long')

    if username in ('discordtag', 'everyone', 'here'):
        raise ValueError('Restricted username')

    if any(c in ('@', '#', ':', '```') for c in username):
        raise ValueError('Usernames must not contain "@", "#", ":" or "```"')

    return username.strip()


def check_webhook_name(name: str) -> Optional[str]:
    """Validates a Webhook name according to Discord's guidelines.

        Parameters
        ----------
        name : str
            The name to check.

        Returns
        -------
        str, optional
            The sanitized name.

        Raises
        ------
        ValueError
            Raised in case the name violates Discord's policy.
        """

    if 2 > len(name) > 32:
        raise ValueError('Name must be between 2 and 32 characters long')

    return name.strip()


def strip_codeblocks(text: str) -> List[Optional[str]]:
    """Given a text, this strips all code block characters away.

    In case a multiline codeblock was used, this returns a list
    where the first element is the language and the second one
    the enclosed text.

    For single-line codeblocks (``I'm a codeblock``), the first
    element is always ``None``.
    """

    match = CODEBLOCK_REGEX.search(text)
    if not match:
        return [None, text.strip('` \n')]

    return [match.group(1), match.group(2)]
