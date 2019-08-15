# -*- coding: utf-8 -*-

from .base import Base, Field, GenerativeField
from .snowflake import Snowflake
from .user import User

__all__ = (
    'Emoji',
    'Reaction'
)


class Emoji(Base):
    """
    Discord emoji

    Discord emojis are interesting because their the only discord model where the ID is optional.
    If an emoji is just a normal unicode emoji, it won't have an ID, and instead you can find the
    emoji in the name.

    Attributes
    ----------
    id : Snowflake
        The emoji ID if applicable
    name : str
        The name of the emoji or the emoji itself
    roles : GenerativeField
        The roles that can use this emoji
    user : :class:`clamor.models.user.User`
        The user that created this emoji
    require_colons : bool
        Whether this emoji uses colons (is a guild emoji or not)
    managed : bool
        Whether this emoji is managed (same as require_colons?)
    animated : bool
        Whether this emoji is animated or not
    """
    id = Field(Snowflake)
    name = Field(str)
    roles = GenerativeField('Role')
    user = Field(User)
    require_colons = Field(bool)
    managed = Field(bool)
    animated = Field(bool)

    @property
    def string(self):
        if self.id:
            return "{}:{}".format(self.name, self.id)
        return self.name


class Reaction(Base):
    """
    Reaction to a message

    The reaction model only represents a single emoji reacted to a message.

    Attributes
    ----------
    count : int
        The amount of reactions for this emoji
    me : bool
        Whether we reacted to the message
    emoji : Emoji

    """
    count = Field(int)
    me = Field(bool)
    emoji = Field(Emoji)
