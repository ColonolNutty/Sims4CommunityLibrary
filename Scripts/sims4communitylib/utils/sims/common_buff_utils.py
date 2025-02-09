"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, List, Tuple, Iterator

from buffs.buff import Buff
from distributor.shared_messages import IconInfoData
from objects.components.buff_component import BuffComponent
from protocolbuffers.Localization_pb2 import LocalizedString
from server_commands.argument_helpers import TunableInstanceParam
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.buffs_enum import CommonBuffId
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonBuffUtils(_HasS4CLClassLog):
    """Utilities for manipulating Buffs on Sims.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_buff_utils'

    @classmethod
    def has_fertility_boosting_buff(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_fertility_boosting_buff(sim_info)

        Determine if any fertility boosting buffs are currently active on a Sim.

        .. note::

            Fertility Boosting Buffs:

            - Fertility Potion
            - Fertility Potion Masterwork
            - Fertility Potion Normal
            - Fertility Potion Outstanding
            - Massage Table Fertility Boost
            - Massage Table Fertility Boost Incense

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if they have any fertility boosting buffs. False, if not.
        :rtype: CommonTestResult
        """
        buff_ids = (
            CommonBuffId.OBJECT_HERBALIST_POTION_FERTILITY_POTION,
            CommonBuffId.OBJECT_HERBALIST_POTION_FERTILITY_POTION_MASTERWORK,
            CommonBuffId.OBJECT_HERBALIST_POTION_FERTILITY_POTION_NORMAL,
            CommonBuffId.OBJECT_HERBALIST_POTION_FERTILITY_POTION_OUTSTANDING,
            CommonBuffId.OBJECT_MASSAGE_TABLE_FERTILITY_BOOST,
            CommonBuffId.OBJECT_MASSAGE_TABLE_FERTILITY_BOOST_INCENSE
        )
        return cls.has_any_buffs(sim_info, buff_ids)

    @classmethod
    def has_morning_person_buff(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_morning_person_buff(sim_info)

        Determine if any Morning Person Trait buffs are currently active on a Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if they have any morning person buffs. False, if not.
        :rtype: CommonTestResult
        """
        buff_ids = (
            CommonBuffId.TRAIT_MORNING_PERSON,
            CommonBuffId.TRAIT_MORNING_PERSON_ACTIVE,
            CommonBuffId.TRAIT_MORNING_PERSON_CHECK_ACTIVE
        )
        return cls.has_any_buffs(sim_info, buff_ids)

    @classmethod
    def has_night_owl_buff(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_night_owl_buff(sim_info)

        Determine if any Night Owl Trait buffs are currently active on a Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if they have any night owl buffs. False, if not.
        :rtype: CommonTestResult
        """
        buff_ids = (
            CommonBuffId.TRAIT_NIGHT_OWL,
            CommonBuffId.TRAIT_NIGHT_OWL_ACTIVE,
            CommonBuffId.TRAIT_NIGHT_OWL_CHECK_ACTIVE
        )
        return cls.has_any_buffs(sim_info, buff_ids)

    @classmethod
    def has_buff(cls, sim_info: SimInfo, *buff: Union[int, CommonBuffId, Buff]) -> CommonTestResult:
        """has_buff(sim_info, buff)

        Determine if the Sim has a Buff.

        :param sim_info: The Sim being checked.
        :type sim_info: SimInfo
        :param buff: The buff to check for.
        :type buff: Union[int, CommonBuffId, Buff]
        :return: The result of testing. True, if the Sim has the specified buff. False, if not.
        :rtype: CommonTestResult
        """
        return cls.has_any_buffs(sim_info, buff)

    @classmethod
    def has_any_buffs(cls, sim_info: SimInfo, buffs: Iterator[Union[int, CommonBuffId, Buff]]) -> CommonTestResult:
        """has_any_buffs(sim_info, buffs)

        Determine if the Sim has any of the specified buffs.

        :param sim_info: The Sim being checked.
        :type sim_info: SimInfo
        :param buffs: An iterator of buffs to check for.
        :type buffs: Iterator[Union[int, CommonBuffId, Buff]]
        :return: The result of testing. True, if the Sim has any of the specified buffs. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not buffs:
            return CommonTestResult(False, reason='No buffs were specified.', hide_tooltip=True)
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            return CommonTestResult(False, reason=f'Target Sim {sim_info} did not have a Buff Component.', hide_tooltip=True)
        from objects.components.buff_component import BuffComponent
        buff_component: BuffComponent = CommonComponentUtils.get_component(sim_info, CommonComponentType.BUFF)
        for buff in buffs:
            _buff = cls.load_buff_by_id(buff)
            cls.get_log().format_with_message('Got the buff', buff=_buff)
            if _buff is None:
                continue
            if buff_component.has_buff(_buff):
                return CommonTestResult(True, reason=f'{sim_info} has buff {_buff}.', tooltip_text=CommonStringId.S4CL_SIM_HAS_BUFF, tooltip_tokens=(sim_info, str(_buff)))
        return CommonTestResult(False, reason=f'{sim_info} does not have any buff(s) {buffs}.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_BUFFS, tooltip_tokens=(sim_info, str(buffs)))

    @classmethod
    def has_all_buffs(cls, sim_info: SimInfo, buffs: Iterator[Union[int, CommonBuffId, Buff]]) -> CommonTestResult:
        """has_all_buffs(sim_info, buffs)

        Determine if the Sim has all the specified buffs.

        :param sim_info: The Sim being checked.
        :type sim_info: SimInfo
        :param buffs: An iterator of buffs to check for.
        :type buffs: Iterator[Union[int, CommonBuffId, Buff]]
        :return: The result of testing. True, if the Sim has all of the specified buffs. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not buffs:
            return CommonTestResult(False, reason='No buffs were specified.', hide_tooltip=True)
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            return CommonTestResult(False, reason=f'Target Sim {sim_info} did not have a Buff Component.', hide_tooltip=True)
        from objects.components.buff_component import BuffComponent
        buff_component: BuffComponent = CommonComponentUtils.get_component(sim_info, CommonComponentType.BUFF, return_type=BuffComponent)
        for buff in buffs:
            _buff = cls.load_buff_by_id(buff)
            cls.get_log().format_with_message('Got the buff', buff=_buff)
            if _buff is None:
                continue
            if not buff_component.has_buff(_buff):
                return CommonTestResult(False, reason=f'{sim_info} does not have buff {_buff}.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_BUFF, tooltip_tokens=(sim_info, str(_buff)))
        return CommonTestResult(True, reason=f'{sim_info} has all buffs {buffs}.', tooltip_text=CommonStringId.S4CL_SIM_HAS_ALL_BUFFS, tooltip_tokens=(sim_info, str(buffs)))

    @classmethod
    def get_buffs(cls, sim_info: SimInfo) -> List[Buff]:
        """get_buffs(sim_info)

        Retrieve all buffs currently active on a Sim.

        :param sim_info: The Sim to retrieve the buffs of.
        :type sim_info: SimInfo
        :return: A collection of currently active buffs on the Sim.
        :rtype: Tuple[Buff]
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            return list()
        from objects.components.buff_component import BuffComponent
        buff_component: BuffComponent = CommonComponentUtils.get_component(sim_info, CommonComponentType.BUFF)
        buffs = list()
        for buff in buff_component:
            if buff is None or not isinstance(buff, Buff):
                continue
            buffs.append(buff)
        return buffs

    @classmethod
    def get_buff_ids(cls, sim_info: SimInfo) -> List[int]:
        """get_buff_ids(sim_info)

        Retrieve decimal identifiers for all Buffs of a Sim.

        :param sim_info: The Sim to checked.
        :type sim_info: SimInfo
        :return: A collection of Buff identifiers on a Sim.
        :rtype: List[int]
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            return list()
        buff_ids = list()
        sim_buffs = cls.get_buffs(sim_info)
        for buff in sim_buffs:
            buff_id = cls.get_buff_id(buff)
            if buff_id is None:
                continue
            buff_ids.append(buff_id)
        return buff_ids

    @classmethod
    def add_buff(cls, sim_info: SimInfo, *buff: Union[int, CommonBuffId], buff_reason: Union[int, str, LocalizedString, CommonStringId] = None) -> CommonExecutionResult:
        """add_buff(sim_info, buff, buff_reason=None)

        Add a Buff to a Sim.

        :param sim_info: The Sim to add the buff to.
        :type sim_info: SimInfo
        :param buff: The buff being added.
        :type buff: Union[int, CommonBuffId, Buff]
        :param buff_reason: The text that will display when the player hovers over the buffs. What caused the buffs to be added.
        :type buff_reason: Union[int, str, LocalizedString, CommonStringId], optional
        :return: The result of adding the buffs. True, if the specified buff was successfully added. False, if not.
        :rtype: CommonExecutionResult
        """
        return cls.add_buffs(sim_info, buff, buff_reason=buff_reason)

    @classmethod
    def add_buffs(cls, sim_info: SimInfo, buffs: Iterator[Union[int, CommonBuffId, Buff]], buff_reason: Union[int, str, LocalizedString, CommonStringId] = None) -> CommonExecutionResult:
        """add_buffs(sim_info, buffs, buff_reason=None)

        Add Buffs to a Sim.

        :param sim_info: The Sim to add the specified buffs to.
        :type sim_info: SimInfo
        :param buffs: An iterator of identifiers of buffs being added.
        :type buffs: Iterator[Union[int, CommonBuffId, Buff]]
        :param buff_reason: The text that will display when the player hovers over the buffs. What caused the buffs to be added.
        :type buff_reason: Union[int, str, LocalizedString, CommonStringId], optional
        :return: The result of adding the buffs. True, if all of the specified buffs were successfully added. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            cls.get_log().format_with_message('Failed to add Buff to Sim. They did not have a Buff component!', buffs=buffs, sim=sim_info, buff_reason=buff_reason)
            return CommonExecutionResult(False, reason=f'Target Sim {sim_info} did not have a Buff Component.', hide_tooltip=True)
        localized_buff_reason = None
        if buff_reason is not None:
            localized_buff_reason = CommonLocalizationUtils.create_localized_string(buff_reason)
        has_any_loaded = False
        success = True
        failed_to_add_buffs = list()
        for buff_id in buffs:
            buff = cls.load_buff_by_id(buff_id)
            if buff is None:
                cls.get_log().format_with_message('No buff found using identifier.', buffs=buffs, sim=sim_info, buff_reason=buff_reason, buff_id=buff_id)
                failed_to_add_buffs.append(buff_id)
                continue
            has_any_loaded = True
            add_result = sim_info.add_buff_from_op(buff, buff_reason=localized_buff_reason)
            if not add_result:
                cls.get_log().format_with_message('Failed to add buff.', buff=buff, sim=sim_info, buff_reason=buff_reason, reason=add_result)
                success = False
                failed_to_add_buffs.append(buff)
            else:
                cls.get_log().format_with_message('Successfully added buff.', buff=buff, sim=sim_info, buff_reason=buff_reason)
        cls.get_log().format_with_message('Finished adding buffs to Sim.', buffs=buffs, sim=sim_info, buff_reason=buff_reason, success=success, has_any_loaded=has_any_loaded, failed_to_add_buffs=failed_to_add_buffs)
        if not success:
            failed_to_add_buffs_str = ', '.join([cls.get_buff_name(buff) or str(buff) if isinstance(buff, Buff) else str(buff) for buff in failed_to_add_buffs])
            return CommonExecutionResult(False, reason=f'Failed to add buffs. {failed_to_add_buffs_str}', tooltip_text=CommonStringId.S4CL_FAILED_TO_ADD_BUFFS_TO_SIM, tooltip_tokens=(sim_info, failed_to_add_buffs_str))
        if not has_any_loaded:
            return CommonExecutionResult(True, reason=f'Finished "adding" buffs to {sim_info}, but none of the specified buffs were loaded.', tooltip_text=CommonStringId.S4CL_BUFFS_WERE_ADDED_TO_SIM_BUT_NONE_WERE_LOADED, tooltip_tokens=(sim_info,))
        return CommonExecutionResult(True, reason=f'Successfully added buffs to {sim_info}.', tooltip_text=CommonStringId.S4CL_SUCCESSFULLY_ADDED_BUFFS_TO_SIM, tooltip_tokens=(sim_info,))

    @classmethod
    def remove_buff(cls, sim_info: SimInfo, *buff: Union[int, CommonBuffId, Buff]) -> CommonExecutionResult:
        """remove_buff(sim_info, buff)

        Remove a Buff from a Sim.

        :param sim_info: The Sim to remove the buff from.
        :type sim_info: SimInfo
        :param buff: The buff being removed.
        :type buff: Union[int, CommonBuffId, Buff]
        :return: The result of removing the buff. True, if the buff was successfully removed. False, if not.
        :rtype: CommonExecutionResult
        """
        return cls.remove_buffs(sim_info, buff)

    @classmethod
    def remove_buffs(cls, sim_info: SimInfo, buffs: Iterator[Union[int, CommonBuffId, Buff]]) -> CommonExecutionResult:
        """remove_buffs(sim_info, buffs)

        Remove Buffs from a Sim.

        :param sim_info: The Sim to remove the specified buffs from.
        :type sim_info: SimInfo
        :param buffs: An iterator of identifiers of buffs being removed.
        :type buffs: Iterator[Union[int, CommonBuffId, Buff]]
        :return: The result of removing the buffs. True, if all of the specified buffs were successfully removed. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            return CommonExecutionResult(False, reason=f'Target Sim {sim_info} did not have a Buff Component.', hide_tooltip=True)
        has_any_loaded = False
        success = True
        failed_to_remove_buffs = list()
        for buff_id in buffs:
            buff = cls.load_buff_by_id(buff_id)
            if buff is None:
                failed_to_remove_buffs.append(buff_id)
                continue
            if not cls.has_buff(sim_info, buff_id):
                continue
            has_any_loaded = True
            sim_info.remove_buff_by_type(buff)
            if cls.has_buff(sim_info, buff):
                failed_to_remove_buffs.append(buff)
                success = False

        if not success:
            failed_to_remove_buffs_str = ', '.join([cls.get_buff_name(buff) or str(buff) if isinstance(buff, Buff) else str(buff) for buff in failed_to_remove_buffs])
            return CommonExecutionResult(False, reason=f'Failed to remove buffs from {sim_info}. {failed_to_remove_buffs_str}', tooltip_text=CommonStringId.S4CL_FAILED_TO_REMOVE_BUFFS_FROM_SIM, tooltip_tokens=(sim_info, failed_to_remove_buffs_str))
        if not has_any_loaded:
            return CommonExecutionResult(True, reason=f'Finished "removing" buffs from {sim_info}, but none of the specified buffs were loaded.', tooltip_text=CommonStringId.S4CL_BUFFS_WERE_REMOVED_FROM_SIM_BUT_NONE_WERE_LOADED, tooltip_tokens=(sim_info,))
        return CommonExecutionResult(True, reason=f'Successfully removed buffs from {sim_info}.', tooltip_text=CommonStringId.S4CL_SUCCESSFULLY_REMOVED_BUFFS_FROM_SIM, tooltip_tokens=(sim_info,))

    @classmethod
    def get_buff_id(cls, buff_identifier: Union[int, Buff]) -> Union[int, None]:
        """get_buff_id(buff_identifier)

        Retrieve the GUID (Decimal Identifier) of a Buff.

        :param buff_identifier: The identifier or instance of a Buff.
        :type buff_identifier: Union[int, Buff]
        :return: The decimal identifier of the Buff or None if the Buff does not have an id.
        :rtype: Union[int, None]
        """
        if isinstance(buff_identifier, int):
            return buff_identifier
        return getattr(buff_identifier, 'guid64', None)

    @classmethod
    def get_buff_name(cls, buff: Buff) -> Union[str, None]:
        """get_buff_name(buff)

        Retrieve the Name of a Buff.

        :param buff: An instance of a Buff.
        :type buff: Buff
        :return: The name of a Buff or None if a problem occurs.
        :rtype: Union[str, None]
        """
        if buff is None:
            return None
        return str(buff)

    @classmethod
    def get_buff_names(cls, buffs: Iterator[Buff]) -> Tuple[str]:
        """get_buff_names(buffs)

        Retrieve the Names of a collection of Buffs.

        :param buffs: A collection of Buff instances.
        :type buffs: Iterator[Buff]
        :return: A collection of names for all specified Buffs.
        :rtype: Tuple[str]
        """
        if buffs is None or not buffs:
            return tuple()
        names: List[str] = []
        for buff in buffs:
            # noinspection PyBroadException
            try:
                name = cls.get_buff_name(buff)
                if not name:
                    continue
            except:
                continue
            names.append(name)
        return tuple(names)

    @classmethod
    def get_buff_component(cls, sim_info: SimInfo) -> Union[BuffComponent, None]:
        """get_buff_component(sim_info)

        Retrieve the buff component of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The buff component of the Sim or None if not found.
        :rtype: Union[BuffComponent, None]
        """
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            return None
        result: BuffComponent = CommonComponentUtils.get_component(sim_info, CommonComponentType.BUFF)
        return result

    @classmethod
    def is_buff_available(cls, buff: Union[int, CommonBuffId, Buff]) -> bool:
        """is_buff_available(buff)

        Determine if a Buff is available for use.

        .. note:: If the Buff is part of a package that is not installed, it will be considered as not available.

        :param buff: The buff to check for.
        :type buff: Union[int, CommonBuffId, Buff]
        :return: True, if the Buff is available for use. False, if not.
        :rtype: bool
        """
        return cls.load_buff_by_id(buff) is not None

    @classmethod
    def load_buff_by_id(cls, buff: Union[int, CommonBuffId, Buff]) -> Union[Buff, None]:
        """load_buff_by_id(buff)

        Load an instance of a Buff by its identifier.

        :param buff: The identifier of a Buff.
        :type buff: Union[int, CommonBuffId, Buff]
        :return: An instance of a Buff matching the decimal identifier or None if not found.
        :rtype: Union[Buff, None]
        """
        if isinstance(buff, Buff):
            return buff
        # noinspection PyBroadException
        try:
            # noinspection PyCallingNonCallable
            buff_instance = buff()
            if isinstance(buff_instance, Buff):
                # noinspection PyTypeChecker
                return buff
        except:
            pass
        # noinspection PyBroadException
        try:
            buff: int = int(buff)
        except:
            # noinspection PyTypeChecker
            buff: Buff = buff
            return buff

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.BUFF, buff)


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.add_buff',
    'Add a buff to a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('buff', 'Buff Id or Tuning Name', 'The decimal identifier or Tuning Name of the Buff to add.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to add the buff to.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.addbuff',
    )
)
def _common_add_buff(output: CommonConsoleCommandOutput, buff: TunableInstanceParam(Types.BUFF), sim_info: SimInfo = None, buff_reason: str = None):
    if buff is None or isinstance(buff, str):
        return
    if sim_info is None:
        return
    output(f'Adding buff {buff} to Sim {sim_info}')
    result = CommonBuffUtils.add_buff(sim_info, buff, buff_reason=buff_reason)
    if result:
        output(f'SUCCESS: Successfully added buff {buff} to Sim {sim_info}: {result.reason}')
    else:
        output(f'FAILED: Failed to add buff {buff} to Sim {sim_info}: {result.reason}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_buff',
    'Remove a buff from a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('buff', 'Buff Id or Tuning Name', 'The decimal identifier or Tuning Name of the Buff to remove.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to remove the buff from.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.removebuff',
    )
)
def _common_remove_buff(output: CommonConsoleCommandOutput, buff: TunableInstanceParam(Types.BUFF), sim_info: SimInfo = None):
    if buff is None:
        return
    if sim_info is None:
        return
    output(f'Removing buff {buff} from Sim {sim_info}')
    result = CommonBuffUtils.remove_buff(sim_info, buff)
    if result:
        output(f'SUCCESS: Successfully removed buff {buff} from Sim {sim_info}: {result.reason}')
    else:
        output(f'FAILED: Failed to remove buff {buff} from Sim {sim_info}: {result.reason}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_buffs',
    'Print a list of all buffs on a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib_testing.printbuffs',
    )
)
def _common_print_buffs_on_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        return
    log = CommonBuffUtils.get_log()
    try:
        log.enable()
        output(f'Attempting to print buffs on Sim {sim_info}')
        buff_strings: List[str] = list()
        for buff in CommonBuffUtils.get_buffs(sim_info):
            buff_name = CommonBuffUtils.get_buff_name(buff)
            buff_id = CommonBuffUtils.get_buff_id(buff)
            buff_strings.append(f'{buff_name} ({buff_id})')

        buff_strings = sorted(buff_strings, key=lambda x: x)
        sim_buffs = ', '.join(buff_strings)
        text = ''
        text += f'Buffs:\n{sim_buffs}\n\n'
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        log.debug(f'{sim_info} Buffs ({sim_id})')
        log.debug(text)
        CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string(f'{sim_info} Buffs ({sim_id})'),
            CommonLocalizationUtils.create_localized_string(text)
        ).show(
            icon=IconInfoData(obj_instance=CommonSimUtils.get_sim_instance(sim_info))
        )
    finally:
        log.disable()

