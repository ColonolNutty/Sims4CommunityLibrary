"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.events.event_handling.common_event import CommonEvent
from zone import Zone


class S4CLZoneUpdateEvent(CommonEvent):
    """S4CLZoneUpdateEvent(zone, is_paused, ticks_since_last_update)

    An event that occurs when a Zone has been updated.

    .. note:: This event can occur while the game is paused.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
        from sims4communitylib.modinfo import ModInfo

        class ExampleEventListener:

            # In order to listen to an event, your function must match these criteria:
            # - The function is static (staticmethod).
            # - The first and only required argument has the name "event_data".
            # - The first and only required argument has the Type Hint for the event you are listening for.
            # - The argument passed to "handle_events" is the name of your Mod.
            @staticmethod
            @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
            def handle_event(event_data: S4CLZoneUpdateEvent):
                pass

    :param zone: The Zone that was updated.
    :type zone: Zone
    :param is_paused: A value indicating if the game was paused during the dispatching of this event.
    :type is_paused: bool
    :param ticks_since_last_update: The number of ticks since the last zone update in milliseconds.
    :type ticks_since_last_update: int
    """

    def __init__(self, zone: Zone, is_paused: bool, ticks_since_last_update: int):
        self._zone = zone
        self._is_paused = is_paused
        self._ticks_since_last_update = ticks_since_last_update

    @property
    def zone(self) -> Zone:
        """The Zone that was updated.

        :return: The Zone that was updated.
        :rtype: Zone
        """
        return self._zone

    @property
    def is_paused(self) -> bool:
        """Determine if the game was paused during the update.

        :return: True, if the game was paused. False, if the game was not paused.
        :rtype: bool
        """
        return self._is_paused

    @property
    def ticks_since_last_update(self) -> int:
        """The number of ticks in milliseconds since the last zone update.

        :return: The number of ticks in milliseconds since the last zone update.
        :rtype: int
        """
        return self._ticks_since_last_update
