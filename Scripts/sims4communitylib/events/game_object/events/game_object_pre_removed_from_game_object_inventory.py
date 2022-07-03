"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.game_object import GameObject
from sims4communitylib.events.event_handling.common_event import CommonEvent
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils


class S4CLGameObjectPreRemovedFromGameObjectInventoryEvent(CommonEvent):
    """S4CLGameObjectPreRemovedFromGameObjectInventoryEvent(game_object, removed_game_object)

    An event that occurs before a Game Object is removed from the inventory of another Game Object.

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
            def handle_event(event_data: S4CLGameObjectPreRemovedFromGameObjectInventoryEvent):
                pass

    :param game_object: The Game Object that changed.
    :type game_object: GameObject
    :param removed_game_object: The Object that was removed from the inventory of the Game Object.
    :type removed_game_object: GameObject
    """

    def __init__(self, game_object: GameObject, removed_game_object: GameObject):
        self._game_object = game_object
        self._removed_game_object = removed_game_object

    @property
    def game_object(self) -> GameObject:
        """The Game Object that is having the Game Object removed from its inventory.

        :return: The Game Object that is having the Game Object removed from its inventory.
        :rtype: GameObject
        """
        return self._game_object

    @property
    def removed_game_object(self) -> GameObject:
        """The Game Object that is being removed.

        :return: The Game Object that is being removed.
        :rtype: GameObject
        """
        return self._removed_game_object

    @property
    def removed_game_object_id(self) -> int:
        """The decimal identifier of the Game Object that is being removed.

        :return: The decimal identifier of the Game Object that is being removed.
        :rtype: int
        """
        return CommonObjectUtils.get_object_id(self.removed_game_object)

    @property
    def removed_game_object_guid(self) -> int:
        """The guid identifier of the Game Object that is being removed.

        :return: The guid identifier of the Game Object that is being removed.
        :rtype: int
        """
        # noinspection PyTypeChecker
        return CommonObjectUtils.get_object_guid(self.removed_game_object)
