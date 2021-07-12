"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event import CommonEvent
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from traits.trait_tracker import TraitTracker
from traits.traits import Trait


class S4CLSimTraitAddedEvent(CommonEvent):
    """S4CLSimTraitAddedEvent(sim_info, trait, trait_tracker)

    An event that occurs when a Trait is added to a Sim.

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
            def handle_event(event_data: S4CLSimTraitAddedEvent):
                pass

    :param sim_info: The Sim that changed.
    :type sim_info: SimInfo
    :param trait: The Trait that was added.
    :type trait: Trait
    :param trait_tracker: The Trait Tracker being added to.
    :type trait_tracker: TraitTracker
    """

    def __init__(self, sim_info: SimInfo, trait: Trait, trait_tracker: TraitTracker):
        self._sim_info = sim_info
        self._trait = trait
        self._trait_tracker = trait_tracker

    @property
    def sim_info(self) -> SimInfo:
        """The Sim that received the trait.

        :return: The Sim that received the trait.
        :rtype: SimInfo
        """
        return self._sim_info

    @property
    def trait(self) -> Trait:
        """The Trait that was added.

        :return: The Trait that was added.
        :rtype: Trait
        """
        return self._trait

    @property
    def trait_tracker(self) -> TraitTracker:
        """The Trait Tracker being added to.

        :return: The Trait Tracker being added to.
        :rtype: TraitTracker
        """
        return self._trait_tracker

    @property
    def trait_id(self) -> int:
        """The decimal identifier of the Trait.

        :return: The decimal identifier of the Trait.
        :rtype: int
        """
        return CommonTraitUtils.get_trait_id(self.trait)
