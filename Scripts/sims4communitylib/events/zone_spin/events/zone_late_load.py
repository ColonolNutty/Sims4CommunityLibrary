"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.events.event_handling.common_event import CommonEvent
from zone import Zone


class S4CLZoneLateLoadEvent(CommonEvent):
    """S4CLZoneLateLoadEvent(zone, household_id, active_sim_id, game_loaded=False, game_loading=False)

    An event that occurs when a Zone has finished spinning up.

    .. note:: This event occurs after the :class:`.S4CLZoneEarlyLoadEvent`

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
            def handle_event(event_data: S4CLZoneLateLoadEvent):
                pass

    :param zone: The Zone that has finished spinning up.
    :type zone: Zone
    :param household_id: The identifier of the Household that owns the Zone.
    :type household_id: int
    :param active_sim_id: The identifier of the Active Sim.
    :type active_sim_id: int
    :param game_loaded: A value indicating if the game has been loaded.
    :type game_loaded: bool
    :param game_loading: A value indicating if the game is currently loading.
    :type game_loading: bool
    """

    def __init__(self, zone: Zone, household_id: int, active_sim_id: int, game_loaded: bool=False, game_loading: bool=False):
        self._zone = zone
        self._household_id = household_id
        self._active_sim_id = active_sim_id
        self._game_loaded = game_loaded
        self._game_loading = game_loading

    @property
    def zone(self) -> Zone:
        """The Zone that has finished spinning up.

        :return: The Zone that has finished spinning up.
        :rtype: Zone
        """
        return self._zone

    @property
    def household_id(self) -> int:
        """The identifier of the Household that owns the Zone.

        :return: The identifier of the Household that owns the Zone.
        :rtype: int
        """
        return self._household_id

    @property
    def active_sim_id(self) -> int:
        """The identifier of the Active Sim.

        :return: The identifier of the Active Sim.
        :rtype: int
        """
        return self._active_sim_id

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
