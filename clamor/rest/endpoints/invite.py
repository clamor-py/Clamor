# -*- coding: utf-8 -*-

from ..routes import Routes
from .base import *

__all__ = (
    'InviteWrapper',
)


class InviteWrapper(EndpointsWrapper):
    """"""

    async def get_invite(self, invite_code: str, with_counts: bool = False) -> dict:
        """"""

        return await self.http.make_request(Routes.GET_INVITE,
                                            dict(invite=invite_code),
                                            params=optional(**{'with_counts': with_counts}))

    async def delete_invite(self, invite_code: str, reason: str = None) -> dict:
        """"""

        return await self.http.make_request(Routes.DELETE_INVITE,
                                            dict(invite=invite_code),
                                            reason=reason)
