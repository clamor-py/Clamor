# -*- coding: utf-8 -*-

from enum import Enum

from .base import Base, Field, Flags
from .snowflake import Snowflake


__all__ = (
    "Attachments",
    "MessageTypes",
    "PremiumType",
    "UserFlags",
    "Visibility",
    "ChannelTypes",
    "MessageFlags",
    "MessageActivities",
    "MessageApplication",
    "MessageReference",
    "TargetUserType"
)


class Attachments(Base):
    """
    Message attachment model

    All files attached to messages will use this class to represent them. Discord never actually
    downloads the files, but instead attachments are just links to the actual files. Images are
    the only files that have the height and width attributes.

    Attributes
    ----------
    id : Snowflake
        The ID of the attachment
    filename : str
        The name of the file
    size : int
        The size of the file in bytes
    url : str
        A url that contains the original file
    proxy_url : str
        A proxy version of the url
    height : int
        The height of the image (image only)
    width : int
        The width of the image (image only)
    """
    id = Field(Snowflake)
    filename = Field(str)
    size = Field(int)
    url = Field(str)
    proxy_url = Field(str)
    height = Field(int)
    width = Field(int)


class MessageTypes(Enum):
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    GUILD_MEMBER_JOIN = 7
    USER_PREMIUM_GUILD_SUBSCRIPTION = 8
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1 = 9
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2 = 10
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12


class Visibility(Enum):
    INVISIBLE = 0
    VISIBLE = 1


class UserFlags(Flags):
    DISCORD_EMPLOYEE = 1
    DISCORD_PARTNER = 2
    HYPESQUAD_EVENTS = 4
    BUG_HUNTER = 8
    HOUSE_BRAVERY = 16
    HOUSE_BRILLIANCE = 32
    HOUSE_BALANCE = 64
    EARLY_SUPPORTER = 128
    TEAM_USER = 256


class PremiumType(Enum):
    DEFAULT = 0
    NITRO_CLASSIC = 1
    NITRO = 2


class ChannelTypes(Enum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6


class MessageFlags(Flags):
    CROSSPOSTED = 1
    IS_CROSSPOST = 2
    SUPPRESS_EMBEDS = 4


class MessageActivities(Enum):
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5


class MessageApplication(Base):
    id = Field(Snowflake)
    cover_image = Field(str)
    description = Field(str)
    icon = Field(str)
    name = Field(str)


class MessageReference(Base):
    message_id = Field(Snowflake)
    channel_id = Field(Snowflake)
    guild_id = Field(Snowflake)

    @property
    def message(self):
        return self._client.cache.get("Message", self.channel_id, self.message_id)

    @property
    def channel(self):
        return self._client.cache.get("Channel", self.channel_id)

    @property
    def guild(self):
        return self._client.cache.get("Guild", self.guild_id)


class TargetUserType(Enum):
    STREAM = 1
