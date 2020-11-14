"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from buffs.buff import Buff
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event import CommonEvent
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils


class S4CLSimBuffAddedEvent(CommonEvent):
    """S4CLSimBuffAddedEvent(sim_info, buff)

    An event that occurs when a Buff is added to a Sim.

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
            def handle_event(event_data: S4CLSimBuffAddedEvent):
                pass

    :param sim_info: The Sim that changed.
    :type sim_info: SimInfo
    :param buff: The Buff that was added.
    :type buff: Buff
    """

    def __init__(self, sim_info: SimInfo, buff: Buff):
        self._sim_info = sim_info
        self._buff = buff

    @property
    def sim_info(self) -> SimInfo:
        """The Sim that received the buff.

        :return: The Sim that received the buff.
        :rtype: SimInfo
        """
        return self._sim_info

    @property
    def buff(self) -> Buff:
        """The Buff that was added.

        :return: The Buff that was added.
        :rtype: Buff
        """
        return self._buff

    @property
    def buff_id(self) -> int:
        """The decimal identifier of the Buff.

        :return: The decimal identifier of the Buff.
        :rtype: int
        """
        return CommonBuffUtils.get_buff_id(self.buff)
