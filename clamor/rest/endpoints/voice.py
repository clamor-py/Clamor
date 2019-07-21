# -*- coding: utf-8 -*-

from ..routes import Routes
from .base import *

__all__ = (
    'VoiceWrapper',
)


class VoiceWrapper(EndpointsWrapper):
    """A higher-level wrapper around Voice endpoints.

    .. seealso:: Voice endpoints https://discordapp.com/developers/docs/resources/voice
    """

    async def list_voice_regions(self) -> list:
        return await self.http.make_request(Routes.LIST_VOICE_REGIONS)
