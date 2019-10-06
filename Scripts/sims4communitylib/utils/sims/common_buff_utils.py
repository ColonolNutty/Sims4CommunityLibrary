"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

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
    """ Utilities for handling buffs on sims. """
    @classmethod
    def has_fertility_boosting_buff(cls, sim_info: SimInfo) -> bool:
        """
            Determine if any fertility boosting buffs are currently active on a sim.

            Fertility Boosting Buffs:
            - Fertility Potion
            - Fertility Potion Masterwork
            - Fertility Potion Normal
            - Fertility Potion Outstanding
            - Massage Table Fertility Boost
            - Massage Table Fertility Boost Incense
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

    @classmethod
    def has_morning_person_buff(cls, sim_info: SimInfo) -> bool:
        """
            Determine if any Morning Person Trait buffs are currently active on a sim.
        """
        buff_ids = (
            CommonBuffId.TRAIT_MORNING_PERSON,
            CommonBuffId.TRAIT_MORNING_PERSON_ACTIVE,
            CommonBuffId.TRAIT_MORNING_PERSON_CHECK_ACTIVE
        )
        return CommonBuffUtils.has_buff(sim_info, *buff_ids)

    @classmethod
    def has_night_owl_buff(cls, sim_info: SimInfo) -> bool:
        """
            Determine if any Night Owl Trait buffs are currently active on a sim.
        """
        buff_ids = (
            CommonBuffId.TRAIT_NIGHT_OWL,
            CommonBuffId.TRAIT_NIGHT_OWL_ACTIVE,
            CommonBuffId.TRAIT_NIGHT_OWL_CHECK_ACTIVE
        )
        return CommonBuffUtils.has_buff(sim_info, *buff_ids)

    @classmethod
    def has_buff(cls, sim_info: SimInfo, *buff_ids: int) -> bool:
        """
            Determine if any of the specified buffs are currently active on a sim.
        :param sim_info: The sim being checked.
        :param buff_ids: The decimal identifiers of the Buffs being located.
        :return: True if the sim has any of the specified buffs.
        """
        if sim_info is None:
            CommonExceptionHandler.log_exception(ModInfo.MOD_NAME, 'argument sim_info was \'None\' for {} of class {}'.format(CommonBuffUtils.has_buff.__name__, CommonBuffUtils.__name__))
            return False
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.BUFF):
            return False
        if not buff_ids:
            return False
        sim_buffs = CommonBuffUtils.get_buffs(sim_info)
        for buff in sim_buffs:
            buff_id = getattr(buff, 'guid64', None)
            if buff_id in buff_ids:
                return True
        return False

    @classmethod
    def get_buffs(cls, sim_info: SimInfo) -> List[Buff]:
        """
            Retrieve all buffs currently active on a sim.
        """
        if sim_info is None:
            CommonExceptionHandler.log_exception(ModInfo.MOD_NAME, 'argument sim_info was \'None\' for {} of class {}'.format(CommonBuffUtils.get_buffs.__name__, CommonBuffUtils.__name__))
            return list()
        if not hasattr(sim_info, 'get_active_buff_types'):
            return list()
        return list(sim_info.get_active_buff_types())

    @classmethod
    def add_buff(cls, sim_info: SimInfo, *buff_ids: int, buff_reason: [int, str, LocalizedString]=None) -> bool:
        """
            Add the specified buffs to a sim.
        :param sim_info: The sim to add the specified buffs to.
        :param buff_ids: The decimal identifiers of buffs to add.
        :param buff_reason: The text that will display when the player hovers over the buffs. What caused the buffs to be added.
        :return: True if all of the specified buffs were successfully added.
        """
        if sim_info is None:
            CommonExceptionHandler.log_exception(ModInfo.MOD_NAME, 'argument sim_info was \'None\' for {} of class {}'.format(CommonBuffUtils.add_buff.__name__, CommonBuffUtils.__name__))
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

    @classmethod
    def remove_buff(cls, sim_info: SimInfo, *buff_ids: int) -> bool:
        """
            Remove the specified buffs from a sim.
        :param sim_info: The sim to remove the specified buffs from.
        :param buff_ids: The decimal identifiers of buffs to remove.
        :return: True if all of the specified buffs were successfully removed.
        """
        if sim_info is None:
            CommonExceptionHandler.log_exception(ModInfo.MOD_NAME, 'Argument sim_info was \'None\' for {} of class {}'.format(CommonBuffUtils.remove_buff.__name__, CommonBuffUtils.__name__))
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
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=None)
    def _load_buff_instance(buff_identifier: int) -> Union[Buff, None]:
        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.BUFF, buff_identifier)
