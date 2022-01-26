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
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.statistics_enum import CommonStatisticId
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.resources.common_statistic_utils import CommonStatisticUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from statistics.base_statistic import BaseStatistic


class CommonSimStatisticUtils(_HasS4CLClassLog):
    """Utilities for manipulating the Statistics of Sims.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_sim_statistic_utils'

    @classmethod
    def has_statistic(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic]) -> CommonTestResult:
        """has_statistic(sim_info, statistic)

        Determine if a Sim has any of the specified Statistics.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to check.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :return: True, if the Sim has any of the statistics. False, if not.
        :rtype: bool
        """
        statistic = CommonSimStatisticUtils.get_statistic(sim_info, statistic, add=False)
        if statistic is not None:
            return CommonTestResult(True, f'{sim_info} had statistic {statistic}.')
        return CommonTestResult(False, f'{sim_info} did not have statistic {statistic}.')

    @classmethod
    def has_statistics(cls, sim_info: SimInfo, statistics: Iterator[Union[int, CommonStatisticId, BaseStatistic]]) -> CommonTestResult:
        """has_statistics(sim_info, statistics)

        Determine if a Sim has any of the specified Statistics.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistics: An iterator of identifiers for statistics to check.
        :type statistics: Iterator[Union[int, CommonStatisticId, BaseStatistic]]
        :return: True, if the Sim has any of the specified statistics. False, if not.
        :rtype: bool
        """
        for statistic in statistics:
            result = CommonSimStatisticUtils.has_statistic(sim_info, statistic)
            if result:
                return result
        return CommonTestResult(False, f'{sim_info} did not have any of the specified statistics.')

    # noinspection PyUnusedLocal
    @classmethod
    def is_statistic_locked(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], add_dynamic: bool=True, add: bool= False) -> CommonTestResult:
        """is_statistic_locked(sim_info, statistic, add_dynamic=True, add=False)

        Determine if a statistic is locked for the specified Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to check.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param add_dynamic: OBSOLETE: Add the statistic component to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: The result of checking if the statistic is locked or not. True, if the statistic is locked. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', statistic=statistic, sim=sim_info)
            return CommonTestResult(False, 'sim_info was None.')
        statistic_id = CommonStatisticUtils.get_statistic_id(statistic)
        if statistic_id is None:
            cls.get_log().format_with_message('No statistic found when checking locked.', statistic=statistic, sim=sim_info)
            return CommonTestResult(False, 'The specified statistic did not exist.')
        statistic_instance = CommonSimStatisticUtils.get_statistic(sim_info, statistic_id, add=add)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Sim when checking locked.', statistic=statistic, statistic_id=statistic_id, sim=sim_info)
            return CommonTestResult(False, f'{sim_info} did not have statistic {statistic}.')
        if sim_info.is_locked(statistic_instance):
            return CommonTestResult(True, 'Statistic is locked.')
        return CommonTestResult(False, 'Statistic is not locked.')

    @classmethod
    def get_statistic_level(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic]) -> float:
        """get_statistic_level(sim_info, statistic)

        Retrieve the User Value of a Statistic for the specified Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to retrieve the user value of.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :return: The value of the statistic, `-1.0` if the statistic is not found.
        :rtype: float
        """
        statistic_instance = CommonSimStatisticUtils.get_statistic(sim_info, statistic)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Sim when getting level.', statistic=statistic, sim=sim_info)
            return -1.0
        return statistic_instance.get_user_value()

    # noinspection PyUnusedLocal
    @classmethod
    def get_statistic(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], add_dynamic: bool=True, add: bool=False) -> Union[BaseStatistic, None]:
        """get_statistic(sim_info, statistic, statistic, add_dynamic=True, add=False)

        Retrieve a Statistic for the specified Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to retrieve of.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param add_dynamic: OBSOLETE: Add the statistic component to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: An instance of the statistic or None if a problem occurs.
        :rtype: Union[BaseStatistic, None]
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', statistic=statistic, sim=sim_info)
            return None
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found when loading statistic by id.', statistic=statistic, sim=sim_info)
            return None
        return sim_info.get_statistic(statistic_instance, add=add)

    # noinspection PyUnusedLocal
    @classmethod
    def get_statistic_value(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], add_dynamic: bool=False, add: bool=False) -> float:
        """get_statistic_value(sim_info, statistic, add_dynamic=True, add=False)

        Retrieve the Value of a Statistic for the specified Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to retrieve the value of.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param add_dynamic: OBSOLETE: Add the statistic component to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim. This argument is no longer used and will be ignored.
        :type add: bool, optional
        :return: The value of the statistic, `-1.0` if the statistic is not found.
        :rtype: float
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', statistic=statistic, sim=sim_info)
            return -1.0
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Sim when getting statistic value.', statistic=statistic, sim=sim_info)
            return -1.0
        try:
            if not CommonComponentUtils.has_component(sim_info, CommonComponentType.STATISTIC):
                if not add:
                    return -1.0
                else:
                    CommonComponentUtils.add_dynamic_component(sim_info, CommonComponentType.STATISTIC)
            statistic_component: StatisticComponent = CommonComponentUtils.get_component(sim_info, CommonComponentType.STATISTIC, add_dynamic=add_dynamic)
            if statistic_component is None:
                return -1.0
            return statistic_component.get_stat_value(statistic_instance)
        except Exception as ex:
            cls.get_log().format_error_with_message('An error occurred while getting statistic value.', sim_info=sim_info, sim_type=type(sim_info), has_get_stat_value=hasattr(sim_info, 'get_stat_value'), get_stat_value=sim_info.get_stat_value, exception=ex, update_tokens=False)

    # noinspection PyUnusedLocal
    @classmethod
    def set_statistic_value(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool=True, add: bool=True) -> CommonExecutionResult:
        """set_statistic_value(sim_info, statistic, value, add_dynamic=True, add=True)

        Set the Value of a Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to add a value to.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The amount to add.
        :type value: float
        :param add_dynamic: OBSOLETE: Add the statistic component to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: The result of setting the statistic value. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', statistic=statistic, sim=sim_info)
            return CommonExecutionResult(False, 'sim_info was None.')
        result = CommonSimStatisticUtils.is_statistic_locked(sim_info, statistic, add=add)
        if result:
            cls.get_log().format_with_message('Statistic is locked and thus cannot be set.', statistic=statistic, sim=sim_info)
            return result
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found when setting value.', statistic=statistic, sim=sim_info)
            return CommonExecutionResult(False, 'The specified statistic did not exist.')
        sim_info.set_stat_value(statistic_instance, value)
        return CommonExecutionResult.TRUE

    # noinspection PyUnusedLocal
    @classmethod
    def set_statistic_level(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add: bool=True) -> CommonExecutionResult:
        """set_statistic_level(sim_info, statistic, value, add_dynamic=True, add=True)

        Set the Level of a Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to add a user value to.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The level to set the statistic to.
        :type value: float
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: The result of setting the statistic level. True, if successful. False, if not successful.
        :rtype: CommonExecutionResult
        """
        return CommonSimStatisticUtils.set_statistic_user_value(sim_info, statistic, value, add=add)

    # noinspection PyUnusedLocal
    @classmethod
    def set_statistic_user_value(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool=True, add: bool=True) -> CommonExecutionResult:
        """set_statistic_user_value(sim_info, statistic, value, add_dynamic=True, add=True)

        Set the User Value of a Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to add a user value to.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The user value to set the statistic to.
        :type value: float
        :param add_dynamic: OBSOLETE: Add the statistic component to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', statistic=statistic, sim=sim_info)
            return CommonExecutionResult(False, 'sim_info was None.')
        result = CommonSimStatisticUtils.is_statistic_locked(sim_info, statistic, add=add)
        if result:
            cls.get_log().format_with_message('Statistic is locked and thus cannot be set.', statistic=statistic, sim=sim_info)
            return result
        statistic_instance = CommonSimStatisticUtils.get_statistic(sim_info, statistic, add=add)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Sim when setting statistic user value.', statistic=statistic, sim=sim_info)
            return CommonExecutionResult(False, 'The specified statistic did not exist.')
        statistic_instance.set_user_value(value)
        return CommonExecutionResult(True, f'Statistic {statistic} level successfully set on Sim {sim_info}.')

    # noinspection PyUnusedLocal
    @classmethod
    def add_statistic_value(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool=True, add: bool=True) -> CommonExecutionResult:
        """add_statistic_value(sim_info, statistic, value, add_dynamic=True, add=True)

        Change the Value of a Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to add a value to.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The amount to add.
        :type value: float
        :param add_dynamic: OBSOLETE: Add the statistic component to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: The result of setting the statistic value. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', statistic=statistic, sim=sim_info)
            return CommonExecutionResult(False, 'SimInfo was None.')
        return CommonSimStatisticUtils.set_statistic_value(sim_info, statistic, CommonSimStatisticUtils.get_statistic_value(sim_info, statistic) + value, add=add)

    @classmethod
    def remove_statistic(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic]) -> bool:
        """remove_statistic(sim_info, statistic)

        Remove a Statistic from the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to remove.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', statistic=statistic, sim=sim_info)
            return False
        statistic = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic is None:
            cls.get_log().format_with_message('No statistic found on Sim when removing statistic.', statistic=statistic, sim=sim_info)
            return True
        sim_info.remove_statistic(statistic)
        return True

    # noinspection PyUnusedLocal
    @classmethod
    def add_statistic_modifier(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool=True, add: bool=True) -> Union[int, None]:
        """add_statistic_modifier(sim_info, statistic, value, add_dynamic=True, add=True)

        Add a Modifier to the specified Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic containing the modifier.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The modifier to add.
        :type value: float
        :param add_dynamic: OBSOLETE: Add the statistic component to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: The handle id for the statistic modifier or None if the modifier failed to apply.
        :rtype: Union[int, None]
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', statistic=statistic, sim=sim_info)
            return None
        statistic = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic is None:
            cls.get_log().format_with_message('No statistic found on Sim.', statistic=statistic, sim=sim_info)
            return None
        return sim_info.add_statistic_modifier(statistic, value)

    # noinspection PyUnusedLocal
    @classmethod
    def remove_statistic_modifier(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """remove_statistic_modifier(sim_info, statistic, value, add_dynamic=True, add=True)

        Remove a Modifier from a Sim by value.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to remove the modifier from.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The modifier to remove.
        :type value: float
        :param add_dynamic: OBSOLETE: Add the statistic component to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', statistic=statistic, sim=sim_info)
            return False
        statistic_instance = CommonSimStatisticUtils.get_statistic(sim_info, statistic, add=add)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Sim.', statistic=statistic, sim=sim_info)
            return False
        statistic_instance.remove_statistic_modifier(value)
        return True

    @classmethod
    def remove_statistic_modifier_by_handle_id(cls, sim_info: SimInfo, modifier_handle_id: int) -> bool:
        """remove_statistic_modifier_by_handle_id(sim_info, modifier_handle_id)

        Remove a Statistic Modifier from a Sim by a handle id.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param modifier_handle_id: The handle id for the statistic modifier being removed.
        :type modifier_handle_id: int
        :return: True, if the modifier was removed successfully. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', modifier_handle=modifier_handle_id, sim=sim_info)
            return False
        return sim_info.remove_statistic_modifier(modifier_handle_id)

    # noinspection PyUnusedLocal
    @classmethod
    def remove_all_statistic_modifiers_for_statistic(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], add_dynamic: bool=True, add: bool=True) -> bool:
        """remove_all_statistic_modifiers_for_statistic(sim_info, statistic, add_dynamic=True, add=True)

        Remove all Modifiers from the specified Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to remove modifiers from.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param add_dynamic: OBSOLETE: Add the statistic component to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', statistic=statistic, sim=sim_info)
            return False
        statistic_instance = CommonSimStatisticUtils.get_statistic(sim_info, statistic, add=add)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Sim.', statistic=statistic, sim=sim_info)
            return False
        if not hasattr(statistic_instance, '_statistic_modifiers') or statistic_instance._statistic_modifiers is None:
            return False
        for value in list(statistic_instance._statistic_modifiers):
            statistic_instance.remove_statistic_modifier(value)
        return True


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_statistic_commands')
log.enable()


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
        if CommonSimStatisticUtils.set_statistic_value(sim_info, CommonStatisticUtils.get_statistic_id(statistic), value):
            output('Successfully set statistic value.')
        else:
            output('Failed to set statistic.')
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to set statistic {} to Sim {}.'.format(str(statistic), sim_name), exception=ex)
        output('Failed to set statistic {} to Sim {}. {}'.format(str(statistic), sim_name, str(ex)))


