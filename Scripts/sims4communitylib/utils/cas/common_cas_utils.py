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

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 's4cl_common_cas_utils')


class CommonCASUtils:
    """Utilities for manipulating Sim cas parts.

    """
    @staticmethod
    def is_cas_part_loaded(cas_part_id: int) -> bool:
        """Determine if a CAS part is loaded within the game.
        note:: If the cas part is part of a package that is not installed, it will be considered as not loaded.

        :param cas_part_id: The Decimal identifier of a CAS part.
        :return: True if the CAS part is loaded within the game, False if not.
        """
        return CommonCASUtils.get_body_type_of_cas_part(cas_part_id) > 0

    @staticmethod
    def get_body_type_of_cas_part(cas_part_id: int) -> Union[BodyType, None]:
        """Retrieve the BodyType of a CAS part.

        :param cas_part_id: The decimal identifier of a CAS part.
        :return: The default BodyType of the CAS part or None if the Body Type of a cas part is not an actual BodyType.
        """
        body_type = get_caspart_bodytype(cas_part_id)
        if body_type not in BodyType:
            return None
        return BodyType(body_type)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def attach_cas_part_to_sim(sim_info: SimInfo, cas_part_id: int, body_type: BodyType=BodyType.NONE, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None) -> bool:
        """Add a cas part at the specified BodyType to the Sims outfit.

        :param sim_info: The SimInfo of a Sim to add the cas part to.
        :param cas_part_id: The decimal identifier of a CAS part to attach to the Sim.
        :param body_type: The BodyType the cas part will be attached to. If no value is provided or it is None, the BodyType of the cas part itself will be used.
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to modify. If no value is provided, the Sims current outfit will be used.
        :return: True if the cas part was successfully attached, False if not.
        """
        log.format_with_message('Attempting to attach cas part to Sim', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        if cas_part_id == -1 or cas_part_id is None:
            raise RuntimeError('No cas_part_id was provided.')
        log.debug('Pre-saving outfits.')
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
                log.format_with_message('Outfit is not the outfit we want to update, skipping.', outfit_id=outfit.outfit_id, outfit_category=outfit.category)
                continue
            log.debug('Updating outfit.')
            # noinspection PyUnresolvedReferences
            previous_cas_parts_list = list(outfit.parts.ids)
            if cas_part_id not in previous_cas_parts_list:
                log.format_with_message('Adding cas part id.', cas_part_id=cas_part_id)
                previous_cas_parts_list.append(cas_part_id)
            outfit.parts = S4Common_pb2.IdList()
            # noinspection PyUnresolvedReferences
            outfit.parts.ids.extend(previous_cas_parts_list)
            # noinspection PyUnresolvedReferences
            previous_body_types_list = list(outfit.body_types_list.body_types)
            if body_type not in previous_body_types_list:
                log.format_with_message('Adding body type.', body_type=body_type)
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
        log.debug('Done adding cas part to Sim.')
        return True

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def detach_cas_part_from_sim(sim_info: SimInfo, cas_part_id: int, body_type: Union[BodyType, None]=BodyType.NONE, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None) -> bool:
        """Remove a cas part at the specified BodyType from the Sims outfit.

        :param sim_info: The SimInfo of a Sim to remove the cas part from.
        :param cas_part_id: The decimal identifier of a CAS part to detach from the Sim.
        :param body_type: The BodyType the cas part will be detached from. If no value is provided, the BodyType of the cas part itself will be used. If set to None, the cas part will be removed from all body types.
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to modify. If no value is provided, the Sims current outfit will be used.
        :return: True if the cas part was successfully detached, False if not.
        """
        log.format_with_message('Attempting to remove cas part from Sim', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        if cas_part_id == -1 or cas_part_id is None:
            raise RuntimeError('No cas_part_id was provided.')
        log.debug('Saving outfits.')
        saved_outfits = sim_info.save_outfits()
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        log.format_with_message('Removing cas parts from outfit category and index.', outfit_category_and_index=outfit_category_and_index)
        outfit_data = CommonOutfitUtils.get_outfit_data(sim_info, outfit_category_and_index=outfit_category_and_index)
        outfit_identifier = frozenset(dict(zip(list(outfit_data.body_types), list(outfit_data.part_ids))).items())
        if body_type == BodyType.NONE:
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        if body_type is None:
            body_type = CommonCASUtils.get_body_type_cas_part_is_attached_to(sim_info, cas_part_id, outfit_category_and_index=outfit_category_and_index)
        log.format_with_message('Using body_type', body_type=body_type)
        for outfit in saved_outfits.outfits:
            log.format_with_message('Attempting to update outfit.', outfit=outfit)
            # noinspection PyUnresolvedReferences
            _outfit_identifier = frozenset(dict(zip(list(outfit.body_types_list.body_types), list(outfit.parts.ids))).items())
            if int(outfit.category) != int(outfit_category_and_index[0]) or outfit.outfit_id != outfit_data.outfit_id or _outfit_identifier != outfit_identifier:
                log.format_with_message('Outfit is not the outfit we want to update, skipping.', outfit_id=outfit.outfit_id, outfit_category=outfit.category)
                continue
            log.debug('Updating outfit.')
            # noinspection PyUnresolvedReferences
            previous_cas_parts_list = list(outfit.parts.ids)
            if cas_part_id in previous_cas_parts_list:
                log.format_with_message('Removing cas part id.', cas_part_id=cas_part_id)
                previous_cas_parts_list.remove(cas_part_id)
            outfit.parts = S4Common_pb2.IdList()
            # noinspection PyUnresolvedReferences
            outfit.parts.ids.extend(previous_cas_parts_list)
            # noinspection PyUnresolvedReferences
            previous_body_types_list = list(outfit.body_types_list.body_types)
            if body_type is not None and body_type in previous_body_types_list:
                log.format_with_message('Removing body type.', body_type=body_type)
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
        log.debug('Done removing cas part from Sim.')
        return True

    @staticmethod
    def has_cas_part_attached(sim_info: SimInfo, cas_part_id: int, body_type: Union[BodyType, None]=BodyType.NONE, outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> bool:
        """Determine if a Sim has the specified cas part attached to their outfit.

        :param sim_info: The SimInfo of the Sim to check.
        :param cas_part_id: A decimal identifier of the CAS part to locate.
        :param body_type: The BodyType the cas part will be located at. If no value is provided, it defaults to the BodyType of the cas part itself. If set to None, the cas part will be located within any body type.
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to check. Default is the Sims current outfit.
        :return: True if the Sims outfit contains any of the specified cas parts.
        """
        log.format_with_message('Checking if cas part is attached to Sim.', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        if body_type == BodyType.NONE:
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        log.format(body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        outfit_parts = CommonOutfitUtils.get_outfit_parts(sim_info, outfit_category_and_index=outfit_category_and_index)
        if not outfit_parts:
            log.debug('No body parts found.')
            return False
        log.format_with_message('Found body parts from outfit.', body_parts=outfit_parts)
        if body_type is None:
            log.debug('No body type specified.')
            return cas_part_id in outfit_parts.values()
        if body_type not in outfit_parts:
            log.debug('Specified body type not found within body parts.')
            return False
        log.debug('Body type found within Sims outfit parts.')
        attached_cas_part_id = outfit_parts[body_type]
        log.format(attached_cas_part_id=attached_cas_part_id)
        return cas_part_id == attached_cas_part_id

    @staticmethod
    def get_body_type_cas_part_is_attached_to(sim_info: SimInfo, cas_part_id: int, outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> BodyType:
        """Retrieve the BodyType that a cas part is attached to within a Sims outfit.

        :param sim_info: The SimInfo of the Sim to check.
        :param cas_part_id: A decimal identifier of the CAS part to locate.
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to check. Default is the Sims current outfit.
        :return: The BodyType the specified cas part id is attached to or -1 if the cas part is not found.
        """
        log.format_with_message('Retrieving BodyType for cas part.', sim=sim_info, cas_part_id=cas_part_id, outfit_category_and_index=outfit_category_and_index)
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        log.format(cas_part_id=cas_part_id, outfit_category_and_index=outfit_category_and_index)
        outfit_parts = CommonOutfitUtils.get_outfit_parts(sim_info, outfit_category_and_index=outfit_category_and_index)
        if not outfit_parts:
            log.debug('No body parts found.')
            return BodyType.NONE
        log.format_with_message('Found body parts from outfit.', body_parts=outfit_parts)
        for body_type in outfit_parts.keys():
            if cas_part_id != outfit_parts[body_type]:
                continue
            log.format_with_message('Found BodyType.', body_type=BodyType(body_type))
            return BodyType(body_type)
        log.debug('No BodyType found matching the cas part.')
        return BodyType.NONE

    @staticmethod
    def get_cas_part_id_at_body_type(sim_info: SimInfo, body_type: BodyType, outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> int:
        """Retrieve the cas part identifier attached to the specified BodyType within a Sims outfit.

        :param sim_info: The SimInfo of the Sim to check.
        :param body_type: The BodyType to check.
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to check. Default is the Sims current outfit.
        :return: The cas part identifier attached to the specified BodyType or -1 if the body type is not found.
        """
        log.format_with_message('Checking if cas part is attached to Sim.', sim=sim_info, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        log.format(body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        outfit_parts = CommonOutfitUtils.get_outfit_parts(sim_info, outfit_category_and_index=outfit_category_and_index)
        if not outfit_parts:
            log.debug('No body_parts found on Sim.')
            return -1
        log.format_with_message('Found body parts from outfit.', body_parts=outfit_parts)
        if body_type not in outfit_parts:
            log.debug('The specified BodyType was not found within the Sims outfit.')
            return -1
        log.debug('BodyType found within Sims outfit parts.')
        return outfit_parts[body_type]
