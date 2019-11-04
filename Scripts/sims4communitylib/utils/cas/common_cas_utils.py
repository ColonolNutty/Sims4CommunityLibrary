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
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils


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
        return CommonCASUtils.get_body_type_of_cas_part(cas_part_id) > BodyType.NONE

    @staticmethod
    def get_body_type_of_cas_part(cas_part_id: int) -> BodyType:
        """
            Retrieve the body type of a CAS part.
        :param cas_part_id: An identifier of the CAS part.
        :return: The BodyType the cas part will attach to by default.
        """
        return get_caspart_bodytype(cas_part_id)

    @staticmethod
    def attach_cas_part_to_sim(sim_info: SimInfo, cas_part_id: int, body_type: BodyType=BodyType.NONE, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None) -> bool:
        """
            Add a cas part to the specified body type of a sim.
        :param sim_info: The SimInfo of a sim to add the cas part to.
        :param cas_part_id: A decimal identifier of the CAS part to attach to the sim.
        :param body_type: The body type the cas part will be attached to. Default is the body type of the cas part itself.
        :param outfit_category_and_index: The outfit category and index of the sim to be added to. Default is the sims current outfit.
        :return: True if successfully attached to the sim, False if not.
        """
        if cas_part_id == -1:
            return False
        saved_outfits = sim_info.save_outfits()
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        outfit_data = CommonOutfitUtils.get_outfit_data(sim_info, outfit_category_and_index=outfit_category_and_index)
        outfit_identifier = frozenset(dict(zip(list(outfit_data.body_types_list.body_types), list(outfit_data.parts.ids))).items())
        if body_type == BodyType.NONE:
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        for outfit in saved_outfits.outfits:
            # noinspection PyUnresolvedReferences
            _outfit_identifier = frozenset(dict(zip(list(outfit.body_types_list.body_types), list(outfit.parts.ids))).items())
            if int(outfit.category) != int(outfit_category_and_index[0]) or outfit.outfit_id != outfit_data.outfit_id or _outfit_identifier != outfit_identifier:
                continue
            outfit.parts = S4Common_pb2.IdList()
            # noinspection PyUnresolvedReferences
            outfit.parts.ids.extend([cas_part_id])
            outfit.body_types_list = Outfits_pb2.BodyTypesList()
            # noinspection PyUnresolvedReferences
            outfit.body_types_list.body_types.extend([body_type])
        sim_info._base.outfits = saved_outfits.SerializeToString()
        sim_info._base.outfit_type_and_index = outfit_category_and_index
        CommonOutfitUtils.resend_outfits(sim_info)
        return True

    @staticmethod
    def detach_cas_part_from_sim(sim_info: SimInfo, cas_part_id: int, body_type: BodyType=BodyType.NONE, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None) -> bool:
        """
            Remove the cas part attached to the specified body type of a sim.
        :param sim_info: The SimInfo of a sim to remove the cas part from.
        :param cas_part_id: A decimal identifier of the CAS part to detach from the sim.
        :param body_type: The body type the cas part will be detached from. Default is the body type of the cas part itself.
        :param outfit_category_and_index: The outfit category and index of the sim to be added to. Default is the sims current outfit.
        :return: True if successfully detached, False if not.
        """
        saved_outfits = sim_info.save_outfits()
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        outfit_data = CommonOutfitUtils.get_outfit_data(sim_info, outfit_category_and_index=outfit_category_and_index)
        outfit_identifier = frozenset(dict(zip(list(outfit_data.body_types_list.body_types), list(outfit_data.parts.ids))).items())
        if body_type == BodyType.NONE:
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        for outfit in saved_outfits.outfits:
            # noinspection PyUnresolvedReferences
            _outfit_identifier = frozenset(dict(zip(list(outfit.body_types_list.body_types), list(outfit.parts.ids))).items())
            if int(outfit.category) != int(outfit_category_and_index[0]) or outfit.outfit_id != outfit_data.outfit_id or _outfit_identifier != outfit_identifier:
                continue
            # noinspection PyUnresolvedReferences
            previous_cas_parts_list = list(outfit.parts.ids)
            previous_cas_parts_list.remove(cas_part_id)
            outfit.parts = S4Common_pb2.IdList()
            # noinspection PyUnresolvedReferences
            outfit.parts.ids.extend(previous_cas_parts_list)
            # noinspection PyUnresolvedReferences
            previous_body_types_list = list(outfit.body_types_list.body_types)
            previous_body_types_list.remove(body_type)
            outfit.body_types_list = Outfits_pb2.BodyTypesList()
            # noinspection PyUnresolvedReferences
            outfit.body_types_list.body_types.extend(previous_body_types_list)
        sim_info._base.outfits = saved_outfits.SerializeToString()
        sim_info._base.outfit_type_and_index = outfit_category_and_index
        CommonOutfitUtils.resend_outfits(sim_info)
        return True

    @staticmethod
    def has_cas_part_attached(sim_info: SimInfo, cas_part_id: int, body_type: BodyType=BodyType.NONE, outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> bool:
        """
            Determine if a sim has a cas part attached to their outfit.
        :param sim_info: The SimInfo of the sim to check.
        :param cas_part_id: A decimal identifier of the CAS part to locate
        :param body_type: The body type the cas part will be located at. Default is the body type of the cas part itself.
        If body_type is None, the cas part will be located within any body type.
        :param outfit_category_and_index: The outfit category and index of the sim to be added to. Default is the sims current outfit.
        :return: True if the sims outfit contains any of the specified cas parts.
        """
        if body_type == BodyType.NONE:
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        body_parts = CommonOutfitUtils.get_outfit_parts(sim_info, outfit_category_and_index)
        if not body_parts:
            return False
        if body_type is None:
            return cas_part_id in body_parts.values()
        if body_type not in body_parts:
            return False
        attached_cas_part_id = body_parts[body_type]
        return cas_part_id == attached_cas_part_id
