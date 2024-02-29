"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Dict, Callable, Iterator

import sims4.collections
from rewards.reward import Reward
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.whims.common_satisfaction_reward_store_item import CommonSatisfactionRewardStoreItem

# noinspection PyBroadException
try:
    from satisfaction.satisfaction_tracker import SatisfactionTracker
except:
    from whims.whims_tracker import WhimsTracker

    SatisfactionTracker = WhimsTracker
    # noinspection PyUnresolvedReferences
    SatisfactionTracker.SatisfactionAwardTypes = WhimsTracker.WhimAwardTypes


class CommonSatisfactionRewardStoreUtils:
    """Utilities for manipulating the Satisfaction Rewards Store.

    """
    @staticmethod
    def add_reward_trait_to_rewards_store(reward_trait_definition_id: int, reward_point_cost: int) -> bool:
        """add_reward_trait_to_rewards_store(reward_trait_definition_id, reward_point_cost)

        Add a Reward Trait to the Satisfaction Rewards Store.

        :param reward_trait_definition_id: The decimal identifier of a Reward Trait.
        :type reward_trait_definition_id: int
        :param reward_point_cost: The amount of Satisfaction Reward Points the Reward Trait will cost the Sim to receive.
        :type reward_point_cost: int
        :return: True, if the Trait was added to the Rewards Store successfully. False, if not.
        :rtype: bool
        """
        return CommonSatisfactionRewardStoreUtils._add_reward_to_rewards_store(reward_trait_definition_id, reward_point_cost, SatisfactionTracker.SatisfactionAwardTypes.TRAIT)

    @staticmethod
    def add_reward_buff_to_rewards_store(reward_buff_definition_id: int, reward_point_cost: int) -> bool:
        """add_reward_buff_to_rewards_store(reward_buff_definition_id, reward_point_cost)

        Add a Reward Buff to the Satisfaction Rewards Store.

        :param reward_buff_definition_id: The decimal identifier of a Reward Buff.
        :type reward_buff_definition_id: int
        :param reward_point_cost: The amount of Satisfaction Reward Points the Reward Buff will cost the Sim to receive.
        :type reward_point_cost: int
        :return: True, if the Reward Buff was added to the Rewards Store successfully. False, if not.
        :rtype: bool
        """
        return CommonSatisfactionRewardStoreUtils._add_reward_to_rewards_store(reward_buff_definition_id, reward_point_cost, SatisfactionTracker.SatisfactionAwardTypes.BUFF)

    @staticmethod
    def add_reward_object_to_rewards_store(reward_object_definition_id: int, reward_point_cost: int) -> bool:
        """add_reward_object_to_rewards_store(reward_object_definition_id, reward_point_cost)

        Add a Reward Object to the Satisfaction Rewards Store.

        :param reward_object_definition_id: The decimal identifier of a Reward Object.
        :type reward_object_definition_id: int
        :param reward_point_cost: The amount of Satisfaction Reward Points the Reward Object will cost the Sim to receive.
        :type reward_point_cost: int
        :return: True, if the Reward Object was added to the Rewards Store successfully. False, if not.
        :rtype: bool
        """
        return CommonSatisfactionRewardStoreUtils._add_reward_to_rewards_store(reward_object_definition_id, reward_point_cost, SatisfactionTracker.SatisfactionAwardTypes.OBJECT)

    @staticmethod
    def add_reward_cas_part_to_rewards_store(reward_cas_part_definition_id: int, reward_point_cost: int) -> bool:
        """add_reward_cas_part_to_rewards_store(reward_cas_part_definition_id, reward_point_cost)

        Add a Reward CAS Part to the Satisfaction Rewards Store.

        :param reward_cas_part_definition_id: The decimal identifier of a Reward CAS Part.
        :type reward_cas_part_definition_id: int
        :param reward_point_cost: The amount of Satisfaction Reward Points the Reward CAS Part will cost the Sim to receive.
        :type reward_point_cost: int
        :return: True, if the Reward CAS Part was added to the Rewards Store successfully. False, if not.
        :rtype: bool
        """
        return CommonSatisfactionRewardStoreUtils._add_reward_to_rewards_store(reward_cas_part_definition_id, reward_point_cost, SatisfactionTracker.SatisfactionAwardTypes.CASPART)

    @staticmethod
    def remove_reward_from_rewards_store(reward_item_definition_id: int) -> bool:
        """remove_reward_from_rewards_store(reward_item_definition_id)

        Remove a Reward Item from the Satisfaction Rewards Store.

        :param reward_item_definition_id: The decimal identifier of a Reward Item.
        :type reward_item_definition_id: int
        :return: True, if the Reward Item was removed from the Rewards Store successfully. False, if not.
        :rtype: bool
        """
        return CommonSatisfactionRewardStoreUtils._remove_reward_from_rewards_store(reward_item_definition_id)

    @staticmethod
    def get_all_satisfaction_reward_store_items_generator(
        include_satisfaction_reward_callback: Callable[[CommonSatisfactionRewardStoreItem], bool]=None
    ) -> Iterator[CommonSatisfactionRewardStoreItem]:
        """get_all_satisfaction_reward_store_items_generator(include_satisfaction_reward_callback=None)

        Retrieve all Satisfaction Rewards in the Satisfaction Rewards Store.

        :param include_satisfaction_reward_callback: If the result of this callback is True, the Satisfaction Reward\
         and Satisfaction Reward Data (Cost, Award Type), will be included in the results. If set to None, All Satisfaction Rewards will be included.
        :type include_satisfaction_reward_callback: Callable[[CommonRewardStoreItem]], bool], optional
        :return: All items from the satisfaction reward store.
        :rtype: Iterator[CommonSatisfactionRewardStoreItem]
        """
        satisfaction_reward_store_items: Dict[Reward, Tuple[int, SatisfactionTracker.SatisfactionAwardTypes]] = dict(SatisfactionTracker.SATISFACTION_STORE_ITEMS)
        for (reward, data) in satisfaction_reward_store_items.items():
            reward_cost = data.cost
            reward_type = CommonResourceUtils.get_enum_by_int_value(int(data.award_type), SatisfactionTracker.SatisfactionAwardTypes, default_value=None)
            reward_store_item = CommonSatisfactionRewardStoreItem(reward, reward_cost, reward_type)
            if include_satisfaction_reward_callback is not None and not include_satisfaction_reward_callback(reward_store_item):
                continue
            yield reward_store_item

    @staticmethod
    def _add_reward_to_rewards_store(reward_definition_id: int, reward_point_cost: int, reward_type: SatisfactionTracker.SatisfactionAwardTypes) -> bool:
        sim_reward_instance = CommonSatisfactionRewardStoreUtils._load_reward_instance(reward_definition_id)
        if sim_reward_instance is None:
            return False
        sim_reward_data_immutable_slots_cls = sims4.collections.make_immutable_slots_class(['cost', 'award_type'])
        reward_data = sim_reward_data_immutable_slots_cls(dict(cost=reward_point_cost, award_type=reward_type))
        store_items = dict(SatisfactionTracker.SATISFACTION_STORE_ITEMS)
        store_items[sim_reward_instance] = reward_data
        SatisfactionTracker.SATISFACTION_STORE_ITEMS = sims4.collections.FrozenAttributeDict(store_items)
        return True

    @staticmethod
    def _remove_reward_from_rewards_store(reward_definition_id: int) -> bool:
        sim_reward_instance = CommonSatisfactionRewardStoreUtils._load_reward_instance(reward_definition_id)
        if sim_reward_instance is None:
            return False
        store_items = dict(SatisfactionTracker.SATISFACTION_STORE_ITEMS)
        if sim_reward_instance in store_items:
            del store_items[sim_reward_instance]
            SatisfactionTracker.SATISFACTION_STORE_ITEMS = sims4.collections.FrozenAttributeDict(store_items)
        return True

    @staticmethod
    def _load_reward_instance(reward_definition_id: int) -> Reward:
        if isinstance(reward_definition_id, Reward):
            return reward_definition_id
        # noinspection PyBroadException
        try:
            # noinspection PyCallingNonCallable
            reward_definition_id_instance = reward_definition_id()
            if isinstance(reward_definition_id_instance, Reward):
                # noinspection PyTypeChecker
                return reward_definition_id
        except:
            pass
        # noinspection PyBroadException
        try:
            reward_definition_id: int = int(reward_definition_id)
        except:
            # noinspection PyTypeChecker
            reward_definition_id: Reward = reward_definition_id
            return reward_definition_id

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.REWARD, reward_definition_id)
