# -*- coding: utf-8 -*-

from collections import defaultdict
from enum import Enum
from inspect import iscoroutinefunction
from functools import wraps
from typing import Any, Callable, Coroutine

from clamor.exceptions import InvalidListener

from anyio import create_task_group

__all__ = (
    'check_coroutine',
    'Emitter',
    'ListenerPod',
    'Priority',
)


def check_coroutine(func):
    @wraps(func)
    def wrapper(self, listener: Callable[..., Coroutine[Any, Any, None]]):
        if not iscoroutinefunction(listener):
            raise InvalidListener("Listener must be a coroutine")
        return func(self, listener)

    return wrapper


class Priority(Enum):
    BEFORE = 0
    NORMAL = 1
    AFTER = 2


class ListenerPod:
    """Event listener module.

    Listeners that all follow a certain event will exist in the same pod. Pods will separate
    listeners into self-explanatory categories, before, normal, and after. The listeners will
    trigger in order from before to after, with each listener triggering synchronously with
    listeners from the same category.

    Attributes
    ----------
    before : set
        Listeners that will trigger first.
    normal : set
        Listeners that will trigger second.
    after : set
        Listeners that will trigger third.
    """

    def __init__(self):
        self.before = set()
        self.normal = set()
        self.after = set()

    def __bool__(self):
        return bool(self.before) or bool(self.normal) or bool(self.after)

    @check_coroutine
    def add_before(self, listener: Callable[..., Coroutine[Any, Any, None]]):
        """Adds a listener (Before).

        Adds a coroutine to the before category.

        Parameters
        ----------
        listener : Coroutine
            A coroutine to be triggered on its respective event.
        """
        self.before.add(listener)

    @check_coroutine
    def add_normal(self, listener: Callable[..., Coroutine[Any, Any, None]]):
        """Adds a listener (Normal).

        Adds a coroutine to the normal category.

        Parameters
        ----------
        listener : Coroutine
            A coroutine to be triggered on its respective event.
        """
        self.normal.add(listener)

    @check_coroutine
    def add_after(self, listener: Callable[..., Coroutine[Any, Any, None]]):
        """Adds a listener (After).

        Adds a coroutine to the after category.

        Parameters
        ----------
        listener : Coroutine
            A coroutine to be triggered on its respective event.
        """
        self.after.add(listener)

    async def emit(self, *args):
        """Trigger listeners in the pod

        All listeners in the before category will be spawned with the appropriate payload, and
        once all those have finished, the normal category is triggered, and then the after category.

        Parameters
        ----------
        args
            The arguments to be distributed.
        """
        async with create_task_group() as tg:
            for listener in self.before:
                await tg.spawn(listener, *args)
        async with create_task_group() as tg:
            for listener in self.normal:
                await tg.spawn(listener, *args)
        async with create_task_group() as tg:
            for listener in self.after:
                await tg.spawn(listener, *args)


class Emitter:
    """Main event emitter.

    This is what orchestrates all the event pods, adds listeners, removes them and triggers events.
    Events can be anything, for example ints, strings or enum members.

    Attributes
    ----------
    listeners : defaultdict(:class `~clamor.utils.emitter.ListenerPod`:)
        A default dict that holds event names to listener pods.
    """

    def __init__(self):
        self.listeners = defaultdict(ListenerPod)

    def add_listener(self, event: Any,
                     listener: Callable[..., Coroutine[Any, Any, None]],
                     order: Priority = Priority.NORMAL):
        """Adds a listener.

        Adds a listener to the correct pod and category, which by default is the normal priority.

        Parameters
        ----------
        event : :class:`typing.Any`
            The event to listen to.
        listener : Coroutine
            A coroutine to be triggered on its respective event.
        order : :class:`~clamor.utils.emitter.Priority`
            The order this listener should be triggered in.
        """

        # Create a pod if one does not exist for the event, then add the listener
        # using the respective method, based on the priority.
        getattr(self.listeners[event], "add_" + order.name.lower())(listener)

    async def emit(self, event: Any, *args):
        """Emits an event.

        Triggers the corresponding :class:`~clamor.utils.emitter.ListenerPod` if one exists.

        Parameters
        ----------
        event: :class:`typing.Any`
            The event to listen to.
        args
            The arguments to be distributed.
        """

        if self.listeners[event]:
            await self.listeners[event].emit(*args)

    def clear_event(self, event: Any):
        """Clears all listeners.

        Removes all listeners, to matter the category, from the provided event.

        Parameters
        ----------
        event : :class:`typing.Any`
            The event to remove.
        """

        self.listeners.pop(event)

    def remove_listener(self, event: Any, listener: Callable[..., Coroutine[Any, Any, None]]):
        """Removes a specific listener from an event.

        Removes a the provided listener from an event, no matter the category.

        Parameters
        ----------
        event : :class:`typing.Any`
            The event to search.
        listener : Coroutine
            The listener to remove.
        """

        if event in self.listeners:
            if listener in self.listeners[event].before:
                self.listeners[event].before.remove(listener)
            if listener in self.listeners[event].normal:
                self.listeners[event].normal.remove(listener)
            if listener in self.listeners[event].after:
                self.listeners[event].after.remove(listener)
