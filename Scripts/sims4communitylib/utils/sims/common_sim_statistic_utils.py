"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator

from distributor.shared_messages import IconInfoData
from objects.components.statistic_component import StatisticComponent
from server_commands.argument_helpers import TunableInstanceParam
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.statistics_enum import CommonStatisticId
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.resources.common_statistic_utils import CommonStatisticUtils
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
        statistic = cls.get_statistic(sim_info, statistic, add=False)
        if statistic is not None:
            return CommonTestResult(True, reason=f'{sim_info} has statistic {statistic}.', tooltip_text=CommonStringId.S4CL_SIM_HAS_STATISTIC, tooltip_tokens=(sim_info, str(statistic)))
        return CommonTestResult(False, reason=f'{sim_info} does not have statistic {statistic}.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_STATISTIC, tooltip_tokens=(sim_info, str(statistic)))

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
            result = cls.has_statistic(sim_info, statistic)
            if result:
                return result
        return CommonTestResult(False, reason=f'{sim_info} did not have any of the specified statistics.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_STATISTICS, tooltip_tokens=(sim_info, ', '.join([str(stati) for stati in statistics])))

    # noinspection PyUnusedLocal
    @classmethod
    def is_statistic_locked(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], add_dynamic: bool = False, add: bool = False) -> CommonTestResult:
        """is_statistic_locked(sim_info, statistic, add_dynamic=False, add=False)

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
            return CommonTestResult(False, reason='sim_info was None.', hide_tooltip=True)
        statistic_id = CommonStatisticUtils.get_statistic_id(statistic)
        if statistic_id is None:
            cls.get_log().format_with_message('No statistic found when checking locked.', statistic=statistic, sim=sim_info)
            return CommonTestResult(False, reason='The specified statistic did not exist.', hide_tooltip=True)
        statistic_instance = cls.get_statistic(sim_info, statistic_id, add=add)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Sim when checking locked.', statistic=statistic, statistic_id=statistic_id, sim=sim_info)
            return CommonTestResult(False, reason=f'{sim_info} did not have statistic {statistic}.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_STATISTIC, tooltip_tokens=(sim_info, str(statistic)))
        if sim_info.is_locked(statistic_instance):
            return CommonTestResult(True, reason=f'Statistic {statistic} is locked for {sim_info}.', tooltip_text=CommonStringId.S4CL_STATISTIC_IS_LOCKED_FOR_SIM, tooltip_tokens=(str(statistic), sim_info))
        return CommonTestResult(False, reason=f'Statistic {statistic} is not locked for {sim_info}.', tooltip_text=CommonStringId.S4CL_STATISTIC_IS_NOT_LOCKED_FOR_SIM, tooltip_tokens=(str(statistic), sim_info))

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
        statistic_instance = cls.get_statistic(sim_info, statistic)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Sim when getting level.', statistic=statistic, sim=sim_info)
            return -1.0
        return statistic_instance.get_user_value()

    # noinspection PyUnusedLocal
    @classmethod
    def get_statistic(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], add_dynamic: bool = False, add: bool = False) -> Union[BaseStatistic, None]:
        """get_statistic(sim_info, statistic, statistic, add_dynamic=False, add=False)

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
        if sim_info.get_tracker(statistic_instance) is None:
            return None
        return sim_info.get_statistic(statistic_instance, add=add)

    # noinspection PyUnusedLocal
    @classmethod
    def get_statistic_value(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], add_dynamic: bool = False, add: bool = False) -> float:
        """get_statistic_value(sim_info, statistic, add_dynamic=False, add=False)

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
    def set_statistic_value(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool = True, add: bool = True) -> CommonExecutionResult:
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
            return CommonExecutionResult(False, reason='sim_info was None.', hide_tooltip=True)
        result = cls.is_statistic_locked(sim_info, statistic, add=add)
        if result:
            cls.get_log().format_with_message('Statistic is locked and thus cannot be set.', statistic=statistic, sim=sim_info)
            return result
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found when setting value.', statistic=statistic, sim=sim_info)
            return CommonExecutionResult(False, reason='The specified statistic did not exist.', hide_tooltip=True)
        sim_info.set_stat_value(statistic_instance, value)
        return CommonExecutionResult.TRUE

    # noinspection PyUnusedLocal
    @classmethod
    def set_statistic_value_to_max(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], add_dynamic: bool = True, add: bool = True) -> CommonExecutionResult:
        """set_statistic_value_to_max(sim_info, statistic, add_dynamic=True, add=True)

        Set the Value of a Statistic for the specified Sim to its max value.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param statistic: The identifier of the statistic to add a value to.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param add_dynamic: OBSOLETE: Add the statistic component to the Sim. This argument is no longer used and will be ignored.
        :type add_dynamic: bool, optional
        :param add: Whether to add the statistic to the Sim.
        :type add: bool, optional
        :return: The result of setting the statistic value. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        return cls.set_statistic_value(sim_info, statistic, CommonStatisticUtils.get_statistic_max_value(statistic), add_dynamic=add_dynamic, add=add)

    # noinspection PyUnusedLocal
    @classmethod
    def set_statistic_level(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add: bool = True) -> CommonExecutionResult:
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
        return cls.set_statistic_user_value(sim_info, statistic, value, add=add)

    # noinspection PyUnusedLocal
    @classmethod
    def set_statistic_user_value(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool = True, add: bool = True) -> CommonExecutionResult:
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
            return CommonExecutionResult(False, reason='sim_info was None.', hide_tooltip=True)
        result = cls.is_statistic_locked(sim_info, statistic, add=add)
        if result:
            cls.get_log().format_with_message('Statistic is locked and thus cannot be set.', statistic=statistic, sim=sim_info)
            return result
        statistic_instance = cls.get_statistic(sim_info, statistic, add=add)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Sim when setting statistic user value.', statistic=statistic, sim=sim_info)
            return CommonExecutionResult(False, reason='The specified statistic did not exist.', hide_tooltip=True)
        statistic_instance.set_user_value(value)
        return CommonExecutionResult(True, reason=f'Statistic {statistic} level successfully set on Sim {sim_info}.', tooltip_text=CommonStringId.S4CL_STATISTIC_LEVEL_SET_ON_SIM, tooltip_tokens=(str(statistic), sim_info))

    # noinspection PyUnusedLocal
    @classmethod
    def add_statistic_value(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool = True, add: bool = True) -> CommonExecutionResult:
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
            raise AssertionError('Argument sim_info was None')
        return cls.set_statistic_value(sim_info, statistic, cls.get_statistic_value(sim_info, statistic) + value, add=add)

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
    def add_statistic_modifier(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool = True, add: bool = True):
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
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', statistic=statistic, sim=sim_info)
            return None
        statistic = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic is None:
            cls.get_log().format_with_message('No statistic found on Sim.', statistic=statistic, sim=sim_info)
            return None
        stat = sim_info.get_statistic(statistic)
        if stat is None:
            return
        stat.add_statistic_modifier(value)
        return None

    # noinspection PyUnusedLocal
    @classmethod
    def remove_statistic_modifier(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float, add_dynamic: bool = True, add: bool = True) -> bool:
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
        statistic_instance = cls.get_statistic(sim_info, statistic, add=add)
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
    def remove_all_statistic_modifiers_for_statistic(cls, sim_info: SimInfo, statistic: Union[int, CommonStatisticId, BaseStatistic], add_dynamic: bool = True, add: bool = True) -> bool:
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
        statistic_instance = cls.get_statistic(sim_info, statistic, add=add)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Sim.', statistic=statistic, sim=sim_info)
            return False
        if not hasattr(statistic_instance, '_statistic_modifiers') or statistic_instance._statistic_modifiers is None:
            return False
        for value in list(statistic_instance._statistic_modifiers):
            statistic_instance.remove_statistic_modifier(value)
        return True


