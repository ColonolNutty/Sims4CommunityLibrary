"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator

from distributor.shared_messages import IconInfoData
from objects.components.statistic_component import StatisticComponent
from objects.game_object import GameObject
from server_commands.argument_helpers import TunableInstanceParam
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
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.resources.common_statistic_utils import CommonStatisticUtils
from statistics.base_statistic import BaseStatistic
from statistics.statistic_tracker import StatisticTracker


class CommonObjectStatisticUtils(_HasS4CLClassLog):
    """Utilities for manipulating the Statistics of Objects.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_object_statistic_utils'

    @classmethod
    def has_statistic(cls, game_object: GameObject, statistic: Union[int, CommonStatisticId, BaseStatistic]) -> CommonTestResult:
        """has_statistic(game_object, statistic)

        Determine if an Object has any of the specified Statistics.

        :param game_object: The Object to check.
        :type game_object: GameObject
        :param statistic: The identifier of the statistic to check.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :return: True, if the Object has any of the statistics. False, if not.
        :rtype: bool
        """
        statistic = cls.get_statistic(game_object, statistic)
        if statistic is not None:
            return CommonTestResult(True, reason=f'Object {game_object} has statistic {statistic}.', tooltip_text=CommonStringId.S4CL_OBJECT_HAS_STATISTIC, tooltip_tokens=(str(game_object), str(statistic)))
        return CommonTestResult(False, reason=f'Object {game_object} does not have statistic {statistic}.', tooltip_text=CommonStringId.S4CL_OBJECT_DOES_NOT_HAVE_STATISTIC, tooltip_tokens=(str(game_object), str(statistic)))

    @classmethod
    def has_statistics(cls, game_object: GameObject, statistics: Iterator[Union[int, CommonStatisticId, BaseStatistic]]) -> CommonTestResult:
        """has_statistics(game_object, statistics)

        Determine if an Object has any of the specified Statistics.

        :param game_object: The Object to check.
        :type game_object: GameObject
        :param statistics: An iterator of identifiers for statistics to check.
        :type statistics: Iterator[Union[int, CommonStatisticId, BaseStatistic]]
        :return: True, if the Object has any of the specified statistics. False, if not.
        :rtype: bool
        """
        for statistic in statistics:
            result = cls.has_statistic(game_object, statistic)
            if result:
                return result
        return CommonTestResult(False, reason=f'Object {game_object} does not have any of {statistics}.', tooltip_text=CommonStringId.S4CL_OBJECT_DOES_NOT_HAVE_ANY_STATISTICS, tooltip_tokens=(str(game_object), str(statistics)))

    # noinspection PyUnusedLocal
    @classmethod
    def is_statistic_locked(cls, game_object: GameObject, statistic: Union[int, CommonStatisticId, BaseStatistic]) -> CommonTestResult:
        """is_statistic_locked(game_object, statistic)

        Determine if a statistic is locked for the specified Object.

        :param game_object: The Object to check.
        :type game_object: GameObject
        :param statistic: The identifier of the statistic to check.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :return: The result of checking if the statistic is locked or not. True, if the statistic is locked. False, if not.
        :rtype: CommonExecutionResult
        """
        if game_object is None:
            cls.get_log().format_with_message('game_object was None!', statistic=statistic, game_object=game_object)
            return CommonTestResult(False, reason='game_object was None.', hide_tooltip=True)
        statistic_id = CommonStatisticUtils.get_statistic_id(statistic)
        if statistic_id is None:
            cls.get_log().format_with_message('No statistic found when checking locked.', statistic=statistic, game_object=game_object)
            return CommonTestResult(False, reason='The specified statistic did not exist.', hide_tooltip=True)
        statistic_instance = cls.get_statistic(game_object, statistic_id)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Object when checking locked.', statistic=statistic, statistic_id=statistic_id, game_object=game_object)
            return CommonTestResult(False, reason=f'Object {game_object} does not have statistic {statistic}.', tooltip_text=CommonStringId.S4CL_OBJECT_DOES_NOT_HAVE_STATISTIC, tooltip_tokens=(str(game_object), str(statistic)))
        statistic_component: StatisticComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.STATISTIC)
        if statistic_component is None:
            return CommonTestResult(False, reason=f'Object {game_object} did not have statistic component.', hide_tooltip=True)
        if statistic_component.is_stat_type_locked(statistic_instance):
            return CommonTestResult(True, reason=f'{game_object} has statistic {statistic_instance} locked.', tooltip_text=CommonStringId.S4CL_OBJECT_HAS_STATISTIC_LOCKED, tooltip_tokens=(str(game_object), str(statistic_instance)))
        return CommonTestResult(False, reason=f'{game_object} has statistic {statistic_instance} unlocked.', tooltip_text=CommonStringId.S4CL_OBJECT_HAS_STATISTIC_UNLOCKED, tooltip_tokens=(str(game_object), str(statistic_instance)))

    # noinspection PyUnusedLocal
    @classmethod
    def get_statistic(cls, game_object: GameObject, statistic: Union[int, CommonStatisticId, BaseStatistic]) -> Union[BaseStatistic, None]:
        """get_statistic(game_object, statistic, statistic, add=False)

        Retrieve a Statistic for the specified Object.

        :param game_object: The Object to check.
        :type game_object: GameObject
        :param statistic: The identifier of the statistic to retrieve of.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :return: An instance of the statistic or None if a problem occurs.
        :rtype: Union[BaseStatistic, None]
        """
        if game_object is None:
            cls.get_log().format_with_message('game_object was None!', statistic=statistic, game_object=game_object)
            return None
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found when loading statistic by id.', statistic=statistic, game_object=game_object)
            return None
        statistic_tracker = cls.get_statistic_tracker(game_object)
        return statistic_tracker.get_statistic(statistic_instance, add=False)

    # noinspection PyUnusedLocal
    @classmethod
    def get_statistic_value(cls, game_object: GameObject, statistic: Union[int, CommonStatisticId, BaseStatistic]) -> float:
        """get_statistic_value(game_object, statistic)

        Retrieve the Value of a Statistic for the specified Object.

        :param game_object: The Object to check.
        :type game_object: GameObject
        :param statistic: The identifier of the statistic to retrieve the value of.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :return: The value of the statistic, `-1.0` if the statistic is not found.
        :rtype: float
        """
        if game_object is None:
            cls.get_log().format_with_message('game_object was None!', statistic=statistic, game_object=game_object)
            return -1.0
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Object when getting statistic value.', statistic=statistic, game_object=game_object)
            return -1.0
        try:
            statistic_component: StatisticComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.STATISTIC)
            if statistic_component is None:
                return -1.0
            return statistic_component.get_stat_value(statistic_instance)
        except Exception as ex:
            cls.get_log().format_error_with_message('An error occurred while getting statistic value.', game_object=game_object, game_object_type=type(game_object), has_get_stat_value=hasattr(game_object, 'get_stat_value'), get_stat_value=game_object.get_stat_value, exception=ex, update_tokens=False)

    # noinspection PyUnusedLocal
    @classmethod
    def set_statistic_value(cls, game_object: GameObject, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float) -> CommonExecutionResult:
        """set_statistic_value(game_object, statistic, value)

        Set the Value of a Statistic for the specified Object.

        :param game_object: The Object to modify.
        :type game_object: GameObject
        :param statistic: The identifier of the statistic to add a value to.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The amount to add.
        :type value: float
        :return: The result of setting the statistic value. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        if game_object is None:
            cls.get_log().format_with_message('game_object was None!', statistic=statistic, game_object=game_object)
            return CommonExecutionResult(False, reason='game_object was None.', hide_tooltip=True)
        result = cls.is_statistic_locked(game_object, statistic)
        if result:
            cls.get_log().format_with_message('Statistic is locked and thus cannot be set.', statistic=statistic, game_object=game_object)
            return result
        statistic_instance = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found when loading statistic by id.', statistic=statistic, game_object=game_object)
            return CommonExecutionResult(False, reason=f'Statistic not found with id {statistic}.', hide_tooltip=True)
        statistic_component: StatisticComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.STATISTIC)
        if statistic_component is None:
            return CommonExecutionResult(False, reason=f'Failed to create statistic component on object.', hide_tooltip=True)
        statistic_component.set_stat_value(statistic_instance, value)
        return CommonExecutionResult.TRUE

    # noinspection PyUnusedLocal
    @classmethod
    def add_statistic_value(cls, game_object: GameObject, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float) -> CommonExecutionResult:
        """add_statistic_value(game_object, statistic, value)

        Change the Value of a Statistic for the specified Object.

        :param game_object: The Object to modify.
        :type game_object: GameObject
        :param statistic: The identifier of the statistic to add a value to.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The amount to add.
        :type value: float
        :return: The result of setting the statistic value. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        if game_object is None:
            raise AssertionError('Argument game_object was None')
        return cls.set_statistic_value(game_object, statistic, cls.get_statistic_value(game_object, statistic) + value)

    @classmethod
    def remove_statistic(cls, game_object: GameObject, statistic: Union[int, CommonStatisticId, BaseStatistic]) -> bool:
        """remove_statistic(game_object, statistic)

        Remove a Statistic from the specified Object.

        :param game_object: The Object to modify.
        :type game_object: GameObject
        :param statistic: The identifier of the statistic to remove.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if game_object is None:
            cls.get_log().format_with_message('game_object was None!', statistic=statistic, game_object=game_object)
            return False
        statistic_instance = cls.get_statistic(game_object, statistic)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Object when removing statistic.', statistic=statistic, game_object=game_object)
            return True
        statistic_tracker = cls.get_statistic_tracker(game_object)
        statistic_tracker.remove_statistic(statistic_instance)
        return True

    # noinspection PyUnusedLocal
    @classmethod
    def add_statistic_modifier(cls, game_object: GameObject, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float):
        """add_statistic_modifier(game_object, statistic, value)

        Add a Modifier to the specified Statistic for the specified Object.

        :param game_object: The Object to modify.
        :type game_object: GameObject
        :param statistic: The identifier of the statistic containing the modifier.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The modifier to add.
        :type value: float
        """
        if game_object is None:
            cls.get_log().format_with_message('game_object was None!', statistic=statistic, game_object=game_object)
            return None
        statistic = CommonStatisticUtils.load_statistic_by_id(statistic)
        if statistic is None:
            cls.get_log().format_with_message('No statistic found on Object.', statistic=statistic, game_object=game_object)
            return None
        statistic_instance = cls.get_statistic(game_object, statistic)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Object.', statistic=statistic, game_object=game_object)
            return
        statistic_instance.add_statistic_modifier(value)
        return None

    # noinspection PyUnusedLocal
    @classmethod
    def remove_statistic_modifier(cls, game_object: GameObject, statistic: Union[int, CommonStatisticId, BaseStatistic], value: float) -> bool:
        """remove_statistic_modifier(game_object, statistic, value)

        Remove a Modifier from an Object by value.

        :param game_object: The Object to modify.
        :type game_object: GameObject
        :param statistic: The identifier of the statistic to remove the modifier from.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :param value: The modifier to remove.
        :type value: float
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if game_object is None:
            cls.get_log().format_with_message('game_object was None!', statistic=statistic, game_object=game_object)
            return False
        statistic_instance = cls.get_statistic(game_object, statistic)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Object.', statistic=statistic, game_object=game_object)
            return False
        statistic_instance.remove_statistic_modifier(value)
        return True

    @classmethod
    def remove_statistic_modifier_by_handle_id(cls, game_object: GameObject, modifier_handle_id: int) -> bool:
        """remove_statistic_modifier_by_handle_id(game_object, modifier_handle_id)

        Remove a Statistic Modifier from an Object by a handle id.

        :param game_object: The Object to modify.
        :type game_object: GameObject
        :param modifier_handle_id: The handle id for the statistic modifier being removed.
        :type modifier_handle_id: int
        :return: True, if the modifier was removed successfully. False, if not.
        :rtype: bool
        """
        if game_object is None:
            cls.get_log().format_with_message('game_object was None!', modifier_handle=modifier_handle_id, game_object=game_object)
            return False
        return game_object.remove_statistic_modifier(modifier_handle_id)

    # noinspection PyUnusedLocal
    @classmethod
    def remove_all_statistic_modifiers_for_statistic(cls, game_object: GameObject, statistic: Union[int, CommonStatisticId, BaseStatistic]) -> bool:
        """remove_all_statistic_modifiers_for_statistic(game_object, statistic)

        Remove all Modifiers from the specified Statistic for the specified Object.

        :param game_object: The Object to modify.
        :type game_object: GameObject
        :param statistic: The identifier of the statistic to remove modifiers from.
        :type statistic: Union[int, CommonStatisticId, BaseStatistic]
        :return: True, if successful. False, if not successful.
        :rtype: bool
        """
        if game_object is None:
            cls.get_log().format_with_message('game_object was None!', statistic=statistic, game_object=game_object)
            return False
        statistic_instance = cls.get_statistic(game_object, statistic)
        if statistic_instance is None:
            cls.get_log().format_with_message('No statistic found on Object.', statistic=statistic, game_object=game_object)
            return False
        if not hasattr(statistic_instance, '_statistic_modifiers') or statistic_instance._statistic_modifiers is None:
            return False
        for value in list(statistic_instance._statistic_modifiers):
            statistic_instance.remove_statistic_modifier(value)
        return True

    @classmethod
    def get_statistic_tracker(cls, game_object: GameObject) -> StatisticTracker:
        """get_statistic_tracker(game_object)

        Retrieve the statistic tracker of an object.

        :param game_object: An Object.
        :type game_object: GameObject
        :return: The statistic tracker for the object.
        :rtype: StatisticTracker
        """
        return game_object.statistic_tracker


commands_log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_statistic_commands_object')
commands_log.enable()


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_statistic_value_object',
    'Print the value of a statistic on an Object.',
    command_arguments=(
        CommonConsoleCommandArgument('statistic', 'Statistic Id or Tuning Name', 'The tuning name or decimal identifier of a Statistic.'),
        CommonConsoleCommandArgument('game_object', 'Object Id or Name', 'The name or instance id of the Object to check.'),
    ),
    command_aliases=(
        's4clib.print_stat_value_object',
        's4clib.printstatvalueobject',
        's4clib.printstatisticvalueobject'
    )
)
def _common_print_statistic_value_object(output: CommonConsoleCommandOutput, statistic: TunableInstanceParam(Types.STATISTIC), game_object: GameObject):
    if statistic is None:
        output('ERROR: No Statistic specified or the specified Statistic did not exist!')
        return
    if game_object is None:
        return
    output(f'Attempting to get statistic {statistic} on Object {game_object}.')
    statistic_value = CommonObjectStatisticUtils.get_statistic_value(game_object, CommonStatisticUtils.get_statistic_id(statistic))
    output(f'Got statistic value of {statistic_value} of {statistic} on Object {game_object}.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_statistic_value_object',
    'Set the value of a statistic on an Object.',
    command_arguments=(
        CommonConsoleCommandArgument('statistic', 'Statistic Id or Tuning Name', 'The tuning name or decimal identifier of a Statistic.'),
        CommonConsoleCommandArgument('value', 'Decimal Number', 'The value to set the statistic to.'),
        CommonConsoleCommandArgument('game_object', 'Object Id or Name', 'The name or instance id of the Object to change.'),
    ),
    command_aliases=(
        's4clib.set_stat_value_object',
        's4clib.setstatvalueobject',
        's4clib.setstatisticvalueobject'
    )
)
def _common_set_statistic_value_object(output: CommonConsoleCommandOutput, statistic: TunableInstanceParam(Types.STATISTIC), value: float, game_object: GameObject):
    if statistic is None:
        output('ERROR: No Statistic specified or the specified Statistic did not exist!')
        return
    if game_object is None:
        return
    output(f'Attempting to set statistic {statistic} on Object {game_object} to value {value}.')
    if CommonObjectStatisticUtils.set_statistic_value(game_object, CommonStatisticUtils.get_statistic_id(statistic), value):
        output(f'SUCCESS: Successfully set statistic {statistic} of Object {game_object} to value {value}.')
    else:
        output(f'FAILED: Failed to set statistic {statistic} of Object {game_object} to value {value}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_statistic_object',
    'Remove a Statistic or Commodity from an Object.',
    command_arguments=(
        CommonConsoleCommandArgument('statistic', 'Statistic Id or Tuning Name', 'The tuning name or decimal identifier of a Statistic or Commodity.'),
        CommonConsoleCommandArgument('game_object', 'Object Id or Name', 'The name or instance id of the Object to change.'),
    ),
    command_aliases=(
        's4clib.remove_commodity_object',
        's4clib.remove_stat_object',
        's4clib.removestatobject',
        's4clib.removestatisticobject'
    )
)
def _common_remove_statistic_object(output: CommonConsoleCommandOutput, statistic: TunableInstanceParam(Types.STATISTIC), game_object: GameObject):
    if statistic is None:
        output('ERROR: No Statistic specified or the specified Statistic did not exist!')
        return
    if game_object is None:
        output('No object specified!')
        return
    output(f'Attempting to remove statistic {statistic} from Object {game_object}.')
    if CommonObjectStatisticUtils.remove_statistic(game_object, CommonStatisticUtils.get_statistic_id(statistic)):
        output(f'SUCCESS: Successfully removed statistic {statistic} from Object {game_object}.')
    else:
        output(f'FAILED: Failed to remove statistic {statistic} from Object {game_object}.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_statistics_object',
    'Print a list of a Statistics on an Object.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Object Id or Name', 'The name or instance id of the Object to check.'),
    ),
    command_aliases=(
        's4clib_testing.printstatisticsobject',
    )
)
def _common_print_statistics_object(output: CommonConsoleCommandOutput, game_object: GameObject):
    log = CommonObjectStatisticUtils.get_log()
    try:
        log.enable()
        output(f'Printing statistics of Object {game_object}')
        text = ''
        for stat in list(game_object.statistic_tracker):
            statistic_id = CommonStatisticUtils.get_statistic_id(stat)
            statistic_value = CommonObjectStatisticUtils.get_statistic_value(game_object, statistic_id)
            text += f'{stat} ({statistic_id}): {statistic_value}\n'
        game_object_id = CommonObjectUtils.get_object_id(game_object)
        log.debug(f'{game_object} Statistics ({game_object_id})')
        log.debug(text)
        CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string(f'{game_object} Statistics ({game_object_id})'),
            CommonLocalizationUtils.create_localized_string(text)
        ).show(
            icon=IconInfoData(obj_instance=game_object)
        )
    finally:
        log.disable()


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_commodities_object',
    'Print a list of a Commodities on an Object.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Object Id or Name', 'The name or instance id of the Object to check.'),
    ),
    command_aliases=(
        's4clib_testing.printcommoditiesobject',
    )
)
def _common_print_commodities_object(output: CommonConsoleCommandOutput, game_object: GameObject):
    log = CommonObjectStatisticUtils.get_log()
    try:
        log.enable()
        output(f'Printing commodities of Object {game_object}')
        text = ''
        for stat in list(game_object.commodity_tracker):
            statistic_id = CommonStatisticUtils.get_statistic_id(stat)
            statistic_value = CommonObjectStatisticUtils.get_statistic_value(game_object, statistic_id)
            text += f'{stat} ({statistic_id}): {statistic_value}\n'
        game_object_id = CommonObjectUtils.get_object_id(game_object)
        log.debug(f'{game_object} Commodities ({game_object_id})')
        log.debug(text)
        CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string(f'{game_object} Commodities ({game_object_id})'),
            CommonLocalizationUtils.create_localized_string(text)
        ).show(
            icon=IconInfoData(obj_instance=game_object)
        )
    finally:
        log.disable()


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_static_commodities_object',
    'Print a list of a Static Commodities on an Object.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Object Id or Name', 'The name or instance id of the Object to check.'),
    ),
    command_aliases=(
        's4clib_testing.printstaticcommoditiesobject',
    )
)
def _common_print_static_commodities_object(output: CommonConsoleCommandOutput, game_object: GameObject):
    log = CommonObjectStatisticUtils.get_log()
    try:
        log.enable()
        output(f'Printing static commodities of Object {game_object}')
        text = ''
        for stat in list(game_object.static_commodity_tracker):
            statistic_id = CommonStatisticUtils.get_statistic_id(stat)
            text += f'{stat} ({statistic_id})\n'
        game_object_id = CommonObjectUtils.get_object_id(game_object)
        log.debug(f'{game_object} Static Commodities ({game_object_id})')
        log.debug(text)
        CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string(f'{game_object} Static Commodities ({game_object_id})'),
            CommonLocalizationUtils.create_localized_string(text)
        ).show(
            icon=IconInfoData(obj_instance=game_object)
        )
    finally:
        log.disable()
