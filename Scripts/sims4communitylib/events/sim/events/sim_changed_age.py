"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims.sim_info_types import Age
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLSimChangedAgeEvent(CommonEvent):
    """S4CLSimChangedAgeEvent(sim_info, old_age, new_age)

    An event that occurs when a Sim has changed their current Age.

    .. note:: This can occur when an Adult Sim becomes an Elder Sim or an Elder Sim becomes an Adult Sim.

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
            def handle_event(event_data: S4CLSimChangedAgeEvent):
                pass

    :param sim_info: The Sim that changed Ages.
    :type sim_info: SimInfo
    :param old_age: The Age the Sim has changed from.
    :type old_age: Age
    :param new_age: The Age the Sim has changed to.
    :type new_age: Age
    """

    def __init__(self, sim_info: SimInfo, old_age: Age, new_age: Age):
        self._sim_info = sim_info
        self._old_age = old_age
        self._new_age = new_age

    @property
    def sim_info(self) -> SimInfo:
        """The Sim that changed Ages.

        :return: The Sim that changed Ages.
        :rtype: SimInfo
        """
        return self._sim_info

    @property
    def old_age(self) -> Age:
        """The Age the Sim has changed from.

        :return: The Age the Sim has changed from.
        :rtype: Age
        """
        return self._old_age

    @property
    def new_age(self) -> Age:
        """The Age the Sim has changed to.

        :return: The Age the Sim has changed to.
        :rtype: Age
        """
        return self._new_age
