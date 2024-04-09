"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from relationships.relationship_bit import RelationshipBit
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLSimRelationshipBitAddedEvent(CommonEvent):
    """S4CLSimRelationshipBitAddedEvent(sim_info_a, sim_info_b, relationship_bit)

    An event that occurs when a Relationship Bit is added from Sim A to Sim B.

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
            def handle_event(event_data: S4CLSimRelationshipBitAddedEvent):
                pass

    :param sim_info_a: The Sim with the relationship bit toward Sim B.
    :type sim_info_a: SimInfo
    :param sim_info_b: The Sim with the relationship bit from Sim A.
    :type sim_info_b: SimInfo
    :param relationship_bit: The RelationshipBit that was added.
    :type relationship_bit: RelationshipBit
    """

    def __init__(self, sim_info_a: SimInfo, sim_info_b: SimInfo, relationship_bit: RelationshipBit):
        self._sim_info_a = sim_info_a
        self._sim_info_b = sim_info_b
        self._relationship_bit = relationship_bit

    @property
    def sim_info_a(self) -> SimInfo:
        """The Sim that has a Relationship Bit toward Sim B.

        :return: The Sim that has a Relationship Bit toward Sim B.
        :rtype: SimInfo
        """
        return self._sim_info_a

    @property
    def sim_info_b(self) -> SimInfo:
        """The Sim that has a Relationship Bit from Sim A.

        :return: The Sim that has a Relationship Bit from Sim A.
        :rtype: SimInfo
        """
        return self._sim_info_b

    @property
    def relationship_bit(self) -> RelationshipBit:
        """The RelationshipBit that was added.

        :return: The RelationshipBit that was added.
        :rtype: RelationshipBit
        """
        return self._relationship_bit

    @property
    def relationship_bit_id(self) -> int:
        """The decimal identifier of the RelationshipBit.

        :return: The decimal identifier of the RelationshipBit.
        :rtype: int
        """
        from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
        return CommonRelationshipUtils.get_relationship_bit_guid(self.relationship_bit)
