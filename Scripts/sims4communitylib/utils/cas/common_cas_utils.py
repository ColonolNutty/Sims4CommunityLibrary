"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

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
    """Utilities for manipulating the CAS parts of Sims.

    """

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def is_cas_part_loaded(cas_part_id: int) -> bool:
        """is_cas_part_loaded(cas_part_id)

        Determine if a CAS part is loaded within the game.

        .. note:: If the CAS part is part of a package that is not installed, it will be considered as not loaded.

        .. note:: A CAS part is considered as "loaded" when the BodyType it has can be found within the sims.outfits.outfit_enums.BodyType enum.

        :param cas_part_id: The Decimal identifier of a CAS part.
        :type cas_part_id: int
        :return: True if the CAS part is loaded within the game, False if not.
        :rtype: bool
        """
        body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        if body_type is None:
            return False
        return body_type > 0

    @staticmethod
    def get_body_type_of_cas_part(cas_part_id: int) -> Union[BodyType, None]:
        """get_body_type_of_cas_part(cas_part_id)

        Retrieve the BodyType of a CAS part.

        .. note:: For some reason not every CAS part has a BodyType.

        :param cas_part_id: The decimal identifier of a CAS part.
        :type cas_part_id: int
        :return: The default BodyType of the CAS part or None if the BodyType of a CAS part is not an actual BodyType.
        :rtype: Union[BodyType, None]
        """
        body_type = get_caspart_bodytype(cas_part_id)
        if body_type not in BodyType:
            return None
        return BodyType(body_type)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def attach_cas_part_to_sim(sim_info: SimInfo, cas_part_id: int, body_type: BodyType=BodyType.NONE, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None) -> bool:
        """attach_cas_part_to_sim(sim_info, cas_part_id, body_type=BodyType.NONE, outfit_category_and_index=None)

        Add a CAS part at the specified BodyType to the Sims outfit.

        :param sim_info: The SimInfo of a Sim to add the CAS part to.
        :type sim_info: SimInfo
        :param cas_part_id: The decimal identifier of a CAS part to attach to the Sim.
        :type cas_part_id: int
        :param body_type: The BodyType the CAS part will be attached to. If no value is provided or it is None, the BodyType of the CAS part itself will be used.
        :type body_type: BodyType, optional
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to modify. If no value is provided, the Sims current outfit will be used.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: True if the CAS part was successfully attached to the Sim. False if the CAS part was not successfully attached to the Sim.
        :rtype: bool
        """
        log.format_with_message('Attempting to attach CAS part to Sim', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
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
                log.format_with_message('Adding CAS part id.', cas_part_id=cas_part_id)
                previous_cas_parts_list.append(cas_part_id)
            outfit.parts = S4Common_pb2.IdList()
            # noinspection PyUnresolvedReferences
            outfit.parts.ids.extend(previous_cas_parts_list)
            # noinspection PyUnresolvedReferences
            previous_body_types_list = list(outfit.body_types_list.body_types)
            if body_type not in previous_body_types_list:
                log.format_with_message('Adding BodyType.', body_type=body_type)
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
        log.debug('Done adding CAS part to Sim.')
        return True

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def detach_cas_part_from_sim(sim_info: SimInfo, cas_part_id: int, body_type: Union[BodyType, None]=BodyType.NONE, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None) -> bool:
        """detach_cas_part_from_sim(sim_info, cas_part_id, body_type=BodyType.NONE, outfit_category_and_index=None)

        Remove a CAS part at the specified BodyType from the Sims outfit.

        :param sim_info: The SimInfo of a Sim to remove the CAS part from.
        :type sim_info: SimInfo
        :param cas_part_id: The decimal identifier of a CAS part to detach from the Sim.
        :type cas_part_id: int
        :param body_type: The BodyType the CAS part will be detached from. If no value is provided, the BodyType of the CAS part itself will be used. If set to None, the CAS part will be removed from all BodyTypes.
        :type body_type: Union[BodyType, None], optional
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to modify. If no value is provided, the Sims current outfit will be used.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: True if the CAS part was successfully detached from the Sim. False if the CAS part was not successfully detached from the Sim.
        :rtype: bool
        """
        log.format_with_message('Attempting to remove CAS part from Sim', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        if cas_part_id == -1 or cas_part_id is None:
            raise RuntimeError('No cas_part_id was provided.')
        log.debug('Saving outfits.')
        saved_outfits = sim_info.save_outfits()
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        log.format_with_message('Removing CAS parts from outfit category and index.', outfit_category_and_index=outfit_category_and_index)
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
                log.format_with_message('Removing CAS part id.', cas_part_id=cas_part_id)
                previous_cas_parts_list.remove(cas_part_id)
            outfit.parts = S4Common_pb2.IdList()
            # noinspection PyUnresolvedReferences
            outfit.parts.ids.extend(previous_cas_parts_list)
            # noinspection PyUnresolvedReferences
            previous_body_types_list = list(outfit.body_types_list.body_types)
            if body_type is not None and body_type in previous_body_types_list:
                log.format_with_message('Removing BodyType.', body_type=body_type)
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
        log.debug('Done removing CAS part from Sim.')
        return True

    @staticmethod
    def has_cas_part_attached(sim_info: SimInfo, cas_part_id: int, body_type: Union[BodyType, None]=BodyType.NONE, outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> bool:
        """has_cas_part_attached(sim_info, cas_part_id, body_type=BodyType.NONE, outfit_category_and_index=None)

        Determine if a Sim has the specified CAS part attached to their outfit.

        :param sim_info: The SimInfo of the Sim to check.
        :type sim_info: SimInfo
        :param cas_part_id: A decimal identifier of the CAS part to locate.
        :type cas_part_id: int
        :param body_type: The BodyType the CAS part will be located at. If no value is provided, it defaults to the BodyType of the CAS part itself. If set to None, the CAS part will be located within any BodyType.
        :type body_type: Union[BodyType, None], optional
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to check. Default is the Sims current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: True, if the Sims outfit contain the specified CAS part. False, if the Sims outfit does not contain the specified CAS part.
        :rtype: bool
        """
        log.format_with_message('Checking if CAS part is attached to Sim.', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
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
            log.debug('No BodyType specified.')
            return cas_part_id in outfit_parts.values()
        if body_type not in outfit_parts:
            log.debug('Specified BodyType not found within body parts.')
            return False
        log.debug('BodyType found within Sims outfit parts.')
        attached_cas_part_id = outfit_parts[body_type]
        log.format(attached_cas_part_id=attached_cas_part_id)
        return cas_part_id == attached_cas_part_id

    @staticmethod
    def get_body_type_cas_part_is_attached_to(sim_info: SimInfo, cas_part_id: int, outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> BodyType:
        """get_body_type_cas_part_is_attached_to(sim_info, cas_part_id, outfit_category_and_index=None)

        Retrieve the BodyType that a CAS part is attached to within a Sims outfit.

        :param sim_info: The SimInfo of the Sim to check.
        :type sim_info: SimInfo
        :param cas_part_id: A decimal identifier of the CAS part to locate.
        :type cas_part_id: int
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to check. Default is the Sims current outfit.
        :type outfit_category_and_index: Tuple[OutfitCategory, int], optional
        :return: The BodyType the specified CAS part id is attached to or -1 if the CAS part is not found.
        :rtype: BodyType
        """
        log.format_with_message('Retrieving BodyType for CAS part.', sim=sim_info, cas_part_id=cas_part_id, outfit_category_and_index=outfit_category_and_index)
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
            log.format_with_message('Found the BodyType the specified CAS part is attached to.', body_type=BodyType(body_type))
            return BodyType(body_type)
        log.debug('No BodyType was found matching the specified CAS part.')
        return BodyType.NONE

    @staticmethod
    def get_cas_part_id_at_body_type(sim_info: SimInfo, body_type: BodyType, outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> int:
        """get_cas_part_id_at_body_type(sim_info, body_type, outfit_category_and_index=None)

        Retrieve the CAS part identifier attached to the specified BodyType within a Sims outfit.

        :param sim_info: The SimInfo of the Sim to check.
        :type sim_info: SimInfo
        :param body_type: The BodyType to check.
        :type body_type: BodyType
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to check. Default is the Sims current outfit.
        :type outfit_category_and_index: Tuple[OutfitCategory, int], optional
        :return: The CAS part identifier attached to the specified BodyType or -1 if the BodyType is not found.
        :rtype: int
        """
        log.format_with_message('Checking if CAS part is attached to Sim.', sim=sim_info, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
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
        log.debug('BodyType has been found within Sims outfit parts. Returning the CAS part belonging to it.')
        return outfit_parts[body_type]
