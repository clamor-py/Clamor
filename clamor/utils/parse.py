import re

EMOJI_REGEX = re.compile(r'<a?(:\w+:\d+)>')


def parse_emoji(emoji: str) -> str:
    match = EMOJI_REGEX.match(emoji)
    if match:
        emoji = match.group(1)

    return emoji
