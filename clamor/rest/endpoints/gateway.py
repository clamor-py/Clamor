# -*- coding: utf-8 -*-

from ..routes import Routes
from .base import *

__all__ = (
    'GatewayWrapper',
)


class GatewayWrapper(EndpointsWrapper):
    """A higher-level wrapper around Gateway endpoints.

    .. seealso:: Gateway endpoints https://discordapp.com/developers/docs/topics/gateway
    """

    async def get_gateway(self) -> dict:
        return await self.http.make_request(Routes.GET_GATEWAY)

    async def get_gateway_bot(self) -> dict:
        return await self.http.make_request(Routes.GET_GATEWAY_BOT)
