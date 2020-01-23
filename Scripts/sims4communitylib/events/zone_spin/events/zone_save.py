"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from sims4communitylib.events.event_handling.common_event import CommonEvent
from zone import Zone


class S4CLZoneSaveEvent(CommonEvent):
    """An Event that Occurs upon zone save.

    """
    def __init__(self, zone: Zone, save_slot_data: Any=None, game_loaded: bool=False, game_loading: bool=False):
        self._zone = zone
        self._save_slot_data = save_slot_data
        self._game_loaded = game_loaded
        self._game_loading = game_loading

    @property
    def zone(self) -> Zone:
        """The zone being saved.

        """
        return self._zone

    @property
    def save_slot_data(self) -> Any:
        """Data pertaining to the save slot.

        """
        return self._save_slot_data

    @property
    def game_loaded(self) -> bool:
        """Determine if the game has loaded.

        """
        return self._game_loaded

    @property
    def game_loading(self) -> bool:
        """Determine if the game is loading.

        """
        return self._game_loading
