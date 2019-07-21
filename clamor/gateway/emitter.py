# -*- coding: utf-8 -*-

from typing import Callable, Coroutine, Union, Any

from .exceptions import InvalidListener
from .opcodes import opcodes


class Emitter:
    def __init__(self):
        self.reg = list()
        for i in range(len(opcodes)): self.reg.append(None)

    def add_listener(self, opcode: Union[int, str], listener: Callable[..., Coroutine[Any, Any, None]]):
        if isinstance(opcode, str):
            opcode = opcodes[opcode]
        self.reg[opcode] = listener

    async def emit(self, opcode: Union[int, str], data):
        if isinstance(opcode, str):
            opcode = opcodes[opcode]
        if self.reg[opcode]:
            await self.reg[opcode](data)
