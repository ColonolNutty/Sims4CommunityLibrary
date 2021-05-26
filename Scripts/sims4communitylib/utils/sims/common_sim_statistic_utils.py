"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator
from objects.components.statistic_component import StatisticComponent
from server_commands.argument_helpers import TunableInstanceParam, OptionalTargetParam
from sims.sim_info import SimInfo
from sims4.commands import Command, CommandType, CheatOutput
from sims4.resources import Types
from sims4communitylib.enums.statistics_enum import CommonStatisticId
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.resources.common_statistic_utils import CommonStatisticUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from statistics.base_statistic import BaseStatistic
from statistics.statistic import Statistic
from statistics.statistic_tracker import StatisticTracker


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
    def has_statistic(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, Statistic]) -> bool:
        """has_statistic(sim_info, statistic)

        Determine if a sim has any of the specified Statistics.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to check.
        :type statistic: Union[int, CommonStatisticId, Statistic]
        :return: True, if the Sim has any of the statistics. False, if not.
        :rtype: bool
        """
        return CommonSimStatisticUtils.has_statistics(sim_info, (statistic,))

    @staticmethod
    def has_statistics(sim_info: SimInfo, statistics: Iterator[Union[int, CommonStatisticId, Statistic]]) -> bool:
        """has_statistics(sim_info, statistics)

        Determine if a sim has any of the specified Statistics.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistics: An iterator of identifiers for statistics to check.
        :type statistics: Iterator[Union[int, CommonStatisticId, Statistic]]
        :return: True, if the Sim has any of the statistics. False, if not.
        :rtype: bool
        """
        for statistic in statistics:
            response = CommonSimStatisticUtils._get_statistics_tracker(sim_info, statistic)
            if response.statistics_tracker is None or response.statistic_instance is None:
                continue
            if response.statistics_tracker.has_statistic(response.statistic_instance):
                return True
        return False

    @staticmethod
    def is_statistic_locked(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, Statistic], add_dynamic: bool=True, add: bool= False) -> bool:
        """is_statistic_locked(sim_info, statistic, add_dynamic=True, add=False)

        Determine if a statistic is locked for the specified Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to check.
        :type statistic: Union[int, CommonStatisticId, Statistic]
        :param add_dynamic: Add the statistic components to the Sim.
        :type add_dynamic: bool, optional
        :param add: Add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if the statistic is locked. False, if not.
        :rtype: bool
        """
        response = CommonSimStatisticUtils._get_statistics_tracker(sim_info, statistic, add_dynamic=add_dynamic)
        if response.statistic_instance is None:
            return False
        if response.statistics_tracker is None:
            return False
        statistic_instance = response.statistics_tracker.get_statistic(response.statistic_instance, add=add)
        if statistic_instance is None:
            return False
        return statistic_instance.get_decay_rate_modifier() == 0 or response.statistics_component.is_locked(statistic_instance)

    @staticmethod
    def get_statistic_level(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, Statistic]) -> float:
        """get_statistic_level(sim_info, statistic)

        Retrieve the User Value of a Statistic for the specified Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to retrieve the user value of.
        :type statistic: Union[int, CommonStatisticId, Statistic]
        :return: The value of the statistic, `-1.0` if the statistic is not found, or `0.0` if a problem occurs.
        :rtype: float
        """
        statistic_instance = CommonSimStatisticUtils.get_statistic(sim_info, statistic)
        if statistic_instance is None:
            return 0.0
        return statistic_instance.get_user_value()

    @staticmethod
    def get_statistic(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, Statistic], add_dynamic: bool=True, add: bool=False) -> Union[BaseStatistic, None]:
        """get_statistic(sim_info, statistic, statistic, add_dynamic=True, add=False)

        Retrieve a Statistic for the specified Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to retrieve of.
        :type statistic: Union[int, CommonStatisticId, Statistic]
        :param add_dynamic: Add the statistic components to the Sim.
        :type add_dynamic: bool, optional
        :param add: Add the statistic to the Sim.
        :type add: bool, optional
        :return: An instance of the statistic or None if a problem occurs.
        :rtype: Union[BaseStatistic, None]
        """
        if sim_info is None:
            return None
        response = CommonSimStatisticUtils._get_statistics_tracker(sim_info, statistic, add_dynamic=add_dynamic)
        if response.statistics_tracker is None or response.statistic_instance is None:
            return None
        return response.statistics_tracker.get_statistic(response.statistic_instance, add=add)

    @staticmethod
    def get_statistic_value(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, Statistic], add_dynamic: bool=True, add: bool=False) -> float:
        """get_statistic_value(sim_info, statistic, add_dynamic=True, add=False)

        Retrieve the Value of a Statistic for the specified Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to retrieve the value of.
        :type statistic: Union[int, CommonStatisticId, Statistic]
        :param add_dynamic: Add the statistic components to the Sim.
        :type add_dynamic: bool, optional
        :param add: Add the statistic to the Sim.
        :type add: bool, optional
        :return: The value of the statistic, `-1.0` if the statistic is not found, or `0.0` if a problem occurs.
        :rtype: float
        """
        response = CommonSimStatisticUtils._get_statistics_tracker(sim_info, statistic, add_dynamic=add_dynamic)
        statistic_instance = response.statistic_instance
        if statistic_instance is None:
            return -1.0
        if response.statistics_tracker is not None:
            statistic_of_sim = response.statistics_tracker.get_statistic(statistic_instance, add=add)
            if statistic_of_sim is not None:
                return statistic_of_sim.get_value()
        if hasattr(statistic_instance, 'get_initial_value'):
            return statistic_instance.get_initial_value()
        return statistic_instance.default_value

    @staticmethod
    def set_statistic_value(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, Statistic], value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """set_statistic_value(sim_info, statistic, value, add_dynamic=True, add=True)

        Set the Value of a Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to add a value to.
        :type statistic: Union[int, CommonStatisticId, Statistic]
        :param value: The amount to add.
        :type value: float
        :param add_dynamic: Add the statistic components to the Sim.
        :type add_dynamic: bool, optional
        :param add: Add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if sim_info is None:
            return False
        if CommonSimStatisticUtils.is_statistic_locked(sim_info, statistic):
            return False
        response = CommonSimStatisticUtils._get_statistics_tracker(sim_info, statistic, add_dynamic=add_dynamic)
        if response.statistics_tracker is None or response.statistic_instance is None:
            return False
        response.statistics_tracker.set_value(response.statistic_instance, value, add=add)
        return True

    @staticmethod
    def set_statistic_user_value(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, Statistic], value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """set_statistic_user_value(sim_info, statistic, value, add_dynamic=True, add=True)

        Set the User Value of a Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to add a user value to.
        :type statistic: Union[int, CommonStatisticId, Statistic]
        :param value: The amount to add.
        :type value: float
        :param add_dynamic: Add the statistic components to the Sim.
        :type add_dynamic: bool, optional
        :param add: Add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if sim_info is None:
            return False
        statistic_instance = CommonSimStatisticUtils.get_statistic(sim_info, statistic, add_dynamic=add_dynamic, add=add)
        if statistic_instance is None:
            return False
        return statistic_instance.set_user_value(value)

    @staticmethod
    def add_statistic_value(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, Statistic], value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """add_statistic_value(sim_info, statistic, value, add_dynamic=True, add=True)

        Change the Value of a Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to add a value to.
        :type statistic: Union[int, CommonStatisticId, Statistic]
        :param value: The amount to add.
        :type value: float
        :param add_dynamic: Add the statistic components to the Sim.
        :type add_dynamic: bool, optional
        :param add: Add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if sim_info is None:
            return False
        if isinstance(statistic, int) or isinstance(statistic, CommonStatisticId):
            statistic = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic is None:
            return False
        if not isinstance(statistic, Statistic):
            return False
        if CommonSimStatisticUtils.is_statistic_locked(sim_info, statistic):
            return False
        response = CommonSimStatisticUtils._get_statistics_tracker(sim_info, statistic, add_dynamic=add_dynamic)
        if response.statistics_tracker is None or response.statistic_instance is None:
            return False
        response.statistics_tracker.add_value(response.statistic_instance, value, add=add)
        return True

    @staticmethod
    def remove_statistic(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, Statistic]) -> bool:
        """remove_statistic(sim_info, statistic)

        Remove a Statistic from the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to remove.
        :type statistic: Union[int, CommonStatisticId, Statistic]
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if isinstance(statistic, int) or isinstance(statistic, CommonStatisticId):
            statistic = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic is None:
            return False
        if not isinstance(statistic, Statistic):
            return False
        tracker = sim_info.get_tracker(statistic)
        tracker.remove_statistic(statistic)
        return True

    @staticmethod
    def add_statistic_modifier(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, Statistic], value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """add_statistic_modifier(sim_info, statistic, value, add_dynamic=True, add=True)

        Add a Modifier to the specified Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic containing the modifier.
        :type statistic: Union[int, CommonStatisticId, Statistic]
        :param value: The modifier to add.
        :type value: float
        :param add_dynamic: Add the statistic components to the Sim.
        :type add_dynamic: bool, optional
        :param add: Add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if sim_info is None:
            return False
        statistic_instance = CommonSimStatisticUtils.get_statistic(sim_info, statistic, add_dynamic=add_dynamic, add=add)
        if statistic_instance is None:
            return False
        statistic_instance.add_statistic_modifier(value)
        return True

    @staticmethod
    def remove_statistic_modifier(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, Statistic], value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """remove_statistic_modifier(sim_info, statistic, value, add_dynamic=True, add=True)

        Remove a Modifier from the specified Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to remove the modifier from.
        :type statistic: Union[int, CommonStatisticId, Statistic]
        :param value: The modifier to remove.
        :type value: float
        :param add_dynamic: Add the statistic components to the Sim.
        :type add_dynamic: bool, optional
        :param add: Add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if sim_info is None:
            return False
        statistic_instance = CommonSimStatisticUtils.get_statistic(sim_info, statistic, add_dynamic=add_dynamic, add=add)
        if statistic_instance is None:
            return False
        statistic_instance.remove_statistic_modifier(value)
        return True

    @staticmethod
    def remove_all_statistic_modifiers_for_statistic(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, Statistic], add_dynamic: bool=True, add: bool=True) -> bool:
        """remove_all_statistic_modifiers_for_statistic(sim_info, statistic, add_dynamic=True, add=True)

        Remove all Modifiers from the specified Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to remove modifiers from.
        :type statistic: Union[int, CommonStatisticId, Statistic]
        :param add_dynamic: Add the statistic components to the Sim.
        :type add_dynamic: bool, optional
        :param add: Add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if sim_info is None:
            return False
        statistic_instance = CommonSimStatisticUtils.get_statistic(sim_info, statistic, add_dynamic=add_dynamic, add=add)
        if statistic_instance is None:
            return False
        if statistic_instance._statistic_modifiers is None:
            return False
        for value in list(statistic_instance._statistic_modifiers):
            statistic_instance.remove_statistic_modifier(value)
        return True

    @staticmethod
    def _get_statistics_tracker(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, Statistic], add_dynamic: bool=True) -> CommonGetStatisticTrackerResponse:
        if sim_info is None:
            return CommonGetStatisticTrackerResponse(None, None, None)
        if isinstance(statistic, int) or isinstance(statistic, CommonStatisticId):
            statistic = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic is None:
            return CommonGetStatisticTrackerResponse(None, None, None)
        if not isinstance(statistic, Statistic):
            return CommonGetStatisticTrackerResponse(None, None, None)
        statistics_component: StatisticComponent = CommonComponentUtils.get_component(sim_info, CommonComponentType.STATISTIC, add_dynamic=add_dynamic)
        if statistics_component is None:
            return CommonGetStatisticTrackerResponse(None, statistic, None)
        return CommonGetStatisticTrackerResponse(statistics_component.get_tracker(statistic), statistic, statistics_component)


@Command('s4clib.set_statistic_value', command_type=CommandType.Live)
def _common_set_statistic_value(statistic: TunableInstanceParam(Types.STATISTIC), value: float, opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    if statistic is None:
        output('Failed, Statistic not specified or Statistic did not exist! s4clib.set_statistic_value <statistic_name_or_id> <value> [opt_sim=None]')
        return
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    sim_name = CommonSimNameUtils.get_full_name(sim_info)
    output('Setting statistic {} to Sim {}'.format(str(statistic), sim_name))
    try:
        if CommonSimStatisticUtils.set_statistic_value(sim_info, statistic, value):
            output('Successfully set statistic value.')
        else:
            output('Failed to set statistic.')
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to set statistic {} to Sim {}.'.format(str(statistic), sim_name), exception=ex)
        output('Failed to set statistic {} to Sim {}. {}'.format(str(statistic), sim_name, str(ex)))


@Command('s4clib.set_statistic_user_value', command_type=CommandType.Live)
def _common_set_statistic_user_value(statistic: TunableInstanceParam(Types.STATISTIC), value: float, opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    if statistic is None:
        output('Failed, Statistic not specified or Statistic did not exist! s4clib.set_statistic_value <statistic_name_or_id> <value> [opt_sim=None]')
        return
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    sim_name = CommonSimNameUtils.get_full_name(sim_info)
    output('Setting statistic {} to Sim {}'.format(str(statistic), sim_name))
    try:
        if CommonSimStatisticUtils.set_statistic_user_value(sim_info, statistic, value):
            output('Successfully set statistic value.')
        else:
            output('Failed to set statistic.')
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to set statistic {} to Sim {}.'.format(str(statistic), sim_name), exception=ex)
        output('Failed to set statistic {} to Sim {}. {}'.format(str(statistic), sim_name, str(ex)))


@Command('s4clib.remove_statistic', 's4clib.remove_commodity', command_type=CommandType.Live)
def _common_remove_statistic(statistic: TunableInstanceParam(Types.STATISTIC), opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    if statistic is None:
        output('Failed, Statistic not specified or Statistic did not exist! s4clib.remove_statistic <statistic_name_or_id> [opt_sim=None]')
        return
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    sim_name = CommonSimNameUtils.get_full_name(sim_info)
    output('Removing statistic {} from Sim {}'.format(str(statistic), sim_name))
    try:
        if CommonSimStatisticUtils.remove_statistic(sim_info, statistic):
            output('Successfully removed statistic.')
        else:
            output('Failed to remove statistic.')
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to remove statistic {} from Sim {}.'.format(str(statistic), sim_name), exception=ex)
        output('Failed to remove statistic {} from Sim {}. {}'.format(str(statistic), sim_name, str(ex)))
