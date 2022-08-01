"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims4communitylib.enums.statistics_enum import CommonStatisticId
from statistics.base_statistic import BaseStatistic
from statistics.statistic_instance_manager import StatisticInstanceManager


class CommonStatisticUtils:
    """Utilities for manipulating Statistics.

    """
    @staticmethod
    def get_statistic_initial_value(statistic_id: Union[int, CommonStatisticId, BaseStatistic]) -> float:
        """get_statistic_initial_value(statistic_id)

        Retrieve the Initial Value of a Statistic.

        :param statistic_id: The identifier of the Statistic to use.
        :type statistic_id: Union[int, CommonStatisticId, BaseStatistic]
        :return: The initial value of the statistic.
        :rtype: float
        """
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic_id)
        if statistic_instance is None:
            return -1.0
        if hasattr(statistic_instance, 'get_initial_value'):
            return statistic_instance.get_initial_value()
        return statistic_instance.default_value

    @staticmethod
    def get_statistic_min_value(statistic_id: Union[int, CommonStatisticId, BaseStatistic]) -> float:
        """get_statistic_min_value(statistic_id)

        Retrieve the Minimum Value of a Statistic.

        :param statistic_id: The identifier of the Statistic to use.
        :type statistic_id: Union[int, CommonStatisticId, BaseStatistic]
        :return: The minimum value of the statistic.
        :rtype: float
        """
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic_id)
        if statistic_instance is None:
            return -1.0
        return statistic_instance.min_value

    @staticmethod
    def get_statistic_max_value(statistic_id: Union[int, CommonStatisticId, BaseStatistic]) -> float:
        """get_statistic_max_value(statistic_id)

        Retrieve the Maximum Value of a Statistic.

        :param statistic_id: The identifier of the Statistic to use.
        :type statistic_id: Union[int, CommonStatisticId, BaseStatistic]
        :return: The maximum value of the statistic.
        :rtype: float
        """
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic_id)
        if statistic_instance is None:
            return -1.0
        return statistic_instance.max_value

    @staticmethod
    def get_statistic_id(statistic_identifier: Union[int, BaseStatistic]) -> Union[int, None]:
        """get_statistic_id(statistic_identifier)

        Retrieve the decimal identifier of a Statistic.

        :param statistic_identifier: The identifier or instance of a Statistic.
        :type statistic_identifier: Union[int, BaseStatistic]
        :return: The decimal identifier of the Statistic or None if the Statistic does not have an id.
        :rtype: Union[int, None]
        """
        if isinstance(statistic_identifier, int):
            return statistic_identifier
        if hasattr(statistic_identifier, 'id'):
            return statistic_identifier.id
        return getattr(statistic_identifier, 'guid64', None)

    @staticmethod
    def load_statistic_by_id(statistic_id: Union[int, CommonStatisticId, BaseStatistic]) -> Union[BaseStatistic, None]:
        """load_statistic_by_id(statistic_id)

        Load an instance of a Statistic by its decimal identifier.

        :param statistic_id: The decimal identifier of a Statistic.
        :type statistic_id: Union[int, CommonStatisticId, BaseStatistic]
        :return: An instance of a Statistic matching the decimal identifier or None if not found.
        :rtype: Union[BaseStatistic, None]
        """
        if isinstance(statistic_id, BaseStatistic):
            return statistic_id
        # noinspection PyBroadException
        try:
            # noinspection PyCallingNonCallable
            statistic_instance = statistic_id()
            if isinstance(statistic_instance, BaseStatistic):
                return statistic_id
        except:
            pass
        # noinspection PyBroadException
        try:
            statistic_id: int = int(statistic_id)
        except:
            # noinspection PyTypeChecker
            statistic_id: BaseStatistic = statistic_id
            return statistic_id

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.STATISTIC, statistic_id) or CommonResourceUtils.load_instance(Types.STATIC_COMMODITY, statistic_id)

    @staticmethod
    def get_statistic_instance_manager() -> StatisticInstanceManager:
        """get_statistic_instance_manager()

        Retrieve the manager that manages all Statistics.

        :return: The manager that manages all Statistics.
        :rtype: StatisticInstanceManager
        """
        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        # noinspection PyTypeChecker
        return CommonResourceUtils.get_instance_manager(Types.STATISTIC)
