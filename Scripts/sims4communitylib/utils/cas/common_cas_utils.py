"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union

from cas.cas import get_caspart_bodytype
from protocolbuffers import S4Common_pb2, Outfits_pb2
from sims.outfits.outfit_enums import OutfitCategory, BodyType
from sims.sim_info import SimInfo
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry.get().register_log(ModInfo.MOD_NAME, 's4cl_common_cas_utils')


class CommonCASUtils:
    """ Utilities for manipulating sim cas parts. """
    @staticmethod
    def is_cas_part_loaded(cas_part_id: int) -> bool:
        """
            Determine whether or not a CAS part has been loaded by the game.

            Note: If the cas part is part of a package that is not installed, it will be considered as not loaded.
        :param cas_part_id: A Decimal identifier of the CAS part to locate.
        :return: True if the CAS part has been loaded by the game, False if not.
        """
        return CommonCASUtils.get_body_type_of_cas_part(cas_part_id) > 0

    @staticmethod
    def get_body_type_of_cas_part(cas_part_id: int) -> BodyType:
        """
            Retrieve the body type of a CAS part.
        :param cas_part_id: An identifier of the CAS part.
        :return: The BodyType the cas part will attach to by default.
        """
        return get_caspart_bodytype(cas_part_id)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def attach_cas_part_to_sim(sim_info: SimInfo, cas_part_id: int, body_type: BodyType=BodyType.NONE, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None) -> bool:
        """
            Add a cas part to the specified body type of a sim.
        :param sim_info: The SimInfo of a sim to add the cas part to.
        :param cas_part_id: A decimal identifier of the CAS part to attach to the sim.
        :param body_type: The body type the cas part will be attached to. Default is the body type of the cas part itself.
        :param outfit_category_and_index: The outfit category and index of the sim to be added to. Default is the sims current outfit.
        :return: True if successfully attached to the sim, False if not.
        """
        log.format_with_message('Attempting to attach cas part to sim', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        if cas_part_id == -1:
            log.debug('No cas part id.')
            return False
        log.debug('Saving outfits.')
        saved_outfits = sim_info.save_outfits()
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        log.format_with_message('Using outfit category and index.', outfit_category_and_index=outfit_category_and_index)
        outfit_data = CommonOutfitUtils.get_outfit_data(sim_info, outfit_category_and_index=outfit_category_and_index)
        outfit_identifier = frozenset(dict(zip(list(outfit_data.body_types), list(outfit_data.part_ids))).items())
        if body_type is None or body_type == BodyType.NONE:
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        log.format_with_message('Using body_type', body_type=body_type)
        for outfit in saved_outfits.outfits:
            log.format_with_message('Attempting to update outfit.', outfit=outfit)
            # noinspection PyUnresolvedReferences
            _outfit_identifier = frozenset(dict(zip(list(outfit.body_types_list.body_types), list(outfit.parts.ids))).items())
            if int(outfit.category) != int(outfit_category_and_index[0]) or outfit.outfit_id != outfit_data.outfit_id or _outfit_identifier != outfit_identifier:
                log.debug('Outfit is not the outfit we want to update, skipping.')
                continue
            log.debug('Updating outfit.')
            # noinspection PyUnresolvedReferences
            previous_cas_parts_list = list(outfit.parts.ids)
            if cas_part_id not in previous_cas_parts_list:
                log.debug('Adding cas part id.')
                previous_cas_parts_list.append(cas_part_id)
            outfit.parts = S4Common_pb2.IdList()
            # noinspection PyUnresolvedReferences
            outfit.parts.ids.extend(previous_cas_parts_list)
            # noinspection PyUnresolvedReferences
            previous_body_types_list = list(outfit.body_types_list.body_types)
            if body_type not in previous_body_types_list:
                log.debug('Adding body type.')
                previous_body_types_list.append(body_type)
            outfit.body_types_list = Outfits_pb2.BodyTypesList()
            # noinspection PyUnresolvedReferences
            outfit.body_types_list.body_types.extend(previous_body_types_list)
            log.debug('Done updating outfit.')
        log.debug('Done updating outfits.')
        sim_info._base.outfits = saved_outfits.SerializeToString()
        sim_info._base.outfit_type_and_index = outfit_category_and_index
        log.debug('Resending outfits.')
        CommonOutfitUtils.resend_outfits(sim_info)
        log.debug('Done attaching cas part to sim.')
        return True

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def detach_cas_part_from_sim(sim_info: SimInfo, cas_part_id: int, body_type: Union[BodyType, None]=BodyType.NONE, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None) -> bool:
        """
            Remove the cas part attached to the specified body type of a sim.
        :param sim_info: The SimInfo of a sim to remove the cas part from.
        :param cas_part_id: A decimal identifier of the CAS part to detach from the sim.
        :param body_type: The body type the cas part will be detached from. Default is the body type of the cas part itself.
        If body_type is None, the cas part will be removed from all body types.
        :param outfit_category_and_index: The outfit category and index of the sim to be added to. Default is the sims current outfit.
        :return: True if successfully detached, False if not.
        """
        log.format_with_message('Attempting to remove cas part from sim', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        if cas_part_id == -1:
            log.debug('No cas part id.')
            return False
        log.debug('Saving outfits.')
        saved_outfits = sim_info.save_outfits()
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        log.format_with_message('Using outfit category and index.', outfit_category_and_index=outfit_category_and_index)
        outfit_data = CommonOutfitUtils.get_outfit_data(sim_info, outfit_category_and_index=outfit_category_and_index)
        outfit_identifier = frozenset(dict(zip(list(outfit_data.body_types), list(outfit_data.part_ids))).items())
        if body_type == BodyType.NONE:
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        log.format_with_message('Using body_type', body_type=body_type)
        for outfit in saved_outfits.outfits:
            log.format_with_message('Attempting to update outfit.', outfit=outfit)
            # noinspection PyUnresolvedReferences
            _outfit_identifier = frozenset(dict(zip(list(outfit.body_types_list.body_types), list(outfit.parts.ids))).items())
            if int(outfit.category) != int(outfit_category_and_index[0]) or outfit.outfit_id != outfit_data.outfit_id or _outfit_identifier != outfit_identifier:
                log.debug('Outfit is not the outfit we want to update, skipping.')
                continue
            log.debug('Updating outfit.')
            # noinspection PyUnresolvedReferences
            previous_cas_parts_list = list(outfit.parts.ids)
            if cas_part_id in previous_cas_parts_list:
                log.debug('Removing cas part id.')
                previous_cas_parts_list.remove(cas_part_id)
            outfit.parts = S4Common_pb2.IdList()
            # noinspection PyUnresolvedReferences
            outfit.parts.ids.extend(previous_cas_parts_list)
            # noinspection PyUnresolvedReferences
            previous_body_types_list = list(outfit.body_types_list.body_types)
            if body_type is not None and body_type in previous_body_types_list:
                log.debug('Removing body type.')
                previous_body_types_list.remove(body_type)
            outfit.body_types_list = Outfits_pb2.BodyTypesList()
            # noinspection PyUnresolvedReferences
            outfit.body_types_list.body_types.extend(previous_body_types_list)
            log.debug('Done updating outfit.')
        log.debug('Done updating outfits.')
        sim_info._base.outfits = saved_outfits.SerializeToString()
        sim_info._base.outfit_type_and_index = outfit_category_and_index
        log.debug('Resending outfits.')
        CommonOutfitUtils.resend_outfits(sim_info)
        log.debug('Done attaching cas part to sim.')
        return True

    @staticmethod
    def has_cas_part_attached(sim_info: SimInfo, cas_part_id: int, body_type: Union[BodyType, None]=BodyType.NONE, outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> bool:
        """
            Determine if a sim has a cas part attached to their outfit.
        :param sim_info: The SimInfo of the sim to check.
        :param cas_part_id: A decimal identifier of the CAS part to locate
        :param body_type: The body type the cas part will be located at. Default is the body type of the cas part itself.
        If body_type is None, the cas part will be located within any body type.
        :param outfit_category_and_index: The outfit category and index of the sims outfit to check. Default is the sims current outfit.
        :return: True if the sims outfit contains any of the specified cas parts.
        """
        log.format_with_message('Checking if cas part is attached to sim.', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        if body_type == BodyType.NONE:
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        log.format(body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        body_parts = CommonOutfitUtils.get_outfit_parts(sim_info, outfit_category_and_index)
        if not body_parts:
            log.debug('No body parts found.')
            return False
        log.format_with_message('Found body parts from outfit.', body_parts=body_parts)
        if body_type is None:
            log.debug('No body type specified.')
            return cas_part_id in body_parts.values()
        if body_type not in body_parts:
            log.debug('Specified body type not found within body parts.')
            return False
        log.debug('Body type found within sims outfit parts.')
        attached_cas_part_id = body_parts[body_type]
        log.format(attached_cas_part_id=attached_cas_part_id)
        return cas_part_id == attached_cas_part_id

    @staticmethod
    def get_cas_part_id_at_body_type(sim_info: SimInfo, body_type: BodyType, outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> int:
        """
            Retrieve the cas part located at the specified body type
        :param sim_info: The SimInfo of the sim to check.
        :param body_type: The body type to locate cas parts at.
        :param outfit_category_and_index: The outfit category and index of the sims outfit to check. Default is the sims current outfit.
        :return: True if the sims outfit contains any of the specified cas parts.
        """
        log.format_with_message('Checking if cas part is attached to sim.', sim=sim_info, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        log.format(body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        body_parts = CommonOutfitUtils.get_outfit_parts(sim_info, outfit_category_and_index)
        if not body_parts:
            log.debug('No body parts found.')
            return -1
        log.format_with_message('Found body parts from outfit.', body_parts=body_parts)
        if body_type not in body_parts:
            log.debug('Specified body type not found within body parts.')
            return -1
        log.debug('Body type found within sims outfit parts.')
        return body_parts[body_type]
