"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from server.client import Client
from sims4communitylib.events.event_handling.common_event import CommonEvent
from zone import Zone


class S4CLZoneTeardownEvent(CommonEvent):
    """S4CLZoneTeardownEvent(zone, client, game_loaded=False, game_loading=False)

    An event that occurs upon a Zone being saved (Before it has been torn down).

    .. note:: This event can occur when the Player travels to another lot.

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
            def handle_event(event_data: S4CLZoneTeardownEvent):
                pass

    :param zone: The Zone being torn down.
    :type zone: Zone
    :param client: An instance of the Client.
    :type client: Client
    :param game_loaded: A value indicating if the game has been loaded.
    :type game_loaded: bool
    :param game_loading: A value indicating if the game is currently loading.
    :type game_loading: bool
    """

    def __init__(self, zone: Zone, client: Client, game_loaded: bool=False, game_loading: bool=False):
        self._zone = zone
        self._client = client
        self._game_loaded = game_loaded
        self._game_loading = game_loading

    @property
    def zone(self) -> Zone:
        """The Zone being torn down.

        :return: The Zone being torn down.
        :rtype: Zone
        """
        return self._zone

    @property
    def client(self) -> Client:
        """An instance of the Client.

        :return: An instance of the Client.
        :rtype: Client
        """
        return self._client

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
