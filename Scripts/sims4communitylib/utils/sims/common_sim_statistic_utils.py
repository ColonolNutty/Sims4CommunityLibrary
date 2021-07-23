"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator
from server_commands.argument_helpers import TunableInstanceParam, OptionalTargetParam
from sims.sim_info import SimInfo
from sims4.commands import Command, CommandType, CheatOutput
from sims4.resources import Types
from sims4communitylib.enums.statistics_enum import CommonStatisticId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.resources.common_statistic_utils import CommonStatisticUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from statistics.base_statistic import BaseStatistic
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'common_sim_statistic_utils')


class CommonSimStatisticUtils:
    """Utilities for manipulating the Statistics of Sims.

    """
    @staticmethod
    def has_statistic(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic]) -> bool:
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
        return statistic is not None

    @staticmethod
    def has_statistics(sim_info: SimInfo, statistics: Iterator[Union[int, CommonStatisticId, BaseStatistic]]) -> bool:
        """has_statistics(sim_info, statistics)

        Determine if a Sim has any of the specified Statistics.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistics: An iterator of identifiers for statistics to check.
        :type statistics: Iterator[Union[int, CommonStatisticId, BaseStatistic]]
        :return: True, if the Sim has any of the statistics. False, if not.
        :rtype: bool
        """
        for statistic in statistics:
            if CommonSimStatisticUtils.has_statistic(sim_info, statistic):
                return True
        return False

    # noinspection PyUnusedLocal
    @staticmethod
    def is_statistic_locked(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], add_dynamic: bool=True, add: bool= False) -> bool:
        """is_statistic_locked(sim_info, statistic, add_dynamic=True, add=False)

        Determine if a statistic is locked for the specified Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to check.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param add_dynamic: Add the statistic components to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if the statistic is locked. False, if not.
        :rtype: bool
        """
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic_instance is None:
            return False
        return sim_info.is_locked(statistic_instance)

    @staticmethod
    def get_statistic_level(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic]) -> float:
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
            return -1.0
        return statistic_instance.get_user_value()

    # noinspection PyUnusedLocal
    @staticmethod
    def get_statistic(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], add_dynamic: bool=True, add: bool=False) -> Union[BaseStatistic, None]:
        """get_statistic(sim_info, statistic, statistic, add_dynamic=True, add=False)

        Retrieve a Statistic for the specified Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to retrieve of.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param add_dynamic: Add the statistic components to the Sim. This argument is no longer used and will be ignored. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: An instance of the statistic or None if a problem occurs.
        :rtype: Union[BaseStatistic, None]
        """
        if sim_info is None:
            return None
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic_instance is None:
            log.format_with_message('No instance', tinstance=statistic)
            return None
        return sim_info.get_statistic(statistic_instance, add=add)

    # noinspection PyUnusedLocal
    @staticmethod
    def get_statistic_value(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], add_dynamic: bool=True, add: bool=False) -> float:
        """get_statistic_value(sim_info, statistic, add_dynamic=True, add=False)

        Retrieve the Value of a Statistic for the specified Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to retrieve the value of.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param add_dynamic: Add the statistic components to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim. This argument is no longer used and will be ignored.
        :type add: bool, optional
        :return: The value of the statistic, `-1.0` if the statistic is not found.
        :rtype: float
        """
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic_instance is None:
            log.format_with_message('No statistic found on Sim.', statistic=statistic, sim=sim_info)
            return -1.0
        return sim_info.get_stat_value(statistic_instance)

    # noinspection PyUnusedLocal
    @staticmethod
    def set_statistic_value(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """set_statistic_value(sim_info, statistic, value, add_dynamic=True, add=True)

        Set the Value of a Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to add a value to.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The amount to add.
        :type value: float
        :param add_dynamic: Add the statistic components to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if sim_info is None:
            return False
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic_instance is None:
            log.format_with_message('No statistic found on Sim.', statistic=statistic, sim=sim_info)
            return False
        if CommonSimStatisticUtils.is_statistic_locked(sim_info, statistic_instance):
            log.format_with_message('Stat is locked.', statistic=statistic, statistic_instance=statistic_instance, sim=sim_info)
            return False
        sim_info.set_stat_value(statistic_instance, value)
        return True

    # noinspection PyUnusedLocal
    @staticmethod
    def set_statistic_level(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add: bool=True) -> bool:
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
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        return CommonSimStatisticUtils.set_statistic_user_value(sim_info, statistic, value, add=add)

    # noinspection PyUnusedLocal
    @staticmethod
    def set_statistic_user_value(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """set_statistic_user_value(sim_info, statistic, value, add_dynamic=True, add=True)

        Set the User Value of a Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to add a user value to.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The user value to set the statistic to.
        :type value: float
        :param add_dynamic: Add the statistic components to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if sim_info is None:
            return False
        statistic_instance = CommonSimStatisticUtils.get_statistic(sim_info, statistic, add=add)
        if statistic_instance is None:
            return False
        statistic_instance.set_user_value(value)
        return True

    # noinspection PyUnusedLocal
    @staticmethod
    def add_statistic_value(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """add_statistic_value(sim_info, statistic, value, add_dynamic=True, add=True)

        Change the Value of a Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to add a value to.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The amount to add.
        :type value: float
        :param add_dynamic: Add the statistic components to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        return CommonSimStatisticUtils.set_statistic_value(sim_info, statistic, CommonSimStatisticUtils.get_statistic_value(sim_info, statistic) + value, add=add)

    @staticmethod
    def remove_statistic(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic]) -> bool:
        """remove_statistic(sim_info, statistic)

        Remove a Statistic from the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to remove.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        statistic = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic is None:
            return False
        sim_info.remove_statistic(statistic)
        return True

    # noinspection PyUnusedLocal
    @staticmethod
    def add_statistic_modifier(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool=True, add: bool=True) -> Union[int, None]:
        """add_statistic_modifier(sim_info, statistic, value, add_dynamic=True, add=True)

        Add a Modifier to the specified Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic containing the modifier.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The modifier to add.
        :type value: float
        :param add_dynamic: Add the statistic components to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: The handle id for the statistic modifier or None if the modifier failed to apply.
        :rtype: Union[int, None]
        """
        if sim_info is None:
            return None
        statistic = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic is None:
            return False
        return sim_info.add_statistic_modifier(statistic, value)

    # noinspection PyUnusedLocal
    @staticmethod
    def remove_statistic_modifier(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool=True, add: bool=True) -> bool:
        """remove_statistic_modifier(sim_info, statistic, value, add_dynamic=True, add=True)

        Remove a Modifier from a Sim by value.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to remove the modifier from.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The modifier to remove.
        :type value: float
        :param add_dynamic: Add the statistic components to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if sim_info is None:
            return False
        statistic_instance = CommonSimStatisticUtils.get_statistic(sim_info, statistic, add=add)
        if statistic_instance is None:
            return False
        statistic_instance.remove_statistic_modifier(value)
        return True

    @staticmethod
    def remove_statistic_modifier_by_handle_id(sim_info: SimInfo, modifier_handle: int) -> bool:
        """remove_statistic_modifier_by_handle_id(sim_info, modifier_handle)

        Remove a Statistic Modifier from a Sim by a handle id.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param modifier_handle: The handle id for the statistic modifier being removed.
        :type modifier_handle: int
        :return: True, if the modifier was successfully removed successful. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        return sim_info.remove_statistic_modifier(modifier_handle)

    # noinspection PyUnusedLocal
    @staticmethod
    def remove_all_statistic_modifiers_for_statistic(sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], add_dynamic: bool=True, add: bool=True) -> bool:
        """remove_all_statistic_modifiers_for_statistic(sim_info, statistic, add_dynamic=True, add=True)

        Remove all Modifiers from the specified Statistic for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to remove modifiers from.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param add_dynamic: Add the statistic components to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether or not to add the statistic to the Sim.
        :type add: bool, optional
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if sim_info is None:
            return False
        statistic_instance = CommonSimStatisticUtils.get_statistic(sim_info, statistic, add=add)
        if statistic_instance is None:
            return False
        if not hasattr(statistic_instance, '_statistic_modifiers') or statistic_instance._statistic_modifiers is None:
            return False
        for value in list(statistic_instance._statistic_modifiers):
            statistic_instance.remove_statistic_modifier(value)
        return True


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
        if CommonSimStatisticUtils.set_statistic_value(sim_info, statistic.id, value):
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
        if CommonSimStatisticUtils.remove_statistic(sim_info, statistic.id):
            output('Successfully removed statistic.')
        else:
            output('Failed to remove statistic.')
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to remove statistic {} from Sim {}.'.format(str(statistic), sim_name), exception=ex)
        output('Failed to remove statistic {} from Sim {}. {}'.format(str(statistic), sim_name, str(ex)))
