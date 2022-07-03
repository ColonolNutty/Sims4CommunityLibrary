"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.game_object import GameObject
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event import CommonEvent
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils


class S4CLGameObjectAddedToSimInventoryEvent(CommonEvent):
    """S4CLGameObjectAddedToSimInventoryEvent(sim_info, added_game_object)

    An event that occurs when a Game Object is added to the inventory of a Sim.

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
            def handle_event(event_data: S4CLGameObjectAddedToSimInventoryEvent):
                pass

    :param sim_info: The Sim that changed.
    :type sim_info: SimInfo
    :param added_game_object: The Game Object that was added to the inventory of the Sim.
    :type added_game_object: GameObject
    """

    def __init__(self, sim_info: SimInfo, added_game_object: GameObject):
        self._sim_info = sim_info
        self._added_game_object = added_game_object

    @property
    def sim_info(self) -> SimInfo:
        """The Sim that received the added object.

        :return: The Sim that received the added object.
        :rtype: SimInfo
        """
        return self._sim_info

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
    def added_object_guid(self) -> int:
        """The guid identifier of the Game Object that was added.

        :return: The guid identifier of the Game Object that was added.
        :rtype: int
        """
        return CommonObjectUtils.get_object_guid(self.added_game_object)
