from collections import deque
from typing import Callable
from weakref import WeakValueDictionary

from clamor import Base


class CacheCategory:

    def __init__(self, max: int, fallback: Callable, *ids: str):
        self.fallback = fallback
        self.ids = ids
        self.active = WeakValueDictionary()
        self.cached = deque(maxlen=max)

    def add_active(self, obj: Base):
        key = tuple(getattr(obj, id) for id in self.ids)
        self.active[key] = obj

    def get(self, *ids):
        cached_obj = self.active.get(ids) \
                     or next((obj for obj in self.cached if
                              all(getattr(obj, id, None) == ids[i] for i, id in
                                  enumerate(self.ids))), None)
        if cached_obj is None:
            return self.fallback(*ids)
        return cached_obj


class Cache:

    MAX_CACHE = 25

    def __init__(self, client):
        self.client = client
        self.categories = {
            "Guild": CacheCategory(self.MAX_CACHE,
                                   self.client.api.get_guild,
                                   "id"),
            "Webhook": CacheCategory(self.MAX_CACHE,
                                     self.client.api.get_webhook,
                                     "id"),
            "Channel": CacheCategory(self.MAX_CACHE,
                                     self.client.api.get_channel,
                                     "id")
        }

    def get(self, category: str, *ids: int):
        return self.categories[category].get(*ids)
