"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLSimChangedGenderEvent(CommonEvent):
    """S4CLSimChangedGenderEvent(sim_info, old_gender, new_gender)

    An event that occurs when a Sim has changed their current gender.

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
            def handle_event(event_data: S4CLSimChangedGenderEvent):
                pass

    :param sim_info: The Sim that changed.
    :type sim_info: SimInfo
    :param old_gender: The gender the Sim has changed from.
    :type old_gender: CommonGender
    :param new_gender: The gender the Sim has changed to.
    :type new_gender: CommonGender
    """

    def __init__(self, sim_info: SimInfo, old_gender: CommonGender, new_gender: CommonGender):
        self._sim_info = sim_info
        self._old_gender = old_gender
        self._new_gender = new_gender

    @property
    def sim_info(self) -> SimInfo:
        """The Sim that changed."""
        return self._sim_info

    @property
    def old_gender(self) -> CommonGender:
        """The gender the Sim has changed from."""
        return self._old_gender

    @property
    def new_gender(self) -> CommonGender:
        """The gender the Sim has changed to."""
        return self._new_gender
