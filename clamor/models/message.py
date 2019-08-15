# -*- coding: utf-8 -*-

from typing import List, Union

from clamor.utils.files import File
from .base import Base, Field, datetime, GenerativeField, snowflakify
from .base import timestamp as discord_timestamp
from .emoji import Reaction, Emoji
from .guild import Member, Role
from .snowflake import Snowflake
from .solo import Attachments, ChannelTypes, MessageTypes, \
    MessageFlags, MessageActivities, MessageApplication, MessageReference
from .user import User


__all__ = (
    "MentionUser",
    "MentionChannel",
    "Embed",
    "EmbedField",
    "EmbedAuthor",
    "EmbedThumbnail",
    "EmbedImage",
    "EmbedFooter",
    "EmbedProvider",
    "EmbedVideo",
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


class EmbedFooter(Base):
    """
    Embed footer

    (The bottom most text of an embed)

    Attributes
    ----------
    text : str
        The footer text
    icon_url : str
        A url to the footer's icon
    proxy_icon_url : str
        A proxied version of the url
    """
    text = Field(str)  # type: str
    icon_url = Field(str)  # type: str
    proxy_icon_url = Field(str)  # type: str


class EmbedImage(Base):
    """
    Embed image

    (The large image to the right / center)

    Attributes
    ----------
    url : str
        A url to the image source
    proxy_url : str
        A proxied version of the url
    height : int
        The height of the image
    width : int
        The width of the image
    """
    url = Field(str)  # type: str
    proxy_url = Field(str)  # type: str
    height = Field(int)  # type: int
    width = Field(int)  # type: int


class EmbedThumbnail(Base):
    """
    Embed thumbnail

    (Small icon at the top left)

    Attributes
    ----------
    url : str
        A url to the image source
    proxy_url : str
        A proxied version of the url
    height : int
        The height of the image
    width : int
        The width of the image
    """
    url = Field(str)  # type: str
    proxy_url = Field(str)  # type: str
    height = Field(int)  # type: int
    width = Field(int)  # type: int


class EmbedVideo(Base):
    """
    Embed video

    (Video that will take up most of the embed)

    Attributes
    ----------
    url : str
        The source of the video
    height : int
        The height of the video
    width : int
        The width of the video
    """
    url = Field(str)  # type: str
    height = Field(int)  # type: int
    width = Field(int)  # type: int


class EmbedProvider(Base):
    """
    Embed provider

    (The provider of the embed, for webhooks)

    Attributes
    ----------
    name : str
        The name of the provider
    url : str
        A url to the provider
    """
    name = Field(str)  # type: str
    url = Field(str)  # type: str


class EmbedAuthor(Base):
    """
    Embed author

    (The name and avatar of the author, on the very top)

    Attributes
    ----------
    name : str
        The name of the author
    url : str
        A url to the author
    icon_url : str
        The author's icon location
    proxy_icon_url : str
        A proxied author icon
    """
    name = Field(str)  # type: str
    url = Field(str)  # type: str
    icon_url = Field(str)  # type: str
    proxy_icon_url = Field(str)  # type: str


class EmbedField(Base):
    """
    Embed field

    (Boxes that will be added to the bottom of the embed)

    Attributes
    ----------
    name : str
        The field's name
    value : str
        The field's value
    inline : bool
        Whether the field will be inline
    """
    name = Field(str)  # type: str
    value = Field(str)  # type: str
    inline = Field(bool)  # type: bool


class Embed(Base):
    """
    Message embed, for rich messages

    Message embeds are special, in that they can allow for messages to have more than just
    attachments. You can display many images, and use more markdown than a normal message would
    allow. It's advised you use a message builder to make an embed, however you can make one by
    yourself.

    Attributes
    ----------
    title : str
        The title of the embed, which is displayed at the top
    type : str
        The type of embed, bot embeds will have the type 'rich'
    description : str
        The main body of the embed, can use more markdown than normal
    url : str
        A url that will be added to the title
    timestamp : datetime
        A timestamp that will be added to the footer, can be whatever time
    color : int
        A integer representing a color's hex value
    footer : :class:`clamor.models.message.EmbedFooter`
        The embed footer, see the footer class for details.
    image : :class:`clamor.models.message.EmbedImage`
        The embed image, see the image class for details.
    thumbnail : :class:`clamor.models.message.EmbedThumbnail`
        The embed thumbnail, see the thumbnail class for details.
    video : :class:`clamor.models.message.EmbedVideo`
        The embed video, see video class for details.
    provider : :class:`clamor.models.message.EmbedProvider`
        The embed provider, see provider class for details.
    author : :class:`clamor.models.message.EmbedAuthor`
        The embed author, see author class for details.
    fields : list(:class:`clamor.models.message.EmbedImage`)
        The embed fields, see field class for details.
    """
    title = Field(str)  # type: str
    type = Field(str)  # type: str
    description = Field(str)  # type: str
    url = Field(str)  # type: str
    timestamp = Field(datetime)  # type: datetime
    color = Field(int)  # type: int
    footer = Field(EmbedFooter)  # type: EmbedFooter
    image = Field(EmbedImage)  # type: EmbedImage
    thumbnail = Field(EmbedThumbnail)  # type: EmbedThumbnail
    video = Field(EmbedVideo)  # type: EmbedVideo
    provider = Field(EmbedProvider)  # type: EmbedProvider
    author = Field(EmbedAuthor)  # type: EmbedAuthor
    fields = Field(EmbedField, array=True)  # type: List[EmbedField]

    def set_footer(self, text: str, icon_url: str = None):
        self.footer = EmbedFooter({
            "text": text,
            "icon_url": icon_url
        }, self._client)

    def set_image(self, url: str):
        self.image = EmbedImage({
            "url": url
        }, self._client)

    def set_thumbnail(self, url: str):
        self.thumbnail = EmbedThumbnail({
            "url": url
        }, self._client)

    def set_author(self, name: str, url: str, icon_url: str):
        self.author = EmbedAuthor({
            "name": name,
            "url": url,
            "icon_url": icon_url
        }, self._client)

    def add_field(self, name: str, value: str, inline: bool = False):
        field = EmbedField({
                "name": name,
                "value": value,
                "inline": inline
            }, self._client)
        if self.fields:
            self.fields.append(field)
        else:
            self.fields = [field]


class MessageActivity(Base):
    """
    Activities sent in messages

    Messages can contain things such as spectate requests or game invites, this represents that.

    Attributes
    ----------
    party_id : str
        The ID of the activity's party
    type : :class:`clamor.models.solo.MessageActivities`
        The type of activity request
    """
    party_id = Field(str)  # type: str
    type = Field(MessageActivities)  # type: MessageActivities


class Message(Base):
    """
    The discord text message class

    Discord messages used to be simple, and now they're not. But that's ok, because they do contain
    a lot of useful information. You can send responses from the message class just like you would
    with a channel. Not all messages are going to have any content, make sure you check the message
    type.

    Attributes
    ----------
    id : Snowflake
        The message's ID
    channel_id : Snowflake
        The ID of the channel the message was posted in
    guild_id : Snowflake
        The ID of the guild the channel is in, this is not set in DMs
    author : User
        The user who sent the message
    member : Member
        A partial member version of the user, so API requests are not needed.
    content : str
        The message contents as text
    timestamp : datetime
        The time the message was posted
    edited_timestamp : datetime
        The time the message was edited
    tts : bool
        Whether the message is text-to-speech
    mention_everyone : bool
        Whether the mention contains @everyone
    mentions : list(:class:`clamor.models.message.MentionUser`)
        Partial users for all the users mentioned
    mention_roles : generator(:class:`clamor.models.guild.Role`)
        A generator of roles that were mentioned
    attachments : list(:class:`clamor.models.message.Attachments`)
        A list of files that were attached to the message
    embeds : list(:class:`clamor.models.message.Embed`)
        A list of embeds that were attached to the message
    reactions : list(:class:`clamor.models.emoji.Reaction`)
        A list of emojis that were reacted to the message
    nonce : Snowflake
        A integer used to prevent duplicate messages
    pinned : bool
        Whether the message was pinned or not
    webhook_id : Snowflake
        The ID of the webhook that sent the message if applicable
    types : :class:`clamor.models.solo.MessageTypes`
        The type of message that was sent
    application : :class:`clamor.models.solor.MessageApplication`
        The application that is related to the message? (I'm not really sure)
    message_reference : :class:`clamor.models.solo.MessageReference`
        The message that this message references too
    activity : :class:`clamor.models.solo.MessageActivity`
        The activity that this this message is related too
    flags : :class:`clamor.models.solo.MessageFlags`
        Flags that are added to the message
    channel : :class:`clamor.models.channel.Channel`
        The channel that the message was posted in
    guild : :class:`clamor.models.guild.Guild`
        The guild that the channel is in
    """
    id = Field(Snowflake)  # type: Snowflake
    channel_id = Field(Snowflake)  # type: Snowflake
    guild_id = Field(Snowflake)  # type: Snowflake
    author = Field(User)  # type: User
    member = Field(Member)  # type: Member
    content = Field(str)  # type: str
    timestamp = Field(discord_timestamp)  # type: datetime
    edited_timestamp = Field(discord_timestamp)  # type: datetime
    tts = Field(bool)  # type: bool
    mention_everyone = Field(bool)  # type: bool
    mentions = Field(MentionUser, array=True)  # type: List[MentionUser]
    mention_roles = GenerativeField(Role)  # type: GenerativeField
    attachments = Field(Attachments, array=True)  # type: List[Attachments]
    embeds = Field(Embed, array=True)  # type: List[Embed]
    reactions = Field(Reaction, array=True)  # type: List[Reaction]
    nonce = Field(Snowflake)  # type: Snowflake
    pinned = Field(bool)  # type: bool
    webhook_id = Field(Snowflake)  # type: Snowflake
    types = Field(MessageTypes)  # type: MessageTypes
    application = Field(MessageApplication)  # type: MessageApplication
    message_reference = Field(MessageReference)  # type: MessageReference
    activity = Field(MessageActivity)  # type: MessageActivity
    flags = Field(MessageFlags)  # type: MessageFlags

    @property
    def channel(self):
        return self._client.cache.get("Channel", self.channel_id)

    @property
    def guild(self):
        return self._client.cache.get("Guild", self.guild_id)

    def respond(self, content: str, ):
        pass

    async def react(self, emoji: Union[str, Emoji]):
        """
        Add a reaction

        Add a reaction to this message, the emoji can be unicode, or an emoji object.

        Parameters
        ----------
        emoji : str or :class:`clamor.models.emoji.Emoji`
            The emoji you want to react with
        """
        await self._client.api.create_reaction(
            self.channel_id,
            self.id,
            emoji if isinstance(emoji, str) else emoji.string
        )

    async def unreact(self, emoji: Union[str, Emoji]):
        """
        Remove your reaction

        Remove your own reaction. You cannot use this to remove someone else's reaction.

        Parameters
        ----------
        emoji : str or :class:`clamor.models.emoji.Emoji`
            The emoji you would like to unreact
        """
        await self._client.api.delete_own_reaction(
            self.channel_id,
            self.id,
            emoji if isinstance(emoji, str) else emoji.string
        )

    async def remove_reaction(self, user: Union[Snowflake, str, User], emoji: Union[str, Emoji]):
        """
        Remove someone's reaction

        Remove someone's reaction from this message

        Parameters
        ----------
        emoji : str or :class:`clamor.models.emoji.Emoji`
            The emoji you would like to remove from the reactions
        """
        await self._client.api.delete_user_reaction(
            self.channel_id,
            self.id,
            snowflakify(user),
            emoji if isinstance(emoji, str) else emoji.string
        )

    async def purge_reactions(self):
        """
        Remove all reactions

        This method will remove all the reactions from a message, not just yours.
        """
        await self._client.api.delete_all_reactions(
            self.channel_id,
            self.id
        )

    async def edit(self, content: str = None, embed: Union[Embed, dict] = None) -> 'Message':
        """
        Edit this message

        You can change the content and or embed with this method. If you do not set either the
        content or embed, the method won't call the endpoint and just return itself. This method
        does not change the this method, and instead will return a new, updated one.

        Parameters
        ----------
        content : str
            The message contents
        embed : dict or :class:`clamor.models.message.Embed`
            The embed attached to the message

        Returns
        -------
        :class:`clamor.models.message.Message`
            The new, updated message. This message won't change.
        """
        if not all((content, embed)):
            return self
        return await self._client.api.edit_message(
            self.channel_id,
            self.id,
            content=content,
            embed=embed if isinstance(embed, dict) else embed._source
        )

    async def delete(self, reason: str = None):
        """
        Delete this message

        Delete this message, if this is your message you won't need permissions to do it.

        Parameters
        ----------
        reason : str
            The reason for deleting the message
        """
        await self._client.api.delete_message(
            self.channel_id,
            self.id,
            reason
        )

    async def pin(self):
        """
        Pin this message

        Pin this message to the channel it's in
        """
        await self._client.api.add_pinned_channel_message(
            self.channel_id,
            self.id
        )

    async def unpin(self, reason: str = None):
        """
        Unpin this message

        Unpin this message from the channel it's in

        Parameters
        ----------
        reason : str
            The reason for unpinning the message
        """
        await self._client.api.delete_pinned_channel_message(
            self.channel_id,
            self.id,
            reason
        )