# log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'buff_not_properly_adding_log')
#
# @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), BuffComponent, BuffComponent._can_add_buff_type.__name__)
# def _common_can_add_buff_type(original, self, buff_type):
#     if not buff_type.can_add(self.owner):
#         log.format_with_message(f'Cannot add buff {buff_type}. Can Add')
#         return (False, None)
#     mood = buff_type.mood_type
#     if mood is not None and mood.excluding_traits is not None and self.owner.trait_tracker.has_any_trait(mood.excluding_traits):
#         log.format_with_message(f'Cannot add buff {buff_type}. MOOD', mood=mood, mood_excluding_traits=mood.excluding_traits)
#         return (False, None)
#     if buff_type.exclusive_index is None:
#         log.format_with_message(f'Can add buff {buff_type}. Exclusive Index')
#         return (True, None)
#     for conflicting_buff_type in self._active_buffs:
#         if conflicting_buff_type is buff_type:
#             pass
#         elif conflicting_buff_type.exclusive_index == buff_type.exclusive_index:
#             if buff_type.exclusive_weight < conflicting_buff_type.exclusive_weight:
#                 log.format_with_message(f'Cannot add buff {buff_type}. Conflicting buff.', buff_weight=buff_type.exclusive_weight, conflicting_buff_weight=conflicting_buff_type.exclusive_weight)
#                 return (False, None)
#             log.format_with_message(f'Cannot add buff {buff_type}. Conflicting buff 23432.', conflicting_buff_type=conflicting_buff_type)
#             return (True, conflicting_buff_type)
#     log.format_with_message(f'Can add buff {buff_type}.')
#     return (True, None)