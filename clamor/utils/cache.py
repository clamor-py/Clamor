# -*- coding: utf-8 -*-

from collections import deque
from typing import Callable
from weakref import WeakValueDictionary

from ..models import Base

__all__ = (
    'Cache',
    'CacheCategory',
)


class CacheCategory:

    def __init__(self, max: int, fallback: Callable, *ids: str):
        self.fallback = fallback
        self.ids = ids
        self.active = WeakValueDictionary()
        self.cached = deque(maxlen=max)

    def add_active(self, obj: Base):
        key = tuple(getattr(obj, id) for id in self.ids)
        self.active[key] = obj

    def get(self, *ids, ignore_fallback: bool = False):
        cached_obj = self.active.get(ids) \
                     or next((obj for obj in self.cached if
                              all(getattr(obj, id, None) == ids[i] for i, id in
                                  enumerate(self.ids))), None)
        if cached_obj is None and not ignore_fallback:
            return self.fallback(*ids)
        return cached_obj


class Cache:

    MAX_CACHE = 25

    def __init__(self, client):
        self.client = client
        self.categories = {
            'Guild': CacheCategory(self.MAX_CACHE,
                                   self.client.api.get_guild,
                                   'id'),
            'Webhook': CacheCategory(self.MAX_CACHE,
                                     self.client.api.get_webhook,
                                     'id'),
            'Channel': CacheCategory(self.MAX_CACHE,
                                     self.client.api.get_channel,
                                     'id'),
            'User': CacheCategory(self.MAX_CACHE,
                                  self.client.api.get_user,
                                  'id'),
            'Message': CacheCategory(self.MAX_CACHE,
                                     self.client.api.get_channel_message,
                                     'channel_id', 'id')
        }

    def add(self, model: Base):
        if model.name_ in self.categories:
            self.categories[model.name_].add_active(model)

    def get(self, category: str, *ids: int):
        return self.categories[category].get(*ids)
