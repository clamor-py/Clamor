from typing import Optional

import re

EMOJI_REGEX = re.compile(r'<a?(:\w+:\d+)>')


def parse_emoji(emoji: str) -> str:
    match = EMOJI_REGEX.match(emoji)
    if match:
        emoji = match.group(1)

    return emoji


def check_username(username: str) -> Optional[str]:
    if not username:
        return None

    if 2 > len(username) > 32:
        raise ValueError('Usernames must be beween 2 and 32 characters long')

    if username in ('discordtag', 'everyone', 'here'):
        raise ValueError('Restricted username')

    if any(c in ('@', '#', ':', '```') for c in username):
        raise ValueError('Usernames must not contain "@", "#", ":" or "```"')

    return username.strip()
