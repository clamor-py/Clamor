# -*- coding: utf-8 -*-

from datetime import datetime

__all__ = (
    'Snowflake',
)


class Snowflake(int):

    DISCORD_EPOCH = 1420070400000

    """
    An object to represent a discord snowflake
    
    Keep in mind, that this is just a normal int with some added properties.
    This is the only object that doesn't inherit from :class:`~clamor.models.base.Model`.
    For the most part, you can just treat this like a normal int.
    
    Attributes
    ----------
    increment : int
        "For every ID that is generated on that process, this number is incremented" ~ Discord docs
    internal_process_id : int
        Undocumented, but supposedly the ID of the process that made the snowflake
    internal_worker_id : int
        Undocumented, but supposedly the ID of the worker that made the snowflake
    timestamp : datetime.datetime
        A datetime object containing the point in time that the snowflake was created
    """

    @property
    def increment(self):
        return self & 0xFFF

    @property
    def internal_process_id(self):
        return (self & 0x1F000) >> 12

    @property
    def internal_worker_id(self):
        return (self & 0x3E0000) >> 17

    @property
    def timestamp(self):
        return datetime.utcfromtimestamp(((self >> 22) + self.DISCORD_EPOCH) / 1000)

    def is_valid(self):
        """
        Complete a series of checks to see if it could be a snowflake

        The following checks are to ensure that it *could* be a discord ID.
            1. Makes sure it isn't 0 or less
            2. It makes sure the snowflake isn't larger than 64 bits.
            3. It makes sure the snowflake is at least 22 bits.
            4. It makes sure the timestamp isn't less than the discord epoch.
            5. It makes sure the timestamp isn't greater than now

        Returns
        -------
        bool
            True if the ID could belong to discord, False otherwise.
        """
        if self <= 0:
            return False
        elif 22 > self.bit_length() > 64:
            return False
        elif self.timestamp < datetime.utcfromtimestamp(self.DISCORD_EPOCH / 1000):
            return False
        elif self.timestamp > datetime.now():
            return False
        return True
