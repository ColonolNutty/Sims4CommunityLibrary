"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple

from event_testing.resolver import Resolver
from interactions.utils.loot import LootActions
from sims4communitylib.enums.enumtypes.common_int import CommonInt


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
    def apply_loot_actions_by_ids_using_resolver(loot_actions_ids: Tuple[int], resolver: Resolver) -> bool:
        """apply_loot_actions_by_ids_using_resolver(loot_actions_ids, resolver)

        Apply loot actions by their ids using a resolver.

        :param loot_actions_ids: A collection of decimal identifiers of LootActions instances to apply.
        :type loot_actions_ids: Tuple[int]
        :param resolver: A resolver used in various ways by loot actions. The resolver could be a SingleSimResolver, which will attempt to apply the loot to a single Sim, a DoubleSimResolver, which will attempt to apply to two Sims, or various other types of resolvers.
        :type resolver: Resolver
        :return: True, if at least one of the loot actions applied successfully. False, if not.
        :rtype: bool
        """
        has_applied_at_least_one = False
        for loot_actions_id in loot_actions_ids:
            loot_actions = CommonLootActionUtils.load_loot_actions_by_id(loot_actions_id)
            if loot_actions is None:
                continue
            loot_actions.apply_to_resolver(resolver)
            has_applied_at_least_one = True
        return has_applied_at_least_one

    @classmethod
    def combine_loot_actions(cls, loot_action_a: Union[int, CommonInt, LootActions], loot_actions: Tuple[Union[int, CommonInt, LootActions], ...]):
        """combine_loot_actions(loot_action_a, loot_actions)

        Combine Loot Actions into Loot Action A.

        .. note:: Tests are not combined into Loot Action A.

        :param loot_action_a: The loot action to modify.
        :type loot_action_a: Union[int, CommonInt, LootActions]
        :param loot_actions: The loot actions that will be combined into Loot Action A
        :type loot_actions: Tuple[Union[int, CommonInt, LootActions]]
        """
        loot_action: LootActions = CommonLootActionUtils.load_loot_actions_by_id(loot_action_a)
        if loot_action is None:
            return

        if hasattr(loot_action, 'loot_actions') and loot_action.loot_actions:
            loot_actions_to_add_to = list(loot_action.loot_actions)
            for loot_action_id_to_combine in loot_actions:
                loot_action_to_combine: LootActions = CommonLootActionUtils.load_loot_actions_by_id(loot_action_id_to_combine)
                if loot_action_to_combine is None:
                    continue
                if hasattr(loot_action_to_combine, 'loot_actions') and loot_action_to_combine.loot_actions:
                    # noinspection PyUnresolvedReferences
                    loot_actions_to_add_to.extend(list(loot_action_to_combine.loot_actions))
            loot_action.loot_actions = tuple(loot_actions_to_add_to)

        if hasattr(loot_action, 'random_loot_actions') and loot_action.random_loot_actions:
            random_loot_actions_to_add_to = list(loot_action.random_loot_actions)
            for loot_action_id_to_combine in loot_actions:
                loot_action_to_combine: LootActions = CommonLootActionUtils.load_loot_actions_by_id(loot_action_id_to_combine)
                if loot_action_to_combine is None:
                    continue
                if hasattr(loot_action_to_combine, 'random_loot_actions') and loot_action_to_combine.random_loot_actions:
                    # noinspection PyUnresolvedReferences
                    random_loot_actions_to_add_to.extend(list(loot_action_to_combine.random_loot_actions))
            loot_action.random_loot_actions = tuple(random_loot_actions_to_add_to)


    @staticmethod
    def load_loot_actions_by_id(loot_actions_id: Union[int, LootActions]) -> Union[LootActions, None]:
        """load_loot_actions_by_id(loot_actions_id)

        Load a Loot Actions instance by its decimal identifier.

        :param loot_actions_id: The decimal identifier of a LootActions instance.
        :type loot_actions_id: Union[int, LootActions]
        :return: An instance of a Loot Actions matching the decimal identifier or None if not found.
        :rtype: Union[LootActions, None]
        """
        if isinstance(loot_actions_id, LootActions):
            return loot_actions_id
        # noinspection PyBroadException
        try:
            # noinspection PyCallingNonCallable
            loot_actions_instance = loot_actions_id()
            if isinstance(loot_actions_instance, LootActions):
                return loot_actions_id
        except:
            pass
        # noinspection PyBroadException
        try:
            loot_actions_id: int = int(loot_actions_id)
        except:
            loot_actions_id: LootActions = loot_actions_id
            return loot_actions_id

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.ACTION, loot_actions_id)
