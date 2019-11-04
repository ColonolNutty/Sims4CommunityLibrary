"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.events.event_handling.common_event import CommonEvent
from zone import Zone


class S4CLZoneLateLoadEvent(CommonEvent):
    """ An Event that Occurs upon late load of a zone. """
    def __init__(self, zone: Zone, household_id: int, active_sim_id: int, game_loaded: bool=False, game_loading: bool=False):
        self._zone = zone
        self._household_id = household_id
        self._active_sim_id = active_sim_id
        self._game_loaded = game_loaded
        self._game_loading = game_loading

    @property
    def zone(self) -> Zone:
        """ The zone being loaded. """
        return self._zone

    @property
    def household_id(self) -> int:
        """ The decimal identifier of the household being loaded. """
        return self._household_id

    @property
    def active_sim_id(self) -> int:
        """ The decimal identifier of the sim being loaded. """
        return self._active_sim_id

    @property
    def game_loaded(self) -> bool:
        """ Determine if the game has loaded. """
        return self._game_loaded

    @property
    def game_loading(self) -> bool:
        """ Determine if the game is loading. """
        return self._game_loading
