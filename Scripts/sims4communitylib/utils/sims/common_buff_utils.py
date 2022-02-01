"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, List, Tuple, Iterator

from buffs.buff import Buff
from distributor.shared_messages import IconInfoData
from protocolbuffers.Localization_pb2 import LocalizedString
from server_commands.argument_helpers import TunableInstanceParam
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.enums.buffs_enum import CommonBuffId
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonBuffUtils(HasClassLog):
    """Utilities for manipulating Buffs on Sims.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_buff_utils'

    @staticmethod
    def has_fertility_boosting_buff(sim_info: SimInfo) -> bool:
        """has_fertility_boosting_buff(sim_info)

        Determine if any fertility boosting buffs are currently active on a sim.

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
        :return: True, if they have any fertility boosting buffs. False, if not.
        :rtype: bool
        """
        buff_ids = (
            CommonBuffId.OBJECT_HERBALIST_POTION_FERTILITY_POTION,
            CommonBuffId.OBJECT_HERBALIST_POTION_FERTILITY_POTION_MASTERWORK,
            CommonBuffId.OBJECT_HERBALIST_POTION_FERTILITY_POTION_NORMAL,
            CommonBuffId.OBJECT_HERBALIST_POTION_FERTILITY_POTION_OUTSTANDING,
            CommonBuffId.OBJECT_MASSAGE_TABLE_FERTILITY_BOOST,
            CommonBuffId.OBJECT_MASSAGE_TABLE_FERTILITY_BOOST_INCENSE
        )
        return CommonBuffUtils.has_buff(sim_info, *buff_ids)

    @staticmethod
    def has_morning_person_buff(sim_info: SimInfo) -> bool:
        """has_morning_person_buff(sim_info)

        Determine if any Morning Person Trait buffs are currently active on a Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if they have any morning person buffs. False, if not.
        :rtype: bool
        """
        buff_ids = (
            CommonBuffId.TRAIT_MORNING_PERSON,
            CommonBuffId.TRAIT_MORNING_PERSON_ACTIVE,
            CommonBuffId.TRAIT_MORNING_PERSON_CHECK_ACTIVE
        )
        return CommonBuffUtils.has_buff(sim_info, *buff_ids)

    @staticmethod
    def has_night_owl_buff(sim_info: SimInfo) -> bool:
        """has_night_owl_buff(sim_info)

        Determine if any Night Owl Trait buffs are currently active on a sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if they have any night owl buffs. False, if not.
        :rtype: bool
        """
        buff_ids = (
            CommonBuffId.TRAIT_NIGHT_OWL,
            CommonBuffId.TRAIT_NIGHT_OWL_ACTIVE,
            CommonBuffId.TRAIT_NIGHT_OWL_CHECK_ACTIVE
        )
        return CommonBuffUtils.has_buff(sim_info, *buff_ids)

    @staticmethod
    def has_buff(sim_info: SimInfo, *buffs: Union[int, CommonBuffId, Buff]) -> bool:
        """has_buff(sim_info, *buffs)

        Determine if any of the specified buffs are currently active on a sim.

        :param sim_info: The sim being checked.
        :type sim_info: SimInfo
        :param buffs: The identifiers of Buffs.
        :type buffs: Union[int, CommonBuffId, Buff]
        :return: True, if the sim has any of the specified buffs.
        :rtype: int
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            return False
        if not buffs:
            return False
        buff_ids = [CommonBuffUtils.get_buff_id(buff) for buff in buffs]
        sim_buff_ids = CommonBuffUtils.get_buff_ids(sim_info)
        for sim_buff_id in sim_buff_ids:
            if sim_buff_id in buff_ids:
                return True
        return False

    @staticmethod
    def get_buffs(sim_info: SimInfo) -> List[Buff]:
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

    @staticmethod
    def get_buff_ids(sim_info: SimInfo) -> List[int]:
        """get_buff_ids(sim_info)

        Retrieve decimal identifiers for all Buffs of a sim.

        :param sim_info: The sim to checked.
        :type sim_info: SimInfo
        :return: A collection of Buff identifiers on a Sim.
        :rtype: List[int]
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            return list()
        buff_ids = list()
        sim_buffs = CommonBuffUtils.get_buffs(sim_info)
        for buff in sim_buffs:
            buff_id = CommonBuffUtils.get_buff_id(buff)
            if buff_id is None:
                continue
            buff_ids.append(buff_id)
        return buff_ids

    @classmethod
    def add_buff(cls, sim_info: SimInfo, *buffs: Union[int, CommonBuffId], buff_reason: Union[int, str, LocalizedString, CommonStringId]=None) -> bool:
        """add_buff(sim_info, *buffs, buff_reason=None)

        Add the specified buffs to a sim.

        :param sim_info: The sim to add the specified buffs to.
        :type sim_info: SimInfo
        :param buffs: An iterable of identifiers of buffs being added.
        :type buffs: Union[int, CommonBuffId, Buff]
        :param buff_reason: The text that will display when the player hovers over the buffs. What caused the buffs to be added.
        :type buff_reason: Union[int, str, LocalizedString, CommonStringId], optional
        :return: True, if all of the specified buffs were successfully added. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            cls.get_log().format_with_message('Failed to add Buff to Sim. They did not have a Buff component!', buffs=buffs, sim=sim_info, buff_reason=buff_reason)
            return False
        localized_buff_reason = None
        if buff_reason is not None:
            localized_buff_reason = CommonLocalizationUtils.create_localized_string(buff_reason)
        has_any = False
        success = True
        for buff_id in buffs:
            buff = CommonBuffUtils.load_buff_by_id(buff_id)
            if buff is None:
                cls.get_log().format_with_message('No buff found using identifier.', buffs=buffs, sim=sim_info, buff_reason=buff_reason, buff_id=buff_id)
                continue
            if not sim_info.add_buff_from_op(buff, buff_reason=localized_buff_reason):
                cls.get_log().format_with_message('Failed to add buff for unknown reasons.', buff=buff, sim=sim_info, buff_reason=buff_reason)
                success = False
            else:
                cls.get_log().format_with_message('Successfully added buff.', buff=buff, sim=sim_info, buff_reason=buff_reason)
                has_any = True
        cls.get_log().format_with_message('Finished adding buffs to Sim.', buffs=buffs, sim=sim_info, buff_reason=buff_reason, success=success, has_any=has_any)
        return success and has_any

    @staticmethod
    def remove_buff(sim_info: SimInfo, *buffs: Union[int, CommonBuffId, Buff]) -> bool:
        """remove_buff(sim_info, *buffs)

        Remove the specified buffs from a sim.

        :param sim_info: The sim to remove the specified buffs from.
        :type sim_info: SimInfo
        :param buffs: An iterable of identifiers of buffs being removed.
        :type buffs: Union[int, CommonBuffId, Buff]
        :return: True, if all of the specified buffs were successfully removed. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            return False
        has_any = False
        success = True
        for buff in buffs:
            buff = CommonBuffUtils.load_buff_by_id(buff)
            if buff is None:
                continue
            sim_info.remove_buff_by_type(buff)
            has_any = True
            if CommonBuffUtils.has_buff(sim_info, buff):
                success = False
        return success and has_any

    @staticmethod
    def get_buff_id(buff_identifier: Union[int, Buff]) -> Union[int, None]:
        """get_buff_id(buff_identifier)

        Retrieve the decimal identifier of a Buff.

        :param buff_identifier: The identifier or instance of a Buff.
        :type buff_identifier: Union[int, Buff]
        :return: The decimal identifier of the Buff or None if the Buff does not have an id.
        :rtype: Union[int, None]
        """
        if isinstance(buff_identifier, int):
            return buff_identifier
        return getattr(buff_identifier, 'guid64', None)

    @staticmethod
    def get_buff_name(buff: Buff) -> Union[str, None]:
        """get_buff_name(buff)

        Retrieve the Name of a Buff.

        :param buff: An instance of a Buff.
        :type buff: Buff
        :return: The name of a Buff or None if a problem occurs.
        :rtype: Union[str, None]
        """
        if buff is None:
            return None
        # noinspection PyBroadException
        try:
            return buff.__class__.__name__ or ''
        except:
            return ''

    @staticmethod
    def get_buff_names(buffs: Iterator[Buff]) -> Tuple[str]:
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
                name = CommonBuffUtils.get_buff_name(buff)
                if not name:
                    continue
            except:
                continue
            names.append(name)
        return tuple(names)

    @staticmethod
    def load_buff_by_id(buff: Union[int, CommonBuffId, Buff]) -> Union[Buff, None]:
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
            buff: int = int(buff)
        except:
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
def _common_add_buff(output: CommonConsoleCommandOutput, buff: TunableInstanceParam(Types.BUFF), sim_info: SimInfo=None, buff_reason: str=None):
    if buff is None:
        return
    if sim_info is None:
        return
    output(f'Adding buff {buff} to Sim {sim_info}')
    result = CommonBuffUtils.add_buff(sim_info, buff, buff_reason=buff_reason)
    if result:
        output(f'SUCCESS: Successfully added buff {buff} to Sim {sim_info}.')
    else:
        output(f'FAILED: Failed to add buff {buff} to Sim {sim_info}: {result}')


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
def _common_remove_buff(output: CommonConsoleCommandOutput, buff: TunableInstanceParam(Types.BUFF), sim_info: SimInfo=None):
    if buff is None:
        return
    if sim_info is None:
        return
    output(f'Removing buff {buff} from Sim {sim_info}')
    result = CommonBuffUtils.remove_buff(sim_info, buff)
    if result:
        output(f'SUCCESS: Successfully removed buff {buff} from Sim {sim_info}.')
    else:
        output(f'FAILED: Failed to remove buff {buff} from Sim {sim_info}: {result}')


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
def _common_print_buffs_on_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo=None):
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
