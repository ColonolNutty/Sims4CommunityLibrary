"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.events.event_handling.common_event import CommonEvent
from zone import Zone


class S4CLZonePostLoadEvent(CommonEvent):
    """S4CLZonePostLoadEvent(zone, game_loaded=False, game_loading=False)

    An event that occurs when the Zone has finished loading and the loading screen is no longer visible.

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
            def handle_event(event_data: S4CLZonePostLoadEvent):
                pass

    :param zone: The Zone that was loaded.
    :type zone: Zone
    :param game_loaded: A value indicating if the game has been loaded.
    :type game_loaded: bool
    :param game_loading: A value indicating if the game is currently loading.
    :type game_loading: bool
    """

    def __init__(self, zone: Zone, game_loaded: bool=False, game_loading: bool=False):
        self._zone = zone
        self._game_loaded = game_loaded
        self._game_loading = game_loading

    @property
    def zone(self) -> Zone:
        """The Zone that was loaded.

        :return: The Zone that was loaded.
        :rtype: Zone
        """
        return self._zone

    @property
    def game_loaded(self) -> bool:
        """Determine if the game has loaded at least once.

        :return: True, if the game has loaded at least once. False, if the game has not loaded.
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
