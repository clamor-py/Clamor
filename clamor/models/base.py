# -*- coding: utf-8 -*-

from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Type, Tuple, Union

from .snowflake import Snowflake

__all__ = (
    'Base',
    'BaseMeta',
    'Field',
    'Flags',
    'Snowflakable',
    'Snowflake',
    'snowflakify',
    'datetime',
    'GenerativeField'
)


TIMESTAMP_FORMATS = [
    '%Y-%m-%dT%H:%M:%S.%f',
    '%Y-%m-%dT%H:%M:%S',
]


class Field:

    def __init__(self, typ: Callable, alt: str = None, array: bool = False):
        self.type = typ
        self.alt = alt
        self._name = None
        self.array = array

    def set_name(self, name: str):
        if self._name is not None:
            raise AttributeError("Name was already set, can not be set again.")
        self._name = name

    def __call__(self, value: Any):
        if value is None:
            return [] if self.array else None

        if self.array:
            return [v if isinstance(v, self.type) else self.type(value) for v in value]
        else:
            if not isinstance(value, self.type):
                return self.type(value)
            return value


class BaseMeta(type):

    def __new__(mcs, name: str, bases: Tuple[Type[Any]], clsattrs: Dict[str, Any]):
        for name_, field in clsattrs.items():
            if isinstance(field, Field):
                field.set_name(name_)
        clsattrs["name_"] = name
        return super().__new__(mcs, name, bases, clsattrs)


class Base(metaclass=BaseMeta):

    def __init__(self, source: Dict[str, Any], client):
        self._source = source
        self._client = client
        if self.id is not None:
            self._client.cache.add(self)

    def __getattribute__(self, item: str):
        value = super().__getattribute__(item)
        if isinstance(value, Field):
            if isinstance(value, GenerativeField):
                return value(self._client.cache, self._source[value.alt or item])
            return value(self._source[value.alt or item])
        return value


class Flags(Enum):

    @classmethod
    def get(cls, flags: int):
        return tuple(a for a in cls if flags & a.value)


Snowflakable = Union[str, int, Base]


def snowflakify(obj: Snowflakable) -> Snowflake:
    if isinstance(obj, Base):
        return obj.id
    return Snowflake(obj)


def timestamp(data):
    if not data:
        return None

    if isinstance(data, int):
        return datetime.utcfromtimestamp(data)

    for fmt in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(data.rsplit('+', 1)[0], fmt)
        except (ValueError, TypeError):
            continue

    raise ValueError('"{}" is not a valid timestamp'.format(data))


class GenerativeField(Field):

    def __call__(self, cache, values: List[Snowflake]):
        for value in values:
            yield cache.get(self.type.__name__, value)
