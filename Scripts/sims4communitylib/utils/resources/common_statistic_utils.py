"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims4communitylib.enums.statistics_enum import CommonStatisticId
from statistics.statistic import Statistic
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4.resources import Types


class CommonStatisticUtils:
    """Utilities for manipulating Statistics.

    """
    @staticmethod
    def get_statistic_initial_value(statistic_id: Union[int, CommonStatisticId]) -> float:
        """get_statistic_initial_value(statistic_id)

        Retrieve the Initial Value of a Statistic.

        :param statistic_id: The identifier of the Statistic to use.
        :type statistic_id: Union[int, CommonStatisticId]
        :return: The initial value of the statistic.
        :rtype: float
        """
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic_id)
        if statistic_instance is None:
            return -1.0
        if not hasattr(statistic_instance, 'get_initial_value'):
            return statistic_instance.default_value
        return statistic_instance.get_initial_value()

    @staticmethod
    def get_statistic_min_value(statistic_id: Union[int, CommonStatisticId]) -> float:
        """get_statistic_min_value(statistic_id)

        Retrieve the Minimum Value of a Statistic.

        :param statistic_id: The identifier of the Statistic to use.
        :type statistic_id: Union[int, CommonStatisticId]
        :return: The minimum value of the statistic.
        :rtype: float
        """
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic_id)
        if statistic_instance is None:
            return -1.0
        return statistic_instance.min_value

    @staticmethod
    def get_statistic_max_value(statistic_id: Union[int, CommonStatisticId]) -> float:
        """get_statistic_max_value(statistic_id)

        Retrieve the Maximum Value of a Statistic.

        :param statistic_id: The identifier of the Statistic to use.
        :type statistic_id: Union[int, CommonStatisticId]
        :return: The maximum value of the statistic.
        :rtype: float
        """
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic_id)
        if statistic_instance is None:
            return -1.0
        return statistic_instance.max_value

    @staticmethod
    def load_statistic_by_id(statistic_id: Union[int, CommonStatisticId]) -> Union[Statistic, None]:
        """load_statistic(statistic_id)

        Load an instance of a Statistic by its decimal identifier.

        :param statistic_id: The decimal identifier of a Statistic.
        :type statistic_id: Union[int, CommonStatisticId]
        :return: An instance of a Statistic matching the decimal identifier or None if not found.
        :rtype: Union[Statistic, None]
        """
        return CommonResourceUtils.load_instance(Types.STATISTIC, statistic_id)
