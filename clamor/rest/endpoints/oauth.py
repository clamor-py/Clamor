# -*- coding: utf-8 -*-

from ..routes import Routes
from .base import *

__all__ = (
    'OAuthWrapper',
)


class OAuthWrapper(EndpointsWrapper):
    """"""

    async def get_current_application_info(self) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_CURRENT_APPLICATION_INFO)
