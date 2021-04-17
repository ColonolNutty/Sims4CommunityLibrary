"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict

from sims.sim_info import SimInfo
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.common_occult_type import CommonOccultType
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.enums.sim_type import CommonSimType


class CommonSimTypeUtils:
    """Utilities for determining the type of a Sim. i.e. Player, NPC, Service, etc.

    """
    _COMBINE_SIM_TYPE_MAPPING: Dict[CommonSimType, CommonSimType] = {
        CommonSimType.CHILD_SMALL_DOG: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_SMALL_DOG_VAMPIRE: CommonSimType.CHILD_DOG_VAMPIRE,
        CommonSimType.CHILD_SMALL_DOG_GHOST: CommonSimType.CHILD_DOG_GHOST,
        CommonSimType.CHILD_SMALL_DOG_ALIEN: CommonSimType.CHILD_DOG_ALIEN,
        CommonSimType.CHILD_SMALL_DOG_MERMAID: CommonSimType.CHILD_DOG_MERMAID,
        CommonSimType.CHILD_SMALL_DOG_WITCH: CommonSimType.CHILD_DOG_WITCH,
        CommonSimType.CHILD_SMALL_DOG_ROBOT: CommonSimType.CHILD_DOG_ROBOT,
        CommonSimType.CHILD_LARGE_DOG: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_LARGE_DOG_VAMPIRE: CommonSimType.CHILD_DOG_VAMPIRE,
        CommonSimType.CHILD_LARGE_DOG_GHOST: CommonSimType.CHILD_DOG_GHOST,
        CommonSimType.CHILD_LARGE_DOG_ALIEN: CommonSimType.CHILD_DOG_ALIEN,
        CommonSimType.CHILD_LARGE_DOG_MERMAID: CommonSimType.CHILD_DOG_MERMAID,
        CommonSimType.CHILD_LARGE_DOG_WITCH: CommonSimType.CHILD_DOG_WITCH,
        CommonSimType.CHILD_LARGE_DOG_ROBOT: CommonSimType.CHILD_DOG_ROBOT
    }

    _SIM_TO_SIM_TYPE_MAPPING: Dict[CommonSpecies, Dict[CommonAge, Dict[CommonOccultType, CommonSimType]]] = {
        CommonSpecies.HUMAN: {
            CommonAge.ELDER: {
                CommonOccultType.NON_OCCULT: CommonSimType.ELDER_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.ELDER_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ELDER_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ELDER_HUMAN_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.ELDER_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ELDER_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ELDER_HUMAN_ROBOT
            },
            CommonAge.ADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_HUMAN_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.ADULT_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_HUMAN_ROBOT
            },
            CommonAge.YOUNGADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.YOUNG_ADULT_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.YOUNG_ADULT_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.YOUNG_ADULT_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.YOUNG_ADULT_HUMAN_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.YOUNG_ADULT_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.YOUNG_ADULT_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.YOUNG_ADULT_HUMAN_ROBOT
            },
            CommonAge.TEEN: {
                CommonOccultType.NON_OCCULT: CommonSimType.TEEN_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.TEEN_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.TEEN_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.TEEN_HUMAN_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.TEEN_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.TEEN_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.TEEN_HUMAN_ROBOT
            },
            CommonAge.CHILD: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_HUMAN_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.CHILD_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_HUMAN_ROBOT
            },
            CommonAge.TODDLER: {
                CommonOccultType.NON_OCCULT: CommonSimType.TODDLER_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.TODDLER_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.TODDLER_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.TODDLER_HUMAN_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.TODDLER_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.TODDLER_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.TODDLER_HUMAN_ROBOT
            },
            CommonAge.BABY: {
                CommonOccultType.NON_OCCULT: CommonSimType.BABY_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.BABY_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.BABY_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.BABY_HUMAN_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.BABY_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.BABY_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.BABY_HUMAN_ROBOT
            }
        },
        CommonSpecies.SMALL_DOG: {
            CommonAge.ELDER: {
                CommonOccultType.NON_OCCULT: CommonSimType.ELDER_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ELDER_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ELDER_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ELDER_SMALL_DOG_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.ELDER_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ELDER_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ELDER_SMALL_DOG_ROBOT
            },
            CommonAge.ADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_SMALL_DOG_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.ADULT_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_SMALL_DOG_ROBOT
            },
            CommonAge.YOUNGADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_SMALL_DOG_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.ADULT_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_SMALL_DOG_ROBOT
            },
            CommonAge.TEEN: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_SMALL_DOG_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.ADULT_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_SMALL_DOG_ROBOT
            },
            CommonAge.CHILD: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_SMALL_DOG_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.CHILD_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_SMALL_DOG_ROBOT
            },
            CommonAge.TODDLER: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_SMALL_DOG_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.CHILD_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_SMALL_DOG_ROBOT
            },
            CommonAge.BABY: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_SMALL_DOG_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.CHILD_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_SMALL_DOG_ROBOT
            }
        },
        CommonSpecies.LARGE_DOG: {
            CommonAge.ELDER: {
                CommonOccultType.NON_OCCULT: CommonSimType.ELDER_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ELDER_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ELDER_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ELDER_LARGE_DOG_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.ELDER_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ELDER_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ELDER_LARGE_DOG_ROBOT
            },
            CommonAge.ADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_LARGE_DOG_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.ADULT_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_LARGE_DOG_ROBOT
            },
            CommonAge.YOUNGADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_LARGE_DOG_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.ADULT_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_LARGE_DOG_ROBOT
            },
            CommonAge.TEEN: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_LARGE_DOG_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.ADULT_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_LARGE_DOG_ROBOT
            },
            CommonAge.CHILD: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_LARGE_DOG_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.CHILD_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_LARGE_DOG_ROBOT
            },
            CommonAge.TODDLER: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_LARGE_DOG_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.CHILD_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_LARGE_DOG_ROBOT
            },
            CommonAge.BABY: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_LARGE_DOG_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.CHILD_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_LARGE_DOG_ROBOT
            }
        },
        CommonSpecies.CAT: {
            CommonAge.ELDER: {
                CommonOccultType.NON_OCCULT: CommonSimType.ELDER_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.ELDER_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ELDER_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ELDER_CAT_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.ELDER_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ELDER_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ELDER_CAT_ROBOT
            },
            CommonAge.ADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_CAT_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.ADULT_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_CAT_ROBOT
            },
            CommonAge.YOUNGADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_CAT_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.ADULT_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_CAT_ROBOT
            },
            CommonAge.TEEN: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_CAT_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.ADULT_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_CAT_ROBOT
            },
            CommonAge.CHILD: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_CAT_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.CHILD_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_CAT_ROBOT
            },
            CommonAge.TODDLER: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_CAT_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.CHILD_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_CAT_ROBOT
            },
            CommonAge.BABY: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_CAT_ALIEN,
                CommonOccultType.MERMAID: CommonSimType.CHILD_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_CAT_ROBOT
            }
        }
    }
    _SIM_TYPE_TO_SIGNATURE_MAPPING: Dict[CommonSimType, str] = {
        # Human
        CommonSimType.ELDER_HUMAN: 'ElHu',
        CommonSimType.ELDER_HUMAN_VAMPIRE: 'ElHuVa',
        CommonSimType.ELDER_HUMAN_GHOST: 'ElHuGh',
        CommonSimType.ELDER_HUMAN_ALIEN: 'ElHuAl',
        CommonSimType.ELDER_HUMAN_MERMAID: 'ElHuMer',
        CommonSimType.ELDER_HUMAN_WITCH: 'ElHuWi',
        CommonSimType.ELDER_HUMAN_ROBOT: 'ElHuRo',
        CommonSimType.ADULT_HUMAN: 'AdHu',
        CommonSimType.ADULT_HUMAN_VAMPIRE: 'AdHuVa',
        CommonSimType.ADULT_HUMAN_GHOST: 'AdHuGh',
        CommonSimType.ADULT_HUMAN_ALIEN: 'AdHuAl',
        CommonSimType.ADULT_HUMAN_MERMAID: 'AdHuMer',
        CommonSimType.ADULT_HUMAN_WITCH: 'AdHuWi',
        CommonSimType.ADULT_HUMAN_ROBOT: 'AdHuRo',
        CommonSimType.YOUNG_ADULT_HUMAN: 'AdHu',
        CommonSimType.YOUNG_ADULT_HUMAN_VAMPIRE: 'YadHuVa',
        CommonSimType.YOUNG_ADULT_HUMAN_GHOST: 'YadHuGh',
        CommonSimType.YOUNG_ADULT_HUMAN_ALIEN: 'YadHuAl',
        CommonSimType.YOUNG_ADULT_HUMAN_MERMAID: 'YadHuMer',
        CommonSimType.YOUNG_ADULT_HUMAN_WITCH: 'YadHuWi',
        CommonSimType.YOUNG_ADULT_HUMAN_ROBOT: 'YadHuRo',
        CommonSimType.TEEN_HUMAN: 'TnHu',
        CommonSimType.TEEN_HUMAN_VAMPIRE: 'TnHuVa',
        CommonSimType.TEEN_HUMAN_GHOST: 'TnHuGh',
        CommonSimType.TEEN_HUMAN_ALIEN: 'TnHuAl',
        CommonSimType.TEEN_HUMAN_MERMAID: 'TnHuMer',
        CommonSimType.TEEN_HUMAN_WITCH: 'TnHuWi',
        CommonSimType.TEEN_HUMAN_ROBOT: 'TnHuRo',
        CommonSimType.CHILD_HUMAN: 'ChldHu',
        CommonSimType.CHILD_HUMAN_VAMPIRE: 'ChldHuVa',
        CommonSimType.CHILD_HUMAN_GHOST: 'ChldHuGh',
        CommonSimType.CHILD_HUMAN_ALIEN: 'ChldHuAl',
        CommonSimType.CHILD_HUMAN_MERMAID: 'ChldHuMer',
        CommonSimType.CHILD_HUMAN_WITCH: 'ChldHuWi',
        CommonSimType.CHILD_HUMAN_ROBOT: 'ChldHuRo',
        CommonSimType.TODDLER_HUMAN: 'TdlrHu',
        CommonSimType.TODDLER_HUMAN_VAMPIRE: 'TdlrHuVa',
        CommonSimType.TODDLER_HUMAN_GHOST: 'TdlrHuGh',
        CommonSimType.TODDLER_HUMAN_ALIEN: 'TdlrHuAl',
        CommonSimType.TODDLER_HUMAN_MERMAID: 'TdlrHuMer',
        CommonSimType.TODDLER_HUMAN_WITCH: 'TdlrHuWi',
        CommonSimType.TODDLER_HUMAN_ROBOT: 'TdlrHuRo',
        CommonSimType.BABY_HUMAN: 'BbyHu',
        CommonSimType.BABY_HUMAN_VAMPIRE: 'BbyHuVa',
        CommonSimType.BABY_HUMAN_GHOST: 'BbyHuGh',
        CommonSimType.BABY_HUMAN_ALIEN: 'BbyHuAl',
        CommonSimType.BABY_HUMAN_MERMAID: 'BbyHuMer',
        CommonSimType.BABY_HUMAN_WITCH: 'BbyHuWi',
        CommonSimType.BABY_HUMAN_ROBOT: 'BbyHuRo',
        # Small Dog
        CommonSimType.ELDER_SMALL_DOG: 'ElSd',
        CommonSimType.ELDER_SMALL_DOG_VAMPIRE: 'ElSdVa',
        CommonSimType.ELDER_SMALL_DOG_GHOST: 'ElSdGh',
        CommonSimType.ELDER_SMALL_DOG_ALIEN: 'ElSdAl',
        CommonSimType.ELDER_SMALL_DOG_MERMAID: 'ElSdMer',
        CommonSimType.ELDER_SMALL_DOG_WITCH: 'ElSdWi',
        CommonSimType.ELDER_SMALL_DOG_ROBOT: 'ElSdRo',
        CommonSimType.ADULT_SMALL_DOG: 'AdSd',
        CommonSimType.ADULT_SMALL_DOG_VAMPIRE: 'AdSdVa',
        CommonSimType.ADULT_SMALL_DOG_GHOST: 'AdSdGh',
        CommonSimType.ADULT_SMALL_DOG_ALIEN: 'AdSdAl',
        CommonSimType.ADULT_SMALL_DOG_MERMAID: 'AdSdMer',
        CommonSimType.ADULT_SMALL_DOG_WITCH: 'AdSdWi',
        CommonSimType.ADULT_SMALL_DOG_ROBOT: 'AdSdRo',
        # Child Dog
        CommonSimType.CHILD_DOG: 'ChldDg',
        CommonSimType.CHILD_DOG_VAMPIRE: 'ChldDgVa',
        CommonSimType.CHILD_DOG_GHOST: 'ChldDgGh',
        CommonSimType.CHILD_DOG_ALIEN: 'ChldDgAl',
        CommonSimType.CHILD_DOG_MERMAID: 'ChldDgMer',
        CommonSimType.CHILD_DOG_WITCH: 'ChldDgWi',
        CommonSimType.CHILD_DOG_ROBOT: 'ChldDgRo',
        # Small Dog
        CommonSimType.CHILD_SMALL_DOG: 'ChldSd',
        CommonSimType.CHILD_SMALL_DOG_VAMPIRE: 'ChldSdVa',
        CommonSimType.CHILD_SMALL_DOG_GHOST: 'ChldSdGh',
        CommonSimType.CHILD_SMALL_DOG_ALIEN: 'ChldSdAl',
        CommonSimType.CHILD_SMALL_DOG_MERMAID: 'ChldSdMer',
        CommonSimType.CHILD_SMALL_DOG_WITCH: 'ChldSdWi',
        CommonSimType.CHILD_SMALL_DOG_ROBOT: 'ChldSdRo',
        # Large Dog
        CommonSimType.ELDER_LARGE_DOG: 'ElLd',
        CommonSimType.ELDER_LARGE_DOG_VAMPIRE: 'ElLdVa',
        CommonSimType.ELDER_LARGE_DOG_GHOST: 'ElLdGh',
        CommonSimType.ELDER_LARGE_DOG_ALIEN: 'ElLdAl',
        CommonSimType.ELDER_LARGE_DOG_MERMAID: 'ElLdMer',
        CommonSimType.ELDER_LARGE_DOG_WITCH: 'ElLdWi',
        CommonSimType.ELDER_LARGE_DOG_ROBOT: 'ElLdRo',
        CommonSimType.ADULT_LARGE_DOG: 'AdLd',
        CommonSimType.ADULT_LARGE_DOG_VAMPIRE: 'AdLdVa',
        CommonSimType.ADULT_LARGE_DOG_GHOST: 'AdLdGh',
        CommonSimType.ADULT_LARGE_DOG_ALIEN: 'AdLdAl',
        CommonSimType.ADULT_LARGE_DOG_MERMAID: 'AdLdMer',
        CommonSimType.ADULT_LARGE_DOG_WITCH: 'AdLdWi',
        CommonSimType.ADULT_LARGE_DOG_ROBOT: 'AdLdRo',
        CommonSimType.CHILD_LARGE_DOG: 'ChldLd',
        CommonSimType.CHILD_LARGE_DOG_VAMPIRE: 'ChldLdVa',
        CommonSimType.CHILD_LARGE_DOG_GHOST: 'ChldLdGh',
        CommonSimType.CHILD_LARGE_DOG_ALIEN: 'ChldLdAl',
        CommonSimType.CHILD_LARGE_DOG_MERMAID: 'ChldLdMer',
        CommonSimType.CHILD_LARGE_DOG_WITCH: 'ChldLdWi',
        CommonSimType.CHILD_LARGE_DOG_ROBOT: 'ChldLdRo',
        # Cat
        CommonSimType.ELDER_CAT: 'ElCat',
        CommonSimType.ELDER_CAT_VAMPIRE: 'ElCatVa',
        CommonSimType.ELDER_CAT_GHOST: 'ElCatGh',
        CommonSimType.ELDER_CAT_ALIEN: 'ElCatAl',
        CommonSimType.ELDER_CAT_MERMAID: 'ElCatMer',
        CommonSimType.ELDER_CAT_WITCH: 'ElCatWi',
        CommonSimType.ELDER_CAT_ROBOT: 'ElCatRo',
        CommonSimType.ADULT_CAT: 'AdCat',
        CommonSimType.ADULT_CAT_VAMPIRE: 'AdCatVa',
        CommonSimType.ADULT_CAT_GHOST: 'AdCatGh',
        CommonSimType.ADULT_CAT_ALIEN: 'AdCatAl',
        CommonSimType.ADULT_CAT_MERMAID: 'AdCatMer',
        CommonSimType.ADULT_CAT_WITCH: 'AdCatWi',
        CommonSimType.ADULT_CAT_ROBOT: 'AdCatRo',
        CommonSimType.CHILD_CAT: 'ChldCat',
        CommonSimType.CHILD_CAT_VAMPIRE: 'ChldCatVa',
        CommonSimType.CHILD_CAT_GHOST: 'ChldCatGh',
        CommonSimType.CHILD_CAT_ALIEN: 'ChldCatAl',
        CommonSimType.CHILD_CAT_MERMAID: 'ChldCatMer',
        CommonSimType.CHILD_CAT_WITCH: 'ChldCatWi',
        CommonSimType.CHILD_CAT_ROBOT: 'ChldCatRo'
    }

    _OCCULT_SIM_TYPE_TO_NON_OCCULT_SIM_TYPE_MAPPING: Dict[CommonSimType, CommonSimType] = {
        # Human
        CommonSimType.ELDER_HUMAN: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_VAMPIRE: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_GHOST: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_ALIEN: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_MERMAID: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_WITCH: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_ROBOT: CommonSimType.ELDER_HUMAN,
        CommonSimType.ADULT_HUMAN: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_VAMPIRE: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_GHOST: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_ALIEN: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_MERMAID: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_WITCH: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_ROBOT: CommonSimType.ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_VAMPIRE: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_GHOST: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_ALIEN: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_MERMAID: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_WITCH: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_ROBOT: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.CHILD_HUMAN: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_VAMPIRE: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_GHOST: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_ALIEN: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_MERMAID: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_WITCH: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_ROBOT: CommonSimType.CHILD_HUMAN,
        CommonSimType.TODDLER_HUMAN: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_VAMPIRE: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_GHOST: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_ALIEN: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_MERMAID: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_WITCH: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_ROBOT: CommonSimType.TODDLER_HUMAN,
        CommonSimType.BABY_HUMAN: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_VAMPIRE: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_GHOST: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_ALIEN: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_MERMAID: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_WITCH: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_ROBOT: CommonSimType.BABY_HUMAN,
        # Small Dog
        CommonSimType.ELDER_SMALL_DOG: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_VAMPIRE: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_GHOST: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_ALIEN: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_MERMAID: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_WITCH: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_ROBOT: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_VAMPIRE: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_GHOST: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_ALIEN: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_MERMAID: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_WITCH: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_ROBOT: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.CHILD_DOG: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_VAMPIRE: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_GHOST: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_ALIEN: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_MERMAID: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_WITCH: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_ROBOT: CommonSimType.CHILD_DOG,

        CommonSimType.CHILD_SMALL_DOG: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_VAMPIRE: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_GHOST: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_ALIEN: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_MERMAID: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_WITCH: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_ROBOT: CommonSimType.CHILD_SMALL_DOG,
        # Large Dog
        CommonSimType.ELDER_LARGE_DOG: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_VAMPIRE: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_GHOST: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_ALIEN: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_MERMAID: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_WITCH: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_ROBOT: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_VAMPIRE: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_GHOST: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_ALIEN: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_MERMAID: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_WITCH: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_ROBOT: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_VAMPIRE: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_GHOST: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_ALIEN: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_MERMAID: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_WITCH: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_ROBOT: CommonSimType.CHILD_LARGE_DOG,
        # Cat
        CommonSimType.ELDER_CAT: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_VAMPIRE: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_GHOST: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_ALIEN: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_MERMAID: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_WITCH: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_ROBOT: CommonSimType.ELDER_CAT,
        CommonSimType.ADULT_CAT: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_VAMPIRE: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_GHOST: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_ALIEN: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_MERMAID: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_WITCH: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_ROBOT: CommonSimType.ADULT_CAT,
        CommonSimType.CHILD_CAT: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_VAMPIRE: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_GHOST: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_ALIEN: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_MERMAID: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_WITCH: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_ROBOT: CommonSimType.CHILD_CAT,
    }

    @staticmethod
    def is_non_player_sim(sim_info: SimInfo) -> bool:
        """is_non_player_sim(sim_info)

        Determine if a Sim is a Non Player Sim.

        .. note:: An NPC Sim is a sim that is not a part of the active household.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is an NPC. False, if not.
        :rtype: bool
        """
        return sim_info.is_npc

    @staticmethod
    def is_player_sim(sim_info: SimInfo) -> bool:
        """is_player_sim(sim_info)

        Determine if a Sim is a Player Sim.

        .. note:: A Player Sim is a Sim that is a part of the active household.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Player Sim. False, if not.
        :rtype: bool
        """
        return not CommonSimTypeUtils.is_non_player_sim(sim_info)

    @staticmethod
    def is_played_sim(sim_info: SimInfo) -> bool:
        """is_played_sim(sim_info)

        Determine if a Sim is a Played Sim.

        .. note:: This does not indicate whether or not a Sim is a Player Sim or Non Player Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Played Sim. False, if not.
        :rtype: bool
        """
        return sim_info.is_played_sim

    @staticmethod
    def is_service_sim(sim_info: SimInfo) -> bool:
        """Determine if a Sim is a Service Sim.

        .. note::

            Service Sims:

            - Butler
            - Chalet
            - City Repair
            - Forest Ranger
            - Gardener
            - Grim Reaper
            - Maid
            - Mailman
            - Massage Therapist
            - Master Fisherman
            - Master Gardener
            - Master Herbalist
            - Nanny
            - Pizza Delivery
            - Repairman
            - Restaurant Critic
            - Statue Busker

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Service Sim. False, if not.
        :rtype: bool
        """
        from sims4communitylib.enums.traits_enum import CommonTraitId
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        trait_ids = (
            CommonTraitId.IS_BUTLER,
            CommonTraitId.IS_CHALET_GARDENS_GHOST,
            CommonTraitId.IS_CITY_REPAIR,
            CommonTraitId.IS_FOREST_RANGER,
            CommonTraitId.IS_GARDENER,
            CommonTraitId.IS_GARDENER_SERVICE,
            CommonTraitId.IS_GRIM_REAPER,
            CommonTraitId.IS_MAID,
            CommonTraitId.IS_MAILMAN,
            CommonTraitId.IS_MASSAGE_THERAPIST,
            CommonTraitId.IS_MASTER_FISHERMAN,
            CommonTraitId.IS_MASTER_GARDENER,
            CommonTraitId.IS_MASTER_HERBALIST,
            CommonTraitId.IS_NANNY,
            CommonTraitId.IS_PIZZA_DELIVERY,
            CommonTraitId.IS_REPAIR,
            CommonTraitId.IS_RESTAURANT_CRITIC,
            CommonTraitId.IS_STATUE_BUSKER
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def determine_sim_type(sim_info: SimInfo, combine_teen_young_adult_and_elder_age: bool=True, combine_child_dog_types: bool=True) -> CommonSimType:
        """determine_sim_type(sim_info, combine_teen_young_adult_and_elder_age=True, combine_child_dog_types=True)

        Determine the type of Sim a Sim is based on their Age, Species, and Occult Type.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param combine_teen_young_adult_and_elder_age: If set to True, Teen, Young Adult, Adult, and Elder, will all receive an ADULT denoted Sim Type instead of TEEN, YOUNG_ADULT, ADULT, and ELDER respectively. i.e. A Human Teen Sim would be denoted as ADULT_HUMAN.
        If set to False, they will receive their own Sim Types. i.e. A Human Teen Sim would be denoted as TEEN_HUMAN. Default is True.
        :type combine_teen_young_adult_and_elder_age: bool, optional
        :param combine_child_dog_types: If set to True, the Child Dog Sim Types will be combined into a single Sim Type, i.e. CHILD_DOG. If set to False, the Child Dog Sim Types will be returned as their more specific values. i.e. CHILD_LARGE_DOG, CHILD_SMALL_DOG, etc. Default is True.
        :type combine_child_dog_types: bool, optional
        :return: The type of Sim the Sim is or CommonSimType.NONE if no type was found for the Sim.
        :rtype: CommonSimType
        """
        species = CommonSpecies.get_species(sim_info)
        age = CommonAge.get_age(sim_info)
        if combine_teen_young_adult_and_elder_age and age in (CommonAge.TEEN, CommonAge.YOUNGADULT, CommonAge.ADULT, CommonAge.ELDER):
            age = CommonAge.ADULT
        occult_type = CommonOccultType.determine_occult_type(sim_info)
        sim_type = CommonSimTypeUtils._determine_sim_type(species, age, occult_type)
        if combine_child_dog_types and sim_type in CommonSimTypeUtils._COMBINE_SIM_TYPE_MAPPING:
            return CommonSimTypeUtils._COMBINE_SIM_TYPE_MAPPING[sim_type]
        return sim_type

    @staticmethod
    def _determine_sim_type(species: CommonSpecies, age: CommonAge, occult_type: CommonOccultType) -> CommonSimType:
        if species not in CommonSimTypeUtils._SIM_TO_SIM_TYPE_MAPPING\
                or age not in CommonSimTypeUtils._SIM_TO_SIM_TYPE_MAPPING[species]\
                or occult_type not in CommonSimTypeUtils._SIM_TO_SIM_TYPE_MAPPING[species][age]:
            return CommonSimType.NONE
        return CommonSimTypeUtils._SIM_TO_SIM_TYPE_MAPPING[species][age][occult_type]

    @staticmethod
    def are_same_age_and_species(sim_type_one: CommonSimType, sim_type_two: CommonSimType) -> bool:
        """are_same_age_and_species(sim_type_one, sim_type_two)

        Determine if two Sim Types are comprised of the same Age and Species.

        :param sim_type_one: An instance of a Sim Type.
        :type sim_type_one: CommonSimType
        :param sim_type_two: An instance of a Sim Type.
        :type sim_type_two: CommonSimType
        :return: True, if both Sim types are the same Age and Species, ignoring Occult Types. False, if not.
        :rtype: bool
        """
        if sim_type_one == sim_type_two:
            return True
        return CommonSimTypeUtils.convert_to_non_occult_variant(sim_type_one) == CommonSimTypeUtils.convert_to_non_occult_variant(sim_type_two)

    @staticmethod
    def convert_to_signature(sim_type: CommonSimType) -> str:
        """convert_to_signature(sim_type)

        Convert a Sim Type to a unique signature.

        :param sim_type: The sim type to convert.
        :type sim_type: CommonSimType
        :return: A string signature that uniquely represents the Sim Type or the name of the Sim Type, if no unique signature is found.
        :rtype: str
        """
        if sim_type not in CommonSimTypeUtils._SIM_TYPE_TO_SIGNATURE_MAPPING:
            return sim_type.name
        return CommonSimTypeUtils._SIM_TYPE_TO_SIGNATURE_MAPPING[sim_type]

    @staticmethod
    def convert_to_non_occult_variant(sim_type: CommonSimType) -> CommonSimType:
        """convert_sim_type_to_non_occult_variant(sim_type)

        Convert an Occult sim type to a Non-Occult Sim Type.

        :param sim_type: The Sim Type to convert.
        :type sim_type: CommonSimType
        :return: The Non-Occult variant of the Sim Type or itself, if no Non-Occult variant is found.
        :rtype: CommonSimType
        """
        if sim_type not in CommonSimTypeUtils._OCCULT_SIM_TYPE_TO_NON_OCCULT_SIM_TYPE_MAPPING:
            return sim_type
        return CommonSimTypeUtils._OCCULT_SIM_TYPE_TO_NON_OCCULT_SIM_TYPE_MAPPING[sim_type]
