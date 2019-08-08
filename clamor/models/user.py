# -*- coding: utf-8 -*-

from enum import Enum

from .base import Base, Field, Flags
from .snowflake import Snowflake

__all__ = (
    'AVATAR_URL',
    'DEFAULT_AVATAR_URL',
    'Connection',
    'PremiumType',
    'User',
    'UserFlags',
    'Visibility',
)

DEFAULT_AVATAR_URL = 'https://cdn.discordapp.com/embed/avatars/{}.png'
AVATAR_URL = 'https://cdn.discordapp.com/avatars/{}/{}.{}?size={}'


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


class User(Base):
    """A user on Discord.

    This model represents normal discord users, not users from Oauth. While you can't send messages
    to users directly, you can create a channel with them by using the :meth:`dm` method.

    Attributes
    ----------
    id : :class:`clamor.models.snowflake.Snowflake`
        The user's discord ID.
    username : str
        The user's name without the :attr:`discriminator`.
    discriminator : str
        The user's discriminator.
    avatar : str
        The user's profile picture's hash.
    bot : bool
        Whether the user is a bot account or not.
    mfa_enabled : bool
        Whether the user has Two-factor authentication enabled.
    locale : str
        The user's locale setting.
    flags : :class:`clamor.models.user.UserFlags`
        Certain user attributes that are displayed on the user's profile as icons.
    premium_type : :class:`clamor.model.user.PremiumType`
        Information on the user's paid subscription status.
    avatar_url : str
        Shorthand for :func:`clamor.model.user.User.create_avatar_url` without arguments.
    creation_date : datetime.datetime
        When the user registered with discord (shorthand for user.id.timestamp).
    mention : str
        A string containing the user as a mention.
    name : str
        The username and discriminator combined with a '#'.
    """

    id = Field(Snowflake)  # type: Snowflake
    username = Field(str)  # type: str
    discriminator = Field(str)  # type: str
    avatar = Field(str)  # type: str
    bot = Field(bool)  # type: bool
    mfa_enabled = Field(bool)  # type: bool
    locale = Field(str)  # type: str
    flags = Field(UserFlags.get)  # type: Tuple[UserFlags]
    premium_type = Field(PremiumType)  # type: PremiumType

    @property
    def avatar_url(self):
        return self.create_avatar_url()

    @property
    def creation_date(self):
        return self.id.timestamp

    @property
    def mention(self):
        return "<@{}>".format(self.id)

    @property
    def name(self):
        return "{}#{}".format(self.username, self.discriminator)

    def create_avatar_url(self, format: str = None, size: int = 1024):
        """Create a url to get the user's avatar.

        This function will create a link to the user's avatar. If they have not set on it will link
        to a default avatar. You can specify the format, but if you don't, webp will be used for
        normal avatars and gif for animated ones. You can also specify the size.

        Parameters
        ----------
        format : str
            The image format, which can be jpeg / jpg, png, webp, or gif.
        size : int
            The size of the image, can be any power of 2 from 16 to 2048.

        Returns
        -------
        str
            A URL to the user's avatar.
        """

        if not self.avatar:
            return DEFAULT_AVATAR_URL.format(int(self.discriminator) % 5)
        if format is not None:
            return AVATAR_URL.format(self.id, self.avatar, format, size)
        if self.avatar.startswith("a_"):
            return AVATAR_URL.format(self.id, self.avatar, "gif", size)
        return AVATAR_URL.format(self.id, self.avatar, "webp", size)

    def dm(self):
        """Opens a Direct Message (DM) channel with the current user.

        Create a direct message with a user, and return a new channel to represent the conversation.

        Returns
        -------
        :class:`clamor.models.channel.Channel`
            A new DM channel object
        """
        return self.__client.api.create_dm(self.id)


class Visibility(Enum):
    INVISIBLE = 0
    VISIBLE = 1


class Connection(Base):
    """Represents the Connection object attached to every User object.

    Other accounts the user controls, such as youtube, twitch, spotify, etc.

    Attributes
    ----------
    id : str
        The ID of the account.
    name : str
        The name of the account.
    type : str
        The name of the service (YouTube, Twitch, etc).
    revoked : bool
        Whether the connect is revoked.
    verified : bool
        Whether the account is verified.
    friend_sync : bool
        Whether friend sync is enabled.
    show_activity : bool
        Whether changes on this activity will appear on presence updates.
    visibility : :class:`clamor.models.user.Visibility`
        Whether only this user can view the connection.
    """

    id = Field(str)
    name = Field(str)
    type = Field(str)
    revoked = Field(bool)
    verified = Field(bool)
    friend_sync = Field(bool)
    show_activity = Field(bool)
    visibility = Field(Visibility)
