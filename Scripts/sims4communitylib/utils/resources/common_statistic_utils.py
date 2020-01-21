"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union
from sims4communitylib.modinfo import ModInfo
from statistics.statistic import Statistic
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4.resources import Types


class CommonStatisticUtils:
    """Utilities for manipulating the Statistics of Sims.

    """
    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=-1.0)
    def get_statistic_initial_value(statistic_id: int) -> float:
        """Retrieve the Initial Value of a Statistic.

        """
        statistic_instance = CommonStatisticUtils._load_statistic_instance(statistic_id)
        if statistic_instance is None:
            return -1.0
        if not hasattr(statistic_instance, 'get_initial_value'):
            return statistic_instance.default_value
        return statistic_instance.get_initial_value()

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=-1.0)
    def get_statistic_min_value(statistic_id: int) -> float:
        """Retrieve the Minimum Value of a Statistic.

        """
        statistic_instance = CommonStatisticUtils._load_statistic_instance(statistic_id)
        if statistic_instance is None:
            return -1.0
        return statistic_instance.min_value

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=-1.0)
    def get_statistic_max_value(statistic_id: int) -> float:
        """Retrieve the Maximum Value of a Statistic.

        """
        statistic_instance = CommonStatisticUtils._load_statistic_instance(statistic_id)
        if statistic_instance is None:
            return -1.0
        return statistic_instance.max_value

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=None)
    def _load_statistic_instance(statistic_id: int) -> Union[Statistic, None]:
        statistic_instance = CommonResourceUtils.load_instance(Types.STATISTIC, statistic_id)
        if statistic_instance is None:
            return None
        return statistic_instance
