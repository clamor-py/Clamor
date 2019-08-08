# -*- coding: utf-8 -*-

from .base import Base, Field, datetime, GenerativeField
from .emoji import Reaction
from .guild import Member, Role
from .snowflake import Snowflake
from .solo import Attachments, ChannelTypes, MessageTypes, \
    MessageFlags, MessageActivities, MessageApplication, MessageReference
from .user import User


__all__ = (
    "MentionUser",
    "MentionChannel",
    "Embed",
    "Message"
)


class MentionUser(User):
    """
    User class for Messages

    The :class:`clamor.models.message.Message` class's mentions attribute is an array of this
    model. This model is simply a subclass of the User model, that has a member attribute aswell.
    This member attribute is partial, and may not include all of it's information.

    Attributes
    ----------
    member : :class:`clamor.models.guild.Member`
        A partial member object for the user.
    """
    member = Field(Member)  # type: Member


class MentionChannel(Base):
    """
    Channel class for Messages

    When you mention a channel, that mention is parsed by discord and added to the message object.
    These message objects however are incomplete, and may not contain all the information you need.

    Attributes
    ----------
    id : Snowflake
        The ID of the channel.
    guild_id : Snowflake
        The ID of the guild the channel is in if applicable.
    type : :class:`clamor.models.solo.ChannelTypes`
        The type of channel.
    name : str
        The name of the channel.
    """
    id = Field(Snowflake)  # type: Snowflake
    guild_id = Field(Snowflake)  # type: Snowflake
    type = Field(ChannelTypes)  # type: ChannelTypes
    name = Field(str)  # type: str

    @property
    def guild(self):
        return self.client.cache.get("Guild", self.guild_id)

    def get_full(self):
        """
        Get full channel

        While the purpose of this model is to prevent the need to making API calls, it's not always
        enough information to preforce a certain task. In that case you may call this method which
        will retrieve the full channel that was mentioned too.

        Returns
        -------
        :class:`clamor.models.channel.Channel`
            A complete channel model.
        """
        return self.client.cache.get("Channel", self.id)


class Embed(Base):
    pass


class MessageActivity(Base):
    party_id = Field(str)
    type = Field(MessageActivities)


class Message(Base):
    id = Field(Snowflake)
    channel_id = Field(Snowflake)
    guild_id = Field(Snowflake)
    author = Field(User)
    member = Field(Member)
    content = Field(str)
    timestamp = Field(datetime)
    edited_timestamp = Field(datetime)
    tts = Field(bool)
    mention_everyone = Field(bool)
    mentions = Field(MentionUser, array=True)
    mention_roles = GenerativeField(Role)
    attachments = Field(Attachments, array=True)
    embeds = Field(Embed, array=True)
    reactions = Field(Reaction, array=True)
    nonce = Field(Snowflake)
    pinned = Field(bool)
    webhook_id = Field(Snowflake)
    types = Field(MessageTypes)
    application = Field(MessageApplication)
    message_reference = Field(MessageReference)
    activity = Field(MessageActivity)
    flags = Field(MessageFlags)

