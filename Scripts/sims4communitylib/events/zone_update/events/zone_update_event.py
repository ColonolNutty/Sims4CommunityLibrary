"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.events.event_handling.common_event import CommonEvent
from zone import Zone


class S4CLZoneUpdateEvent(CommonEvent):
    """ An event that occurs when the Zone is updated. """
    def __init__(self, zone: Zone, is_paused: bool, ticks_since_last_update: int):
        self._zone = zone
        self._is_paused = is_paused
        self._ticks_since_last_update = ticks_since_last_update

    @property
    def zone(self) -> Zone:
        """ The zone that was updated. """
        return self._zone

    @property
    def is_paused(self) -> bool:
        """ Determine if the game was paused during this event. """
        return self._is_paused

    @property
    def ticks_since_last_update(self) -> int:
        """ The number of ticks since the last zone update. """
        return self._ticks_since_last_update
