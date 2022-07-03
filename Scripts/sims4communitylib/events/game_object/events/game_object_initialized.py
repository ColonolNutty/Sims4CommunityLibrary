"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.game_object import GameObject
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLGameObjectInitializedEvent(CommonEvent):
    """S4CLGameObjectInitializedEvent(game_object)

    An event that occurs after a Game Object has been initialized.

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
            def handle_event(event_data: S4CLGameObjectInitializedEvent):
                pass

    :param game_object: The Game Object that was initialized.
    :type game_object: GameObject
    """

    def __init__(self, game_object: GameObject):
        self._game_object = game_object

    @property
    def game_object(self) -> GameObject:
        """The Game Object that was initialized.

        :return: The Game Object that was initialized.
        :rtype: GameObject
        """
        return self._game_object
