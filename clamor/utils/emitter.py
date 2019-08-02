# -*- coding: utf-8 -*-

from collections import defaultdict
from enum import Enum
from inspect import iscoroutinefunction
from functools import wraps
from typing import Callable, Coroutine, Union, Any, Dict

from clamor.gateway.exceptions import InvalidListener

from anyio import create_task_group


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
    """Event listener module

    Listeners that all follow a certain event will exist in the same pod. Pods will separate
    listeners into self-explanatory categories, before, normal, and after. The listeners will
    trigger in order from before to after, with each listener triggering synchronously with
    listeners from the same category.

    Attributes
    ----------
    before : set
        Listeners that will trigger 1st
    normal : set
        Listeners that will trigger 2nd
    after : set
        Listeners that will trigger 3rd
    """

    def __init__(self):
        self.before = set()
        self.normal = set()
        self.after = set()

    def __bool__(self):
        return bool(self.before) or bool(self.normal) or bool(self.after)

    @check_coroutine
    def add_before(self, listener: Callable[..., Coroutine[Any, Any, None]]):
        """Add listener (Before)

        Add a coroutine to the before category

        Parameters
        ----------
        listener : Coroutine
            A coroutine to be triggered on it's respective event
        """
        self.before.add(listener)

    @check_coroutine
    def add_normal(self, listener: Callable[..., Coroutine[Any, Any, None]]):
        """Add listener (Normal)

        Add a coroutine to the normal category

        Parameters
        ----------
        listener : Coroutine
            A coroutine to be triggered on it's respective event
        """
        self.normal.add(listener)

    @check_coroutine
    def add_after(self, listener: Callable[..., Coroutine[Any, Any, None]]):
        """Add listener (After)

        Add a coroutine to the after category

        Parameters
        ----------
        listener : Coroutine
            A coroutine to be triggered on it's respective event
        """
        self.after.add(listener)

    async def emit(self, data: Dict[str, Any]):
        """Trigger listeners in the pod

        All listeners in the before category will be spawned with the appropriate payload, and
        once all those have finished, the normal category is triggered, and then the after category.

        Parameters
        ----------
        data : dict
            The payload provided by discord to be distributed
        """
        async with create_task_group() as tg:
            for listener in self.before:
                await tg.spawn(listener, data)
        async with create_task_group() as tg:
            for listener in self.normal:
                await tg.spawn(listener, data)
        async with create_task_group() as tg:
            for listener in self.after:
                await tg.spawn(listener, data)


class Emitter:
    """Main event emitter

    This is what orchestrates all the event pods, adds listeners, removes them and triggers events.
    Events can be either an op code, or a name (for opcode 0).

    Attributes
    ----------
    listeners : defaultdict(:class `clamor.gateway.emitter.ListenerPod`:)
        A default dict that holders event namess to listener pods.
    """

    def __init__(self):
        self.listeners = defaultdict(ListenerPod)

    def add_listener(self, event: Union[int, str],
                     listener: Callable[..., Coroutine[Any, Any, None]],
                     order: Priority = Priority.NORMAL):
        """Add a listener

        Add a listener to the correct pod and category, which by default is the normal priority.

        Parameters
        ----------
        event : int or str
            The op code or event to listen too
        listener : Coroutine
            A coroutine to be triggered on it's respective event
        order : :class `clamor.gateway.emitter.Priority`
            The order this listener should be triggered in
        """

        # Create a pod if one does not exist for the event, then add the listener
        # using the respective method, based on the priority.
        getattr(self.listeners[event], "add_" + order.name.lower())(listener)

    async def emit(self, event: Union[int, str], data):
        """Emit an event

        Trigger the corresponding ListenerPod if one exists.

        Parameters
        ----------
        event: int or str
            The op code or event to listen too
        data : dict
            The payload provided by discord to be distributed
        """
        if self.listeners[event]:
            await self.listeners[event].emit(data)

    def clear_event(self, event: Union[str, int]):
        """Clear all listeners

        Removes all listeners, to matter the category, from the provided event.

        Parameters
        ----------
        event : str or int
            The op code or event to remove
        """
        self.listeners.pop(event)

    def remove_listener(self, event: Union[str, int],
                        listener: Callable[..., Coroutine[Any, Any, None]]):
        """Remove a specific listener from an event

        Removes a the provided listener from an event, no matter the category.

        Parameters
        ----------
        event : int or str
            The op code or event to search
        listener : Coroutine
            Listener to remove
        """
        if self.listeners[event]:
            if listener in self.listeners[event].before:
                self.listeners[event].before.remove(listener)
            if listener in self.listeners[event].normal:
                self.listeners[event].normal.remove(listener)
            if listener in self.listeners[event].after:
                self.listeners[event].after.remove(listener)
