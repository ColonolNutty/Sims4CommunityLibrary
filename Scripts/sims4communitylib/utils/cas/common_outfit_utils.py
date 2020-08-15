"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat

import sims4.commands
from typing import Tuple, Union, Dict

from cas.cas import OutfitData
from sims.outfits.outfit_enums import OutfitCategory, BodyType
from sims.sim_info import SimInfo
from sims4communitylib.enums.buffs_enum import CommonBuffId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils


class CommonOutfitUtils:
    """Utilities for handling Sim outfits.

    """
    @staticmethod
    def is_every_day_category(outfit_category: OutfitCategory) -> bool:
        """is_every_day_category(outfit_category)

        Determine if an OutfitCategory is EVERYDAY

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.EVERYDAY. False, if it is not.
        :rtype: bool
        """
        return outfit_category == OutfitCategory.EVERYDAY

    @staticmethod
    def is_formal_category(outfit_category: OutfitCategory) -> bool:
        """is_formal_category(outfit_category)

        Determine if an OutfitCategory is FORMAL

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.FORMAL. False, if it is not.
        :rtype: bool
        """
        return outfit_category == OutfitCategory.FORMAL

    @staticmethod
    def is_athletic_category(outfit_category: OutfitCategory) -> bool:
        """is_athletic_category(outfit_category)

        Determine if an OutfitCategory is ATHLETIC

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.ATHLETIC. False, if it is not.
        :rtype: bool
        """
        return outfit_category == OutfitCategory.ATHLETIC

    @staticmethod
    def is_sleep_category(outfit_category: OutfitCategory) -> bool:
        """is_sleep_category(outfit_category)

        Determine if an OutfitCategory is SLEEP

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.SLEEP. False, if it is not.
        :rtype: bool
        """
        return outfit_category == OutfitCategory.SLEEP

    @staticmethod
    def is_party_category(outfit_category: OutfitCategory) -> bool:
        """is_party_category(outfit_category)

        Determine if an OutfitCategory is PARTY

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.PARTY. False, if it is not.
        :rtype: bool
        """
        return outfit_category == OutfitCategory.PARTY

    @staticmethod
    def is_bathing_category(outfit_category: OutfitCategory) -> bool:
        """is_bathing_category(outfit_category)

        Determine if an OutfitCategory is BATHING

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.BATHING. False, if it is not.
        :rtype: bool
        """
        return outfit_category == OutfitCategory.BATHING

    @staticmethod
    def is_career_category(outfit_category: OutfitCategory) -> bool:
        """is_career_category(outfit_category)

        Determine if an OutfitCategory is CAREER

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.CAREER. False, if it is not.
        :rtype: bool
        """
        return outfit_category == OutfitCategory.CAREER

    @staticmethod
    def is_situation_category(outfit_category: OutfitCategory) -> bool:
        """is_situation_category(outfit_category)

        Determine if an OutfitCategory is SITUATION

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.SITUATION. False, if it is not.
        :rtype: bool
        """
        return outfit_category == OutfitCategory.SITUATION

    @staticmethod
    def is_special_category(outfit_category: OutfitCategory) -> bool:
        """is_special_category(outfit_category)

        Determine if an OutfitCategory is SPECIAL

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.SPECIAL. False, if it is not.
        :rtype: bool
        """
        return outfit_category == OutfitCategory.SPECIAL

    @staticmethod
    def is_swimwear_category(outfit_category: OutfitCategory) -> bool:
        """is_swimwear_category(outfit_category)

        Determine if an OutfitCategory is SWIMWEAR

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.SWIMWEAR. False, if it is not.
        :rtype: bool
        """
        return outfit_category == OutfitCategory.SWIMWEAR

    @staticmethod
    def is_hot_weather_category(outfit_category: OutfitCategory) -> bool:
        """is_hot_weather_category(outfit_category)

        Determine if an OutfitCategory is HOT_WEATHER

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.HOT_WEATHER. False, if it is not.
        :rtype: bool
        """
        return outfit_category == OutfitCategory.HOT_WEATHER

    @staticmethod
    def is_cold_weather_category(outfit_category: OutfitCategory) -> bool:
        """is_cold_weather_category(outfit_category)

        Determine if an OutfitCategory is COLD_WEATHER

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.COLD_WEATHER. False, if it is not.
        :rtype: bool
        """
        return outfit_category == OutfitCategory.COLD_WEATHER

    @staticmethod
    def get_all_outfit_categories() -> Tuple[OutfitCategory]:
        """get_all_outfit_categories()

        Retrieve a collection of all OutfitCategory types.

        :return: A collection of all OutfitCategories.
        :rtype: Tuple[OutfitCategory]
        """
        return tuple(OutfitCategory.values)

    @staticmethod
    def is_wearing_everyday_outfit(sim_info: SimInfo) -> bool:
        """is_wearing_everyday_outfit(sim_info)

        Determine if a Sim is wearing an Everyday outfit.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the sim is wearing an everyday outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_every_day_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_formal_outfit(sim_info: SimInfo) -> bool:
        """is_wearing_formal_outfit(sim_info)

        Determine if a Sim is wearing a Formal outfit.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the sim is wearing a formal outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_formal_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_athletic_outfit(sim_info: SimInfo) -> bool:
        """is_wearing_athletic_outfit(sim_info)

        Determine if a Sim is wearing an Athletic outfit.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the sim is wearing an athletic outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_athletic_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_sleep_outfit(sim_info: SimInfo) -> bool:
        """is_wearing_sleep_outfit(sim_info)

        Determine if a Sim is wearing a Sleep outfit.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the sim is wearing a sleep outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_sleep_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_party_outfit(sim_info: SimInfo) -> bool:
        """is_wearing_party_outfit(sim_info)

        Determine if a Sim is wearing a Party outfit.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the sim is wearing a party outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_party_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_bathing_outfit(sim_info: SimInfo) -> bool:
        """is_wearing_bathing_outfit(sim_info)

        Determine if a Sim is wearing a Bathing outfit.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the sim is wearing their bathing/nude outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_bathing_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_career_outfit(sim_info: SimInfo) -> bool:
        """is_wearing_career_outfit(sim_info)

        Determine if a Sim is wearing a Career outfit.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the sim is wearing a career outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_career_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_situation_outfit(sim_info: SimInfo) -> bool:
        """is_wearing_situation_outfit(sim_info)

        Determine if a Sim is wearing a Situation outfit.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the sim is wearing a situation outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_situation_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_special_outfit(sim_info: SimInfo) -> bool:
        """is_wearing_special_outfit(sim_info)

        Determine if a Sim is wearing a Special outfit.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the sim is wearing a special outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_special_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_swimwear_outfit(sim_info: SimInfo) -> bool:
        """is_wearing_swimwear_outfit(sim_info)

        Determine if a Sim is wearing a Swimwear outfit.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the sim is wearing a swimwear outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_swimwear_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_hot_weather_outfit(sim_info: SimInfo) -> bool:
        """is_wearing_hot_weather_outfit(sim_info)

        Determine if a Sim is wearing a Hot Weather outfit.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the sim is wearing a hot weather outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_hot_weather_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_cold_weather_outfit(sim_info: SimInfo) -> bool:
        """is_wearing_cold_weather_outfit(sim_info)

        Determine if a Sim is wearing a Cold Weather outfit.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the sim is wearing a cold weather outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_cold_weather_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_towel(sim_info: SimInfo) -> bool:
        """is_wearing_towel(sim_info)

        Determine if a Sim is currently wearing a towel.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the sim is wearing a towel. False, if not.
        :rtype: bool
        """
        return CommonBuffUtils.has_buff(sim_info, CommonBuffId.IS_WEARING_TOWEL)

    @staticmethod
    def get_outfit_category_by_name(name: str) -> OutfitCategory:
        """get_outfit_category_by_name(name)

        Retrieve an OutfitCategory by its a name.

        :param name: The name of an outfit category.
        :type name: str
        :return: The OutfitCategory with the specified name or OutfitCategory.CURRENT_OUTFIT if no outfit category was found using the specified name.
        :rtype: OutfitCategory
        """
        upper_case_name = str(name).upper().strip()
        return CommonResourceUtils.get_enum_by_name(upper_case_name, OutfitCategory, default_value=OutfitCategory.CURRENT_OUTFIT)

    @staticmethod
    def get_current_outfit_category(sim_info: SimInfo) -> OutfitCategory:
        """get_current_outfit_category(sim_info)

        Retrieve the current OutfitCategory and Index of a Sim.

        :param sim_info: The Sim to get the outfit category of.
        :type sim_info: SimInfo
        :return: The OutfitCategory of the current outfit a Sim is wearing.
        :rtype: OutfitCategory
        """
        return CommonOutfitUtils.get_current_outfit(sim_info)[0]

    @staticmethod
    def get_current_outfit_index(sim_info: SimInfo) -> int:
        """get_current_outfit_index(sim_info)

        Retrieve the current OutfitCategory and Index of a Sim.

        .. note:: If a Sim has two Athletic outfits and they are wearing the second outfit, the index would be `1`.

        :param sim_info: The Sim to get the outfit index of.
        :type sim_info: SimInfo
        :return: The index of their current outfit relative to the outfits a Sim has in the current OutfitCategory.
        :rtype: int
        """
        return CommonOutfitUtils.get_current_outfit(sim_info)[1]

    @staticmethod
    def get_current_outfit(sim_info: SimInfo) -> Tuple[OutfitCategory, int]:
        """get_current_outfit(sim_info)

        Retrieve the current OutfitCategory and Index of the current sim.

        .. note:: If a Sim has two Athletic outfits and they are wearing the second outfit, the index would be `1`.

        :param sim_info: The Sim to get the current outfit of.
        :type sim_info: SimInfo
        :return: The OutfitCategory and index of the current outfit a Sim is wearing.
        :rtype: Tuple[OutfitCategory, int]
        """
        return sim_info.get_current_outfit()

    @staticmethod
    def get_outfit_data(sim_info: SimInfo, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None) -> OutfitData:
        """get_outfit_data(sim_info, outfit_category_and_index=None)

        Retrieve OutfitData for the specified OutfitCategory and Index of a Sim.

        :param sim_info: The Sim to retrieve outfit data of.
        :type sim_info: SimInfo
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to retrieve data from. Default is the current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: Outfit Data for the specified outfit.
        :rtype: OutfitData
        """
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        return sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])

    @staticmethod
    def has_cas_part_attached(sim_info: SimInfo, cas_part_id: int, outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> bool:
        """has_any_cas_parts_attached(sim_info, cas_part_id, outfit_category_and_index=None)

        Determine if any of the specified CAS Parts are attached to the Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param cas_part_id: A CAS Part identifier.
        :type cas_part_id: int
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to check. Default is the current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: True, if the Sim has the specified CAS Parts attached to the specified outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.has_any_cas_parts_attached(sim_info, (cas_part_id, ), outfit_category_and_index=outfit_category_and_index)

    @staticmethod
    def has_any_cas_parts_attached(sim_info: SimInfo, cas_part_ids: Tuple[int], outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> bool:
        """has_any_cas_parts_attached(sim_info, cas_part_ids, outfit_category_and_index=None)

        Determine if any of the specified CAS Parts are attached to the Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param cas_part_ids: A collection of CAS Part identifiers.
        :type cas_part_ids: Tuple[int]
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to check. Default is the current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: True, if the Sim has any of the specified CAS Parts attached to the specified outfit. False, if not.
        :rtype: bool
        """
        body_parts = CommonOutfitUtils.get_outfit_parts(sim_info, outfit_category_and_index=outfit_category_and_index)
        if not body_parts:
            return False
        outfit_part_ids = body_parts.values()
        for cas_part_id in cas_part_ids:
            if cas_part_id in outfit_part_ids:
                return True
        return False

    @staticmethod
    def get_outfit_parts(sim_info: SimInfo, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None) -> Dict[BodyType, int]:
        """get_outfit_parts(sim_info, outfit_category_and_index=None)

        Retrieve Outfit Parts for the specified OutfitCategory and Index of a Sim.

        :param sim_info: The Sim to retrieve outfit parts of.
        :type sim_info: SimInfo
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to retrieve data from. Default is the current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: A dictionary of body types and cas parts in those body types for the outfit of a Sim.
        :rtype: Dict[BodyType, int]
        """
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        outfit_data = sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])
        if outfit_data is None:
            return dict()
        return dict(zip(list(outfit_data.body_types), list(outfit_data.part_ids)))

    @staticmethod
    def set_current_outfit(sim_info: SimInfo, outfit_category_and_index: Tuple[OutfitCategory, int]):
        """set_current_outfit(sim_info, outfit_category_and_index)

        Set the current outfit of a Sim to the specified OutfitCategory and Index.

        :param sim_info: The Sim to change the outfit of.
        :type sim_info: SimInfo
        :param outfit_category_and_index: The OutfitCategory and index to change to.
        :type outfit_category_and_index: Tuple[OutfitCategory, int]
        """
        sim_info.set_current_outfit(outfit_category_and_index)

    @staticmethod
    def set_outfit_dirty(sim_info: SimInfo, outfit_category: OutfitCategory):
        """set_outfit_dirty(sim_info, outfit_category)

        Flag the specified OutfitCategory of a Sim as dirty.
        This will tell the game that it needs to be updated.

        :param sim_info: The Sim to flag the OutfitCategory for.
        :type sim_info: SimInfo
        :param outfit_category: The OutfitCategory being flagged.
        :type outfit_category: OutfitCategory
        """
        sim_info.set_outfit_dirty(outfit_category)

    @staticmethod
    def set_outfit_clean(sim_info: SimInfo, outfit_category: OutfitCategory):
        """set_outfit_clean(sim_info, outfit_category)

        Flag the specified OutfitCategory of a Sim as clean.

        :param sim_info: The Sim to flag the OutfitCategory for.
        :type sim_info: SimInfo
        :param outfit_category: The OutfitCategory being flagged.
        :type outfit_category: OutfitCategory
        """
        sim_info.clear_outfit_dirty(outfit_category)

    @staticmethod
    def generate_outfit(sim_info: SimInfo, outfit_category_and_index: Tuple[OutfitCategory, int]) -> bool:
        """generate_outfit(sim_info, outfit_category_and_index)

        Generate an outfit for a Sim for the specified OutfitCategory and Index.

        .. note:: If an outfit exists in the specified OutfitCategory and Index, already, it will be overridden.

        :param sim_info: The Sim to generate an outfit for.
        :type sim_info: SimInfo
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to generate.
        :type outfit_category_and_index: Tuple[OutfitCategory, int]
        :return: True, if an outfit was generated successfully. False, if not.
        :rtype: bool
        """
        try:
            sim_info.on_outfit_generated(sim_info, CommonOutfitUtils.get_current_outfit(sim_info))
            sim_info.generate_outfit(*outfit_category_and_index)
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Problem occurred running function \'{}\'.'.format(CommonOutfitUtils.generate_outfit.__name__), exception=ex)
        return False

    @staticmethod
    def resend_outfits(sim_info: SimInfo) -> bool:
        """resend_outfits(sim_info)

        Resend outfit data to a Sim to refresh their outfits.

        :param sim_info: The Sim to resend the outfit for.
        :type sim_info: SimInfo
        :return: True, if outfits were resent successfully. False, if not.
        :rtype: bool
        """
        try:
            sim_info.resend_outfits()
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Problem occurred running function \'{}\'.'.format(CommonOutfitUtils.resend_outfits.__name__), exception=ex)
        return False

    @staticmethod
    def get_previous_outfit(sim_info: SimInfo, default_outfit_category_and_index: Tuple[OutfitCategory, int]=(OutfitCategory.EVERYDAY, 0)) -> Tuple[OutfitCategory, int]:
        """get_previous_outfit(sim_info, default_outfit_category_and_index=(OutfitCategory.EVERYDAY, 0))

        Retrieve the previous outfit a Sim was wearing before their current outfit.

        :param sim_info: The Sim to get the previous outfit of.
        :type sim_info: SimInfo
        :param default_outfit_category_and_index: A default OutfitCategory and index if no previous outfit was found.
        :type default_outfit_category_and_index: Tuple[OutfitCategory, int], optional
        :return: The OutfitCategory and Index of the outfit a Sim was wearing before their current outfit or the default if none was found.
        :rtype: Tuple[OutfitCategory, int]
        """
        return sim_info.get_previous_outfit() or default_outfit_category_and_index

    @staticmethod
    def remove_previous_outfit(sim_info: SimInfo):
        """remove_previous_outfit(sim_info)

        Remove the outfit a Sim was wearing before their current outfit, from the cache.

        :param sim_info: The Sim to remove the outfit from.
        :type sim_info: SimInfo
        """
        sim_info.set_previous_outfit(None, force=True)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def has_outfit(sim_info: SimInfo, outfit_category_and_index: Tuple[OutfitCategory, int]) -> bool:
        """has_outfit(sim_info, outfit_category_and_index)

        Determine if a Sim has an existing outfit in the specified OutfitCategory and Index.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param outfit_category_and_index: The OutfitCategory and index to locate.
        :type outfit_category_and_index: Tuple[OutfitCategory, int], optional
        :return: True, if the Sim has the specified OutfitCategory and Index. False, if not.
        :rtype: bool
        """
        return sim_info.has_outfit(outfit_category_and_index)

    @staticmethod
    def update_outfits(sim_info: SimInfo) -> bool:
        """update_outfits(sim_info)

        Update all outfits of a Sim.

        :param sim_info: The Sim to update outfits for.
        :type sim_info: SimInfo
        :return: True, if the outfits were updated successfully. False, if not.
        :rtype: bool
        """
        try:
            sim_info.on_outfit_changed(sim_info, CommonOutfitUtils.get_current_outfit(sim_info))
            CommonOutfitUtils.resend_outfits(sim_info)
            sim_info.appearance_tracker.evaluate_appearance_modifiers()
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Problem occurred running function \'{}\'.'.format(CommonOutfitUtils.update_outfits.__name__), exception=ex)
        return False


@sims4.commands.Command('s4clib_testing.show_all_outfit_categories', command_type=sims4.commands.CommandType.Live)
def _s4clib_testing_show_all_outfit_categories(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing all outfit categories.')
    categories = CommonOutfitUtils.get_all_outfit_categories()
    output('Outfit categories: {}'.format(pformat(categories)))
