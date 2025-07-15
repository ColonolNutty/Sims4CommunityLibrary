"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Iterator
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.common_occult_type import CommonOccultType
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.enums.sim_type import CommonSimType
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils


class CommonSimTypeUtils:
    """Utilities for determining the type of a Sim. i.e. Player, NPC, Service, etc.

    """
    _CHILD_DOG_SIM_TYPE_MAPPING: Dict[CommonSimType, CommonSimType] = {
        CommonSimType.CHILD_SMALL_DOG: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_SMALL_DOG_VAMPIRE: CommonSimType.CHILD_DOG_VAMPIRE,
        CommonSimType.CHILD_SMALL_DOG_GHOST: CommonSimType.CHILD_DOG_GHOST,
        CommonSimType.CHILD_SMALL_DOG_ALIEN: CommonSimType.CHILD_DOG_ALIEN,
        CommonSimType.CHILD_SMALL_DOG_MERMAID: CommonSimType.CHILD_DOG_MERMAID,
        CommonSimType.CHILD_SMALL_DOG_WITCH: CommonSimType.CHILD_DOG_WITCH,
        CommonSimType.CHILD_SMALL_DOG_ROBOT: CommonSimType.CHILD_DOG_ROBOT,
        CommonSimType.CHILD_SMALL_DOG_SCARECROW: CommonSimType.CHILD_DOG_SCARECROW,
        CommonSimType.CHILD_SMALL_DOG_SKELETON: CommonSimType.CHILD_DOG_SKELETON,
        CommonSimType.CHILD_SMALL_DOG_PLANT_SIM: CommonSimType.CHILD_DOG_PLANT_SIM,
        CommonSimType.CHILD_SMALL_DOG_WEREWOLF: CommonSimType.CHILD_DOG_WEREWOLF,

        CommonSimType.CHILD_LARGE_DOG: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_LARGE_DOG_VAMPIRE: CommonSimType.CHILD_DOG_VAMPIRE,
        CommonSimType.CHILD_LARGE_DOG_GHOST: CommonSimType.CHILD_DOG_GHOST,
        CommonSimType.CHILD_LARGE_DOG_ALIEN: CommonSimType.CHILD_DOG_ALIEN,
        CommonSimType.CHILD_LARGE_DOG_MERMAID: CommonSimType.CHILD_DOG_MERMAID,
        CommonSimType.CHILD_LARGE_DOG_WITCH: CommonSimType.CHILD_DOG_WITCH,
        CommonSimType.CHILD_LARGE_DOG_ROBOT: CommonSimType.CHILD_DOG_ROBOT,
        CommonSimType.CHILD_LARGE_DOG_SCARECROW: CommonSimType.CHILD_DOG_SCARECROW,
        CommonSimType.CHILD_LARGE_DOG_SKELETON: CommonSimType.CHILD_DOG_SKELETON,
        CommonSimType.CHILD_LARGE_DOG_PLANT_SIM: CommonSimType.CHILD_DOG_PLANT_SIM,
        CommonSimType.CHILD_LARGE_DOG_WEREWOLF: CommonSimType.CHILD_DOG_WEREWOLF,
    }

    _SIM_TO_SIM_TYPE_MAPPING: Dict[CommonSpecies, Dict[CommonAge, Dict[CommonOccultType, CommonSimType]]] = {
        CommonSpecies.HUMAN: {
            CommonAge.ELDER: {
                CommonOccultType.NON_OCCULT: CommonSimType.ELDER_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.ELDER_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ELDER_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ELDER_HUMAN_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ELDER_HUMAN_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ELDER_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ELDER_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ELDER_HUMAN_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ELDER_HUMAN_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ELDER_HUMAN_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ELDER_HUMAN_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ELDER_HUMAN_WEREWOLF,
            },
            CommonAge.ADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_HUMAN_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_HUMAN_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_HUMAN_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_HUMAN_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_HUMAN_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_HUMAN_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_HUMAN_WEREWOLF,
            },
            CommonAge.YOUNGADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.YOUNG_ADULT_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.YOUNG_ADULT_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.YOUNG_ADULT_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.YOUNG_ADULT_HUMAN_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.YOUNG_ADULT_HUMAN_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.YOUNG_ADULT_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.YOUNG_ADULT_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.YOUNG_ADULT_HUMAN_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.YOUNG_ADULT_HUMAN_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.YOUNG_ADULT_HUMAN_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.YOUNG_ADULT_HUMAN_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.YOUNG_ADULT_HUMAN_WEREWOLF,
            },
            CommonAge.TEEN: {
                CommonOccultType.NON_OCCULT: CommonSimType.TEEN_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.TEEN_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.TEEN_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.TEEN_HUMAN_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.TEEN_HUMAN_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.TEEN_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.TEEN_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.TEEN_HUMAN_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.TEEN_HUMAN_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.TEEN_HUMAN_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.TEEN_HUMAN_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.TEEN_HUMAN_WEREWOLF,
            },
            CommonAge.CHILD: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_HUMAN_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_HUMAN_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_HUMAN_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_HUMAN_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_HUMAN_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_HUMAN_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_HUMAN_WEREWOLF,
            },
            CommonAge.TODDLER: {
                CommonOccultType.NON_OCCULT: CommonSimType.TODDLER_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.TODDLER_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.TODDLER_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.TODDLER_HUMAN_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.TODDLER_HUMAN_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.TODDLER_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.TODDLER_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.TODDLER_HUMAN_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.TODDLER_HUMAN_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.TODDLER_HUMAN_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.TODDLER_HUMAN_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.TODDLER_HUMAN_WEREWOLF,
            },
            CommonAge.INFANT: {
                CommonOccultType.NON_OCCULT: CommonSimType.INFANT_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.INFANT_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.INFANT_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.INFANT_HUMAN_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.INFANT_HUMAN_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.INFANT_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.INFANT_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.INFANT_HUMAN_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.INFANT_HUMAN_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.INFANT_HUMAN_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.INFANT_HUMAN_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.INFANT_HUMAN_WEREWOLF,
            },
            CommonAge.BABY: {
                CommonOccultType.NON_OCCULT: CommonSimType.BABY_HUMAN,
                CommonOccultType.VAMPIRE: CommonSimType.BABY_HUMAN_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.BABY_HUMAN_GHOST,
                CommonOccultType.ALIEN: CommonSimType.BABY_HUMAN_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.BABY_HUMAN_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.BABY_HUMAN_MERMAID,
                CommonOccultType.WITCH: CommonSimType.BABY_HUMAN_WITCH,
                CommonOccultType.ROBOT: CommonSimType.BABY_HUMAN_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.BABY_HUMAN_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.BABY_HUMAN_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.BABY_HUMAN_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.BABY_HUMAN_WEREWOLF,
            }
        },
        CommonSpecies.SMALL_DOG: {
            CommonAge.ELDER: {
                CommonOccultType.NON_OCCULT: CommonSimType.ELDER_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ELDER_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ELDER_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ELDER_SMALL_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ELDER_SMALL_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ELDER_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ELDER_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ELDER_SMALL_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ELDER_SMALL_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ELDER_SMALL_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ELDER_SMALL_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ELDER_SMALL_DOG_WEREWOLF,
            },
            CommonAge.ADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_SMALL_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_SMALL_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_SMALL_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_SMALL_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_SMALL_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_SMALL_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_SMALL_DOG_WEREWOLF,
            },
            CommonAge.YOUNGADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_SMALL_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_SMALL_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_SMALL_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_SMALL_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_SMALL_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_SMALL_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_SMALL_DOG_WEREWOLF,
            },
            CommonAge.TEEN: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_SMALL_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_SMALL_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_SMALL_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_SMALL_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_SMALL_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_SMALL_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_SMALL_DOG_WEREWOLF,
            },
            CommonAge.CHILD: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_SMALL_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_SMALL_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_SMALL_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_SMALL_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_SMALL_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_SMALL_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_SMALL_DOG_WEREWOLF,
            },
            CommonAge.TODDLER: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_SMALL_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_SMALL_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_SMALL_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_SMALL_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_SMALL_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_SMALL_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_SMALL_DOG_WEREWOLF,
            },
            CommonAge.INFANT: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_SMALL_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_SMALL_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_SMALL_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_SMALL_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_SMALL_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_SMALL_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_SMALL_DOG_WEREWOLF,
            },
            CommonAge.BABY: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_SMALL_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_SMALL_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_SMALL_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_SMALL_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_SMALL_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_SMALL_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_SMALL_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_SMALL_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_SMALL_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_SMALL_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_SMALL_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_SMALL_DOG_WEREWOLF,
            }
        },
        CommonSpecies.LARGE_DOG: {
            CommonAge.ELDER: {
                CommonOccultType.NON_OCCULT: CommonSimType.ELDER_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ELDER_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ELDER_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ELDER_LARGE_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ELDER_LARGE_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ELDER_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ELDER_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ELDER_LARGE_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ELDER_LARGE_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ELDER_LARGE_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ELDER_LARGE_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ELDER_LARGE_DOG_WEREWOLF,
            },
            CommonAge.ADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_LARGE_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_LARGE_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_LARGE_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_LARGE_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_LARGE_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_LARGE_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_LARGE_DOG_WEREWOLF,
            },
            CommonAge.YOUNGADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_LARGE_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_LARGE_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_LARGE_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_LARGE_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_LARGE_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_LARGE_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_LARGE_DOG_WEREWOLF,
            },
            CommonAge.TEEN: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_LARGE_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_LARGE_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_LARGE_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_LARGE_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_LARGE_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_LARGE_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_LARGE_DOG_WEREWOLF,
            },
            CommonAge.CHILD: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_LARGE_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_LARGE_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_LARGE_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_LARGE_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_LARGE_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_LARGE_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_LARGE_DOG_WEREWOLF,
            },
            CommonAge.TODDLER: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_LARGE_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_LARGE_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_LARGE_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_LARGE_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_LARGE_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_LARGE_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_LARGE_DOG_WEREWOLF,
            },
            CommonAge.INFANT: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_LARGE_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_LARGE_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_LARGE_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_LARGE_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_LARGE_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_LARGE_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_LARGE_DOG_WEREWOLF,
            },
            CommonAge.BABY: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_LARGE_DOG,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_LARGE_DOG_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_LARGE_DOG_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_LARGE_DOG_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_LARGE_DOG_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_LARGE_DOG_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_LARGE_DOG_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_LARGE_DOG_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_LARGE_DOG_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_LARGE_DOG_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_LARGE_DOG_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_LARGE_DOG_WEREWOLF,
            }
        },
        CommonSpecies.CAT: {
            CommonAge.ELDER: {
                CommonOccultType.NON_OCCULT: CommonSimType.ELDER_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.ELDER_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ELDER_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ELDER_CAT_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ELDER_CAT_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ELDER_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ELDER_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ELDER_CAT_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ELDER_CAT_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ELDER_CAT_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ELDER_CAT_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ELDER_CAT_WEREWOLF,
            },
            CommonAge.ADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_CAT_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_CAT_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_CAT_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_CAT_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_CAT_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_CAT_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_CAT_WEREWOLF,
            },
            CommonAge.YOUNGADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_CAT_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_CAT_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_CAT_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_CAT_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_CAT_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_CAT_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_CAT_WEREWOLF,
            },
            CommonAge.TEEN: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_CAT_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_CAT_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_CAT_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_CAT_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_CAT_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_CAT_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_CAT_WEREWOLF,
            },
            CommonAge.CHILD: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_CAT_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_CAT_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_CAT_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_CAT_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_CAT_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_CAT_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_CAT_WEREWOLF,
            },
            CommonAge.TODDLER: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_CAT_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_CAT_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_CAT_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_CAT_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_CAT_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_CAT_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_CAT_WEREWOLF,
            },
            CommonAge.INFANT: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_CAT_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_CAT_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_CAT_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_CAT_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_CAT_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_CAT_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_CAT_WEREWOLF,
            },
            CommonAge.BABY: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_CAT,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_CAT_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_CAT_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_CAT_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_CAT_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_CAT_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_CAT_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_CAT_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_CAT_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_CAT_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_CAT_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_CAT_WEREWOLF,
            }
        },
        CommonSpecies.FOX: {
            CommonAge.ELDER: {
                CommonOccultType.NON_OCCULT: CommonSimType.ELDER_FOX,
                CommonOccultType.VAMPIRE: CommonSimType.ELDER_FOX_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ELDER_FOX_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ELDER_FOX_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ELDER_FOX_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ELDER_FOX_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ELDER_FOX_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ELDER_FOX_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ELDER_FOX_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ELDER_FOX_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ELDER_FOX_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ELDER_FOX_WEREWOLF,
            },
            CommonAge.ADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_FOX,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_FOX_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_FOX_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_FOX_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_FOX_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_FOX_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_FOX_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_FOX_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_FOX_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_FOX_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_FOX_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_FOX_WEREWOLF,
            },
            CommonAge.YOUNGADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_FOX,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_FOX_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_FOX_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_FOX_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_FOX_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_FOX_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_FOX_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_FOX_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_FOX_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_FOX_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_FOX_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_FOX_WEREWOLF,
            },
            CommonAge.TEEN: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_FOX,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_FOX_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_FOX_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_FOX_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_FOX_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_FOX_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_FOX_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_FOX_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_FOX_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_FOX_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_FOX_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_FOX_WEREWOLF,
            },
            CommonAge.CHILD: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_FOX,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_FOX_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_FOX_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_FOX_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_FOX_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_FOX_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_FOX_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_FOX_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_FOX_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_FOX_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_FOX_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_FOX_WEREWOLF,
            },
            CommonAge.TODDLER: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_FOX,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_FOX_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_FOX_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_FOX_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_FOX_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_FOX_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_FOX_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_FOX_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_FOX_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_FOX_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_FOX_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_FOX_WEREWOLF,
            },
            CommonAge.INFANT: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_FOX,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_FOX_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_FOX_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_FOX_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_FOX_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_FOX_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_FOX_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_FOX_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_FOX_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_FOX_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_FOX_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_FOX_WEREWOLF,
            },
            CommonAge.BABY: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_FOX,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_FOX_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_FOX_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_FOX_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_FOX_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_FOX_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_FOX_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_FOX_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_FOX_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_FOX_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_FOX_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_FOX_WEREWOLF,
            }
        },
        CommonSpecies.HORSE: {
            CommonAge.ELDER: {
                CommonOccultType.NON_OCCULT: CommonSimType.ELDER_HORSE,
                CommonOccultType.VAMPIRE: CommonSimType.ELDER_HORSE_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ELDER_HORSE_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ELDER_HORSE_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ELDER_HORSE_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ELDER_HORSE_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ELDER_HORSE_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ELDER_HORSE_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ELDER_HORSE_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ELDER_HORSE_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ELDER_HORSE_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ELDER_HORSE_WEREWOLF,
            },
            CommonAge.ADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_HORSE,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_HORSE_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_HORSE_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_HORSE_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_HORSE_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_HORSE_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_HORSE_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_HORSE_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_HORSE_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_HORSE_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_HORSE_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_HORSE_WEREWOLF,
            },
            CommonAge.YOUNGADULT: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_HORSE,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_HORSE_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_HORSE_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_HORSE_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_HORSE_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_HORSE_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_HORSE_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_HORSE_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_HORSE_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_HORSE_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_HORSE_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_HORSE_WEREWOLF,
            },
            CommonAge.TEEN: {
                CommonOccultType.NON_OCCULT: CommonSimType.ADULT_HORSE,
                CommonOccultType.VAMPIRE: CommonSimType.ADULT_HORSE_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.ADULT_HORSE_GHOST,
                CommonOccultType.ALIEN: CommonSimType.ADULT_HORSE_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.ADULT_HORSE_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.ADULT_HORSE_MERMAID,
                CommonOccultType.WITCH: CommonSimType.ADULT_HORSE_WITCH,
                CommonOccultType.ROBOT: CommonSimType.ADULT_HORSE_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.ADULT_HORSE_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.ADULT_HORSE_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.ADULT_HORSE_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.ADULT_HORSE_WEREWOLF,
            },
            CommonAge.CHILD: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_HORSE,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_HORSE_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_HORSE_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_HORSE_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_HORSE_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_HORSE_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_HORSE_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_HORSE_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_HORSE_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_HORSE_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_HORSE_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_HORSE_WEREWOLF,
            },
            CommonAge.TODDLER: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_HORSE,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_HORSE_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_HORSE_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_HORSE_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_HORSE_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_HORSE_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_HORSE_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_HORSE_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_HORSE_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_HORSE_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_HORSE_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_HORSE_WEREWOLF,
            },
            CommonAge.INFANT: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_HORSE,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_HORSE_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_HORSE_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_HORSE_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_HORSE_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_HORSE_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_HORSE_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_HORSE_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_HORSE_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_HORSE_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_HORSE_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_HORSE_WEREWOLF,
            },
            CommonAge.BABY: {
                CommonOccultType.NON_OCCULT: CommonSimType.CHILD_HORSE,
                CommonOccultType.VAMPIRE: CommonSimType.CHILD_HORSE_VAMPIRE,
                CommonOccultType.GHOST: CommonSimType.CHILD_HORSE_GHOST,
                CommonOccultType.ALIEN: CommonSimType.CHILD_HORSE_ALIEN,
                CommonOccultType.FAIRY: CommonSimType.CHILD_HORSE_FAIRY,
                CommonOccultType.MERMAID: CommonSimType.CHILD_HORSE_MERMAID,
                CommonOccultType.WITCH: CommonSimType.CHILD_HORSE_WITCH,
                CommonOccultType.ROBOT: CommonSimType.CHILD_HORSE_ROBOT,
                CommonOccultType.SCARECROW: CommonSimType.CHILD_HORSE_SCARECROW,
                CommonOccultType.SKELETON: CommonSimType.CHILD_HORSE_SKELETON,
                CommonOccultType.PLANT_SIM: CommonSimType.CHILD_HORSE_PLANT_SIM,
                CommonOccultType.WEREWOLF: CommonSimType.CHILD_HORSE_WEREWOLF,
            }
        }
    }
    _SIM_TYPE_TO_SIGNATURE_MAPPING: Dict[CommonSimType, str] = {
        # Human
        # Elder
        CommonSimType.ELDER_HUMAN: 'ElHu',
        CommonSimType.ELDER_HUMAN_VAMPIRE: 'ElHuVa',
        CommonSimType.ELDER_HUMAN_GHOST: 'ElHuGh',
        CommonSimType.ELDER_HUMAN_ALIEN: 'ElHuAl',
        CommonSimType.ELDER_HUMAN_MERMAID: 'ElHuMer',
        CommonSimType.ELDER_HUMAN_WITCH: 'ElHuWi',
        CommonSimType.ELDER_HUMAN_ROBOT: 'ElHuRo',
        CommonSimType.ELDER_HUMAN_SCARECROW: 'ElHuScrw',
        CommonSimType.ELDER_HUMAN_SKELETON: 'ElHuSk',
        CommonSimType.ELDER_HUMAN_PLANT_SIM: 'ElHuPls',
        CommonSimType.ELDER_HUMAN_WEREWOLF: 'ElHuWerWlf',
        CommonSimType.ELDER_HUMAN_FAIRY: 'ElHuFry',
        # Adult
        CommonSimType.ADULT_HUMAN: 'AdHu',
        CommonSimType.ADULT_HUMAN_VAMPIRE: 'AdHuVa',
        CommonSimType.ADULT_HUMAN_GHOST: 'AdHuGh',
        CommonSimType.ADULT_HUMAN_ALIEN: 'AdHuAl',
        CommonSimType.ADULT_HUMAN_MERMAID: 'AdHuMer',
        CommonSimType.ADULT_HUMAN_WITCH: 'AdHuWi',
        CommonSimType.ADULT_HUMAN_ROBOT: 'AdHuRo',
        CommonSimType.ADULT_HUMAN_SCARECROW: 'AdHuScrw',
        CommonSimType.ADULT_HUMAN_SKELETON: 'AdHuSk',
        CommonSimType.ADULT_HUMAN_PLANT_SIM: 'AdHuPls',
        CommonSimType.ADULT_HUMAN_WEREWOLF: 'AdHuWerWlf',
        CommonSimType.ADULT_HUMAN_FAIRY: 'AdHuFry',
        # Young Adult
        CommonSimType.YOUNG_ADULT_HUMAN: 'YadHu',
        CommonSimType.YOUNG_ADULT_HUMAN_VAMPIRE: 'YadHuVa',
        CommonSimType.YOUNG_ADULT_HUMAN_GHOST: 'YadHuGh',
        CommonSimType.YOUNG_ADULT_HUMAN_ALIEN: 'YadHuAl',
        CommonSimType.YOUNG_ADULT_HUMAN_MERMAID: 'YadHuMer',
        CommonSimType.YOUNG_ADULT_HUMAN_WITCH: 'YadHuWi',
        CommonSimType.YOUNG_ADULT_HUMAN_ROBOT: 'YadHuRo',
        CommonSimType.YOUNG_ADULT_HUMAN_SCARECROW: 'YadHuScrw',
        CommonSimType.YOUNG_ADULT_HUMAN_SKELETON: 'YadHuSk',
        CommonSimType.YOUNG_ADULT_HUMAN_PLANT_SIM: 'YadHuPls',
        CommonSimType.YOUNG_ADULT_HUMAN_WEREWOLF: 'YadHuWerWlf',
        CommonSimType.YOUNG_ADULT_HUMAN_FAIRY: 'YadHuFry',
        # Teen
        CommonSimType.TEEN_HUMAN: 'TnHu',
        CommonSimType.TEEN_HUMAN_VAMPIRE: 'TnHuVa',
        CommonSimType.TEEN_HUMAN_GHOST: 'TnHuGh',
        CommonSimType.TEEN_HUMAN_ALIEN: 'TnHuAl',
        CommonSimType.TEEN_HUMAN_MERMAID: 'TnHuMer',
        CommonSimType.TEEN_HUMAN_WITCH: 'TnHuWi',
        CommonSimType.TEEN_HUMAN_ROBOT: 'TnHuRo',
        CommonSimType.TEEN_HUMAN_SCARECROW: 'TnHuScrw',
        CommonSimType.TEEN_HUMAN_SKELETON: 'TnHuSk',
        CommonSimType.TEEN_HUMAN_PLANT_SIM: 'TnHuPls',
        CommonSimType.TEEN_HUMAN_WEREWOLF: 'TnHuWerWlf',
        CommonSimType.TEEN_HUMAN_FAIRY: 'TnHuFry',
        # Child
        CommonSimType.CHILD_HUMAN: 'ChldHu',
        CommonSimType.CHILD_HUMAN_VAMPIRE: 'ChldHuVa',
        CommonSimType.CHILD_HUMAN_GHOST: 'ChldHuGh',
        CommonSimType.CHILD_HUMAN_ALIEN: 'ChldHuAl',
        CommonSimType.CHILD_HUMAN_MERMAID: 'ChldHuMer',
        CommonSimType.CHILD_HUMAN_WITCH: 'ChldHuWi',
        CommonSimType.CHILD_HUMAN_ROBOT: 'ChldHuRo',
        CommonSimType.CHILD_HUMAN_SCARECROW: 'ChldHuScrw',
        CommonSimType.CHILD_HUMAN_SKELETON: 'ChldHuSk',
        CommonSimType.CHILD_HUMAN_PLANT_SIM: 'ChldHuPls',
        CommonSimType.CHILD_HUMAN_WEREWOLF: 'ChldHuWerWlf',
        CommonSimType.CHILD_HUMAN_FAIRY: 'ChldHuFry',
        # Toddler
        CommonSimType.TODDLER_HUMAN: 'TdlrHu',
        CommonSimType.TODDLER_HUMAN_VAMPIRE: 'TdlrHuVa',
        CommonSimType.TODDLER_HUMAN_GHOST: 'TdlrHuGh',
        CommonSimType.TODDLER_HUMAN_ALIEN: 'TdlrHuAl',
        CommonSimType.TODDLER_HUMAN_MERMAID: 'TdlrHuMer',
        CommonSimType.TODDLER_HUMAN_WITCH: 'TdlrHuWi',
        CommonSimType.TODDLER_HUMAN_ROBOT: 'TdlrHuRo',
        CommonSimType.TODDLER_HUMAN_SCARECROW: 'TdlrHuScrw',
        CommonSimType.TODDLER_HUMAN_SKELETON: 'TdlrHuSk',
        CommonSimType.TODDLER_HUMAN_PLANT_SIM: 'TdlrHuPls',
        CommonSimType.TODDLER_HUMAN_WEREWOLF: 'TdlrHuWerWlf',
        CommonSimType.TODDLER_HUMAN_FAIRY: 'TdlrHuFry',
        # Infant
        CommonSimType.INFANT_HUMAN: 'InfntHu',
        CommonSimType.INFANT_HUMAN_VAMPIRE: 'InfntHuVa',
        CommonSimType.INFANT_HUMAN_GHOST: 'InfntHuGh',
        CommonSimType.INFANT_HUMAN_ALIEN: 'InfntHuAl',
        CommonSimType.INFANT_HUMAN_MERMAID: 'InfntHuMer',
        CommonSimType.INFANT_HUMAN_WITCH: 'InfntHuWi',
        CommonSimType.INFANT_HUMAN_ROBOT: 'InfntHuRo',
        CommonSimType.INFANT_HUMAN_SCARECROW: 'InfntHuScrw',
        CommonSimType.INFANT_HUMAN_SKELETON: 'InfntHuSk',
        CommonSimType.INFANT_HUMAN_PLANT_SIM: 'InfntHuPls',
        CommonSimType.INFANT_HUMAN_WEREWOLF: 'InfntHuWerWlf',
        CommonSimType.INFANT_HUMAN_FAIRY: 'InfntHuFry',
        # Baby
        CommonSimType.BABY_HUMAN: 'BbyHu',
        CommonSimType.BABY_HUMAN_VAMPIRE: 'BbyHuVa',
        CommonSimType.BABY_HUMAN_GHOST: 'BbyHuGh',
        CommonSimType.BABY_HUMAN_ALIEN: 'BbyHuAl',
        CommonSimType.BABY_HUMAN_MERMAID: 'BbyHuMer',
        CommonSimType.BABY_HUMAN_WITCH: 'BbyHuWi',
        CommonSimType.BABY_HUMAN_ROBOT: 'BbyHuRo',
        CommonSimType.BABY_HUMAN_SCARECROW: 'BbyHuScrw',
        CommonSimType.BABY_HUMAN_SKELETON: 'BbyHuSk',
        CommonSimType.BABY_HUMAN_PLANT_SIM: 'BbyHuPls',
        CommonSimType.BABY_HUMAN_WEREWOLF: 'BbyHuWerWlf',
        CommonSimType.BABY_HUMAN_FAIRY: 'BbyHuFry',

        # Child Dog
        CommonSimType.CHILD_DOG: 'ChldDg',
        CommonSimType.CHILD_DOG_VAMPIRE: 'ChldDgVa',
        CommonSimType.CHILD_DOG_GHOST: 'ChldDgGh',
        CommonSimType.CHILD_DOG_ALIEN: 'ChldDgAl',
        CommonSimType.CHILD_DOG_MERMAID: 'ChldDgMer',
        CommonSimType.CHILD_DOG_WITCH: 'ChldDgWi',
        CommonSimType.CHILD_DOG_ROBOT: 'ChldDgRo',
        CommonSimType.CHILD_DOG_SCARECROW: 'ChldDgScrw',
        CommonSimType.CHILD_DOG_SKELETON: 'ChldDgSk',
        CommonSimType.CHILD_DOG_PLANT_SIM: 'ChldDgPls',
        CommonSimType.CHILD_DOG_WEREWOLF: 'ChldDgWerWlf',
        CommonSimType.CHILD_DOG_FAIRY: 'ChldDgFry',

        # Small Dog
        # Elder
        CommonSimType.ELDER_SMALL_DOG: 'ElSd',
        CommonSimType.ELDER_SMALL_DOG_VAMPIRE: 'ElSdVa',
        CommonSimType.ELDER_SMALL_DOG_GHOST: 'ElSdGh',
        CommonSimType.ELDER_SMALL_DOG_ALIEN: 'ElSdAl',
        CommonSimType.ELDER_SMALL_DOG_MERMAID: 'ElSdMer',
        CommonSimType.ELDER_SMALL_DOG_WITCH: 'ElSdWi',
        CommonSimType.ELDER_SMALL_DOG_ROBOT: 'ElSdRo',
        CommonSimType.ELDER_SMALL_DOG_SCARECROW: 'ElSdScrw',
        CommonSimType.ELDER_SMALL_DOG_SKELETON: 'ElSdSk',
        CommonSimType.ELDER_SMALL_DOG_PLANT_SIM: 'ElSdPls',
        CommonSimType.ELDER_SMALL_DOG_WEREWOLF: 'ElSdWerWlf',
        CommonSimType.ELDER_SMALL_DOG_FAIRY: 'ElSdFry',
        # Adult
        CommonSimType.ADULT_SMALL_DOG: 'AdSd',
        CommonSimType.ADULT_SMALL_DOG_VAMPIRE: 'AdSdVa',
        CommonSimType.ADULT_SMALL_DOG_GHOST: 'AdSdGh',
        CommonSimType.ADULT_SMALL_DOG_ALIEN: 'AdSdAl',
        CommonSimType.ADULT_SMALL_DOG_MERMAID: 'AdSdMer',
        CommonSimType.ADULT_SMALL_DOG_WITCH: 'AdSdWi',
        CommonSimType.ADULT_SMALL_DOG_ROBOT: 'AdSdRo',
        CommonSimType.ADULT_SMALL_DOG_SCARECROW: 'AdSdScrw',
        CommonSimType.ADULT_SMALL_DOG_SKELETON: 'AdSdSk',
        CommonSimType.ADULT_SMALL_DOG_PLANT_SIM: 'AdSdPls',
        CommonSimType.ADULT_SMALL_DOG_WEREWOLF: 'AdSdWerWlf',
        CommonSimType.ADULT_SMALL_DOG_FAIRY: 'AdSdFry',
        # Child
        CommonSimType.CHILD_SMALL_DOG: 'ChldSd',
        CommonSimType.CHILD_SMALL_DOG_VAMPIRE: 'ChldSdVa',
        CommonSimType.CHILD_SMALL_DOG_GHOST: 'ChldSdGh',
        CommonSimType.CHILD_SMALL_DOG_ALIEN: 'ChldSdAl',
        CommonSimType.CHILD_SMALL_DOG_MERMAID: 'ChldSdMer',
        CommonSimType.CHILD_SMALL_DOG_WITCH: 'ChldSdWi',
        CommonSimType.CHILD_SMALL_DOG_ROBOT: 'ChldSdRo',
        CommonSimType.CHILD_SMALL_DOG_SCARECROW: 'ChldSdScrw',
        CommonSimType.CHILD_SMALL_DOG_SKELETON: 'ChldSdSk',
        CommonSimType.CHILD_SMALL_DOG_PLANT_SIM: 'ChldSdPls',
        CommonSimType.CHILD_SMALL_DOG_WEREWOLF: 'ChldSdWerWlf',
        CommonSimType.CHILD_SMALL_DOG_FAIRY: 'ChldSdFry',

        # Large Dog
        # Elder
        CommonSimType.ELDER_LARGE_DOG: 'ElLd',
        CommonSimType.ELDER_LARGE_DOG_VAMPIRE: 'ElLdVa',
        CommonSimType.ELDER_LARGE_DOG_GHOST: 'ElLdGh',
        CommonSimType.ELDER_LARGE_DOG_ALIEN: 'ElLdAl',
        CommonSimType.ELDER_LARGE_DOG_MERMAID: 'ElLdMer',
        CommonSimType.ELDER_LARGE_DOG_WITCH: 'ElLdWi',
        CommonSimType.ELDER_LARGE_DOG_ROBOT: 'ElLdRo',
        CommonSimType.ELDER_LARGE_DOG_SCARECROW: 'ElLdScrw',
        CommonSimType.ELDER_LARGE_DOG_SKELETON: 'ElLdSk',
        CommonSimType.ELDER_LARGE_DOG_PLANT_SIM: 'ElLdPls',
        CommonSimType.ELDER_LARGE_DOG_WEREWOLF: 'ElLdWerWlf',
        CommonSimType.ELDER_LARGE_DOG_FAIRY: 'ElLdFry',
        # Adult
        CommonSimType.ADULT_LARGE_DOG: 'AdLd',
        CommonSimType.ADULT_LARGE_DOG_VAMPIRE: 'AdLdVa',
        CommonSimType.ADULT_LARGE_DOG_GHOST: 'AdLdGh',
        CommonSimType.ADULT_LARGE_DOG_ALIEN: 'AdLdAl',
        CommonSimType.ADULT_LARGE_DOG_MERMAID: 'AdLdMer',
        CommonSimType.ADULT_LARGE_DOG_WITCH: 'AdLdWi',
        CommonSimType.ADULT_LARGE_DOG_ROBOT: 'AdLdRo',
        CommonSimType.ADULT_LARGE_DOG_SCARECROW: 'AdLdScrw',
        CommonSimType.ADULT_LARGE_DOG_SKELETON: 'AdLdSk',
        CommonSimType.ADULT_LARGE_DOG_PLANT_SIM: 'AdLdPls',
        CommonSimType.ADULT_LARGE_DOG_WEREWOLF: 'AdLdWerWlf',
        CommonSimType.ADULT_LARGE_DOG_FAIRY: 'AdLdFry',
        # Child
        CommonSimType.CHILD_LARGE_DOG: 'ChldLd',
        CommonSimType.CHILD_LARGE_DOG_VAMPIRE: 'ChldLdVa',
        CommonSimType.CHILD_LARGE_DOG_GHOST: 'ChldLdGh',
        CommonSimType.CHILD_LARGE_DOG_ALIEN: 'ChldLdAl',
        CommonSimType.CHILD_LARGE_DOG_MERMAID: 'ChldLdMer',
        CommonSimType.CHILD_LARGE_DOG_WITCH: 'ChldLdWi',
        CommonSimType.CHILD_LARGE_DOG_ROBOT: 'ChldLdRo',
        CommonSimType.CHILD_LARGE_DOG_SCARECROW: 'ChldLdScrw',
        CommonSimType.CHILD_LARGE_DOG_SKELETON: 'ChldLdSk',
        CommonSimType.CHILD_LARGE_DOG_PLANT_SIM: 'ChldLdPls',
        CommonSimType.CHILD_LARGE_DOG_WEREWOLF: 'ChldLdWerWlf',
        CommonSimType.CHILD_LARGE_DOG_FAIRY: 'ChldLdFry',

        # Cat
        # Elder
        CommonSimType.ELDER_CAT: 'ElCat',
        CommonSimType.ELDER_CAT_VAMPIRE: 'ElCatVa',
        CommonSimType.ELDER_CAT_GHOST: 'ElCatGh',
        CommonSimType.ELDER_CAT_ALIEN: 'ElCatAl',
        CommonSimType.ELDER_CAT_MERMAID: 'ElCatMer',
        CommonSimType.ELDER_CAT_WITCH: 'ElCatWi',
        CommonSimType.ELDER_CAT_ROBOT: 'ElCatRo',
        CommonSimType.ELDER_CAT_SCARECROW: 'ElCatScrw',
        CommonSimType.ELDER_CAT_SKELETON: 'ElCatSk',
        CommonSimType.ELDER_CAT_PLANT_SIM: 'ElCatPls',
        CommonSimType.ELDER_CAT_WEREWOLF: 'ElCatWerWlf',
        CommonSimType.ELDER_CAT_FAIRY: 'ElCatFry',
        # Adult
        CommonSimType.ADULT_CAT: 'AdCat',
        CommonSimType.ADULT_CAT_VAMPIRE: 'AdCatVa',
        CommonSimType.ADULT_CAT_GHOST: 'AdCatGh',
        CommonSimType.ADULT_CAT_ALIEN: 'AdCatAl',
        CommonSimType.ADULT_CAT_MERMAID: 'AdCatMer',
        CommonSimType.ADULT_CAT_WITCH: 'AdCatWi',
        CommonSimType.ADULT_CAT_ROBOT: 'AdCatRo',
        CommonSimType.ADULT_CAT_SCARECROW: 'AdCatScrw',
        CommonSimType.ADULT_CAT_SKELETON: 'AdCatSk',
        CommonSimType.ADULT_CAT_PLANT_SIM: 'AdCatPls',
        CommonSimType.ADULT_CAT_WEREWOLF: 'AdCatWerWlf',
        CommonSimType.ADULT_CAT_FAIRY: 'AdCatFry',
        # Child
        CommonSimType.CHILD_CAT: 'ChldCat',
        CommonSimType.CHILD_CAT_VAMPIRE: 'ChldCatVa',
        CommonSimType.CHILD_CAT_GHOST: 'ChldCatGh',
        CommonSimType.CHILD_CAT_ALIEN: 'ChldCatAl',
        CommonSimType.CHILD_CAT_MERMAID: 'ChldCatMer',
        CommonSimType.CHILD_CAT_WITCH: 'ChldCatWi',
        CommonSimType.CHILD_CAT_ROBOT: 'ChldCatRo',
        CommonSimType.CHILD_CAT_SCARECROW: 'ChldCatScrw',
        CommonSimType.CHILD_CAT_SKELETON: 'ChldCatSk',
        CommonSimType.CHILD_CAT_PLANT_SIM: 'ChldCatPls',
        CommonSimType.CHILD_CAT_WEREWOLF: 'ChldCatWerWlf',
        CommonSimType.CHILD_CAT_FAIRY: 'ChldCatFry',

        # Fox
        # Elder
        CommonSimType.ELDER_FOX: 'ElFox',
        CommonSimType.ELDER_FOX_VAMPIRE: 'ElFoxVa',
        CommonSimType.ELDER_FOX_GHOST: 'ElFoxGh',
        CommonSimType.ELDER_FOX_ALIEN: 'ElFoxAl',
        CommonSimType.ELDER_FOX_MERMAID: 'ElFoxMer',
        CommonSimType.ELDER_FOX_WITCH: 'ElFoxWi',
        CommonSimType.ELDER_FOX_ROBOT: 'ElFoxRo',
        CommonSimType.ELDER_FOX_SCARECROW: 'ElFoxScrw',
        CommonSimType.ELDER_FOX_SKELETON: 'ElFoxSk',
        CommonSimType.ELDER_FOX_PLANT_SIM: 'ElFoxPls',
        CommonSimType.ELDER_FOX_WEREWOLF: 'ElFoxWerWlf',
        CommonSimType.ELDER_FOX_FAIRY: 'ElFoxFry',
        # Adult
        CommonSimType.ADULT_FOX: 'AdFox',
        CommonSimType.ADULT_FOX_VAMPIRE: 'AdFoxVa',
        CommonSimType.ADULT_FOX_GHOST: 'AdFoxGh',
        CommonSimType.ADULT_FOX_ALIEN: 'AdFoxAl',
        CommonSimType.ADULT_FOX_MERMAID: 'AdFoxMer',
        CommonSimType.ADULT_FOX_WITCH: 'AdFoxWi',
        CommonSimType.ADULT_FOX_ROBOT: 'AdFoxRo',
        CommonSimType.ADULT_FOX_SCARECROW: 'AdFoxScrw',
        CommonSimType.ADULT_FOX_SKELETON: 'AdFoxSk',
        CommonSimType.ADULT_FOX_PLANT_SIM: 'AdFoxPls',
        CommonSimType.ADULT_FOX_WEREWOLF: 'AdFoxWerWlf',
        CommonSimType.ADULT_FOX_FAIRY: 'AdFoxFry',
        # Child
        CommonSimType.CHILD_FOX: 'ChldFox',
        CommonSimType.CHILD_FOX_VAMPIRE: 'ChldFoxVa',
        CommonSimType.CHILD_FOX_GHOST: 'ChldFoxGh',
        CommonSimType.CHILD_FOX_ALIEN: 'ChldFoxAl',
        CommonSimType.CHILD_FOX_MERMAID: 'ChldFoxMer',
        CommonSimType.CHILD_FOX_WITCH: 'ChldFoxWi',
        CommonSimType.CHILD_FOX_ROBOT: 'ChldFoxRo',
        CommonSimType.CHILD_FOX_SCARECROW: 'ChldFoxScrw',
        CommonSimType.CHILD_FOX_SKELETON: 'ChldFoxSk',
        CommonSimType.CHILD_FOX_PLANT_SIM: 'ChldFoxPls',
        CommonSimType.CHILD_FOX_WEREWOLF: 'ChldFoxWerWlf',
        CommonSimType.CHILD_FOX_FAIRY: 'ChldFoxFry',

        # Horse
        # Elder
        CommonSimType.ELDER_HORSE: 'ElHrs',
        CommonSimType.ELDER_HORSE_VAMPIRE: 'ElHrsVa',
        CommonSimType.ELDER_HORSE_GHOST: 'ElHrsGh',
        CommonSimType.ELDER_HORSE_ALIEN: 'ElHrsAl',
        CommonSimType.ELDER_HORSE_MERMAID: 'ElHrsMer',
        CommonSimType.ELDER_HORSE_WITCH: 'ElHrsWi',
        CommonSimType.ELDER_HORSE_ROBOT: 'ElHrsRo',
        CommonSimType.ELDER_HORSE_SCARECROW: 'ElHrsScrw',
        CommonSimType.ELDER_HORSE_SKELETON: 'ElHrsSk',
        CommonSimType.ELDER_HORSE_PLANT_SIM: 'ElHrsPls',
        CommonSimType.ELDER_HORSE_WEREWOLF: 'ElHrsWerWlf',
        CommonSimType.ELDER_HORSE_FAIRY: 'ElHrsFry',
        # Adult
        CommonSimType.ADULT_HORSE: 'AdHrs',
        CommonSimType.ADULT_HORSE_VAMPIRE: 'AdHrsVa',
        CommonSimType.ADULT_HORSE_GHOST: 'AdHrsGh',
        CommonSimType.ADULT_HORSE_ALIEN: 'AdHrsAl',
        CommonSimType.ADULT_HORSE_MERMAID: 'AdHrsMer',
        CommonSimType.ADULT_HORSE_WITCH: 'AdHrsWi',
        CommonSimType.ADULT_HORSE_ROBOT: 'AdHrsRo',
        CommonSimType.ADULT_HORSE_SCARECROW: 'AdHrsScrw',
        CommonSimType.ADULT_HORSE_SKELETON: 'AdHrsSk',
        CommonSimType.ADULT_HORSE_PLANT_SIM: 'AdHrsPls',
        CommonSimType.ADULT_HORSE_WEREWOLF: 'AdHrsWerWlf',
        CommonSimType.ADULT_HORSE_FAIRY: 'AdHrsFry',
        # Child
        CommonSimType.CHILD_HORSE: 'ChldHrs',
        CommonSimType.CHILD_HORSE_VAMPIRE: 'ChldHrsVa',
        CommonSimType.CHILD_HORSE_GHOST: 'ChldHrsGh',
        CommonSimType.CHILD_HORSE_ALIEN: 'ChldHrsAl',
        CommonSimType.CHILD_HORSE_MERMAID: 'ChldHrsMer',
        CommonSimType.CHILD_HORSE_WITCH: 'ChldHrsWi',
        CommonSimType.CHILD_HORSE_ROBOT: 'ChldHrsRo',
        CommonSimType.CHILD_HORSE_SCARECROW: 'ChldHrsScrw',
        CommonSimType.CHILD_HORSE_SKELETON: 'ChldHrsSk',
        CommonSimType.CHILD_HORSE_PLANT_SIM: 'ChldHrsPls',
        CommonSimType.CHILD_HORSE_WEREWOLF: 'ChldHrsWerWlf',
        CommonSimType.CHILD_HORSE_FAIRY: 'ChldHrsFry',
    }

    _OCCULT_SIM_TYPE_TO_NON_OCCULT_SIM_TYPE_MAPPING: Dict[CommonSimType, CommonSimType] = {
        # Human
        # Elder
        CommonSimType.ELDER_HUMAN: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_VAMPIRE: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_GHOST: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_ALIEN: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_MERMAID: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_WITCH: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_ROBOT: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_SCARECROW: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_SKELETON: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_PLANT_SIM: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_WEREWOLF: CommonSimType.ELDER_HUMAN,
        CommonSimType.ELDER_HUMAN_FAIRY: CommonSimType.ELDER_HUMAN,
        # Adult
        CommonSimType.ADULT_HUMAN: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_VAMPIRE: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_GHOST: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_ALIEN: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_MERMAID: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_WITCH: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_ROBOT: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_SCARECROW: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_SKELETON: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_PLANT_SIM: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_WEREWOLF: CommonSimType.ADULT_HUMAN,
        CommonSimType.ADULT_HUMAN_FAIRY: CommonSimType.ADULT_HUMAN,
        # Young Adult
        CommonSimType.YOUNG_ADULT_HUMAN: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_VAMPIRE: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_GHOST: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_ALIEN: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_MERMAID: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_WITCH: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_ROBOT: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_SCARECROW: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_SKELETON: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_PLANT_SIM: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_WEREWOLF: CommonSimType.YOUNG_ADULT_HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_FAIRY: CommonSimType.YOUNG_ADULT_HUMAN,
        # Teen
        CommonSimType.TEEN_HUMAN: CommonSimType.TEEN_HUMAN,
        CommonSimType.TEEN_HUMAN_VAMPIRE: CommonSimType.TEEN_HUMAN,
        CommonSimType.TEEN_HUMAN_GHOST: CommonSimType.TEEN_HUMAN,
        CommonSimType.TEEN_HUMAN_ALIEN: CommonSimType.TEEN_HUMAN,
        CommonSimType.TEEN_HUMAN_MERMAID: CommonSimType.TEEN_HUMAN,
        CommonSimType.TEEN_HUMAN_WITCH: CommonSimType.TEEN_HUMAN,
        CommonSimType.TEEN_HUMAN_ROBOT: CommonSimType.TEEN_HUMAN,
        CommonSimType.TEEN_HUMAN_SCARECROW: CommonSimType.TEEN_HUMAN,
        CommonSimType.TEEN_HUMAN_SKELETON: CommonSimType.TEEN_HUMAN,
        CommonSimType.TEEN_HUMAN_PLANT_SIM: CommonSimType.TEEN_HUMAN,
        CommonSimType.TEEN_HUMAN_WEREWOLF: CommonSimType.TEEN_HUMAN,
        CommonSimType.TEEN_HUMAN_FAIRY: CommonSimType.TEEN_HUMAN,
        # Child
        CommonSimType.CHILD_HUMAN: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_VAMPIRE: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_GHOST: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_ALIEN: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_MERMAID: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_WITCH: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_ROBOT: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_SCARECROW: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_SKELETON: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_PLANT_SIM: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_WEREWOLF: CommonSimType.CHILD_HUMAN,
        CommonSimType.CHILD_HUMAN_FAIRY: CommonSimType.CHILD_HUMAN,
        # Toddler
        CommonSimType.TODDLER_HUMAN: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_VAMPIRE: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_GHOST: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_ALIEN: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_MERMAID: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_WITCH: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_ROBOT: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_SCARECROW: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_SKELETON: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_PLANT_SIM: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_WEREWOLF: CommonSimType.TODDLER_HUMAN,
        CommonSimType.TODDLER_HUMAN_FAIRY: CommonSimType.TODDLER_HUMAN,
        # Infant
        CommonSimType.INFANT_HUMAN: CommonSimType.INFANT_HUMAN,
        CommonSimType.INFANT_HUMAN_VAMPIRE: CommonSimType.INFANT_HUMAN,
        CommonSimType.INFANT_HUMAN_GHOST: CommonSimType.INFANT_HUMAN,
        CommonSimType.INFANT_HUMAN_ALIEN: CommonSimType.INFANT_HUMAN,
        CommonSimType.INFANT_HUMAN_MERMAID: CommonSimType.INFANT_HUMAN,
        CommonSimType.INFANT_HUMAN_WITCH: CommonSimType.INFANT_HUMAN,
        CommonSimType.INFANT_HUMAN_ROBOT: CommonSimType.INFANT_HUMAN,
        CommonSimType.INFANT_HUMAN_SCARECROW: CommonSimType.INFANT_HUMAN,
        CommonSimType.INFANT_HUMAN_SKELETON: CommonSimType.INFANT_HUMAN,
        CommonSimType.INFANT_HUMAN_PLANT_SIM: CommonSimType.INFANT_HUMAN,
        CommonSimType.INFANT_HUMAN_WEREWOLF: CommonSimType.INFANT_HUMAN,
        CommonSimType.INFANT_HUMAN_FAIRY: CommonSimType.INFANT_HUMAN,

        # Baby
        CommonSimType.BABY_HUMAN: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_VAMPIRE: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_GHOST: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_ALIEN: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_MERMAID: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_WITCH: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_ROBOT: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_SCARECROW: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_SKELETON: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_PLANT_SIM: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_WEREWOLF: CommonSimType.BABY_HUMAN,
        CommonSimType.BABY_HUMAN_FAIRY: CommonSimType.BABY_HUMAN,

        # Dog
        # Child
        CommonSimType.CHILD_DOG: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_VAMPIRE: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_GHOST: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_ALIEN: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_MERMAID: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_WITCH: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_ROBOT: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_SCARECROW: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_SKELETON: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_PLANT_SIM: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_WEREWOLF: CommonSimType.CHILD_DOG,
        CommonSimType.CHILD_DOG_FAIRY: CommonSimType.CHILD_DOG,

        # Small Dog
        # Elder
        CommonSimType.ELDER_SMALL_DOG: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_VAMPIRE: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_GHOST: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_ALIEN: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_MERMAID: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_WITCH: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_ROBOT: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_SCARECROW: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_SKELETON: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_PLANT_SIM: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_WEREWOLF: CommonSimType.ELDER_SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_FAIRY: CommonSimType.ELDER_SMALL_DOG,
        # Adult
        CommonSimType.ADULT_SMALL_DOG: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_VAMPIRE: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_GHOST: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_ALIEN: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_MERMAID: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_WITCH: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_ROBOT: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_SCARECROW: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_SKELETON: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_PLANT_SIM: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_WEREWOLF: CommonSimType.ADULT_SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_FAIRY: CommonSimType.ADULT_SMALL_DOG,
        # Child
        CommonSimType.CHILD_SMALL_DOG: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_VAMPIRE: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_GHOST: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_ALIEN: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_MERMAID: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_WITCH: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_ROBOT: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_SCARECROW: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_SKELETON: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_PLANT_SIM: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_WEREWOLF: CommonSimType.CHILD_SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_FAIRY: CommonSimType.CHILD_SMALL_DOG,

        # Large Dog
        # Elder
        CommonSimType.ELDER_LARGE_DOG: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_VAMPIRE: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_GHOST: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_ALIEN: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_MERMAID: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_WITCH: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_ROBOT: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_SCARECROW: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_SKELETON: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_PLANT_SIM: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_WEREWOLF: CommonSimType.ELDER_LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_FAIRY: CommonSimType.ELDER_LARGE_DOG,
        # Adult
        CommonSimType.ADULT_LARGE_DOG: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_VAMPIRE: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_GHOST: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_ALIEN: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_MERMAID: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_WITCH: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_ROBOT: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_SCARECROW: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_SKELETON: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_PLANT_SIM: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_WEREWOLF: CommonSimType.ADULT_LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_FAIRY: CommonSimType.ADULT_LARGE_DOG,
        # Child
        CommonSimType.CHILD_LARGE_DOG: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_VAMPIRE: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_GHOST: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_ALIEN: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_MERMAID: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_WITCH: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_ROBOT: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_SCARECROW: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_SKELETON: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_PLANT_SIM: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_WEREWOLF: CommonSimType.CHILD_LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_FAIRY: CommonSimType.CHILD_LARGE_DOG,

        # Cat
        # Elder
        CommonSimType.ELDER_CAT: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_VAMPIRE: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_GHOST: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_ALIEN: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_MERMAID: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_WITCH: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_ROBOT: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_SCARECROW: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_SKELETON: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_PLANT_SIM: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_WEREWOLF: CommonSimType.ELDER_CAT,
        CommonSimType.ELDER_CAT_FAIRY: CommonSimType.ELDER_CAT,
        # Adult
        CommonSimType.ADULT_CAT: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_VAMPIRE: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_GHOST: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_ALIEN: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_MERMAID: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_WITCH: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_ROBOT: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_SCARECROW: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_SKELETON: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_PLANT_SIM: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_WEREWOLF: CommonSimType.ADULT_CAT,
        CommonSimType.ADULT_CAT_FAIRY: CommonSimType.ADULT_CAT,
        # Child
        CommonSimType.CHILD_CAT: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_VAMPIRE: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_GHOST: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_ALIEN: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_MERMAID: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_WITCH: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_ROBOT: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_SCARECROW: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_SKELETON: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_PLANT_SIM: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_WEREWOLF: CommonSimType.CHILD_CAT,
        CommonSimType.CHILD_CAT_FAIRY: CommonSimType.CHILD_CAT,

        # Fox
        # Elder
        CommonSimType.ELDER_FOX: CommonSimType.ELDER_FOX,
        CommonSimType.ELDER_FOX_VAMPIRE: CommonSimType.ELDER_FOX,
        CommonSimType.ELDER_FOX_GHOST: CommonSimType.ELDER_FOX,
        CommonSimType.ELDER_FOX_ALIEN: CommonSimType.ELDER_FOX,
        CommonSimType.ELDER_FOX_MERMAID: CommonSimType.ELDER_FOX,
        CommonSimType.ELDER_FOX_WITCH: CommonSimType.ELDER_FOX,
        CommonSimType.ELDER_FOX_ROBOT: CommonSimType.ELDER_FOX,
        CommonSimType.ELDER_FOX_SCARECROW: CommonSimType.ELDER_FOX,
        CommonSimType.ELDER_FOX_SKELETON: CommonSimType.ELDER_FOX,
        CommonSimType.ELDER_FOX_PLANT_SIM: CommonSimType.ELDER_FOX,
        CommonSimType.ELDER_FOX_WEREWOLF: CommonSimType.ELDER_FOX,
        CommonSimType.ELDER_FOX_FAIRY: CommonSimType.ELDER_FOX,
        # Adult
        CommonSimType.ADULT_FOX: CommonSimType.ADULT_FOX,
        CommonSimType.ADULT_FOX_VAMPIRE: CommonSimType.ADULT_FOX,
        CommonSimType.ADULT_FOX_GHOST: CommonSimType.ADULT_FOX,
        CommonSimType.ADULT_FOX_ALIEN: CommonSimType.ADULT_FOX,
        CommonSimType.ADULT_FOX_MERMAID: CommonSimType.ADULT_FOX,
        CommonSimType.ADULT_FOX_WITCH: CommonSimType.ADULT_FOX,
        CommonSimType.ADULT_FOX_ROBOT: CommonSimType.ADULT_FOX,
        CommonSimType.ADULT_FOX_SCARECROW: CommonSimType.ADULT_FOX,
        CommonSimType.ADULT_FOX_SKELETON: CommonSimType.ADULT_FOX,
        CommonSimType.ADULT_FOX_PLANT_SIM: CommonSimType.ADULT_FOX,
        CommonSimType.ADULT_FOX_WEREWOLF: CommonSimType.ADULT_FOX,
        CommonSimType.ADULT_FOX_FAIRY: CommonSimType.ADULT_FOX,
        # Child
        CommonSimType.CHILD_FOX: CommonSimType.CHILD_FOX,
        CommonSimType.CHILD_FOX_VAMPIRE: CommonSimType.CHILD_FOX,
        CommonSimType.CHILD_FOX_GHOST: CommonSimType.CHILD_FOX,
        CommonSimType.CHILD_FOX_ALIEN: CommonSimType.CHILD_FOX,
        CommonSimType.CHILD_FOX_MERMAID: CommonSimType.CHILD_FOX,
        CommonSimType.CHILD_FOX_WITCH: CommonSimType.CHILD_FOX,
        CommonSimType.CHILD_FOX_ROBOT: CommonSimType.CHILD_FOX,
        CommonSimType.CHILD_FOX_SCARECROW: CommonSimType.CHILD_FOX,
        CommonSimType.CHILD_FOX_SKELETON: CommonSimType.CHILD_FOX,
        CommonSimType.CHILD_FOX_PLANT_SIM: CommonSimType.CHILD_FOX,
        CommonSimType.CHILD_FOX_WEREWOLF: CommonSimType.CHILD_FOX,
        CommonSimType.CHILD_FOX_FAIRY: CommonSimType.CHILD_FOX,

        # Horse
        # Elder
        CommonSimType.ELDER_HORSE: CommonSimType.ELDER_HORSE,
        CommonSimType.ELDER_HORSE_VAMPIRE: CommonSimType.ELDER_HORSE,
        CommonSimType.ELDER_HORSE_GHOST: CommonSimType.ELDER_HORSE,
        CommonSimType.ELDER_HORSE_ALIEN: CommonSimType.ELDER_HORSE,
        CommonSimType.ELDER_HORSE_MERMAID: CommonSimType.ELDER_HORSE,
        CommonSimType.ELDER_HORSE_WITCH: CommonSimType.ELDER_HORSE,
        CommonSimType.ELDER_HORSE_ROBOT: CommonSimType.ELDER_HORSE,
        CommonSimType.ELDER_HORSE_SCARECROW: CommonSimType.ELDER_HORSE,
        CommonSimType.ELDER_HORSE_SKELETON: CommonSimType.ELDER_HORSE,
        CommonSimType.ELDER_HORSE_PLANT_SIM: CommonSimType.ELDER_HORSE,
        CommonSimType.ELDER_HORSE_WEREWOLF: CommonSimType.ELDER_HORSE,
        CommonSimType.ELDER_HORSE_FAIRY: CommonSimType.ELDER_HORSE,
        # Adult
        CommonSimType.ADULT_HORSE: CommonSimType.ADULT_HORSE,
        CommonSimType.ADULT_HORSE_VAMPIRE: CommonSimType.ADULT_HORSE,
        CommonSimType.ADULT_HORSE_GHOST: CommonSimType.ADULT_HORSE,
        CommonSimType.ADULT_HORSE_ALIEN: CommonSimType.ADULT_HORSE,
        CommonSimType.ADULT_HORSE_MERMAID: CommonSimType.ADULT_HORSE,
        CommonSimType.ADULT_HORSE_WITCH: CommonSimType.ADULT_HORSE,
        CommonSimType.ADULT_HORSE_ROBOT: CommonSimType.ADULT_HORSE,
        CommonSimType.ADULT_HORSE_SCARECROW: CommonSimType.ADULT_HORSE,
        CommonSimType.ADULT_HORSE_SKELETON: CommonSimType.ADULT_HORSE,
        CommonSimType.ADULT_HORSE_PLANT_SIM: CommonSimType.ADULT_HORSE,
        CommonSimType.ADULT_HORSE_WEREWOLF: CommonSimType.ADULT_HORSE,
        CommonSimType.ADULT_HORSE_FAIRY: CommonSimType.ADULT_HORSE,
        # Child
        CommonSimType.CHILD_HORSE: CommonSimType.CHILD_HORSE,
        CommonSimType.CHILD_HORSE_VAMPIRE: CommonSimType.CHILD_HORSE,
        CommonSimType.CHILD_HORSE_GHOST: CommonSimType.CHILD_HORSE,
        CommonSimType.CHILD_HORSE_ALIEN: CommonSimType.CHILD_HORSE,
        CommonSimType.CHILD_HORSE_MERMAID: CommonSimType.CHILD_HORSE,
        CommonSimType.CHILD_HORSE_WITCH: CommonSimType.CHILD_HORSE,
        CommonSimType.CHILD_HORSE_ROBOT: CommonSimType.CHILD_HORSE,
        CommonSimType.CHILD_HORSE_SCARECROW: CommonSimType.CHILD_HORSE,
        CommonSimType.CHILD_HORSE_SKELETON: CommonSimType.CHILD_HORSE,
        CommonSimType.CHILD_HORSE_PLANT_SIM: CommonSimType.CHILD_HORSE,
        CommonSimType.CHILD_HORSE_WEREWOLF: CommonSimType.CHILD_HORSE,
        CommonSimType.CHILD_HORSE_FAIRY: CommonSimType.CHILD_HORSE,
    }

    _OCCULT_SIM_TYPE_TO_OCCULT_TYPE_MAPPING: Dict[CommonSimType, CommonOccultType] = {
        # Human
        # Elder
        CommonSimType.ELDER_HUMAN: CommonOccultType.NON_OCCULT,
        CommonSimType.ELDER_HUMAN_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.ELDER_HUMAN_GHOST: CommonOccultType.GHOST,
        CommonSimType.ELDER_HUMAN_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.ELDER_HUMAN_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.ELDER_HUMAN_WITCH: CommonOccultType.WITCH,
        CommonSimType.ELDER_HUMAN_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.ELDER_HUMAN_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.ELDER_HUMAN_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.ELDER_HUMAN_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.ELDER_HUMAN_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.ELDER_HUMAN_FAIRY: CommonOccultType.FAIRY,
        # Adult
        CommonSimType.ADULT_HUMAN: CommonOccultType.NON_OCCULT,
        CommonSimType.ADULT_HUMAN_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.ADULT_HUMAN_GHOST: CommonOccultType.GHOST,
        CommonSimType.ADULT_HUMAN_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.ADULT_HUMAN_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.ADULT_HUMAN_WITCH: CommonOccultType.WITCH,
        CommonSimType.ADULT_HUMAN_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.ADULT_HUMAN_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.ADULT_HUMAN_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.ADULT_HUMAN_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.ADULT_HUMAN_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.ADULT_HUMAN_FAIRY: CommonOccultType.FAIRY,
        # Young Adult
        CommonSimType.YOUNG_ADULT_HUMAN: CommonOccultType.NON_OCCULT,
        CommonSimType.YOUNG_ADULT_HUMAN_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.YOUNG_ADULT_HUMAN_GHOST: CommonOccultType.GHOST,
        CommonSimType.YOUNG_ADULT_HUMAN_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.YOUNG_ADULT_HUMAN_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.YOUNG_ADULT_HUMAN_WITCH: CommonOccultType.WITCH,
        CommonSimType.YOUNG_ADULT_HUMAN_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.YOUNG_ADULT_HUMAN_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.YOUNG_ADULT_HUMAN_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.YOUNG_ADULT_HUMAN_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.YOUNG_ADULT_HUMAN_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.YOUNG_ADULT_HUMAN_FAIRY: CommonOccultType.FAIRY,
        # Teen
        CommonSimType.TEEN_HUMAN: CommonOccultType.NON_OCCULT,
        CommonSimType.TEEN_HUMAN_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.TEEN_HUMAN_GHOST: CommonOccultType.GHOST,
        CommonSimType.TEEN_HUMAN_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.TEEN_HUMAN_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.TEEN_HUMAN_WITCH: CommonOccultType.WITCH,
        CommonSimType.TEEN_HUMAN_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.TEEN_HUMAN_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.TEEN_HUMAN_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.TEEN_HUMAN_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.TEEN_HUMAN_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.TEEN_HUMAN_FAIRY: CommonOccultType.FAIRY,
        # Child
        CommonSimType.CHILD_HUMAN: CommonOccultType.NON_OCCULT,
        CommonSimType.CHILD_HUMAN_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.CHILD_HUMAN_GHOST: CommonOccultType.GHOST,
        CommonSimType.CHILD_HUMAN_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.CHILD_HUMAN_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.CHILD_HUMAN_WITCH: CommonOccultType.WITCH,
        CommonSimType.CHILD_HUMAN_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.CHILD_HUMAN_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.CHILD_HUMAN_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.CHILD_HUMAN_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.CHILD_HUMAN_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.CHILD_HUMAN_FAIRY: CommonOccultType.FAIRY,
        # Toddler
        CommonSimType.TODDLER_HUMAN: CommonOccultType.NON_OCCULT,
        CommonSimType.TODDLER_HUMAN_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.TODDLER_HUMAN_GHOST: CommonOccultType.GHOST,
        CommonSimType.TODDLER_HUMAN_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.TODDLER_HUMAN_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.TODDLER_HUMAN_WITCH: CommonOccultType.WITCH,
        CommonSimType.TODDLER_HUMAN_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.TODDLER_HUMAN_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.TODDLER_HUMAN_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.TODDLER_HUMAN_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.TODDLER_HUMAN_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.TODDLER_HUMAN_FAIRY: CommonOccultType.FAIRY,
        # Infant
        CommonSimType.INFANT_HUMAN: CommonOccultType.NON_OCCULT,
        CommonSimType.INFANT_HUMAN_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.INFANT_HUMAN_GHOST: CommonOccultType.GHOST,
        CommonSimType.INFANT_HUMAN_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.INFANT_HUMAN_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.INFANT_HUMAN_WITCH: CommonOccultType.WITCH,
        CommonSimType.INFANT_HUMAN_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.INFANT_HUMAN_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.INFANT_HUMAN_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.INFANT_HUMAN_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.INFANT_HUMAN_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.INFANT_HUMAN_FAIRY: CommonOccultType.FAIRY,
        # Baby
        CommonSimType.BABY_HUMAN: CommonOccultType.NON_OCCULT,
        CommonSimType.BABY_HUMAN_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.BABY_HUMAN_GHOST: CommonOccultType.GHOST,
        CommonSimType.BABY_HUMAN_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.BABY_HUMAN_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.BABY_HUMAN_WITCH: CommonOccultType.WITCH,
        CommonSimType.BABY_HUMAN_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.BABY_HUMAN_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.BABY_HUMAN_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.BABY_HUMAN_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.BABY_HUMAN_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.BABY_HUMAN_FAIRY: CommonOccultType.FAIRY,

        # Dog
        # Child
        CommonSimType.CHILD_DOG: CommonOccultType.NON_OCCULT,
        CommonSimType.CHILD_DOG_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.CHILD_DOG_GHOST: CommonOccultType.GHOST,
        CommonSimType.CHILD_DOG_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.CHILD_DOG_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.CHILD_DOG_WITCH: CommonOccultType.WITCH,
        CommonSimType.CHILD_DOG_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.CHILD_DOG_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.CHILD_DOG_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.CHILD_DOG_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.CHILD_DOG_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.CHILD_DOG_FAIRY: CommonOccultType.FAIRY,

        # Small Dog
        # Elder
        CommonSimType.ELDER_SMALL_DOG: CommonOccultType.NON_OCCULT,
        CommonSimType.ELDER_SMALL_DOG_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.ELDER_SMALL_DOG_GHOST: CommonOccultType.GHOST,
        CommonSimType.ELDER_SMALL_DOG_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.ELDER_SMALL_DOG_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.ELDER_SMALL_DOG_WITCH: CommonOccultType.WITCH,
        CommonSimType.ELDER_SMALL_DOG_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.ELDER_SMALL_DOG_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.ELDER_SMALL_DOG_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.ELDER_SMALL_DOG_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.ELDER_SMALL_DOG_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.ELDER_SMALL_DOG_FAIRY: CommonOccultType.FAIRY,
        # Adult
        CommonSimType.ADULT_SMALL_DOG: CommonOccultType.NON_OCCULT,
        CommonSimType.ADULT_SMALL_DOG_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.ADULT_SMALL_DOG_GHOST: CommonOccultType.GHOST,
        CommonSimType.ADULT_SMALL_DOG_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.ADULT_SMALL_DOG_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.ADULT_SMALL_DOG_WITCH: CommonOccultType.WITCH,
        CommonSimType.ADULT_SMALL_DOG_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.ADULT_SMALL_DOG_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.ADULT_SMALL_DOG_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.ADULT_SMALL_DOG_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.ADULT_SMALL_DOG_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.ADULT_SMALL_DOG_FAIRY: CommonOccultType.FAIRY,
        # Child
        CommonSimType.CHILD_SMALL_DOG: CommonOccultType.NON_OCCULT,
        CommonSimType.CHILD_SMALL_DOG_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.CHILD_SMALL_DOG_GHOST: CommonOccultType.GHOST,
        CommonSimType.CHILD_SMALL_DOG_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.CHILD_SMALL_DOG_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.CHILD_SMALL_DOG_WITCH: CommonOccultType.WITCH,
        CommonSimType.CHILD_SMALL_DOG_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.CHILD_SMALL_DOG_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.CHILD_SMALL_DOG_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.CHILD_SMALL_DOG_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.CHILD_SMALL_DOG_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.CHILD_SMALL_DOG_FAIRY: CommonOccultType.FAIRY,

        # Large Dog
        # Elder
        CommonSimType.ELDER_LARGE_DOG: CommonOccultType.NON_OCCULT,
        CommonSimType.ELDER_LARGE_DOG_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.ELDER_LARGE_DOG_GHOST: CommonOccultType.GHOST,
        CommonSimType.ELDER_LARGE_DOG_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.ELDER_LARGE_DOG_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.ELDER_LARGE_DOG_WITCH: CommonOccultType.WITCH,
        CommonSimType.ELDER_LARGE_DOG_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.ELDER_LARGE_DOG_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.ELDER_LARGE_DOG_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.ELDER_LARGE_DOG_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.ELDER_LARGE_DOG_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.ELDER_LARGE_DOG_FAIRY: CommonOccultType.FAIRY,
        # Adult
        CommonSimType.ADULT_LARGE_DOG: CommonOccultType.NON_OCCULT,
        CommonSimType.ADULT_LARGE_DOG_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.ADULT_LARGE_DOG_GHOST: CommonOccultType.GHOST,
        CommonSimType.ADULT_LARGE_DOG_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.ADULT_LARGE_DOG_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.ADULT_LARGE_DOG_WITCH: CommonOccultType.WITCH,
        CommonSimType.ADULT_LARGE_DOG_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.ADULT_LARGE_DOG_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.ADULT_LARGE_DOG_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.ADULT_LARGE_DOG_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.ADULT_LARGE_DOG_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.ADULT_LARGE_DOG_FAIRY: CommonOccultType.FAIRY,
        # Child
        CommonSimType.CHILD_LARGE_DOG: CommonOccultType.NON_OCCULT,
        CommonSimType.CHILD_LARGE_DOG_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.CHILD_LARGE_DOG_GHOST: CommonOccultType.GHOST,
        CommonSimType.CHILD_LARGE_DOG_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.CHILD_LARGE_DOG_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.CHILD_LARGE_DOG_WITCH: CommonOccultType.WITCH,
        CommonSimType.CHILD_LARGE_DOG_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.CHILD_LARGE_DOG_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.CHILD_LARGE_DOG_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.CHILD_LARGE_DOG_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.CHILD_LARGE_DOG_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.CHILD_LARGE_DOG_FAIRY: CommonOccultType.FAIRY,

        # Cat
        # Elder
        CommonSimType.ELDER_CAT: CommonOccultType.NON_OCCULT,
        CommonSimType.ELDER_CAT_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.ELDER_CAT_GHOST: CommonOccultType.GHOST,
        CommonSimType.ELDER_CAT_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.ELDER_CAT_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.ELDER_CAT_WITCH: CommonOccultType.WITCH,
        CommonSimType.ELDER_CAT_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.ELDER_CAT_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.ELDER_CAT_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.ELDER_CAT_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.ELDER_CAT_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.ELDER_CAT_FAIRY: CommonOccultType.FAIRY,
        # Adult
        CommonSimType.ADULT_CAT: CommonOccultType.NON_OCCULT,
        CommonSimType.ADULT_CAT_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.ADULT_CAT_GHOST: CommonOccultType.GHOST,
        CommonSimType.ADULT_CAT_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.ADULT_CAT_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.ADULT_CAT_WITCH: CommonOccultType.WITCH,
        CommonSimType.ADULT_CAT_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.ADULT_CAT_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.ADULT_CAT_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.ADULT_CAT_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.ADULT_CAT_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.ADULT_CAT_FAIRY: CommonOccultType.FAIRY,
        # Child
        CommonSimType.CHILD_CAT: CommonOccultType.NON_OCCULT,
        CommonSimType.CHILD_CAT_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.CHILD_CAT_GHOST: CommonOccultType.GHOST,
        CommonSimType.CHILD_CAT_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.CHILD_CAT_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.CHILD_CAT_WITCH: CommonOccultType.WITCH,
        CommonSimType.CHILD_CAT_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.CHILD_CAT_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.CHILD_CAT_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.CHILD_CAT_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.CHILD_CAT_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.CHILD_CAT_FAIRY: CommonOccultType.FAIRY,

        # Fox
        # Elder
        CommonSimType.ELDER_FOX: CommonOccultType.NON_OCCULT,
        CommonSimType.ELDER_FOX_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.ELDER_FOX_GHOST: CommonOccultType.GHOST,
        CommonSimType.ELDER_FOX_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.ELDER_FOX_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.ELDER_FOX_WITCH: CommonOccultType.WITCH,
        CommonSimType.ELDER_FOX_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.ELDER_FOX_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.ELDER_FOX_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.ELDER_FOX_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.ELDER_FOX_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.ELDER_FOX_FAIRY: CommonOccultType.FAIRY,
        # Adult
        CommonSimType.ADULT_FOX: CommonOccultType.NON_OCCULT,
        CommonSimType.ADULT_FOX_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.ADULT_FOX_GHOST: CommonOccultType.GHOST,
        CommonSimType.ADULT_FOX_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.ADULT_FOX_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.ADULT_FOX_WITCH: CommonOccultType.WITCH,
        CommonSimType.ADULT_FOX_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.ADULT_FOX_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.ADULT_FOX_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.ADULT_FOX_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.ADULT_FOX_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.ADULT_FOX_FAIRY: CommonOccultType.FAIRY,
        # Child
        CommonSimType.CHILD_FOX: CommonOccultType.NON_OCCULT,
        CommonSimType.CHILD_FOX_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.CHILD_FOX_GHOST: CommonOccultType.GHOST,
        CommonSimType.CHILD_FOX_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.CHILD_FOX_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.CHILD_FOX_WITCH: CommonOccultType.WITCH,
        CommonSimType.CHILD_FOX_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.CHILD_FOX_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.CHILD_FOX_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.CHILD_FOX_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.CHILD_FOX_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.CHILD_FOX_FAIRY: CommonOccultType.FAIRY,

        # Horse
        # Elder
        CommonSimType.ELDER_HORSE: CommonOccultType.NON_OCCULT,
        CommonSimType.ELDER_HORSE_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.ELDER_HORSE_GHOST: CommonOccultType.GHOST,
        CommonSimType.ELDER_HORSE_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.ELDER_HORSE_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.ELDER_HORSE_WITCH: CommonOccultType.WITCH,
        CommonSimType.ELDER_HORSE_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.ELDER_HORSE_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.ELDER_HORSE_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.ELDER_HORSE_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.ELDER_HORSE_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.ELDER_HORSE_FAIRY: CommonOccultType.FAIRY,
        # Adult
        CommonSimType.ADULT_HORSE: CommonOccultType.NON_OCCULT,
        CommonSimType.ADULT_HORSE_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.ADULT_HORSE_GHOST: CommonOccultType.GHOST,
        CommonSimType.ADULT_HORSE_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.ADULT_HORSE_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.ADULT_HORSE_WITCH: CommonOccultType.WITCH,
        CommonSimType.ADULT_HORSE_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.ADULT_HORSE_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.ADULT_HORSE_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.ADULT_HORSE_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.ADULT_HORSE_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.ADULT_HORSE_FAIRY: CommonOccultType.FAIRY,
        # Child
        CommonSimType.CHILD_HORSE: CommonOccultType.NON_OCCULT,
        CommonSimType.CHILD_HORSE_VAMPIRE: CommonOccultType.VAMPIRE,
        CommonSimType.CHILD_HORSE_GHOST: CommonOccultType.GHOST,
        CommonSimType.CHILD_HORSE_ALIEN: CommonOccultType.ALIEN,
        CommonSimType.CHILD_HORSE_MERMAID: CommonOccultType.MERMAID,
        CommonSimType.CHILD_HORSE_WITCH: CommonOccultType.WITCH,
        CommonSimType.CHILD_HORSE_ROBOT: CommonOccultType.ROBOT,
        CommonSimType.CHILD_HORSE_SCARECROW: CommonOccultType.SCARECROW,
        CommonSimType.CHILD_HORSE_SKELETON: CommonOccultType.SKELETON,
        CommonSimType.CHILD_HORSE_PLANT_SIM: CommonOccultType.PLANT_SIM,
        CommonSimType.CHILD_HORSE_WEREWOLF: CommonOccultType.WEREWOLF,
        CommonSimType.CHILD_HORSE_FAIRY: CommonOccultType.FAIRY,
    }

    _OCCULT_SIM_TYPE_TO_AGE_MAPPING: Dict[CommonSimType, CommonAge] = {
        # Human
        # Elder
        CommonSimType.ELDER_HUMAN: CommonAge.ELDER,
        CommonSimType.ELDER_HUMAN_VAMPIRE: CommonAge.ELDER,
        CommonSimType.ELDER_HUMAN_GHOST: CommonAge.ELDER,
        CommonSimType.ELDER_HUMAN_ALIEN: CommonAge.ELDER,
        CommonSimType.ELDER_HUMAN_MERMAID: CommonAge.ELDER,
        CommonSimType.ELDER_HUMAN_WITCH: CommonAge.ELDER,
        CommonSimType.ELDER_HUMAN_ROBOT: CommonAge.ELDER,
        CommonSimType.ELDER_HUMAN_SCARECROW: CommonAge.ELDER,
        CommonSimType.ELDER_HUMAN_SKELETON: CommonAge.ELDER,
        CommonSimType.ELDER_HUMAN_PLANT_SIM: CommonAge.ELDER,
        CommonSimType.ELDER_HUMAN_WEREWOLF: CommonAge.ELDER,
        CommonSimType.ELDER_HUMAN_FAIRY: CommonAge.ELDER,
        # Adult
        CommonSimType.ADULT_HUMAN: CommonAge.ADULT,
        CommonSimType.ADULT_HUMAN_VAMPIRE: CommonAge.ADULT,
        CommonSimType.ADULT_HUMAN_GHOST: CommonAge.ADULT,
        CommonSimType.ADULT_HUMAN_ALIEN: CommonAge.ADULT,
        CommonSimType.ADULT_HUMAN_MERMAID: CommonAge.ADULT,
        CommonSimType.ADULT_HUMAN_WITCH: CommonAge.ADULT,
        CommonSimType.ADULT_HUMAN_ROBOT: CommonAge.ADULT,
        CommonSimType.ADULT_HUMAN_SCARECROW: CommonAge.ADULT,
        CommonSimType.ADULT_HUMAN_SKELETON: CommonAge.ADULT,
        CommonSimType.ADULT_HUMAN_PLANT_SIM: CommonAge.ADULT,
        CommonSimType.ADULT_HUMAN_WEREWOLF: CommonAge.ADULT,
        CommonSimType.ADULT_HUMAN_FAIRY: CommonAge.ADULT,
        # Young Adult
        CommonSimType.YOUNG_ADULT_HUMAN: CommonAge.YOUNGADULT,
        CommonSimType.YOUNG_ADULT_HUMAN_VAMPIRE: CommonAge.YOUNGADULT,
        CommonSimType.YOUNG_ADULT_HUMAN_GHOST: CommonAge.YOUNGADULT,
        CommonSimType.YOUNG_ADULT_HUMAN_ALIEN: CommonAge.YOUNGADULT,
        CommonSimType.YOUNG_ADULT_HUMAN_MERMAID: CommonAge.YOUNGADULT,
        CommonSimType.YOUNG_ADULT_HUMAN_WITCH: CommonAge.YOUNGADULT,
        CommonSimType.YOUNG_ADULT_HUMAN_ROBOT: CommonAge.YOUNGADULT,
        CommonSimType.YOUNG_ADULT_HUMAN_SCARECROW: CommonAge.YOUNGADULT,
        CommonSimType.YOUNG_ADULT_HUMAN_SKELETON: CommonAge.YOUNGADULT,
        CommonSimType.YOUNG_ADULT_HUMAN_PLANT_SIM: CommonAge.YOUNGADULT,
        CommonSimType.YOUNG_ADULT_HUMAN_WEREWOLF: CommonAge.YOUNGADULT,
        CommonSimType.YOUNG_ADULT_HUMAN_FAIRY: CommonAge.YOUNGADULT,
        # Teen
        CommonSimType.TEEN_HUMAN: CommonAge.TEEN,
        CommonSimType.TEEN_HUMAN_VAMPIRE: CommonAge.TEEN,
        CommonSimType.TEEN_HUMAN_GHOST: CommonAge.TEEN,
        CommonSimType.TEEN_HUMAN_ALIEN: CommonAge.TEEN,
        CommonSimType.TEEN_HUMAN_MERMAID: CommonAge.TEEN,
        CommonSimType.TEEN_HUMAN_WITCH: CommonAge.TEEN,
        CommonSimType.TEEN_HUMAN_ROBOT: CommonAge.TEEN,
        CommonSimType.TEEN_HUMAN_SCARECROW: CommonAge.TEEN,
        CommonSimType.TEEN_HUMAN_SKELETON: CommonAge.TEEN,
        CommonSimType.TEEN_HUMAN_PLANT_SIM: CommonAge.TEEN,
        CommonSimType.TEEN_HUMAN_WEREWOLF: CommonAge.TEEN,
        CommonSimType.TEEN_HUMAN_FAIRY: CommonAge.TEEN,
        # Child
        CommonSimType.CHILD_HUMAN: CommonAge.CHILD,
        CommonSimType.CHILD_HUMAN_VAMPIRE: CommonAge.CHILD,
        CommonSimType.CHILD_HUMAN_GHOST: CommonAge.CHILD,
        CommonSimType.CHILD_HUMAN_ALIEN: CommonAge.CHILD,
        CommonSimType.CHILD_HUMAN_MERMAID: CommonAge.CHILD,
        CommonSimType.CHILD_HUMAN_WITCH: CommonAge.CHILD,
        CommonSimType.CHILD_HUMAN_ROBOT: CommonAge.CHILD,
        CommonSimType.CHILD_HUMAN_SCARECROW: CommonAge.CHILD,
        CommonSimType.CHILD_HUMAN_SKELETON: CommonAge.CHILD,
        CommonSimType.CHILD_HUMAN_PLANT_SIM: CommonAge.CHILD,
        CommonSimType.CHILD_HUMAN_WEREWOLF: CommonAge.CHILD,
        CommonSimType.CHILD_HUMAN_FAIRY: CommonAge.CHILD,
        # Toddler
        CommonSimType.TODDLER_HUMAN: CommonAge.TODDLER,
        CommonSimType.TODDLER_HUMAN_VAMPIRE: CommonAge.TODDLER,
        CommonSimType.TODDLER_HUMAN_GHOST: CommonAge.TODDLER,
        CommonSimType.TODDLER_HUMAN_ALIEN: CommonAge.TODDLER,
        CommonSimType.TODDLER_HUMAN_MERMAID: CommonAge.TODDLER,
        CommonSimType.TODDLER_HUMAN_WITCH: CommonAge.TODDLER,
        CommonSimType.TODDLER_HUMAN_ROBOT: CommonAge.TODDLER,
        CommonSimType.TODDLER_HUMAN_SCARECROW: CommonAge.TODDLER,
        CommonSimType.TODDLER_HUMAN_SKELETON: CommonAge.TODDLER,
        CommonSimType.TODDLER_HUMAN_PLANT_SIM: CommonAge.TODDLER,
        CommonSimType.TODDLER_HUMAN_WEREWOLF: CommonAge.TODDLER,
        CommonSimType.TODDLER_HUMAN_FAIRY: CommonAge.TODDLER,
        # Infant
        CommonSimType.INFANT_HUMAN: CommonAge.INFANT,
        CommonSimType.INFANT_HUMAN_VAMPIRE: CommonAge.INFANT,
        CommonSimType.INFANT_HUMAN_GHOST: CommonAge.INFANT,
        CommonSimType.INFANT_HUMAN_ALIEN: CommonAge.INFANT,
        CommonSimType.INFANT_HUMAN_MERMAID: CommonAge.INFANT,
        CommonSimType.INFANT_HUMAN_WITCH: CommonAge.INFANT,
        CommonSimType.INFANT_HUMAN_ROBOT: CommonAge.INFANT,
        CommonSimType.INFANT_HUMAN_SCARECROW: CommonAge.INFANT,
        CommonSimType.INFANT_HUMAN_SKELETON: CommonAge.INFANT,
        CommonSimType.INFANT_HUMAN_PLANT_SIM: CommonAge.INFANT,
        CommonSimType.INFANT_HUMAN_WEREWOLF: CommonAge.INFANT,
        CommonSimType.INFANT_HUMAN_FAIRY: CommonAge.INFANT,
        # Baby
        CommonSimType.BABY_HUMAN: CommonAge.BABY,
        CommonSimType.BABY_HUMAN_VAMPIRE: CommonAge.BABY,
        CommonSimType.BABY_HUMAN_GHOST: CommonAge.BABY,
        CommonSimType.BABY_HUMAN_ALIEN: CommonAge.BABY,
        CommonSimType.BABY_HUMAN_MERMAID: CommonAge.BABY,
        CommonSimType.BABY_HUMAN_WITCH: CommonAge.BABY,
        CommonSimType.BABY_HUMAN_ROBOT: CommonAge.BABY,
        CommonSimType.BABY_HUMAN_SCARECROW: CommonAge.BABY,
        CommonSimType.BABY_HUMAN_SKELETON: CommonAge.BABY,
        CommonSimType.BABY_HUMAN_PLANT_SIM: CommonAge.BABY,
        CommonSimType.BABY_HUMAN_WEREWOLF: CommonAge.BABY,
        CommonSimType.BABY_HUMAN_FAIRY: CommonAge.BABY,

        # Dog
        # Child
        CommonSimType.CHILD_DOG: CommonAge.CHILD,
        CommonSimType.CHILD_DOG_VAMPIRE: CommonAge.CHILD,
        CommonSimType.CHILD_DOG_GHOST: CommonAge.CHILD,
        CommonSimType.CHILD_DOG_ALIEN: CommonAge.CHILD,
        CommonSimType.CHILD_DOG_MERMAID: CommonAge.CHILD,
        CommonSimType.CHILD_DOG_WITCH: CommonAge.CHILD,
        CommonSimType.CHILD_DOG_ROBOT: CommonAge.CHILD,
        CommonSimType.CHILD_DOG_SCARECROW: CommonAge.CHILD,
        CommonSimType.CHILD_DOG_SKELETON: CommonAge.CHILD,
        CommonSimType.CHILD_DOG_PLANT_SIM: CommonAge.CHILD,
        CommonSimType.CHILD_DOG_WEREWOLF: CommonAge.CHILD,
        CommonSimType.CHILD_DOG_FAIRY: CommonAge.CHILD,

        # Small Dog
        # Elder
        CommonSimType.ELDER_SMALL_DOG: CommonAge.ELDER,
        CommonSimType.ELDER_SMALL_DOG_VAMPIRE: CommonAge.ELDER,
        CommonSimType.ELDER_SMALL_DOG_GHOST: CommonAge.ELDER,
        CommonSimType.ELDER_SMALL_DOG_ALIEN: CommonAge.ELDER,
        CommonSimType.ELDER_SMALL_DOG_MERMAID: CommonAge.ELDER,
        CommonSimType.ELDER_SMALL_DOG_WITCH: CommonAge.ELDER,
        CommonSimType.ELDER_SMALL_DOG_ROBOT: CommonAge.ELDER,
        CommonSimType.ELDER_SMALL_DOG_SCARECROW: CommonAge.ELDER,
        CommonSimType.ELDER_SMALL_DOG_SKELETON: CommonAge.ELDER,
        CommonSimType.ELDER_SMALL_DOG_PLANT_SIM: CommonAge.ELDER,
        CommonSimType.ELDER_SMALL_DOG_WEREWOLF: CommonAge.ELDER,
        CommonSimType.ELDER_SMALL_DOG_FAIRY: CommonAge.ELDER,
        # Adult
        CommonSimType.ADULT_SMALL_DOG: CommonAge.ADULT,
        CommonSimType.ADULT_SMALL_DOG_VAMPIRE: CommonAge.ADULT,
        CommonSimType.ADULT_SMALL_DOG_GHOST: CommonAge.ADULT,
        CommonSimType.ADULT_SMALL_DOG_ALIEN: CommonAge.ADULT,
        CommonSimType.ADULT_SMALL_DOG_MERMAID: CommonAge.ADULT,
        CommonSimType.ADULT_SMALL_DOG_WITCH: CommonAge.ADULT,
        CommonSimType.ADULT_SMALL_DOG_ROBOT: CommonAge.ADULT,
        CommonSimType.ADULT_SMALL_DOG_SCARECROW: CommonAge.ADULT,
        CommonSimType.ADULT_SMALL_DOG_SKELETON: CommonAge.ADULT,
        CommonSimType.ADULT_SMALL_DOG_PLANT_SIM: CommonAge.ADULT,
        CommonSimType.ADULT_SMALL_DOG_WEREWOLF: CommonAge.ADULT,
        CommonSimType.ADULT_SMALL_DOG_FAIRY: CommonAge.ADULT,
        # Child
        CommonSimType.CHILD_SMALL_DOG: CommonAge.CHILD,
        CommonSimType.CHILD_SMALL_DOG_VAMPIRE: CommonAge.CHILD,
        CommonSimType.CHILD_SMALL_DOG_GHOST: CommonAge.CHILD,
        CommonSimType.CHILD_SMALL_DOG_ALIEN: CommonAge.CHILD,
        CommonSimType.CHILD_SMALL_DOG_MERMAID: CommonAge.CHILD,
        CommonSimType.CHILD_SMALL_DOG_WITCH: CommonAge.CHILD,
        CommonSimType.CHILD_SMALL_DOG_ROBOT: CommonAge.CHILD,
        CommonSimType.CHILD_SMALL_DOG_SCARECROW: CommonAge.CHILD,
        CommonSimType.CHILD_SMALL_DOG_SKELETON: CommonAge.CHILD,
        CommonSimType.CHILD_SMALL_DOG_PLANT_SIM: CommonAge.CHILD,
        CommonSimType.CHILD_SMALL_DOG_WEREWOLF: CommonAge.CHILD,
        CommonSimType.CHILD_SMALL_DOG_FAIRY: CommonAge.CHILD,

        # Large Dog
        # Elder
        CommonSimType.ELDER_LARGE_DOG: CommonAge.ELDER,
        CommonSimType.ELDER_LARGE_DOG_VAMPIRE: CommonAge.ELDER,
        CommonSimType.ELDER_LARGE_DOG_GHOST: CommonAge.ELDER,
        CommonSimType.ELDER_LARGE_DOG_ALIEN: CommonAge.ELDER,
        CommonSimType.ELDER_LARGE_DOG_MERMAID: CommonAge.ELDER,
        CommonSimType.ELDER_LARGE_DOG_WITCH: CommonAge.ELDER,
        CommonSimType.ELDER_LARGE_DOG_ROBOT: CommonAge.ELDER,
        CommonSimType.ELDER_LARGE_DOG_SCARECROW: CommonAge.ELDER,
        CommonSimType.ELDER_LARGE_DOG_SKELETON: CommonAge.ELDER,
        CommonSimType.ELDER_LARGE_DOG_PLANT_SIM: CommonAge.ELDER,
        CommonSimType.ELDER_LARGE_DOG_WEREWOLF: CommonAge.ELDER,
        CommonSimType.ELDER_LARGE_DOG_FAIRY: CommonAge.ELDER,
        # Adult
        CommonSimType.ADULT_LARGE_DOG: CommonAge.ADULT,
        CommonSimType.ADULT_LARGE_DOG_VAMPIRE: CommonAge.ADULT,
        CommonSimType.ADULT_LARGE_DOG_GHOST: CommonAge.ADULT,
        CommonSimType.ADULT_LARGE_DOG_ALIEN: CommonAge.ADULT,
        CommonSimType.ADULT_LARGE_DOG_MERMAID: CommonAge.ADULT,
        CommonSimType.ADULT_LARGE_DOG_WITCH: CommonAge.ADULT,
        CommonSimType.ADULT_LARGE_DOG_ROBOT: CommonAge.ADULT,
        CommonSimType.ADULT_LARGE_DOG_SCARECROW: CommonAge.ADULT,
        CommonSimType.ADULT_LARGE_DOG_SKELETON: CommonAge.ADULT,
        CommonSimType.ADULT_LARGE_DOG_PLANT_SIM: CommonAge.ADULT,
        CommonSimType.ADULT_LARGE_DOG_WEREWOLF: CommonAge.ADULT,
        CommonSimType.ADULT_LARGE_DOG_FAIRY: CommonAge.ADULT,
        # Child
        CommonSimType.CHILD_LARGE_DOG: CommonAge.CHILD,
        CommonSimType.CHILD_LARGE_DOG_VAMPIRE: CommonAge.CHILD,
        CommonSimType.CHILD_LARGE_DOG_GHOST: CommonAge.CHILD,
        CommonSimType.CHILD_LARGE_DOG_ALIEN: CommonAge.CHILD,
        CommonSimType.CHILD_LARGE_DOG_MERMAID: CommonAge.CHILD,
        CommonSimType.CHILD_LARGE_DOG_WITCH: CommonAge.CHILD,
        CommonSimType.CHILD_LARGE_DOG_ROBOT: CommonAge.CHILD,
        CommonSimType.CHILD_LARGE_DOG_SCARECROW: CommonAge.CHILD,
        CommonSimType.CHILD_LARGE_DOG_SKELETON: CommonAge.CHILD,
        CommonSimType.CHILD_LARGE_DOG_PLANT_SIM: CommonAge.CHILD,
        CommonSimType.CHILD_LARGE_DOG_WEREWOLF: CommonAge.CHILD,
        CommonSimType.CHILD_LARGE_DOG_FAIRY: CommonAge.CHILD,

        # Cat
        # Elder
        CommonSimType.ELDER_CAT: CommonAge.ELDER,
        CommonSimType.ELDER_CAT_VAMPIRE: CommonAge.ELDER,
        CommonSimType.ELDER_CAT_GHOST: CommonAge.ELDER,
        CommonSimType.ELDER_CAT_ALIEN: CommonAge.ELDER,
        CommonSimType.ELDER_CAT_MERMAID: CommonAge.ELDER,
        CommonSimType.ELDER_CAT_WITCH: CommonAge.ELDER,
        CommonSimType.ELDER_CAT_ROBOT: CommonAge.ELDER,
        CommonSimType.ELDER_CAT_SCARECROW: CommonAge.ELDER,
        CommonSimType.ELDER_CAT_SKELETON: CommonAge.ELDER,
        CommonSimType.ELDER_CAT_PLANT_SIM: CommonAge.ELDER,
        CommonSimType.ELDER_CAT_WEREWOLF: CommonAge.ELDER,
        CommonSimType.ELDER_CAT_FAIRY: CommonAge.ELDER,
        # Adult
        CommonSimType.ADULT_CAT: CommonAge.ADULT,
        CommonSimType.ADULT_CAT_VAMPIRE: CommonAge.ADULT,
        CommonSimType.ADULT_CAT_GHOST: CommonAge.ADULT,
        CommonSimType.ADULT_CAT_ALIEN: CommonAge.ADULT,
        CommonSimType.ADULT_CAT_MERMAID: CommonAge.ADULT,
        CommonSimType.ADULT_CAT_WITCH: CommonAge.ADULT,
        CommonSimType.ADULT_CAT_ROBOT: CommonAge.ADULT,
        CommonSimType.ADULT_CAT_SCARECROW: CommonAge.ADULT,
        CommonSimType.ADULT_CAT_SKELETON: CommonAge.ADULT,
        CommonSimType.ADULT_CAT_PLANT_SIM: CommonAge.ADULT,
        CommonSimType.ADULT_CAT_WEREWOLF: CommonAge.ADULT,
        CommonSimType.ADULT_CAT_FAIRY: CommonAge.ADULT,
        # Child
        CommonSimType.CHILD_CAT: CommonAge.CHILD,
        CommonSimType.CHILD_CAT_VAMPIRE: CommonAge.CHILD,
        CommonSimType.CHILD_CAT_GHOST: CommonAge.CHILD,
        CommonSimType.CHILD_CAT_ALIEN: CommonAge.CHILD,
        CommonSimType.CHILD_CAT_MERMAID: CommonAge.CHILD,
        CommonSimType.CHILD_CAT_WITCH: CommonAge.CHILD,
        CommonSimType.CHILD_CAT_ROBOT: CommonAge.CHILD,
        CommonSimType.CHILD_CAT_SCARECROW: CommonAge.CHILD,
        CommonSimType.CHILD_CAT_SKELETON: CommonAge.CHILD,
        CommonSimType.CHILD_CAT_PLANT_SIM: CommonAge.CHILD,
        CommonSimType.CHILD_CAT_WEREWOLF: CommonAge.CHILD,
        CommonSimType.CHILD_CAT_FAIRY: CommonAge.CHILD,

        # Fox
        # Elder
        CommonSimType.ELDER_FOX: CommonAge.ELDER,
        CommonSimType.ELDER_FOX_VAMPIRE: CommonAge.ELDER,
        CommonSimType.ELDER_FOX_GHOST: CommonAge.ELDER,
        CommonSimType.ELDER_FOX_ALIEN: CommonAge.ELDER,
        CommonSimType.ELDER_FOX_MERMAID: CommonAge.ELDER,
        CommonSimType.ELDER_FOX_WITCH: CommonAge.ELDER,
        CommonSimType.ELDER_FOX_ROBOT: CommonAge.ELDER,
        CommonSimType.ELDER_FOX_SCARECROW: CommonAge.ELDER,
        CommonSimType.ELDER_FOX_SKELETON: CommonAge.ELDER,
        CommonSimType.ELDER_FOX_PLANT_SIM: CommonAge.ELDER,
        CommonSimType.ELDER_FOX_WEREWOLF: CommonAge.ELDER,
        CommonSimType.ELDER_FOX_FAIRY: CommonAge.ELDER,
        # Adult
        CommonSimType.ADULT_FOX: CommonAge.ADULT,
        CommonSimType.ADULT_FOX_VAMPIRE: CommonAge.ADULT,
        CommonSimType.ADULT_FOX_GHOST: CommonAge.ADULT,
        CommonSimType.ADULT_FOX_ALIEN: CommonAge.ADULT,
        CommonSimType.ADULT_FOX_MERMAID: CommonAge.ADULT,
        CommonSimType.ADULT_FOX_WITCH: CommonAge.ADULT,
        CommonSimType.ADULT_FOX_ROBOT: CommonAge.ADULT,
        CommonSimType.ADULT_FOX_SCARECROW: CommonAge.ADULT,
        CommonSimType.ADULT_FOX_SKELETON: CommonAge.ADULT,
        CommonSimType.ADULT_FOX_PLANT_SIM: CommonAge.ADULT,
        CommonSimType.ADULT_FOX_WEREWOLF: CommonAge.ADULT,
        CommonSimType.ADULT_FOX_FAIRY: CommonAge.ADULT,
        # Child
        CommonSimType.CHILD_FOX: CommonAge.CHILD,
        CommonSimType.CHILD_FOX_VAMPIRE: CommonAge.CHILD,
        CommonSimType.CHILD_FOX_GHOST: CommonAge.CHILD,
        CommonSimType.CHILD_FOX_ALIEN: CommonAge.CHILD,
        CommonSimType.CHILD_FOX_MERMAID: CommonAge.CHILD,
        CommonSimType.CHILD_FOX_WITCH: CommonAge.CHILD,
        CommonSimType.CHILD_FOX_ROBOT: CommonAge.CHILD,
        CommonSimType.CHILD_FOX_SCARECROW: CommonAge.CHILD,
        CommonSimType.CHILD_FOX_SKELETON: CommonAge.CHILD,
        CommonSimType.CHILD_FOX_PLANT_SIM: CommonAge.CHILD,
        CommonSimType.CHILD_FOX_WEREWOLF: CommonAge.CHILD,
        CommonSimType.CHILD_FOX_FAIRY: CommonAge.CHILD,

        # Horse
        # Elder
        CommonSimType.ELDER_HORSE: CommonAge.ELDER,
        CommonSimType.ELDER_HORSE_VAMPIRE: CommonAge.ELDER,
        CommonSimType.ELDER_HORSE_GHOST: CommonAge.ELDER,
        CommonSimType.ELDER_HORSE_ALIEN: CommonAge.ELDER,
        CommonSimType.ELDER_HORSE_MERMAID: CommonAge.ELDER,
        CommonSimType.ELDER_HORSE_WITCH: CommonAge.ELDER,
        CommonSimType.ELDER_HORSE_ROBOT: CommonAge.ELDER,
        CommonSimType.ELDER_HORSE_SCARECROW: CommonAge.ELDER,
        CommonSimType.ELDER_HORSE_SKELETON: CommonAge.ELDER,
        CommonSimType.ELDER_HORSE_PLANT_SIM: CommonAge.ELDER,
        CommonSimType.ELDER_HORSE_WEREWOLF: CommonAge.ELDER,
        CommonSimType.ELDER_HORSE_FAIRY: CommonAge.ELDER,
        # Adult
        CommonSimType.ADULT_HORSE: CommonAge.ADULT,
        CommonSimType.ADULT_HORSE_VAMPIRE: CommonAge.ADULT,
        CommonSimType.ADULT_HORSE_GHOST: CommonAge.ADULT,
        CommonSimType.ADULT_HORSE_ALIEN: CommonAge.ADULT,
        CommonSimType.ADULT_HORSE_MERMAID: CommonAge.ADULT,
        CommonSimType.ADULT_HORSE_WITCH: CommonAge.ADULT,
        CommonSimType.ADULT_HORSE_ROBOT: CommonAge.ADULT,
        CommonSimType.ADULT_HORSE_SCARECROW: CommonAge.ADULT,
        CommonSimType.ADULT_HORSE_SKELETON: CommonAge.ADULT,
        CommonSimType.ADULT_HORSE_PLANT_SIM: CommonAge.ADULT,
        CommonSimType.ADULT_HORSE_WEREWOLF: CommonAge.ADULT,
        CommonSimType.ADULT_HORSE_FAIRY: CommonAge.ADULT,
        # Child
        CommonSimType.CHILD_HORSE: CommonAge.CHILD,
        CommonSimType.CHILD_HORSE_VAMPIRE: CommonAge.CHILD,
        CommonSimType.CHILD_HORSE_GHOST: CommonAge.CHILD,
        CommonSimType.CHILD_HORSE_ALIEN: CommonAge.CHILD,
        CommonSimType.CHILD_HORSE_MERMAID: CommonAge.CHILD,
        CommonSimType.CHILD_HORSE_WITCH: CommonAge.CHILD,
        CommonSimType.CHILD_HORSE_ROBOT: CommonAge.CHILD,
        CommonSimType.CHILD_HORSE_SCARECROW: CommonAge.CHILD,
        CommonSimType.CHILD_HORSE_SKELETON: CommonAge.CHILD,
        CommonSimType.CHILD_HORSE_PLANT_SIM: CommonAge.CHILD,
        CommonSimType.CHILD_HORSE_WEREWOLF: CommonAge.CHILD,
        CommonSimType.CHILD_HORSE_FAIRY: CommonAge.CHILD,
    }

    _OCCULT_SIM_TYPE_TO_SPECIES_MAPPING: Dict[CommonSimType, CommonSpecies] = {
        # Human
        # Elder
        CommonSimType.ELDER_HUMAN: CommonSpecies.HUMAN,
        CommonSimType.ELDER_HUMAN_VAMPIRE: CommonSpecies.HUMAN,
        CommonSimType.ELDER_HUMAN_GHOST: CommonSpecies.HUMAN,
        CommonSimType.ELDER_HUMAN_ALIEN: CommonSpecies.HUMAN,
        CommonSimType.ELDER_HUMAN_MERMAID: CommonSpecies.HUMAN,
        CommonSimType.ELDER_HUMAN_WITCH: CommonSpecies.HUMAN,
        CommonSimType.ELDER_HUMAN_ROBOT: CommonSpecies.HUMAN,
        CommonSimType.ELDER_HUMAN_SCARECROW: CommonSpecies.HUMAN,
        CommonSimType.ELDER_HUMAN_SKELETON: CommonSpecies.HUMAN,
        CommonSimType.ELDER_HUMAN_PLANT_SIM: CommonSpecies.HUMAN,
        CommonSimType.ELDER_HUMAN_WEREWOLF: CommonSpecies.HUMAN,
        CommonSimType.ELDER_HUMAN_FAIRY: CommonSpecies.HUMAN,
        # Adult
        CommonSimType.ADULT_HUMAN: CommonSpecies.HUMAN,
        CommonSimType.ADULT_HUMAN_VAMPIRE: CommonSpecies.HUMAN,
        CommonSimType.ADULT_HUMAN_GHOST: CommonSpecies.HUMAN,
        CommonSimType.ADULT_HUMAN_ALIEN: CommonSpecies.HUMAN,
        CommonSimType.ADULT_HUMAN_MERMAID: CommonSpecies.HUMAN,
        CommonSimType.ADULT_HUMAN_WITCH: CommonSpecies.HUMAN,
        CommonSimType.ADULT_HUMAN_ROBOT: CommonSpecies.HUMAN,
        CommonSimType.ADULT_HUMAN_SCARECROW: CommonSpecies.HUMAN,
        CommonSimType.ADULT_HUMAN_SKELETON: CommonSpecies.HUMAN,
        CommonSimType.ADULT_HUMAN_PLANT_SIM: CommonSpecies.HUMAN,
        CommonSimType.ADULT_HUMAN_WEREWOLF: CommonSpecies.HUMAN,
        CommonSimType.ADULT_HUMAN_FAIRY: CommonSpecies.HUMAN,
        # Young Adult
        CommonSimType.YOUNG_ADULT_HUMAN: CommonSpecies.HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_VAMPIRE: CommonSpecies.HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_GHOST: CommonSpecies.HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_ALIEN: CommonSpecies.HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_MERMAID: CommonSpecies.HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_WITCH: CommonSpecies.HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_ROBOT: CommonSpecies.HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_SCARECROW: CommonSpecies.HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_SKELETON: CommonSpecies.HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_PLANT_SIM: CommonSpecies.HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_WEREWOLF: CommonSpecies.HUMAN,
        CommonSimType.YOUNG_ADULT_HUMAN_FAIRY: CommonSpecies.HUMAN,
        # Teen
        CommonSimType.TEEN_HUMAN: CommonSpecies.HUMAN,
        CommonSimType.TEEN_HUMAN_VAMPIRE: CommonSpecies.HUMAN,
        CommonSimType.TEEN_HUMAN_GHOST: CommonSpecies.HUMAN,
        CommonSimType.TEEN_HUMAN_ALIEN: CommonSpecies.HUMAN,
        CommonSimType.TEEN_HUMAN_MERMAID: CommonSpecies.HUMAN,
        CommonSimType.TEEN_HUMAN_WITCH: CommonSpecies.HUMAN,
        CommonSimType.TEEN_HUMAN_ROBOT: CommonSpecies.HUMAN,
        CommonSimType.TEEN_HUMAN_SCARECROW: CommonSpecies.HUMAN,
        CommonSimType.TEEN_HUMAN_SKELETON: CommonSpecies.HUMAN,
        CommonSimType.TEEN_HUMAN_PLANT_SIM: CommonSpecies.HUMAN,
        CommonSimType.TEEN_HUMAN_WEREWOLF: CommonSpecies.HUMAN,
        CommonSimType.TEEN_HUMAN_FAIRY: CommonSpecies.HUMAN,
        # Child
        CommonSimType.CHILD_HUMAN: CommonSpecies.HUMAN,
        CommonSimType.CHILD_HUMAN_VAMPIRE: CommonSpecies.HUMAN,
        CommonSimType.CHILD_HUMAN_GHOST: CommonSpecies.HUMAN,
        CommonSimType.CHILD_HUMAN_ALIEN: CommonSpecies.HUMAN,
        CommonSimType.CHILD_HUMAN_MERMAID: CommonSpecies.HUMAN,
        CommonSimType.CHILD_HUMAN_WITCH: CommonSpecies.HUMAN,
        CommonSimType.CHILD_HUMAN_ROBOT: CommonSpecies.HUMAN,
        CommonSimType.CHILD_HUMAN_SCARECROW: CommonSpecies.HUMAN,
        CommonSimType.CHILD_HUMAN_SKELETON: CommonSpecies.HUMAN,
        CommonSimType.CHILD_HUMAN_PLANT_SIM: CommonSpecies.HUMAN,
        CommonSimType.CHILD_HUMAN_WEREWOLF: CommonSpecies.HUMAN,
        CommonSimType.CHILD_HUMAN_FAIRY: CommonSpecies.HUMAN,
        # Toddler
        CommonSimType.TODDLER_HUMAN: CommonSpecies.HUMAN,
        CommonSimType.TODDLER_HUMAN_VAMPIRE: CommonSpecies.HUMAN,
        CommonSimType.TODDLER_HUMAN_GHOST: CommonSpecies.HUMAN,
        CommonSimType.TODDLER_HUMAN_ALIEN: CommonSpecies.HUMAN,
        CommonSimType.TODDLER_HUMAN_MERMAID: CommonSpecies.HUMAN,
        CommonSimType.TODDLER_HUMAN_WITCH: CommonSpecies.HUMAN,
        CommonSimType.TODDLER_HUMAN_ROBOT: CommonSpecies.HUMAN,
        CommonSimType.TODDLER_HUMAN_SCARECROW: CommonSpecies.HUMAN,
        CommonSimType.TODDLER_HUMAN_SKELETON: CommonSpecies.HUMAN,
        CommonSimType.TODDLER_HUMAN_PLANT_SIM: CommonSpecies.HUMAN,
        CommonSimType.TODDLER_HUMAN_WEREWOLF: CommonSpecies.HUMAN,
        CommonSimType.TODDLER_HUMAN_FAIRY: CommonSpecies.HUMAN,
        # Infant
        CommonSimType.INFANT_HUMAN: CommonSpecies.HUMAN,
        CommonSimType.INFANT_HUMAN_VAMPIRE: CommonSpecies.HUMAN,
        CommonSimType.INFANT_HUMAN_GHOST: CommonSpecies.HUMAN,
        CommonSimType.INFANT_HUMAN_ALIEN: CommonSpecies.HUMAN,
        CommonSimType.INFANT_HUMAN_MERMAID: CommonSpecies.HUMAN,
        CommonSimType.INFANT_HUMAN_WITCH: CommonSpecies.HUMAN,
        CommonSimType.INFANT_HUMAN_ROBOT: CommonSpecies.HUMAN,
        CommonSimType.INFANT_HUMAN_SCARECROW: CommonSpecies.HUMAN,
        CommonSimType.INFANT_HUMAN_SKELETON: CommonSpecies.HUMAN,
        CommonSimType.INFANT_HUMAN_PLANT_SIM: CommonSpecies.HUMAN,
        CommonSimType.INFANT_HUMAN_WEREWOLF: CommonSpecies.HUMAN,
        CommonSimType.INFANT_HUMAN_FAIRY: CommonSpecies.HUMAN,
        # Baby
        CommonSimType.BABY_HUMAN: CommonSpecies.HUMAN,
        CommonSimType.BABY_HUMAN_VAMPIRE: CommonSpecies.HUMAN,
        CommonSimType.BABY_HUMAN_GHOST: CommonSpecies.HUMAN,
        CommonSimType.BABY_HUMAN_ALIEN: CommonSpecies.HUMAN,
        CommonSimType.BABY_HUMAN_MERMAID: CommonSpecies.HUMAN,
        CommonSimType.BABY_HUMAN_WITCH: CommonSpecies.HUMAN,
        CommonSimType.BABY_HUMAN_ROBOT: CommonSpecies.HUMAN,
        CommonSimType.BABY_HUMAN_SCARECROW: CommonSpecies.HUMAN,
        CommonSimType.BABY_HUMAN_SKELETON: CommonSpecies.HUMAN,
        CommonSimType.BABY_HUMAN_PLANT_SIM: CommonSpecies.HUMAN,
        CommonSimType.BABY_HUMAN_WEREWOLF: CommonSpecies.HUMAN,
        CommonSimType.BABY_HUMAN_FAIRY: CommonSpecies.HUMAN,

        # Dog
        # Small Dog
        # Elder
        CommonSimType.ELDER_SMALL_DOG: CommonSpecies.SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_VAMPIRE: CommonSpecies.SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_GHOST: CommonSpecies.SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_ALIEN: CommonSpecies.SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_MERMAID: CommonSpecies.SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_WITCH: CommonSpecies.SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_ROBOT: CommonSpecies.SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_SCARECROW: CommonSpecies.SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_SKELETON: CommonSpecies.SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_PLANT_SIM: CommonSpecies.SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_WEREWOLF: CommonSpecies.SMALL_DOG,
        CommonSimType.ELDER_SMALL_DOG_FAIRY: CommonSpecies.SMALL_DOG,
        # Adult
        CommonSimType.ADULT_SMALL_DOG: CommonSpecies.SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_VAMPIRE: CommonSpecies.SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_GHOST: CommonSpecies.SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_ALIEN: CommonSpecies.SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_MERMAID: CommonSpecies.SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_WITCH: CommonSpecies.SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_ROBOT: CommonSpecies.SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_SCARECROW: CommonSpecies.SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_SKELETON: CommonSpecies.SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_PLANT_SIM: CommonSpecies.SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_WEREWOLF: CommonSpecies.SMALL_DOG,
        CommonSimType.ADULT_SMALL_DOG_FAIRY: CommonSpecies.SMALL_DOG,
        # Child
        CommonSimType.CHILD_SMALL_DOG: CommonSpecies.SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_VAMPIRE: CommonSpecies.SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_GHOST: CommonSpecies.SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_ALIEN: CommonSpecies.SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_MERMAID: CommonSpecies.SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_WITCH: CommonSpecies.SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_ROBOT: CommonSpecies.SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_SCARECROW: CommonSpecies.SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_SKELETON: CommonSpecies.SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_PLANT_SIM: CommonSpecies.SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_WEREWOLF: CommonSpecies.SMALL_DOG,
        CommonSimType.CHILD_SMALL_DOG_FAIRY: CommonSpecies.SMALL_DOG,

        # Child
        CommonSimType.CHILD_DOG: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_DOG_VAMPIRE: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_DOG_GHOST: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_DOG_ALIEN: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_DOG_MERMAID: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_DOG_WITCH: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_DOG_ROBOT: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_DOG_SCARECROW: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_DOG_SKELETON: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_DOG_PLANT_SIM: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_DOG_WEREWOLF: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_DOG_FAIRY: CommonSpecies.LARGE_DOG,

        # Large Dog
        # Elder
        CommonSimType.ELDER_LARGE_DOG: CommonSpecies.LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_VAMPIRE: CommonSpecies.LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_GHOST: CommonSpecies.LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_ALIEN: CommonSpecies.LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_MERMAID: CommonSpecies.LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_WITCH: CommonSpecies.LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_ROBOT: CommonSpecies.LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_SCARECROW: CommonSpecies.LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_SKELETON: CommonSpecies.LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_PLANT_SIM: CommonSpecies.LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_WEREWOLF: CommonSpecies.LARGE_DOG,
        CommonSimType.ELDER_LARGE_DOG_FAIRY: CommonSpecies.LARGE_DOG,
        # Adult
        CommonSimType.ADULT_LARGE_DOG: CommonSpecies.LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_VAMPIRE: CommonSpecies.LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_GHOST: CommonSpecies.LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_ALIEN: CommonSpecies.LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_MERMAID: CommonSpecies.LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_WITCH: CommonSpecies.LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_ROBOT: CommonSpecies.LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_SCARECROW: CommonSpecies.LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_SKELETON: CommonSpecies.LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_PLANT_SIM: CommonSpecies.LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_WEREWOLF: CommonSpecies.LARGE_DOG,
        CommonSimType.ADULT_LARGE_DOG_FAIRY: CommonSpecies.LARGE_DOG,
        # Child
        CommonSimType.CHILD_LARGE_DOG: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_VAMPIRE: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_GHOST: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_ALIEN: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_MERMAID: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_WITCH: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_ROBOT: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_SCARECROW: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_SKELETON: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_PLANT_SIM: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_WEREWOLF: CommonSpecies.LARGE_DOG,
        CommonSimType.CHILD_LARGE_DOG_FAIRY: CommonSpecies.LARGE_DOG,

        # Cat
        # Elder
        CommonSimType.ELDER_CAT: CommonSpecies.CAT,
        CommonSimType.ELDER_CAT_VAMPIRE: CommonSpecies.CAT,
        CommonSimType.ELDER_CAT_GHOST: CommonSpecies.CAT,
        CommonSimType.ELDER_CAT_ALIEN: CommonSpecies.CAT,
        CommonSimType.ELDER_CAT_MERMAID: CommonSpecies.CAT,
        CommonSimType.ELDER_CAT_WITCH: CommonSpecies.CAT,
        CommonSimType.ELDER_CAT_ROBOT: CommonSpecies.CAT,
        CommonSimType.ELDER_CAT_SCARECROW: CommonSpecies.CAT,
        CommonSimType.ELDER_CAT_SKELETON: CommonSpecies.CAT,
        CommonSimType.ELDER_CAT_PLANT_SIM: CommonSpecies.CAT,
        CommonSimType.ELDER_CAT_WEREWOLF: CommonSpecies.CAT,
        CommonSimType.ELDER_CAT_FAIRY: CommonSpecies.CAT,
        # Adult
        CommonSimType.ADULT_CAT: CommonSpecies.CAT,
        CommonSimType.ADULT_CAT_VAMPIRE: CommonSpecies.CAT,
        CommonSimType.ADULT_CAT_GHOST: CommonSpecies.CAT,
        CommonSimType.ADULT_CAT_ALIEN: CommonSpecies.CAT,
        CommonSimType.ADULT_CAT_MERMAID: CommonSpecies.CAT,
        CommonSimType.ADULT_CAT_WITCH: CommonSpecies.CAT,
        CommonSimType.ADULT_CAT_ROBOT: CommonSpecies.CAT,
        CommonSimType.ADULT_CAT_SCARECROW: CommonSpecies.CAT,
        CommonSimType.ADULT_CAT_SKELETON: CommonSpecies.CAT,
        CommonSimType.ADULT_CAT_PLANT_SIM: CommonSpecies.CAT,
        CommonSimType.ADULT_CAT_WEREWOLF: CommonSpecies.CAT,
        CommonSimType.ADULT_CAT_FAIRY: CommonSpecies.CAT,
        # Child
        CommonSimType.CHILD_CAT: CommonSpecies.CAT,
        CommonSimType.CHILD_CAT_VAMPIRE: CommonSpecies.CAT,
        CommonSimType.CHILD_CAT_GHOST: CommonSpecies.CAT,
        CommonSimType.CHILD_CAT_ALIEN: CommonSpecies.CAT,
        CommonSimType.CHILD_CAT_MERMAID: CommonSpecies.CAT,
        CommonSimType.CHILD_CAT_WITCH: CommonSpecies.CAT,
        CommonSimType.CHILD_CAT_ROBOT: CommonSpecies.CAT,
        CommonSimType.CHILD_CAT_SCARECROW: CommonSpecies.CAT,
        CommonSimType.CHILD_CAT_SKELETON: CommonSpecies.CAT,
        CommonSimType.CHILD_CAT_PLANT_SIM: CommonSpecies.CAT,
        CommonSimType.CHILD_CAT_WEREWOLF: CommonSpecies.CAT,
        CommonSimType.CHILD_CAT_FAIRY: CommonSpecies.CAT,

        # Fox
        # Elder
        CommonSimType.ELDER_FOX: CommonSpecies.FOX,
        CommonSimType.ELDER_FOX_VAMPIRE: CommonSpecies.FOX,
        CommonSimType.ELDER_FOX_GHOST: CommonSpecies.FOX,
        CommonSimType.ELDER_FOX_ALIEN: CommonSpecies.FOX,
        CommonSimType.ELDER_FOX_MERMAID: CommonSpecies.FOX,
        CommonSimType.ELDER_FOX_WITCH: CommonSpecies.FOX,
        CommonSimType.ELDER_FOX_ROBOT: CommonSpecies.FOX,
        CommonSimType.ELDER_FOX_SCARECROW: CommonSpecies.FOX,
        CommonSimType.ELDER_FOX_SKELETON: CommonSpecies.FOX,
        CommonSimType.ELDER_FOX_PLANT_SIM: CommonSpecies.FOX,
        CommonSimType.ELDER_FOX_WEREWOLF: CommonSpecies.FOX,
        CommonSimType.ELDER_FOX_FAIRY: CommonSpecies.FOX,
        # Adult
        CommonSimType.ADULT_FOX: CommonSpecies.FOX,
        CommonSimType.ADULT_FOX_VAMPIRE: CommonSpecies.FOX,
        CommonSimType.ADULT_FOX_GHOST: CommonSpecies.FOX,
        CommonSimType.ADULT_FOX_ALIEN: CommonSpecies.FOX,
        CommonSimType.ADULT_FOX_MERMAID: CommonSpecies.FOX,
        CommonSimType.ADULT_FOX_WITCH: CommonSpecies.FOX,
        CommonSimType.ADULT_FOX_ROBOT: CommonSpecies.FOX,
        CommonSimType.ADULT_FOX_SCARECROW: CommonSpecies.FOX,
        CommonSimType.ADULT_FOX_SKELETON: CommonSpecies.FOX,
        CommonSimType.ADULT_FOX_PLANT_SIM: CommonSpecies.FOX,
        CommonSimType.ADULT_FOX_WEREWOLF: CommonSpecies.FOX,
        CommonSimType.ADULT_FOX_FAIRY: CommonSpecies.FOX,
        # Child
        CommonSimType.CHILD_FOX: CommonSpecies.FOX,
        CommonSimType.CHILD_FOX_VAMPIRE: CommonSpecies.FOX,
        CommonSimType.CHILD_FOX_GHOST: CommonSpecies.FOX,
        CommonSimType.CHILD_FOX_ALIEN: CommonSpecies.FOX,
        CommonSimType.CHILD_FOX_MERMAID: CommonSpecies.FOX,
        CommonSimType.CHILD_FOX_WITCH: CommonSpecies.FOX,
        CommonSimType.CHILD_FOX_ROBOT: CommonSpecies.FOX,
        CommonSimType.CHILD_FOX_SCARECROW: CommonSpecies.FOX,
        CommonSimType.CHILD_FOX_SKELETON: CommonSpecies.FOX,
        CommonSimType.CHILD_FOX_PLANT_SIM: CommonSpecies.FOX,
        CommonSimType.CHILD_FOX_WEREWOLF: CommonSpecies.FOX,
        CommonSimType.CHILD_FOX_FAIRY: CommonSpecies.FOX,

        # Horse
        # Elder
        CommonSimType.ELDER_HORSE: CommonSpecies.HORSE,
        CommonSimType.ELDER_HORSE_VAMPIRE: CommonSpecies.HORSE,
        CommonSimType.ELDER_HORSE_GHOST: CommonSpecies.HORSE,
        CommonSimType.ELDER_HORSE_ALIEN: CommonSpecies.HORSE,
        CommonSimType.ELDER_HORSE_MERMAID: CommonSpecies.HORSE,
        CommonSimType.ELDER_HORSE_WITCH: CommonSpecies.HORSE,
        CommonSimType.ELDER_HORSE_ROBOT: CommonSpecies.HORSE,
        CommonSimType.ELDER_HORSE_SCARECROW: CommonSpecies.HORSE,
        CommonSimType.ELDER_HORSE_SKELETON: CommonSpecies.HORSE,
        CommonSimType.ELDER_HORSE_PLANT_SIM: CommonSpecies.HORSE,
        CommonSimType.ELDER_HORSE_WEREWOLF: CommonSpecies.HORSE,
        CommonSimType.ELDER_HORSE_FAIRY: CommonSpecies.HORSE,
        # Adult
        CommonSimType.ADULT_HORSE: CommonSpecies.HORSE,
        CommonSimType.ADULT_HORSE_VAMPIRE: CommonSpecies.HORSE,
        CommonSimType.ADULT_HORSE_GHOST: CommonSpecies.HORSE,
        CommonSimType.ADULT_HORSE_ALIEN: CommonSpecies.HORSE,
        CommonSimType.ADULT_HORSE_MERMAID: CommonSpecies.HORSE,
        CommonSimType.ADULT_HORSE_WITCH: CommonSpecies.HORSE,
        CommonSimType.ADULT_HORSE_ROBOT: CommonSpecies.HORSE,
        CommonSimType.ADULT_HORSE_SCARECROW: CommonSpecies.HORSE,
        CommonSimType.ADULT_HORSE_SKELETON: CommonSpecies.HORSE,
        CommonSimType.ADULT_HORSE_PLANT_SIM: CommonSpecies.HORSE,
        CommonSimType.ADULT_HORSE_WEREWOLF: CommonSpecies.HORSE,
        CommonSimType.ADULT_HORSE_FAIRY: CommonSpecies.HORSE,
        # Child
        CommonSimType.CHILD_HORSE: CommonSpecies.HORSE,
        CommonSimType.CHILD_HORSE_VAMPIRE: CommonSpecies.HORSE,
        CommonSimType.CHILD_HORSE_GHOST: CommonSpecies.HORSE,
        CommonSimType.CHILD_HORSE_ALIEN: CommonSpecies.HORSE,
        CommonSimType.CHILD_HORSE_MERMAID: CommonSpecies.HORSE,
        CommonSimType.CHILD_HORSE_WITCH: CommonSpecies.HORSE,
        CommonSimType.CHILD_HORSE_ROBOT: CommonSpecies.HORSE,
        CommonSimType.CHILD_HORSE_SCARECROW: CommonSpecies.HORSE,
        CommonSimType.CHILD_HORSE_SKELETON: CommonSpecies.HORSE,
        CommonSimType.CHILD_HORSE_PLANT_SIM: CommonSpecies.HORSE,
        CommonSimType.CHILD_HORSE_WEREWOLF: CommonSpecies.HORSE,
        CommonSimType.CHILD_HORSE_FAIRY: CommonSpecies.HORSE,
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
        if sim_info is None:
            raise AssertionError('Sim Info was None!')
        # noinspection PyTypeChecker
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
        if sim_info is None:
            raise AssertionError('Sim Info was None!')
        return not CommonSimTypeUtils.is_non_player_sim(sim_info)

    @staticmethod
    def is_played_sim(sim_info: SimInfo) -> bool:
        """is_played_sim(sim_info)

        Determine if a Sim is a Played Sim.

        .. note:: This does not indicate if a Sim is a Player Sim or Non Player Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Played Sim. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            raise AssertionError('Sim Info was None!')
        return sim_info.is_played_sim

    @staticmethod
    def is_service_sim(sim_info: SimInfo) -> CommonTestResult:
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
        :return: The result of testing. True, if the Sim is a Service Sim. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Sim Info was None!')
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
        return CommonTraitUtils.has_any_traits(sim_info, trait_ids)

    @staticmethod
    def is_batuu_alien(sim_info: SimInfo) -> CommonTestResult:
        """Determine if a Sim is a Batuu Alien.

        .. note::

            Alien Sims:

            - Bith
            - Twilek
            - Weequay
            - Abednedo
            - Mirialan
            - Zabrak

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is a Batuu Alien. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Sim Info was None!')
        from sims4communitylib.enums.traits_enum import CommonTraitId
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        trait_ids = (
            CommonTraitId.BATUU_ALIEN_BITH,  # trait_Batuu_Alien_Bith
            CommonTraitId.BATUU_ALIEN_TWILEK,  # trait_Batuu_Alien_Twilek
            CommonTraitId.BATUU_ALIEN_WEEQUAY,  # trait_Batuu_Alien_Weequay
            CommonTraitId.BATUU_ALIEN_ABEDNEDO,  # trait_Batuu_Alien_Abednedo
            CommonTraitId.BATUU_ALIEN_MIRIALAN,  # trait_Batuu_Alien_Mirialan
            CommonTraitId.BATUU_ALIEN_ZABRAK,  # trait_Batuu_Alien_Zabrak
        )
        return CommonTraitUtils.has_any_traits(sim_info, trait_ids)

    @staticmethod
    def is_occult(sim_info: SimInfo, combine_teen_young_adult_and_elder_age: bool = True, combine_child_dog_types: bool = True) -> bool:
        """is_occult(sim_info, combine_teen_young_adult_and_elder_age=True, combine_child_dog_types=True)

        Determine if a Sim has an Occult Sim Type.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param combine_teen_young_adult_and_elder_age: See description of CommonSimTypeUtils.determine_sim_type. Default is True.
        :type combine_teen_young_adult_and_elder_age: bool, optional
        :param combine_child_dog_types: See description of CommonSimTypeUtils.determine_sim_type. Default is True.
        :type combine_child_dog_types: bool, optional
        :return: True, if the specified Sim has an Occult Sim Type. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            raise AssertionError('Sim Info was None!')
        sim_type = CommonSimTypeUtils.determine_sim_type(
            sim_info,
            combine_teen_young_adult_and_elder_age=combine_teen_young_adult_and_elder_age,
            combine_child_dog_types=combine_child_dog_types
        )
        return CommonSimTypeUtils.is_occult_type(sim_type)

    @staticmethod
    def is_occult_type(sim_type: CommonSimType) -> bool:
        """is_occult_type(sim_type)

        Determine if a Sim Type is for an Occult Sim.

        :param sim_type: A Sim Type.
        :type sim_type: CommonSimType
        :return: True, if the Sim Type is for an Occult Sim. False, if not.
        :rtype: bool
        """
        # If the sim_type is an Occult, it will change to its Human variant, thus making them not equal and proving it was an occult. If the sim type is Human, it will not change.
        return CommonSimTypeUtils.convert_to_non_occult_variant(sim_type) != sim_type

    @staticmethod
    def get_all_sim_types_gen(sim_info: SimInfo, combine_teen_young_adult_and_elder_age: bool = True, combine_child_dog_types: bool = True) -> Iterator[CommonSimType]:
        """get_all_sim_types_gen(sim_info, combine_teen_young_adult_and_elder_age=True, combine_child_dog_types=True)

        Determine all types a Sim is based on their Age, Species, and Occult Types.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param combine_teen_young_adult_and_elder_age: If set to True, Teen, Young Adult, Adult, and Elder, will all receive an ADULT denoted Sim Type instead of TEEN, YOUNG_ADULT, ADULT, and ELDER respectively. i.e. A Human Teen Sim would be denoted as ADULT_HUMAN.
            If set to False, they will receive their own Sim Types. i.e. A Human Teen Sim would be denoted as TEEN_HUMAN. Default is True.
        :type combine_teen_young_adult_and_elder_age: bool, optional
        :param combine_child_dog_types: If set to True, the Child Dog Sim Types will be combined into a single Sim Type, i.e. CHILD_DOG. If set to False, the Child Dog Sim Types will be returned as their more specific values. i.e. CHILD_LARGE_DOG, CHILD_SMALL_DOG, etc. Default is True.
        :type combine_child_dog_types: bool, optional
        :return: An iterator of all types the Sim is.
        :rtype: Iterator[CommonSimType]
        """
        if sim_info is None:
            raise AssertionError('Sim Info was None!')
        species = CommonSpecies.get_species(sim_info)
        age = CommonAge.get_age(sim_info)
        from sims4communitylib.utils.sims.common_sim_occult_type_utils import CommonSimOccultTypeUtils
        for occult_type in CommonSimOccultTypeUtils.get_all_occult_types_for_sim_gen(sim_info):
            if CommonOccultUtils.is_robot(sim_info) and occult_type == CommonOccultType.NON_OCCULT:
                continue
            yield CommonSimTypeUtils.determine_sim_type_for_species_age_occult(species, age, occult_type, combine_teen_young_adult_and_elder_age=combine_teen_young_adult_and_elder_age, combine_child_dog_types=combine_child_dog_types)

    @staticmethod
    def determine_sim_type(
        sim_info: SimInfo,
        combine_teen_young_adult_and_elder_age: bool = True,
        combine_child_dog_types: bool = True,
        use_current_occult_type: bool = False
    ) -> CommonSimType:
        """determine_sim_type(sim_info, combine_teen_young_adult_and_elder_age=True, combine_child_dog_types=True, use_current_occult_type=False)

        Determine the type of Sim a Sim is based on their Age, Species, and Occult Type.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param combine_teen_young_adult_and_elder_age: If set to True, Teen, Young Adult, Adult, and Elder, will all receive an ADULT denoted Sim Type instead of TEEN, YOUNG_ADULT, ADULT, and ELDER respectively. i.e. A Human Teen Sim would be denoted as ADULT_HUMAN.
            If set to False, they will receive their own Sim Types. i.e. A Human Teen Sim would be denoted as TEEN_HUMAN. Default is True.
        :type combine_teen_young_adult_and_elder_age: bool, optional
        :param combine_child_dog_types: If set to True, the Child Dog Sim Types will be combined into a single Sim Type, i.e. CHILD_DOG. If set to False, the Child Dog Sim Types will be returned as their more specific values. i.e. CHILD_LARGE_DOG, CHILD_SMALL_DOG, etc. Default is True.
        :type combine_child_dog_types: bool, optional
        :param use_current_occult_type: If set to True, the Sims current occult type will be used, for example an Adult Human Mermaid with no tail would return ADULT_HUMAN instead of ADULT_HUMAN_MERMAID. If set to False, the Sims occult type will be used (whether current or not), for example an Adult Human Mermaid wearing or not wearing their tail would return ADULT_HUMAN_MERMAID. Default is False.
        :param use_current_occult_type: bool, optional
        :return: The type of Sim the Sim is or NONE if no type was found for the Sim.
        :rtype: CommonSimType
        """
        if sim_info is None:
            raise AssertionError('Sim Info was None!')
        species = CommonSpecies.get_species(sim_info)
        age = CommonAge.get_age(sim_info)
        if use_current_occult_type:
            occult_type = CommonOccultType.determine_current_occult_type(sim_info)
        else:
            occult_type = CommonOccultType.determine_occult_type(sim_info)
        sim_type = CommonSimTypeUtils.determine_sim_type_for_species_age_occult(species, age, occult_type, combine_teen_young_adult_and_elder_age=combine_teen_young_adult_and_elder_age, combine_child_dog_types=combine_child_dog_types)
        return sim_type

    @staticmethod
    def determine_sim_type_for_species_age_occult(
        species: CommonSpecies,
        age: CommonAge,
        occult_type: CommonOccultType,
        combine_teen_young_adult_and_elder_age: bool = True,
        combine_child_dog_types: bool = True
    ) -> CommonSimType:
        """determine_sim_type_for_species_age_occult(\
            species,\
            age,\
            occult_type,\
            combine_teen_young_adult_and_elder_age=True,\
            combine_child_dog_types=True,\
            use_current_occult_type=False\
        )

        Determine the type of Sim a Sim is based on their Age, Species, and Occult Type.

        :param species: A CommonSpecies.
        :type species: CommonSpecies
        :param age: An Age.
        :type age: CommonAge
        :param occult_type: An Occult Type.
        :type occult_type: CommonOccultType
        :param combine_teen_young_adult_and_elder_age: If set to True, Teen, Young Adult, Adult, and Elder, will all receive an ADULT denoted Sim Type instead of TEEN, YOUNG_ADULT, ADULT, and ELDER respectively. i.e. If True, a Human Teen Sim would be denoted as ADULT_HUMAN.
        If set to False, they will receive their own Sim Types. i.e. If False, a Human Teen Sim would be denoted as TEEN_HUMAN. Default is True.
        :type combine_teen_young_adult_and_elder_age: bool, optional
        :param combine_child_dog_types: If set to True, the Child Dog Sim Types will be combined into a single Sim Type, i.e. CHILD_DOG. If set to False, the Child Dog Sim Types will be returned as their more specific values. i.e. CHILD_LARGE_DOG, CHILD_SMALL_DOG, etc. Default is True.
        :type combine_child_dog_types: bool, optional
        :return: The type of Sim the Sim is or CommonSimType.NONE if no type was found for the Sim.
        :rtype: CommonSimType
        """
        if age is None or species is None or occult_type is None:
            return CommonSimType.NONE

        if combine_teen_young_adult_and_elder_age and age in (CommonAge.TEEN, CommonAge.YOUNGADULT, CommonAge.ADULT, CommonAge.ELDER):
            age = CommonAge.ADULT

        if species not in CommonSimTypeUtils._SIM_TO_SIM_TYPE_MAPPING\
                or age not in CommonSimTypeUtils._SIM_TO_SIM_TYPE_MAPPING[species]\
                or occult_type not in CommonSimTypeUtils._SIM_TO_SIM_TYPE_MAPPING[species][age]:
            return CommonSimType.NONE

        sim_type = CommonSimTypeUtils._SIM_TO_SIM_TYPE_MAPPING[species][age][occult_type]
        if combine_child_dog_types and sim_type in CommonSimTypeUtils._CHILD_DOG_SIM_TYPE_MAPPING:
            return CommonSimTypeUtils._CHILD_DOG_SIM_TYPE_MAPPING[sim_type]
        return sim_type

    @staticmethod
    def convert_sim_type_to_occult_type(sim_type: CommonSimType) -> CommonOccultType:
        """convert_sim_type_to_occult_type(sim_type)

        Break down a Sim Type and return the resulting Occult Type associated with it.

        :param sim_type: A Sim Type.
        :type sim_type: CommonSimType
        :return: The occult type associated with the Sim Type.
        :rtype: CommonOccultType
        """
        return CommonSimTypeUtils._OCCULT_SIM_TYPE_TO_OCCULT_TYPE_MAPPING.get(sim_type, CommonOccultType.NONE)

    @staticmethod
    def convert_sim_type_to_age(sim_type: CommonSimType) -> CommonAge:
        """convert_sim_type_to_age(sim_type)

        Break down a Sim Type and return the resulting Age associated with it.

        :param sim_type: A Sim Type.
        :type sim_type: CommonSimType
        :return: The age associated with the Sim Type.
        :rtype: CommonAge
        """
        return CommonSimTypeUtils._OCCULT_SIM_TYPE_TO_AGE_MAPPING.get(sim_type, CommonAge.INVALID)

    @staticmethod
    def convert_sim_type_to_species(sim_type: CommonSimType) -> CommonSpecies:
        """convert_sim_type_to_species(sim_type)

        Break down a Sim Type and return the resulting Species associated with it.

        :param sim_type: A Sim Type.
        :type sim_type: CommonSimType
        :return: The species associated with the Sim Type.
        :rtype: CommonSpecies
        """
        return CommonSimTypeUtils._OCCULT_SIM_TYPE_TO_SPECIES_MAPPING.get(sim_type, CommonSpecies.INVALID)

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


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_sim_types',
    'Print a list of all Sim Types a Sim matches to.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to check.', is_optional=True, default_value='Active Sim'),
        CommonConsoleCommandArgument('combine_teen_young_adult_and_elder_age', 'True or False', 'If True, Teen, Young Adult, and Elder will come out with the same Sim Type as an Adult Sim would. (No effect on Sims that do not fall into these ages)', is_optional=True, default_value=False),
        CommonConsoleCommandArgument('combine_child_dog_types', 'True or False', 'If True, Child Small Dog and Child Large Dog will come out as a singular Sim Type of Child Dog. (No effect on Sims that are not Child Dogs)', is_optional=True, default_value=False),
    ),
)
def _common_print_sim_types_for_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo = None, combine_teen_young_adult_and_elder_age: bool = False, combine_child_dog_types: bool = False):
    if sim_info is None:
        return
    output(f'Printing all Sim Types of Sim {sim_info}:')
    for sim_type in CommonSimTypeUtils.get_all_sim_types_gen(sim_info, combine_teen_young_adult_and_elder_age=combine_teen_young_adult_and_elder_age, combine_child_dog_types=combine_child_dog_types):
        sim_type_name = sim_type.name
        output(f'- {sim_type_name}')
