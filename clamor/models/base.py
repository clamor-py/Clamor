from enum import Enum
from typing import Any, Callable, Dict, Type, Tuple, Union

from .snowflake import Snowflake


class Field:

    def __init__(self, typ: Callable, alt: str = None):
        self.type = typ
        self.alt = alt
        self._name = None

    def set_name(self, name: str):
        if self._name is not None:
            raise AttributeError("Name was already set, can not be set again.")
        self._name = name

    def __call__(self, value: Any):
        if value is None:
            return

        if not isinstance(value, self.type):
            return self.type(value)
        return value


class BaseMeta(type):

    def __new__(mcs, name: str, bases: Tuple[Type[Any]], clsattrs: Dict[str, Any]):
        for name, field in clsattrs.items():
            if isinstance(field, Field):
                field.set_name(name)
        return super().__new__(mcs, name, bases, clsattrs)


class Base(metaclass=BaseMeta):

    def __init__(self, source: Dict[str, Any], client):
        self.name_ = self.__class__.__name__
        self.source = source
        self.client = client
        if self.id is not None:
            self.client.cache.active[self.__class__.__name__][self.id] = self

    def __getattr__(self, item: str):
        value = super().__getattribute__(item)
        if isinstance(value, Field):
            return value(self.source[value.alt or item])
        return value


class Flags(Enum):

    @classmethod
    def get(cls, flags: int):
        return tuple(a for a in cls if flags & a.value)


Snowflakable = Union[str, int, Base]


def snowflakify(obj: Snowflakable):
    if isinstance(obj, Base):
        return obj.id
    return Snowflake(obj)
