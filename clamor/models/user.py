from enum import Enum

from clamor.rest.endpoints import UserWrapper
from .base import Base, Field, Flags
from .snowflake import Snowflake

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
    """
    A discord user model

    This model represents normal discord users, not users from Oauth. While you can't send messages
    to users directly, you can create a channel with them by using the `dm` method.

    Attributes
    ----------
    id : :class:`clamor.models.snowflake.Snowflake`
        The user's discord ID
    username : str
        The user's name without the discriminator
    discriminator : str
        A number that separates people with the same username
    avatar : str
        The user's profile picture's hash
    bot : bool
        If True, the user is a bot account
    mfa_enabled : bool
        If True, the user uses 2factor authentication
    locale : str
        The user's preferred language
    flags : :class:`clamor.models.user.UserFlags`
        Certain user attributes that are displayed on the user's profile as icons
    premium_type : :class:`clamor.model.user.PremiumType`
        Information on the user's paid subscription status
    avatar_url : str
        Shorthand for :func:`clamor.model.user.User.create_avatar_url` without arguments
    creation_date : datetime.datetime
        When the user registered with discord (shorthand for user.id.timestamp)
    mention : str
        A string containing the user as a mention
    name : str
        The username and discriinator combined with a '#'
    """
    API_CLASS = UserWrapper

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
        """
        Create a url to get the user's avatar

        This function will create a link to the user's avatar. If they have not set on it will link
        to a default avatar. You can specify the format, but if you don't, webp will be used for
        normal avatars and gif for animated ones. You can also specify the size.

        Parameters
        ----------
        format : str
            The image format, which can be jpeg / jpg, png, webp, or gif
        size : int
            The size of the image, can be any power of 2 from 16 to 2048

        Returns
        -------
        str
            A url to the user's avatar
        """
        if not self.avatar:
            return DEFAULT_AVATAR_URL.format(int(self.discriminator) % 5)
        if format is not None:
            return AVATAR_URL.format(self.id, self.avatar, format, size)
        if self.avatar.startswith("a_"):
            return AVATAR_URL.format(self.id, self.avatar, "gif", size)
        return AVATAR_URL.format(self.id, self.avatar, "webp", size)

    def dm(self):
        pass  # TODO: Finish when channels are added
