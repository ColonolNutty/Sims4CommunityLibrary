"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat

import sims4.commands
from typing import Tuple, Union, Dict

from cas.cas import OutfitData
from sims.outfits.outfit_enums import OutfitCategory, BodyType
from sims.sim_info import SimInfo
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo


class CommonOutfitUtils:
    """ Utilities for handling sim outfits. """
    @staticmethod
    def is_every_day_category(outfit_category: OutfitCategory) -> bool:
        """
            Determine if an OutfitCategory is EVERYDAY
        """
        return outfit_category == OutfitCategory.EVERYDAY

    @staticmethod
    def is_formal_category(outfit_category: OutfitCategory) -> bool:
        """
            Determine if an OutfitCategory is FORMAL
        """
        return outfit_category == OutfitCategory.FORMAL

    @staticmethod
    def is_athletic_category(outfit_category: OutfitCategory) -> bool:
        """
            Determine if an OutfitCategory is ATHLETIC
        """
        return outfit_category == OutfitCategory.ATHLETIC

    @staticmethod
    def is_sleep_category(outfit_category: OutfitCategory) -> bool:
        """
            Determine if an OutfitCategory is SLEEP
        """
        return outfit_category == OutfitCategory.SLEEP

    @staticmethod
    def is_party_category(outfit_category: OutfitCategory) -> bool:
        """
            Determine if an OutfitCategory is PARTY
        """
        return outfit_category == OutfitCategory.PARTY

    @staticmethod
    def is_bathing_category(outfit_category: OutfitCategory) -> bool:
        """
            Determine if an OutfitCategory is BATHING
        """
        return outfit_category == OutfitCategory.BATHING

    @staticmethod
    def is_career_category(outfit_category: OutfitCategory) -> bool:
        """
            Determine if an OutfitCategory is CAREER
        """
        return outfit_category == OutfitCategory.CAREER

    @staticmethod
    def is_situation_category(outfit_category: OutfitCategory) -> bool:
        """
            Determine if an OutfitCategory is SITUATION
        """
        return outfit_category == OutfitCategory.SITUATION

    @staticmethod
    def is_special_category(outfit_category: OutfitCategory) -> bool:
        """
            Determine if an OutfitCategory is SPECIAL
        """
        return outfit_category == OutfitCategory.SPECIAL

    @staticmethod
    def is_swimwear_category(outfit_category: OutfitCategory) -> bool:
        """
            Determine if an OutfitCategory is SWIMWEAR
        """
        return outfit_category == OutfitCategory.SWIMWEAR

    @staticmethod
    def is_hot_weather_category(outfit_category: OutfitCategory) -> bool:
        """
            Determine if an OutfitCategory is HOT_WEATHER
        """
        return outfit_category == OutfitCategory.HOT_WEATHER

    @staticmethod
    def is_cold_weather_category(outfit_category: OutfitCategory) -> bool:
        """
            Determine if an OutfitCategory is COLD_WEATHER
        """
        return outfit_category == OutfitCategory.COLD_WEATHER

    @staticmethod
    def get_all_outfit_categories() -> Tuple[OutfitCategory]:
        """
            Retrieve a collection of all OutfitCategory types.
        """
        return tuple(OutfitCategory.values)

    @staticmethod
    def is_wearing_everyday_outfit(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is wearing an Everyday outfit.
        """
        return CommonOutfitUtils.is_every_day_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_formal_outfit(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is wearing a Formal outfit.
        """
        return CommonOutfitUtils.is_formal_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_athletic_outfit(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is wearing an Athletic outfit.
        """
        return CommonOutfitUtils.is_athletic_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_sleep_outfit(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is wearing a Sleep outfit.
        """
        return CommonOutfitUtils.is_sleep_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_party_outfit(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is wearing a Party outfit.
        """
        return CommonOutfitUtils.is_party_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_bathing_outfit(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is wearing a Bathing outfit.
        """
        return CommonOutfitUtils.is_bathing_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_career_outfit(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is wearing a Career outfit.
        """
        return CommonOutfitUtils.is_career_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_situation_outfit(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is wearing a Situation outfit.
        """
        return CommonOutfitUtils.is_situation_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_special_outfit(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is wearing a Special outfit.
        """
        return CommonOutfitUtils.is_special_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_swimwear_outfit(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is wearing a Swimwear outfit.
        """
        return CommonOutfitUtils.is_swimwear_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_hot_weather_outfit(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is wearing a Hot Weather outfit.
        """
        return CommonOutfitUtils.is_hot_weather_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def is_wearing_cold_weather_outfit(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is wearing a Cold Weather outfit.
        """
        return CommonOutfitUtils.is_cold_weather_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @staticmethod
    def get_current_outfit_category(sim_info: SimInfo) -> OutfitCategory:
        """
            Retrieve the current OutfitCategory and Index of the current sim.
        """
        return CommonOutfitUtils.get_current_outfit(sim_info)[0]

    @staticmethod
    def get_current_outfit_index(sim_info: SimInfo) -> int:
        """
            Retrieve the current OutfitCategory and Index of the current sim.
        """
        return CommonOutfitUtils.get_current_outfit(sim_info)[1]

    @staticmethod
    def get_current_outfit(sim_info: SimInfo) -> Tuple[OutfitCategory, int]:
        """
            Retrieve the current OutfitCategory and Index of the current sim.
        """
        return sim_info.get_current_outfit()

    @staticmethod
    def get_outfit_data(sim_info: SimInfo, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None) -> OutfitData:
        """
            Retrieve OutfitData for the specified OutfitCategory and Index of a sim.
        :param sim_info: The sim to retrieve outfit data of.
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to retrieve data from. Default is the current outfit.
        """
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        return sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])

    @staticmethod
    def get_outfit_parts(sim_info: SimInfo, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None) -> Dict[BodyType, int]:
        """
            Retrieve Outfit Parts for the specified OutfitCategory and Index of a sim.
        :param sim_info: The sim to retrieve outfit parts of.
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to retrieve data from. Default is the current outfit.
        """
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        outfit_data = sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])
        if outfit_data is None:
            return dict()
        return dict(zip(list(outfit_data.body_types), list(outfit_data.part_ids)))

    @staticmethod
    def set_current_outfit(sim_info: SimInfo, outfit_category_and_index: Tuple[OutfitCategory, int]):
        """
            Set the current outfit of a sim to the specified OutfitCategory and Index.
        :param sim_info: The sim to change the outfit of.
        :param outfit_category_and_index: The OutfitCategory and index to change to.
        """
        sim_info.set_current_outfit(outfit_category_and_index)

    @staticmethod
    def set_outfit_dirty(sim_info: SimInfo, outfit_category: OutfitCategory):
        """
            Flag the specified OutfitCategory of a sim as dirty.
            This will tell the game that it needs to be updated.
        :param sim_info: The sim to flag the OutfitCategory for.
        :param outfit_category: The OutfitCategory being flagged.
        """
        sim_info.set_outfit_dirty(outfit_category)

    @staticmethod
    def set_outfit_clean(sim_info: SimInfo, outfit_category: OutfitCategory):
        """
            Flag the specified OutfitCategory of a sim as clean.
        :param sim_info: The sim to flag the OutfitCategory for.
        :param outfit_category: The OutfitCategory being flagged.
        """
        sim_info.clear_outfit_dirty(outfit_category)

    @staticmethod
    def generate_outfit(sim_info: SimInfo, outfit_category_and_index: Tuple[OutfitCategory, int]):
        """
            Generate an outfit for a sim for the specified OutfitCategory and Index.

            Note; If an outfit exists in the specified OutfitCategory and index, already, it will be overwritten.
        """
        sim_info.on_outfit_generated(sim_info, CommonOutfitUtils.get_current_outfit(sim_info))
        sim_info.generate_outfit(*outfit_category_and_index)

    @staticmethod
    def resend_outfits(sim_info: SimInfo):
        """
            Resend outfit data to a sim to refresh their outfits.
        """
        sim_info.resend_outfits()

    @staticmethod
    def get_previous_outfit(sim_info: SimInfo, default_outfit_category_and_index: Tuple[OutfitCategory, int]=(OutfitCategory.EVERYDAY, 0)) -> Tuple[OutfitCategory, int]:
        """
            Retrieve the previous outfit a sim was wearing before their current outfit.
        :param sim_info: The sim to get the previous outfit of.
        :param default_outfit_category_and_index: A default OutfitCategory and index if no previous outfit was found.
        """
        return sim_info.get_previous_outfit() or default_outfit_category_and_index

    @staticmethod
    def remove_previous_outfit(sim_info: SimInfo):
        """
            Remove the previous outfit of a sim.
        """
        sim_info.set_previous_outfit(None, force=True)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=False)
    def has_outfit(sim_info: SimInfo, outfit_category_and_index: Tuple[OutfitCategory, int]) -> bool:
        """
            Determine if a sim has an existing outfit in the specified OutfitCategory and Index.
        :param sim_info: The sim to check.
        :param outfit_category_and_index: The OutfitCategory and index to locate.
        """
        return sim_info.has_outfit(outfit_category_and_index)

    @staticmethod
    def update_outfits(sim_info: SimInfo):
        """
            Update all outfits of a sim.
        """
        sim_info.on_outfit_changed(sim_info, CommonOutfitUtils.get_current_outfit(sim_info))
        CommonOutfitUtils.resend_outfits(sim_info)
        sim_info.appearance_tracker.evaluate_appearance_modifiers()


@sims4.commands.Command('s4clib_testing.show_all_outfit_categories', command_type=sims4.commands.CommandType.Live)
def _s4clib_testing_show_all_outfit_categories(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing all outfit categories.')
    categories = CommonOutfitUtils.get_all_outfit_categories()
    output('Outfit categories: {}'.format(pformat(categories)))
