"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from server.client import Client
from sims4communitylib.events.event_handling.common_event import CommonEvent
from zone import Zone


class S4CLZoneTeardownEvent(CommonEvent):
    """An Event that Occurs upon zone teardown.

    """
    def __init__(self, zone: Zone, client: Client, game_loaded: bool=False, game_loading: bool=False):
        self._zone = zone
        self._client = client
        self._game_loaded = game_loaded
        self._game_loading = game_loading

    @property
    def zone(self) -> Zone:
        """The zone teardown is occurring on.

        """
        return self._zone

    @property
    def client(self) -> Client:
        """A reference to the client.

        """
        return self._client

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
