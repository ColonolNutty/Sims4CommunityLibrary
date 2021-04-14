"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from event_testing.resolver import Resolver
from interactions.utils.loot import LootActions


class CommonLootActionUtils:
    """Utilities for manipulating Loot Actions."""
    @staticmethod
    def apply_loot_actions_using_resolver(loot_actions: LootActions, resolver: Resolver) -> bool:
        """apply_loot_actions_using_resolver(loot_actions, resolver)

        Apply loot actions using a resolver.

        :param loot_actions: The loot actions to apply.
        :type loot_actions: LootActions
        :param resolver: A resolver used in various ways by loot actions. The resolver could be a SingleSimResolver, which will attempt to apply the loot to a single Sim, a DoubleSimResolver, which will attempt to apply to two Sims, or various other types of resolvers.
        :type resolver: Resolver
        :return: True, if the loot actions applied successfully. False, if not.
        :rtype: bool
        """
        if loot_actions is None:
            return False
        loot_actions.apply_to_resolver(resolver)
        return True

    @staticmethod
    def apply_loot_actions_by_id_using_resolver(loot_actions_id: int, resolver: Resolver) -> bool:
        """apply_loot_actions_by_id_using_resolver(loot_actions_id, resolver)

        Apply loot actions by id using a resolver.

        :param loot_actions_id: The decimal identifier of a loot actions instance to apply.
        :type loot_actions_id: int
        :param resolver: A resolver used in various ways by loot actions. The resolver could be a SingleSimResolver, which will attempt to apply the loot to a single Sim, a DoubleSimResolver, which will attempt to apply to two Sims, or various other types of resolvers.
        :type resolver: Resolver
        :return: True, if the loot actions applied successfully. False, if not.
        :rtype: bool
        """
        loot_actions = CommonLootActionUtils.load_loot_actions_by_id(loot_actions_id)
        if loot_actions is None:
            return False
        loot_actions.apply_to_resolver(resolver)
        return True

    @staticmethod
    def load_loot_actions_by_id(loot_id: int) -> Union[LootActions, None]:
        """load_loot_actions_by_id(loot_id)

        Load a Loot Actions instance by its decimal identifier.

        :param loot_id: The decimal identifier of a LootActions instance.
        :type loot_id: int
        :return: An instance of a Loot Actions matching the decimal identifier or None if not found.
        :rtype: Union[LootActions, None]
        """
        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.ACTION, loot_id)