@Command('s4clib.set_statistic_user_value', 's4clib.set_statistic_level', command_type=CommandType.Live)
def _common_set_statistic_user_value(statistic: TunableInstanceParam(Types.STATISTIC), value: float, opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    try:
        if statistic is None:
            output('Failed, Statistic not specified or Statistic did not exist! s4clib.set_statistic_level <statistic_name_or_id> <value> [opt_sim=None]')
            return
        sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
        if sim_info is None:
            output('Failed, no Sim was specified or the specified Sim was not found!')
            return
        sim_name = CommonSimNameUtils.get_full_name(sim_info)
        output('Setting statistic {} to Sim {}'.format(str(statistic), sim_name))
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to set statistic {} to Sim.'.format(str(statistic)), exception=ex)
        output('Failed to set statistic {}. {}'.format(statistic, str(ex)))
        return
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
        if CommonSimStatisticUtils.remove_statistic(sim_info, CommonStatisticUtils.get_statistic_id(statistic)):
            output('Successfully removed statistic.')
        else:
            output('Failed to remove statistic.')
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to remove statistic {} from Sim {}.'.format(str(statistic), sim_name), exception=ex)
        output('Failed to remove statistic {} from Sim {}. {}'.format(str(statistic), sim_name, str(ex)))


@Command('s4clib.print_static_commodities', command_type=CommandType.Live)
def _common_print_static_commodities(opt_sim: OptionalTargetParam=None, _connection: int=None):
    output = CheatOutput(_connection)
    from server_commands.argument_helpers import get_optional_target
    try:
        sim = get_optional_target(opt_sim, output._context)
        if sim is None:
            output("Sim {} doesn't exist".format(opt_sim))
            return False
        sim_info = CommonSimUtils.get_sim_info(sim)
        try:
            output(f'Printing static commodities of Sim {sim_info}')
            static_commodities_text = ''
            for stat in list(sim_info.static_commodity_tracker):
                static_commodities_text += '{} ({})\n'.format(stat, CommonStatisticUtils.get_statistic_id(stat))
            log.debug(static_commodities_text)
        except Exception as ex:
            log.error('Error occurred printing static commodities.', exception=ex)
    except Exception as ex:
        output('An error occurred while printing static commodities.')
        log.error('An error occurred while printing static commodities.', exception=ex)
    return False
