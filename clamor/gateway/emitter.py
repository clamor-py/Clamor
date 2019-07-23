# -*- coding: utf-8 -*-

from typing import Callable, Coroutine, Union, Any

from .exceptions import InvalidListener
from .opcodes import opcodes


class Emitter:
    def __init__(self):
        self.reg = list()
        for i in range(len(opcodes)):
            self.reg.append(None)

    def add_listener(self, op: Union[int, str], listener: Callable[..., Coroutine[Any, Any, None]]):
        if isinstance(op, str):
            op = opcodes[op]
        # Todo: check if listener is valid (coroutine)
        self.reg[op] = listener

    async def emit(self, op: Union[int, str], data, event: str = None):
        if isinstance(op, str):
            op = opcodes[op]
        if self.reg[op]:
            if op == 0 and event:
                await self.reg[op](data, event)
            else:
                await self.reg[op](data)
