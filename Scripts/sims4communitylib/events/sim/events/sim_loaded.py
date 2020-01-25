"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLSimLoadedEvent(CommonEvent):
    """S4CLSimLoadedEvent(sim_info)

    An event that occurs after a Sim has been loaded.

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
            def handle_event(event_data: S4CLSimLoadedEvent):
                pass

    :param sim_info: The Sim that was loaded.
    :type sim_info: SimInfo
    """

    def __init__(self, sim_info: SimInfo):
        self._sim_info = sim_info

    @property
    def sim_info(self) -> SimInfo:
        """The Sim that was loaded.

        :return: The Sim that was loaded.
        :rtype: SimInfo
        """
        return self._sim_info
