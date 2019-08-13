# -*- coding: utf-8 -*-

from .base import Base, Field

__all__ = (
    'Emoji',
    'Reaction'
)


class Emoji(Base):

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
