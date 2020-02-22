"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from rewards.reward import Reward
from whims.whims_tracker import WhimsTracker


class CommonSatisfactionRewardStoreItem:
    """CommonSatisfactionRewardStoreItem(reward, reward_cost, reward_type)

    A wrapper for Reward Store Items.

    :param reward: An instance of a Reward.
    :type reward: Reward
    :param reward_cost: The amount of Satisfaction Reward Points the Reward costs.
    :type reward_cost: int
    :param reward_type: The type of the Reward.
    :type reward_type: WhimsTracker.WhimAwardTypes
    """
    def __init__(self, reward: Reward, reward_cost: int, reward_type: WhimsTracker.WhimAwardTypes):
        self.reward = reward
        self.reward_cost = reward_cost
        self.reward_type = reward_type
