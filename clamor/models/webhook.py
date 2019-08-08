from ..utils.files import File
from .base import Base, Field, Snowflakable, snowflakify
from .snowflake import Snowflake
from .user import User, AVATAR_URL

__all__ = (
    'Webhook',
)


class Webhook(Base):
    """A model to represent Webhooks on Discord.

    Webhooks are easy mode bots, as discord puts it. This model allows you to examine and iteract
    with them. Some methods allow you to use the webhook's token, instead of needing permissions.
    By default, it won't use the token, because you usually won't have access to it.

    Attributes
    ----------
    id : Snowflake
        The ID of the webhook
    guild_id : Snowflake
        The guild's ID, that the webhook belongs too
    channel_id : Snowflake
        The channel'd ID, that the webhook posts in
    user : :class:`clamor.models.user.User`
        The user that created this webhook
    name : str
        The name of the webhook
    avatar : str
        The webhook avatar hash
    token : str
        A secure token that controls the webhook
    guild : :class:`clamor.models.guild.Guild`
        The guild the webhook belongs too
    channel : :class:`clamor.models.channel.Channel`
        The channel the webhook posts in
    avatar_url : str
        Shorthand for create_avatar_url with no parameters
    """
    id = Field(Snowflake)  # type: Snowflake
    guild_id = Field(Snowflake)  # type: Snowflake
    channel_id = Field(Snowflake)  # type: Snowflake
    user = Field(User)  # type: User
    name = Field(str)  # type: str
    avatar = Field(str)  # type: str
    token = Field(str)  # type: str

    @property
    def guild(self):
        return self.__client.cache.get("Guild", self.guild_id)

    @property
    def channel(self):
        return self.__client.cache.get("Channel", self.channel_id)

    @property
    def avatar_url(self):
        return self.create_avatar_url()

    def create_avatar_url(self, format: str = None, size: int = 1024) -> str:
        """
        Create a url to get the webhook's avatar

        This function will create a link to the webhook's avatar. If they have not set on it will
        link to a default avatar. You can specify the format, but if you don't, webp will be used
        for normal avatars and gif for animated ones. You can also specify the size.

        Parameters
        ----------
        format : str
            The image format, which can be jpeg / jpg, png, webp, or gif
        size : int
            The size of the image, can be any power of 2 from 16 to 2048

        Returns
        -------
        str
            A url to the webhook's avatar
        """
        if format is not None:
            return AVATAR_URL.format(self.id, self.avatar, format, size)
        if self.avatar.startswith("a_"):
            return AVATAR_URL.format(self.id, self.avatar, "gif", size)
        return AVATAR_URL.format(self.id, self.avatar, "webp", size)

    def modify(self, name: str = None, avatar: File = None, channel: Snowflakable = None,
               use_token: bool = False, reason: str = None) -> 'Webhook':
        """
        Modify the name, avatar, and or channel

        Modify the name, avatar, and or channel which the webhook posts in. If none of those
        parameters are provided, it will just return itself. If you use a token to call this
        function, you cannot change what channel the webhook posts in, so that parameter will be
        ignored. On success, it will return the modified webhook. This webhook won't change.

        Parameters
        ----------
        name : str
            The new name of the webhook
        avatar : :class:`clamor.utils.files.File`
            The new avatar of the webhook
        channel : Snowflakable
            The new channel the webhook will post in (cannot change if using token)
        use_token : bool
            Instead of using permissions, use the token instead
        reason : str
            The reason for the modification

        Returns
        -------
        :class:`clamor.models.webhook.Webhook`
            The new, modified webhook
        """
        if not any((name, avatar, channel)):
            return self

        if use_token:
            return self.__client.api.modify_webhook_with_token(
                self.id,
                self.token,
                name=name,
                avatar=avatar.data_uri,
                reason=reason
            )
        else:
            return self.__client.api.modify_webhook(
                self.id,
                name=name,
                avatar=avatar.data_uri,
                channel_id=snowflakify(channel),
                reason=reason
            )

    def delete(self, use_token: bool = False, reason: str = None):
        """
        Delete the webhook

        Parameters
        ----------
        use_token : bool
            Instead of using permissions, use the token instead
        reason: str
            The reason for deleting the webhook
        """
        if use_token:
            self.__client.api.delete_webhook_with_token(self.id, self.token, reason)
        else:
            self.__client.api.delete_webhook(self.id, reason)

    # TODO: Added method to execute the webhook, I guess
