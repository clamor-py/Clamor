# -*- coding: utf-8 -*-

from datetime import datetime
from enum import Enum
from inspect import isclass
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
    'timestamp',
    'GenerativeField'
)


TIMESTAMP_FORMATS = [
    '%Y-%m-%dT%H:%M:%S.%f',
    '%Y-%m-%dT%H:%M:%S',
]


class Field:

    def __init__(self, typ: Union[Callable, str], alt: str = None, array: bool = False):
        self.type = typ
        self.alt = alt
        self._name = None
        self.array = array

    def set_name(self, name: str):
        if self._name is not None:
            raise AttributeError("Name was already set, can not be set again.")
        self._name = name

    def __call__(self, client, value: Any):
        if value is None:
            return [] if self.array else None

        castor = lambda x: self.type(x, client) if \
            isclass(self.type) and issubclass(self.type, Base) else self.type

        if self.array:
            return [v if isinstance(v, self.type) else castor(value) for v in value]
        else:
            if not isinstance(value, self.type):
                return castor(value)
            return value


class BaseMeta(type):

    def __new__(mcs, name: str, bases: Tuple[Type[Any]], clsattrs: Dict[str, Any]):
        fields = []
        for name_, field in clsattrs.items():
            if isinstance(field, Field):
                field.set_name(name_)
                fields.append(name_)
        clsattrs["name_"] = name
        clsattrs["fields_"] = frozenset(fields)
        return super().__new__(mcs, name, bases, clsattrs)


class Base(metaclass=BaseMeta):

    def __init__(self, source: Dict[str, Any] = None, client = None):
        self._source = source or {}
        self._client = client
        if self.id is not None:
            self._client.cache.add(self)

    def __getattribute__(self, item: str):
        value = super().__getattribute__(item)
        if isinstance(value, Field):
            return value(self._client, self._source[value.alt or item])
        return value

    def __setattr__(self, key: str, value: Any):
        if key in self.fields_:
            if getattr(self, key).array:
                self._source[key] = [
                    v._source if hasattr(v, "_source") else v for v in value
                ]
            else:
                self._source[key] = value._source if hasattr(value, "_source") else value
        super().__setattr__(key, value)


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

    def __call__(self, client, values: List[Snowflake]):
        for value in values:
            yield client.cache.get(self.type if isinstance(self.type, str) else
                                   self.type.__name__, value)
