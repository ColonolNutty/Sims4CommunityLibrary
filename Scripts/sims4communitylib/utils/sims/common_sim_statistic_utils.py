"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator

from objects.components.statistic_component import StatisticComponent
from sims.sim_info import SimInfo
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.resources.common_statistic_utils import CommonStatisticUtils
from statistics.base_statistic import BaseStatistic
from statistics.statistic import Statistic
from statistics.statistic_tracker import StatisticTracker
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler


class CommonGetStatisticTrackerResponse:
    """The response given when requesting a statistic tracker for a Sim.

    """
    def __init__(
        self,
        statistics_tracker: Union[StatisticTracker, None],
        statistic_instance: Union[Statistic, None],
        statistics_component: Union[StatisticComponent, None]
    ):
        self.statistics_tracker = statistics_tracker
        self.statistic_instance = statistic_instance
        self.statistics_component = statistics_component


class CommonSimStatisticUtils:
    """Utilities for manipulating the Statistics of Sims.

    """
    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def has_statistic(sim_info: SimInfo, statistic_id: int) -> bool:
        """Determine if a sim has any of the specified Statistics.

        """
        return CommonSimStatisticUtils.has_statistics(sim_info, (statistic_id,))

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def has_statistics(sim_info: SimInfo, statistic_ids: Iterator[int]) -> bool:
        """Determine if a sim has any of the specified Statistics.

        """
        for statistic_id in statistic_ids:
            response = CommonSimStatisticUtils._get_statistics_tracker(sim_info, statistic_id)
            if response.statistics_tracker is None or response.statistic_instance is None:
                continue
            if response.statistics_tracker.has_statistic(response.statistic_instance):
                return True
        return False

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def is_statistic_locked(sim_info: SimInfo, statistic_id: int, add_dynamic: bool=True, add: bool= False) -> bool:
        """Determine if a statistic is locked for the specified Sim.

        """
        response = CommonSimStatisticUtils._get_statistics_tracker(sim_info, statistic_id, add_dynamic=add_dynamic)
        if response.statistic_instance is None:
            return False
        if response.statistics_tracker is None:
            return False
        statistic = response.statistics_tracker.get_statistic(response.statistic_instance, add=add)
        if statistic is None:
            return False
        return statistic.get_decay_rate_modifier() == 0 or response.statistics_component.is_locked(statistic)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=0.0)
    def get_statistic_level(sim_info: SimInfo, statistic_id: int) -> float:
        """Retrieve the User Value of a Statistic for the specified Sim.

        """
        statistic = CommonSimStatisticUtils.get_statistic(sim_info, statistic_id)
        if statistic is None:
            return 0.0
        return statistic.get_user_value()

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=None)
    def get_statistic(sim_info: SimInfo, statistic_id: int, add_dynamic: bool=True, add: bool=False) -> Union[BaseStatistic, None]:
        """Retrieve a Statistic for the specified Sim.

        """
        if sim_info is None:
            return None
        response = CommonSimStatisticUtils._get_statistics_tracker(sim_info, statistic_id, add_dynamic=add_dynamic)
        if response.statistics_tracker is None or response.statistic_instance is None:
            return None
        return response.statistics_tracker.get_statistic(response.statistic_instance, add=add)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=0.0)
    def get_statistic_value(sim_info: SimInfo, statistic_id: int, add_dynamic: bool=True, add: bool=False) -> float:
        """Retrieve the Value of a Statistic for the specified Sim.

        """
        response = CommonSimStatisticUtils._get_statistics_tracker(sim_info, statistic_id, add_dynamic=add_dynamic)
        statistic_instance = response.statistic_instance
        if statistic_instance is None:
            return -1.0
        if response.statistics_tracker is not None:
            statistic = response.statistics_tracker.get_statistic(statistic_instance, add=add)
            if statistic is not None:
                return statistic.get_value()
        if hasattr(statistic_instance, 'get_initial_value'):
            return statistic_instance.get_initial_value()
        return statistic_instance.default_value

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def set_statistic_value(sim_info: SimInfo, statistic_id: int, value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """Set the Value of a Statistic for the specified Sim.

        """
        if sim_info is None:
            return False
        response = CommonSimStatisticUtils._get_statistics_tracker(sim_info, statistic_id, add_dynamic=add_dynamic)
        if response.statistics_tracker is None or response.statistic_instance is None:
            return False
        response.statistics_tracker.set_value(response.statistic_instance, value, add=add)
        return True

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def set_statistic_user_value(sim_info: SimInfo, statistic_id: int, value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """Set the User Value of a Statistic for the specified Sim.

        """
        if sim_info is None:
            return False
        statistic = CommonSimStatisticUtils.get_statistic(sim_info, statistic_id, add_dynamic=add_dynamic, add=add)
        if statistic is None:
            return False
        return statistic.set_user_value(value)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def add_statistic_value(sim_info: SimInfo, statistic_id: int, value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """Change the Value of a Statistic for the specified Sim.

        """
        if sim_info is None:
            return False
        response = CommonSimStatisticUtils._get_statistics_tracker(sim_info, statistic_id, add_dynamic=add_dynamic)
        if response.statistics_tracker is None or response.statistic_instance is None:
            return False
        response.statistics_tracker.add_value(response.statistic_instance, value, add=add)
        return True

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def remove_statistic(sim_info: SimInfo, statistic_id: int) -> bool:
        """Remove a Statistic from the specified Sim.

        """
        response = CommonSimStatisticUtils._get_statistics_tracker(sim_info, statistic_id)
        if response.statistics_tracker is None or response.statistic_instance is None:
            return False
        response.statistics_tracker.remove_statistic(response.statistic_instance)
        return True

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def add_statistic_modifier(sim_info: SimInfo, statistic_id: int, value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """Add a Modifier to the specified Statistic for the specified Sim.

        """
        if sim_info is None:
            return False
        statistic = CommonSimStatisticUtils.get_statistic(sim_info, statistic_id, add_dynamic=add_dynamic, add=add)
        if statistic is None:
            return False
        statistic.add_statistic_modifier(value)
        return True

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def remove_statistic_modifier(sim_info: SimInfo, statistic_id: int, value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """Remove a Modifier from the specified Statistic for the specified Sim.

        """
        if sim_info is None:
            return False
        statistic = CommonSimStatisticUtils.get_statistic(sim_info, statistic_id, add_dynamic=add_dynamic, add=add)
        if statistic is None:
            return False
        statistic.remove_statistic_modifier(value)
        return True

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def remove_all_statistic_modifiers_for_statistic(sim_info: SimInfo, statistic_id: int, add_dynamic: bool=True, add: bool=True) -> bool:
        """Remove all Modifiers from the specified Statistic for the specified Sim.

        """
        if sim_info is None:
            return False
        statistic = CommonSimStatisticUtils.get_statistic(sim_info, statistic_id, add_dynamic=add_dynamic, add=add)
        if statistic is None:
            return False
        if statistic._statistic_modifiers is None:
            return False
        for value in list(statistic._statistic_modifiers):
            statistic.remove_statistic_modifier(value)
        return True

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=None)
    def _get_statistics_tracker(sim_info: SimInfo, statistic_id: int, add_dynamic: bool=True) -> CommonGetStatisticTrackerResponse:
        if sim_info is None:
            return CommonGetStatisticTrackerResponse(None, None, None)
        statistic_instance = CommonStatisticUtils._load_statistic_instance(statistic_id)
        if statistic_instance is None:
            return CommonGetStatisticTrackerResponse(None, None, None)
        statistics_component: StatisticComponent = CommonComponentUtils.get_component(sim_info, CommonComponentType.STATISTIC, add_dynamic=add_dynamic)
        if statistics_component is None:
            return CommonGetStatisticTrackerResponse(None, statistic_instance, None)
        return CommonGetStatisticTrackerResponse(statistics_component.get_tracker(statistic_instance), statistic_instance, statistics_component)
