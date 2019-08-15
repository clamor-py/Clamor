# -*- coding: utf-8 -*-

from .base import Base, Field, timestamp, datetime
from .channel import Channel
from .guild import Guild
from .solo import TargetUserType
from .user import User


__all__ = (
    'PartialInvite',
    'FullInvite'
)


class PartialInvite(Base):
    """
    Partial discord invite

    Represents a code that when used, adds a user to a guild or group DM channel. You can't use
    this invite to join a server, because bots can't join servers. You also cannot get the
    metadata directly from the invite, but you can from the guild.

    Attributes
    ----------
    code : str
        The invite code
    guild : :class:`clamor.models.guild.Guild`
        A partial guild object which the invite belongs too
    channel : :class:`clamor.models.channel.Channel`
        A partial channel object that the invite is attached too
    target_user : :class:`clamor.models.user.User`
        A partial user which this invite is for
    target_user_type : :class:`clamor.models.solo.TargetUserType`
        The type of target user for this invite, right now there is only STREAM
    approximate_presence_count : int
        Approx how many members are online on the guild
    approximate_member_count : int
        Approx how many members are on the guild
    """
    code = Field(str)  # type: str
    guild = Field(Guild)  # type: Guild
    channel = Field(Channel)  # type: Channel
    target_user = Field(User)  # type: User
    target_user_type = Field(TargetUserType)  # type: TargetUserType
    approximate_presence_count = Field(int)  # type: int
    approximate_member_count = Field(int)  # type: int

    @property
    def link(self) -> str:
        return "https://discord.gg/" + self.code

    async def delete(self, reason : str = None) -> 'PartialInvite':
        return await self._client.api.delete_invite(self.code, reason)


class FullInvite(PartialInvite):
    """
    Full discord invite

    This in an invite that includes the metadata, which is included when you get invites from a
    channel or guild. See :class:`clamor.models.invite.PartialInvite` for more information.

    Attributes
    ----------
    inviter : :class:`clamor.models.user.User`
        The person who created this invite
    uses : int
        The amount of times this invite has been used
    max_uses : int
        The amount of times this invite can be used
    max_age : int
        The duration in seconds until the invite expires
    temporary : bool
        Whether the invite grants temporary membership or not
    created_at : datetime
        When the invite was created
    revoked : bool
        Whether the invite was revoked
    """
    inviter = Field(User)  # type: User
    uses = Field(int)  # type: int
    max_uses = Field(int)  # type: int
    max_age = Field(int)  # type: int
    temporary = Field(bool)  # type: bool
    created_at = Field(timestamp)  # type: datetime
    revoked = Field(bool)  # type: bool
