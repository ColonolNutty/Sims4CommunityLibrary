"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, List

from buffs.buff import Buff
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.enums.buffs_enum import CommonBuffId
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils


class CommonBuffUtils:
    """Utilities for manipulating Buffs on Sims.

    """
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
    def has_buff(sim_info: SimInfo, *buff_ids: int) -> bool:
        """has_buff(sim_info, *buff_ids)

        Determine if any of the specified buffs are currently active on a sim.

        :param sim_info: The sim being checked.
        :type sim_info: SimInfo
        :param buff_ids: The decimal identifiers of Buffs.
        :type buff_ids: int
        :return: True if the sim has any of the specified buffs.
        :rtype: int
        """
        if sim_info is None:
            CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Argument \'sim_info\' was \'None\' for \'{}\' of class \'{}\''.format(CommonBuffUtils.has_buff.__name__, CommonBuffUtils.__name__))
            return False
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            return False
        if not buff_ids:
            return False
        sim_buffs = CommonBuffUtils.get_buffs(sim_info)
        for buff in sim_buffs:
            buff_id = CommonBuffUtils.get_buff_id(buff)
            if buff_id in buff_ids:
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
            CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Argument \'sim_info\' was \'None\' for \'{}\' of class \'{}\''.format(CommonBuffUtils.get_buffs.__name__, CommonBuffUtils.__name__))
            return list()
        if not hasattr(sim_info, 'get_active_buff_types'):
            return list()
        return list(sim_info.get_active_buff_types())

    @staticmethod
    def add_buff(sim_info: SimInfo, *buff_ids: int, buff_reason: Union[int, str, LocalizedString]=None) -> bool:
        """add_buff(sim_info, *buff_ids, buff_reason=None)

        Add the specified buffs to a sim.

        :param sim_info: The sim to add the specified buffs to.
        :type sim_info: SimInfo
        :param buff_ids: The decimal identifiers of buffs to add.
        :type buff_ids: int
        :param buff_reason: The text that will display when the player hovers over the buffs. What caused the buffs to be added.
        :type buff_reason: Union[int, str, LocalizedString], optional
        :return: True, if all of the specified buffs were successfully added. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Argument \'sim_info\' was \'None\' for \'{}\' of class \'{}\''.format(CommonBuffUtils.add_buff.__name__, CommonBuffUtils.__name__))
            return False
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            return False
        localized_buff_reason = CommonLocalizationUtils.create_localized_string(buff_reason)
        success = True
        for buff_identifier in buff_ids:
            buff_instance = CommonBuffUtils._load_buff_instance(buff_identifier)
            if buff_instance is None:
                continue
            if not sim_info.add_buff_from_op(buff_instance, buff_reason=localized_buff_reason):
                success = False
        return success

    @staticmethod
    def remove_buff(sim_info: SimInfo, *buff_ids: int) -> bool:
        """remove_buff(sim_info, *buff_ids)

        Remove the specified buffs from a sim.

        :param sim_info: The sim to remove the specified buffs from.
        :type sim_info: SimInfo
        :param buff_ids: The decimal identifiers of Buffs to remove.
        :type buff_ids: int
        :return: True, if all of the specified buffs were successfully removed. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Argument \'sim_info\' was \'None\' for \'{}\' of class \'{}\''.format(CommonBuffUtils.remove_buff.__name__, CommonBuffUtils.__name__))
            return False
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            return False
        success = True
        for buff_identifier in buff_ids:
            buff_instance = CommonBuffUtils._load_buff_instance(buff_identifier)
            if buff_instance is None:
                continue
            if not sim_info.remove_buff_by_type(buff_instance):
                success = False
        return success

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
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=None)
    def _load_buff_instance(buff_identifier: int) -> Union[Buff, None]:
        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.BUFF, buff_identifier)