commands_log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_statistic_commands')
commands_log.enable()


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_statistic_value',
    'Print the value of a statistic on a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('statistic', 'Statistic Id or Tuning Name', 'The tuning name or decimal identifier of a Statistic.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.print_stat_value',
        's4clib.printstatvalue',
        's4clib.printstatisticvalue'
    )
)
def _common_print_statistic_value(output: CommonConsoleCommandOutput, statistic: TunableInstanceParam(Types.STATISTIC), sim_info: SimInfo=None):
    if statistic is None:
        output('ERROR: No Statistic specified or the specified Statistic did not exist!')
        return
    if sim_info is None:
        return
    output(f'Attempting to get statistic {statistic} on Sim {sim_info}.')
    statistic_value = CommonSimStatisticUtils.get_statistic_value(sim_info, CommonStatisticUtils.get_statistic_id(statistic))
    output(f'Got statistic value of {statistic_value} of {statistic} on Sim {sim_info}.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_statistic_value',
    'Set the value of a statistic on a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('statistic', 'Statistic Id or Tuning Name', 'The tuning name or decimal identifier of a Statistic.'),
        CommonConsoleCommandArgument('value', 'Decimal Number', 'The value to set the statistic to.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.set_stat_value',
        's4clib.setstatvalue',
        's4clib.setstatisticvalue'
    )
)
def _common_set_statistic_value(output: CommonConsoleCommandOutput, statistic: TunableInstanceParam(Types.STATISTIC), value: float, sim_info: SimInfo=None):
    if statistic is None:
        output('ERROR: No Statistic specified or the specified Statistic did not exist!')
        return
    if sim_info is None:
        return
    output(f'Attempting to set statistic {statistic} on Sim {sim_info} to value {value}.')
    if CommonSimStatisticUtils.set_statistic_value(sim_info, CommonStatisticUtils.get_statistic_id(statistic), value):
        output(f'SUCCESS: Successfully set statistic {statistic} of Sim {sim_info} to value {value}.')
    else:
        output(f'FAILED: Failed to set statistic {statistic} of Sim {sim_info} to value {value}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_statistic_level',
    'Set the user level of a statistic on a Sim (User level should be set instead of setting value for statistics that belong to a Sim, such as Motives or Skills).',
    command_arguments=(
        CommonConsoleCommandArgument('statistic', 'Statistic Id or Tuning Name', 'The tuning name or decimal identifier of a Statistic.'),
        CommonConsoleCommandArgument('level', 'Decimal Number', 'The level to set the statistic to.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.set_statistic_user_value',
        's4clib.set_stat_level',
        's4clib.setstatlevel',
        's4clib.setstatisticlevel'
    )
)
def _common_set_statistic_user_value(output: CommonConsoleCommandOutput, statistic: TunableInstanceParam(Types.STATISTIC), level: float, sim_info: SimInfo=None):
    if statistic is None:
        output('ERROR: No Statistic specified or the specified Statistic did not exist!')
        return
    if sim_info is None:
        return
    output(f'Attempting to set statistic {statistic} on Sim {sim_info} to user level {level}.')
    if CommonSimStatisticUtils.set_statistic_user_value(sim_info, statistic, level):
        output(f'SUCCESS: Successfully set statistic {statistic} on Sim {sim_info} to user level {level}.')
    else:
        output(f'FAILED: Failed to set statistic {statistic} on Sim {sim_info} to user level {level}.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_statistic_level',
    'Print the user level of a statistic on a Sim (User level should be printed instead of the value for statistics that belong to a Sim, such as Motives or Skills).',
    command_arguments=(
        CommonConsoleCommandArgument('statistic', 'Statistic Id or Tuning Name', 'The tuning name or decimal identifier of a Statistic.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.print_statistic_user_value',
        's4clib.print_stat_level',
        's4clib.printstatlevel',
        's4clib.printstatisticlevel'
    )
)
def _common_print_statistic_user_value(output: CommonConsoleCommandOutput, statistic: TunableInstanceParam(Types.STATISTIC), sim_info: SimInfo=None):
    if statistic is None:
        output('ERROR: No Statistic specified or the specified Statistic did not exist!')
        return
    if sim_info is None:
        return
    output(f'Attempting to print statistic {statistic} on Sim {sim_info}.')
    level = CommonSimStatisticUtils.get_statistic_level(sim_info, CommonStatisticUtils.get_statistic_id(statistic))
    output(f'Got statistic level of {level} of {statistic} on Sim {sim_info}.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_statistic',
    'Remove a Statistic or Commodity from a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('statistic', 'Statistic Id or Tuning Name', 'The tuning name or decimal identifier of a Statistic or Commodity.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.remove_commodity',
        's4clib.remove_stat',
        's4clib.removestat',
        's4clib.removestatistic'
    )
)
def _common_remove_statistic(output: CommonConsoleCommandOutput, statistic: TunableInstanceParam(Types.STATISTIC), sim_info: SimInfo=None):
    if statistic is None:
        output('ERROR: No Statistic specified or the specified Statistic did not exist!')
        return
    if sim_info is None:
        return
    output(f'Attempting to remove statistic {statistic} from Sim {sim_info}.')
    if CommonSimStatisticUtils.remove_statistic(sim_info, CommonStatisticUtils.get_statistic_id(statistic)):
        output(f'SUCCESS: Successfully removed statistic {statistic} from Sim {sim_info}.')
    else:
        output(f'FAILED: Failed to remove statistic {statistic} from Sim {sim_info}.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_static_commodities',
    'Print a list of a Static Commodities on a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib_testing.printstaticcommodities',
    )
)
def _common_print_static_commodities(output: CommonConsoleCommandOutput, sim_info: SimInfo=None):
    log = CommonSimStatisticUtils.get_log()
    try:
        log.enable()
        output(f'Printing static commodities of Sim {sim_info}')
        text = ''
        for stat in list(sim_info.static_commodity_tracker):
            statistic_id = CommonStatisticUtils.get_statistic_id(stat)
            text += f'{stat} ({statistic_id})\n'
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        log.debug(f'{sim_info} Static Commodities ({sim_id})')
        log.debug(text)
        CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string(f'{sim_info} Static Commodities ({sim_id})'),
            CommonLocalizationUtils.create_localized_string(text)
        ).show(
            icon=IconInfoData(obj_instance=CommonSimUtils.get_sim_instance(sim_info))
        )
    finally:
        log.disable()
