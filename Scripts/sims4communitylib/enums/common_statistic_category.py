"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from statistics.statistic_categories import StatisticCategory


def _get_statistic_category(name: str) -> Union[StatisticCategory, int]:
    return CommonResourceUtils.get_enum_by_name(name, StatisticCategory, default_value=StatisticCategory.INVALID)


class CommonStatisticCategory(CommonInt):
    """Custom Statistic Category equivalent to the DynamicEnum statistics.statistic_categories.StatisticCategory

    """
    INVALID: 'CommonStatisticCategory' = _get_statistic_category('INVALID')

    ANGRY_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Angry_Buffs')
    ASLEEP_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Asleep_Buffs')
    BAD_FOOD_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('BadFood_Buffs')
    BORED_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Bored_Buffs')
    CHEF_COOK_STYLE_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('ChefCookStyle_Buffs')
    CHILDHOOD_PHASE_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('ChildhoodPhase_Buffs')
    CLOTHING_OPTIONAL_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('ClothingOptional_Buffs')
    CONFIDENT_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Confident_Buffs')
    EMBARRASSED_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Embarrassed_Buffs')
    ENERGIZED_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Energized_Buffs')
    FINE_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Fine_Buffs')
    FLIRTY_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Flirty_Buffs')
    FOCUSED_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Focused_Buffs')
    GAMES_COM_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Gamescom_Buffs')
    GROUNDED_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Grounded_Buffs')
    HACKING_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Hacking_Buffs')
    HAPPY_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Happy_Buffs')
    INJURY_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Injury_Buffs')
    INSPIRED_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Inspired_Buffs')
    ITCHY_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Itchy_Buffs')
    MIND_CONTROL_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('MindControl_Buffs')
    MIND_POWERS_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('MindPowers_Buffs')
    MODULE_TUNABLES: 'CommonStatisticCategory' = _get_statistic_category('MODULE_TUNABLES')
    MOTIVE_COMMODITIES: 'CommonStatisticCategory' = _get_statistic_category('Motive_Commodities')
    OBJECT_BED_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Object_Bed_Buffs')
    OBJECT_BOOK_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Object_Book_Buffs')
    OBJECT_JUNGLE_GYM_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Object_JungleGym_Buffs')
    OBJECT_MICROSCOPE_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Object_Microscope_Buffs')
    OBJECT_MIRROR_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Object_Mirror_Buffs')
    OBJECT_MOTION_GAMING_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Object_MotionGaming_Buffs')
    OBJECT_OBSERVATORY_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Object_Observatory_Buffs')
    OBJECT_STEREO_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Object_Stereo_Buffs')
    OBJECT_TOY_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Object_Toy_Buffs')
    OBJECT_TV_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Object_TV_Buffs')
    PET_SICKNESS_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('PetSickness_Buffs')
    PLAYFUL_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Playful_Buffs')
    PRANK_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Prank_Buffs')
    PRANK_COOLDOWN_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('PrankCooldown_Buffs')
    SAD_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Sad_Buffs')
    SCARED_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Scared_Buffs')
    SICKNESS_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Sickness_Buffs')
    SLOSHED_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Sloshed_Buffs')
    SOCIAL_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Social_Buffs')
    STRESSED_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Stressed_Buffs')
    SURVEY_COOLDOWN_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('SurveyCooldown_Buffs')
    TEEN_MOOD_SWING_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('TeenMoodSwing_Buffs')
    TEMPLE_FUN_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Temple_Fun_Buffs')
    UNCOMFORTABLE_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Uncomfortable_Buffs')
    UNIVERSITY_STUDYING_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('University_Studying_Buffs')
    VAMPIRE_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('Vampire_Buffs')
    WILDLIFE_ENCOUNTER_BUFFS: 'CommonStatisticCategory' = _get_statistic_category('WildlifeEncounter_Buffs')
