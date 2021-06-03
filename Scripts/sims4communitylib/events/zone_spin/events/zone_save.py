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
    """S4CLZoneSaveEvent(zone, save_slot_data=None, game_loaded=False, game_loading=False)

    An event that occurs upon a Zone being saved (Before it has been saved).

    .. note:: This event can occur when the Player is saving the game, switching save files, or traveling to a new zone.

    .. warning:: This event will also occur when the Player closes the game without saving.

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
            def handle_event(event_data: S4CLZoneSaveEvent):
                pass

    :param zone: The Zone being saved.
    :type zone: Zone
    :param save_slot_data: The data that will be saved.
    :type save_slot_data: Any
    :param game_loaded: A value indicating if the game has been loaded.
    :type game_loaded: bool
    :param game_loading: A value indicating if the game is currently loading.
    :type game_loading: bool
    """

    def __init__(self, zone: Zone, save_slot_data: Any=None, game_loaded: bool=False, game_loading: bool=False):
        self._zone = zone
        self._save_slot_data = save_slot_data
        self._game_loaded = game_loaded
        self._game_loading = game_loading

    @property
    def zone(self) -> Zone:
        """The Zone being saved.

        :return: The Zone being saved.
        :rtype: Zone
        """
        return self._zone

    @property
    def save_slot_data(self) -> Any:
        """The data that will be saved.

        :return: The data that will be saved.
        :rtype: Any
        """
        return self._save_slot_data

    @property
    def game_loaded(self) -> bool:
        """Determine if the game has loaded.

        :return: True, if the game has loaded. False, if the game has not loaded.
        :rtype: bool
        """
        return self._game_loaded

    @property
    def game_loading(self) -> bool:
        """Determine if the game is loading.

        :return: True, if the game is currently loading. False, if the game is not currently loading.
        :rtype: bool
        """
        return self._game_loading
