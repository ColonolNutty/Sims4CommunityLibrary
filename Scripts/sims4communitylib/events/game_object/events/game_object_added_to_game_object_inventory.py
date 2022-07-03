"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.game_object import GameObject
from sims4communitylib.events.event_handling.common_event import CommonEvent
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils


class S4CLGameObjectAddedToGameObjectInventoryEvent(CommonEvent):
    """S4CLGameObjectAddedToGameObjectInventoryEvent(game_object, added_game_object)

    An event that occurs when a GameObject is added to the inventory of another Game Object.

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
            @CommonEventRegistry.handle_events(ModInfo.get_identity())
            def handle_event(event_data: S4CLGameObjectAddedToGameObjectInventoryEvent):
                pass

    :param game_object: The Game Object that changed.
    :type game_object: GameObject
    :param added_game_object: The Object that was added to the inventory of the Game Object.
    :type added_game_object: GameObject
    """

    def __init__(self, game_object: GameObject, added_game_object: GameObject):
        self._game_object = game_object
        self._added_game_object = added_game_object

    @property
    def game_object(self) -> GameObject:
        """The Game Object that had the Game Object added to its inventory.

        :return: The Game Object that had the Game Object added to its inventory.
        :rtype: GameObject
        """
        return self._game_object

    @property
    def added_game_object(self) -> GameObject:
        """The Game Object that was added.

        :return: The Game Object that was added.
        :rtype: GameObject
        """
        return self._added_game_object

    @property
    def added_game_object_id(self) -> int:
        """The decimal identifier of the Game Object that was added.

        :return: The decimal identifier of the Game Object that was added.
        :rtype: int
        """
        return CommonObjectUtils.get_object_id(self.added_game_object)

    @property
    def added_game_object_guid(self) -> int:
        """The guid identifier of the Game Object that was added.

        :return: The guid identifier of the Game Object that was added.
        :rtype: int
        """
        # noinspection PyTypeChecker
        return CommonObjectUtils.get_object_guid(self.added_game_object)
