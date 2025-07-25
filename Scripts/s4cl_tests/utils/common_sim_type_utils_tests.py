"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.common_occult_type import CommonOccultType
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.enums.sim_type import CommonSimType
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService
from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils


@CommonTestService.test_class(ModInfo.get_identity())
class _CommonSimTypeUtilsTests:
    @staticmethod
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.NONE, True)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_HUMAN, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_HUMAN_VAMPIRE, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_HUMAN_GHOST, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_HUMAN_ALIEN, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_HUMAN_MERMAID, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_HUMAN_WITCH, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_HUMAN_ROBOT, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_HUMAN_SCARECROW, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_HUMAN_WEREWOLF, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_SMALL_DOG, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_SMALL_DOG_VAMPIRE, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_SMALL_DOG_GHOST, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_SMALL_DOG_ALIEN, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_SMALL_DOG_MERMAID, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_SMALL_DOG_WITCH, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_SMALL_DOG_ROBOT, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_SMALL_DOG_SCARECROW, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_SMALL_DOG_WEREWOLF, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_LARGE_DOG, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_LARGE_DOG_VAMPIRE, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_LARGE_DOG_GHOST, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_LARGE_DOG_ALIEN, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_LARGE_DOG_MERMAID, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_LARGE_DOG_WITCH, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_LARGE_DOG_ROBOT, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_LARGE_DOG_SCARECROW, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_LARGE_DOG_WEREWOLF, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_CAT, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_CAT_VAMPIRE, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_CAT_GHOST, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_CAT_ALIEN, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_CAT_MERMAID, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_CAT_WITCH, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_CAT_ROBOT, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_CAT_SCARECROW, False)
    @CommonTestService.test(CommonSimType.NONE, CommonSimType.ADULT_CAT_WEREWOLF, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_HUMAN, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_HUMAN_VAMPIRE, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN_VAMPIRE, CommonSimType.ADULT_HUMAN_VAMPIRE, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_HUMAN_GHOST, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN_GHOST, CommonSimType.ADULT_HUMAN_GHOST, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_HUMAN_ALIEN, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN_ALIEN, CommonSimType.ADULT_HUMAN_ALIEN, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_HUMAN_MERMAID, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN_MERMAID, CommonSimType.ADULT_HUMAN_MERMAID, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_HUMAN_WITCH, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN_WITCH, CommonSimType.ADULT_HUMAN_WITCH, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_HUMAN_ROBOT, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN_ROBOT, CommonSimType.ADULT_HUMAN_ROBOT, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_HUMAN_SCARECROW, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN_SCARECROW, CommonSimType.ADULT_HUMAN_SCARECROW, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_HUMAN_WEREWOLF, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN_WEREWOLF, CommonSimType.ADULT_HUMAN_WEREWOLF, True)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_SMALL_DOG, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_SMALL_DOG_VAMPIRE, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_SMALL_DOG_GHOST, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_SMALL_DOG_ALIEN, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_SMALL_DOG_MERMAID, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_SMALL_DOG_WITCH, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_SMALL_DOG_ROBOT, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_SMALL_DOG_SCARECROW, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_SMALL_DOG_WEREWOLF, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_LARGE_DOG, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_LARGE_DOG_VAMPIRE, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_LARGE_DOG_GHOST, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_LARGE_DOG_ALIEN, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_LARGE_DOG_MERMAID, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_LARGE_DOG_WITCH, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_LARGE_DOG_ROBOT, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_LARGE_DOG_SCARECROW, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_LARGE_DOG_WEREWOLF, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_CAT, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_CAT_VAMPIRE, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_CAT_GHOST, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_CAT_ALIEN, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_CAT_MERMAID, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_CAT_WITCH, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_CAT_ROBOT, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_CAT_SCARECROW, False)
    @CommonTestService.test(CommonSimType.ADULT_HUMAN, CommonSimType.ADULT_CAT_WEREWOLF, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_SMALL_DOG, True)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_SMALL_DOG_VAMPIRE, True)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_SMALL_DOG_GHOST, True)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_SMALL_DOG_ALIEN, True)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_SMALL_DOG_MERMAID, True)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_SMALL_DOG_WITCH, True)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_SMALL_DOG_ROBOT, True)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_SMALL_DOG_SCARECROW, True)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_SMALL_DOG_WEREWOLF, True)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_LARGE_DOG, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_LARGE_DOG_VAMPIRE, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_LARGE_DOG_GHOST, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_LARGE_DOG_ALIEN, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_LARGE_DOG_MERMAID, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_LARGE_DOG_WITCH, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_LARGE_DOG_ROBOT, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_LARGE_DOG_SCARECROW, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_LARGE_DOG_WEREWOLF, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_CAT, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_CAT_VAMPIRE, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_CAT_GHOST, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_CAT_ALIEN, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_CAT_MERMAID, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_CAT_WITCH, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_CAT_ROBOT, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_CAT_SCARECROW, False)
    @CommonTestService.test(CommonSimType.ADULT_SMALL_DOG, CommonSimType.ADULT_CAT_WEREWOLF, False)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_LARGE_DOG, True)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_LARGE_DOG_VAMPIRE, True)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_LARGE_DOG_GHOST, True)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_LARGE_DOG_ALIEN, True)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_LARGE_DOG_MERMAID, True)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_LARGE_DOG_WITCH, True)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_LARGE_DOG_ROBOT, True)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_LARGE_DOG_SCARECROW, True)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_LARGE_DOG_WEREWOLF, True)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_CAT, False)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_CAT_VAMPIRE, False)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_CAT_GHOST, False)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_CAT_ALIEN, False)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_CAT_MERMAID, False)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_CAT_WITCH, False)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_CAT_ROBOT, False)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_CAT_SCARECROW, False)
    @CommonTestService.test(CommonSimType.ADULT_LARGE_DOG, CommonSimType.ADULT_CAT_WEREWOLF, False)
    @CommonTestService.test(CommonSimType.ADULT_CAT, CommonSimType.ADULT_CAT, True)
    @CommonTestService.test(CommonSimType.ADULT_CAT, CommonSimType.ADULT_CAT_VAMPIRE, True)
    @CommonTestService.test(CommonSimType.ADULT_CAT, CommonSimType.ADULT_CAT_GHOST, True)
    @CommonTestService.test(CommonSimType.ADULT_CAT, CommonSimType.ADULT_CAT_ALIEN, True)
    @CommonTestService.test(CommonSimType.ADULT_CAT, CommonSimType.ADULT_CAT_MERMAID, True)
    @CommonTestService.test(CommonSimType.ADULT_CAT, CommonSimType.ADULT_CAT_WITCH, True)
    @CommonTestService.test(CommonSimType.ADULT_CAT, CommonSimType.ADULT_CAT_ROBOT, True)
    @CommonTestService.test(CommonSimType.ADULT_CAT, CommonSimType.ADULT_CAT_SCARECROW, True)
    @CommonTestService.test(CommonSimType.ADULT_CAT, CommonSimType.ADULT_CAT_WEREWOLF, True)
    @CommonTestService.test(CommonSimType.ADULT_FOX, CommonSimType.ADULT_FOX, True)
    @CommonTestService.test(CommonSimType.ADULT_FOX, CommonSimType.ADULT_FOX_VAMPIRE, True)
    @CommonTestService.test(CommonSimType.ADULT_FOX, CommonSimType.ADULT_FOX_GHOST, True)
    @CommonTestService.test(CommonSimType.ADULT_FOX, CommonSimType.ADULT_FOX_ALIEN, True)
    @CommonTestService.test(CommonSimType.ADULT_FOX, CommonSimType.ADULT_FOX_MERMAID, True)
    @CommonTestService.test(CommonSimType.ADULT_FOX, CommonSimType.ADULT_FOX_WITCH, True)
    @CommonTestService.test(CommonSimType.ADULT_FOX, CommonSimType.ADULT_FOX_ROBOT, True)
    @CommonTestService.test(CommonSimType.ADULT_FOX, CommonSimType.ADULT_FOX_SCARECROW, True)
    @CommonTestService.test(CommonSimType.ADULT_FOX, CommonSimType.ADULT_FOX_WEREWOLF, True)
    def _s4cl_sim_types_are_same_age_and_species(sim_type_one: CommonSimType, sim_type_two: CommonSimType, expected_result: bool) -> None:
        result = CommonSimTypeUtils.are_same_age_and_species(sim_type_one, sim_type_two)
        CommonAssertionUtils.are_equal(result, expected_result, 'Sim Types were not considered similar when they should be. {} and {}'.format(sim_type_one.name, sim_type_two.name) if expected_result else 'Sim Types were considered similar when they should not be. {} and {}'.format(sim_type_one.name, sim_type_two.name))

    @staticmethod
    @CommonTestService.test(CommonSpecies.HUMAN, CommonAge.ADULT, CommonOccultType.NON_OCCULT, CommonSimType.ADULT_HUMAN)
    @CommonTestService.test(CommonSpecies.HUMAN, CommonAge.ADULT, CommonOccultType.VAMPIRE, CommonSimType.ADULT_HUMAN_VAMPIRE)
    @CommonTestService.test(CommonSpecies.HUMAN, CommonAge.ADULT, CommonOccultType.GHOST, CommonSimType.ADULT_HUMAN_GHOST)
    @CommonTestService.test(CommonSpecies.HUMAN, CommonAge.ADULT, CommonOccultType.ALIEN, CommonSimType.ADULT_HUMAN_ALIEN)
    @CommonTestService.test(CommonSpecies.HUMAN, CommonAge.ADULT, CommonOccultType.FAIRY, CommonSimType.ADULT_HUMAN_FAIRY)
    @CommonTestService.test(CommonSpecies.HUMAN, CommonAge.ADULT, CommonOccultType.MERMAID, CommonSimType.ADULT_HUMAN_MERMAID)
    @CommonTestService.test(CommonSpecies.HUMAN, CommonAge.ADULT, CommonOccultType.WITCH, CommonSimType.ADULT_HUMAN_WITCH)
    @CommonTestService.test(CommonSpecies.HUMAN, CommonAge.ADULT, CommonOccultType.ROBOT, CommonSimType.ADULT_HUMAN_ROBOT)
    @CommonTestService.test(CommonSpecies.HUMAN, CommonAge.ADULT, CommonOccultType.SCARECROW, CommonSimType.ADULT_HUMAN_SCARECROW)
    @CommonTestService.test(CommonSpecies.HUMAN, CommonAge.ADULT, CommonOccultType.WEREWOLF, CommonSimType.ADULT_HUMAN_WEREWOLF)
    @CommonTestService.test(CommonSpecies.SMALL_DOG, CommonAge.ADULT, CommonOccultType.NON_OCCULT, CommonSimType.ADULT_SMALL_DOG)
    @CommonTestService.test(CommonSpecies.SMALL_DOG, CommonAge.ADULT, CommonOccultType.VAMPIRE, CommonSimType.ADULT_SMALL_DOG_VAMPIRE)
    @CommonTestService.test(CommonSpecies.SMALL_DOG, CommonAge.ADULT, CommonOccultType.GHOST, CommonSimType.ADULT_SMALL_DOG_GHOST)
    @CommonTestService.test(CommonSpecies.SMALL_DOG, CommonAge.ADULT, CommonOccultType.ALIEN, CommonSimType.ADULT_SMALL_DOG_ALIEN)
    @CommonTestService.test(CommonSpecies.SMALL_DOG, CommonAge.ADULT, CommonOccultType.FAIRY, CommonSimType.ADULT_SMALL_DOG_FAIRY)
    @CommonTestService.test(CommonSpecies.SMALL_DOG, CommonAge.ADULT, CommonOccultType.MERMAID, CommonSimType.ADULT_SMALL_DOG_MERMAID)
    @CommonTestService.test(CommonSpecies.SMALL_DOG, CommonAge.ADULT, CommonOccultType.WITCH, CommonSimType.ADULT_SMALL_DOG_WITCH)
    @CommonTestService.test(CommonSpecies.SMALL_DOG, CommonAge.ADULT, CommonOccultType.ROBOT, CommonSimType.ADULT_SMALL_DOG_ROBOT)
    @CommonTestService.test(CommonSpecies.SMALL_DOG, CommonAge.ADULT, CommonOccultType.SCARECROW, CommonSimType.ADULT_SMALL_DOG_SCARECROW)
    @CommonTestService.test(CommonSpecies.SMALL_DOG, CommonAge.ADULT, CommonOccultType.WEREWOLF, CommonSimType.ADULT_SMALL_DOG_WEREWOLF)
    @CommonTestService.test(CommonSpecies.LARGE_DOG, CommonAge.ADULT, CommonOccultType.NON_OCCULT, CommonSimType.ADULT_LARGE_DOG)
    @CommonTestService.test(CommonSpecies.LARGE_DOG, CommonAge.ADULT, CommonOccultType.VAMPIRE, CommonSimType.ADULT_LARGE_DOG_VAMPIRE)
    @CommonTestService.test(CommonSpecies.LARGE_DOG, CommonAge.ADULT, CommonOccultType.GHOST, CommonSimType.ADULT_LARGE_DOG_GHOST)
    @CommonTestService.test(CommonSpecies.LARGE_DOG, CommonAge.ADULT, CommonOccultType.ALIEN, CommonSimType.ADULT_LARGE_DOG_ALIEN)
    @CommonTestService.test(CommonSpecies.LARGE_DOG, CommonAge.ADULT, CommonOccultType.FAIRY, CommonSimType.ADULT_LARGE_DOG_FAIRY)
    @CommonTestService.test(CommonSpecies.LARGE_DOG, CommonAge.ADULT, CommonOccultType.MERMAID, CommonSimType.ADULT_LARGE_DOG_MERMAID)
    @CommonTestService.test(CommonSpecies.LARGE_DOG, CommonAge.ADULT, CommonOccultType.WITCH, CommonSimType.ADULT_LARGE_DOG_WITCH)
    @CommonTestService.test(CommonSpecies.LARGE_DOG, CommonAge.ADULT, CommonOccultType.ROBOT, CommonSimType.ADULT_LARGE_DOG_ROBOT)
    @CommonTestService.test(CommonSpecies.LARGE_DOG, CommonAge.ADULT, CommonOccultType.SCARECROW, CommonSimType.ADULT_LARGE_DOG_SCARECROW)
    @CommonTestService.test(CommonSpecies.LARGE_DOG, CommonAge.ADULT, CommonOccultType.WEREWOLF, CommonSimType.ADULT_LARGE_DOG_WEREWOLF)
    @CommonTestService.test(CommonSpecies.CAT, CommonAge.ADULT, CommonOccultType.NON_OCCULT, CommonSimType.ADULT_CAT)
    @CommonTestService.test(CommonSpecies.CAT, CommonAge.ADULT, CommonOccultType.VAMPIRE, CommonSimType.ADULT_CAT_VAMPIRE)
    @CommonTestService.test(CommonSpecies.CAT, CommonAge.ADULT, CommonOccultType.GHOST, CommonSimType.ADULT_CAT_GHOST)
    @CommonTestService.test(CommonSpecies.CAT, CommonAge.ADULT, CommonOccultType.ALIEN, CommonSimType.ADULT_CAT_ALIEN)
    @CommonTestService.test(CommonSpecies.CAT, CommonAge.ADULT, CommonOccultType.FAIRY, CommonSimType.ADULT_CAT_FAIRY)
    @CommonTestService.test(CommonSpecies.CAT, CommonAge.ADULT, CommonOccultType.MERMAID, CommonSimType.ADULT_CAT_MERMAID)
    @CommonTestService.test(CommonSpecies.CAT, CommonAge.ADULT, CommonOccultType.WITCH, CommonSimType.ADULT_CAT_WITCH)
    @CommonTestService.test(CommonSpecies.CAT, CommonAge.ADULT, CommonOccultType.ROBOT, CommonSimType.ADULT_CAT_ROBOT)
    @CommonTestService.test(CommonSpecies.CAT, CommonAge.ADULT, CommonOccultType.SCARECROW, CommonSimType.ADULT_CAT_SCARECROW)
    @CommonTestService.test(CommonSpecies.CAT, CommonAge.ADULT, CommonOccultType.WEREWOLF, CommonSimType.ADULT_CAT_WEREWOLF)
    @CommonTestService.test(CommonSpecies.FOX, CommonAge.ADULT, CommonOccultType.NON_OCCULT, CommonSimType.ADULT_FOX)
    @CommonTestService.test(CommonSpecies.FOX, CommonAge.ADULT, CommonOccultType.VAMPIRE, CommonSimType.ADULT_FOX_VAMPIRE)
    @CommonTestService.test(CommonSpecies.FOX, CommonAge.ADULT, CommonOccultType.GHOST, CommonSimType.ADULT_FOX_GHOST)
    @CommonTestService.test(CommonSpecies.FOX, CommonAge.ADULT, CommonOccultType.ALIEN, CommonSimType.ADULT_FOX_ALIEN)
    @CommonTestService.test(CommonSpecies.FOX, CommonAge.ADULT, CommonOccultType.FAIRY, CommonSimType.ADULT_FOX_FAIRY)
    @CommonTestService.test(CommonSpecies.FOX, CommonAge.ADULT, CommonOccultType.MERMAID, CommonSimType.ADULT_FOX_MERMAID)
    @CommonTestService.test(CommonSpecies.FOX, CommonAge.ADULT, CommonOccultType.WITCH, CommonSimType.ADULT_FOX_WITCH)
    @CommonTestService.test(CommonSpecies.FOX, CommonAge.ADULT, CommonOccultType.ROBOT, CommonSimType.ADULT_FOX_ROBOT)
    @CommonTestService.test(CommonSpecies.FOX, CommonAge.ADULT, CommonOccultType.SCARECROW, CommonSimType.ADULT_FOX_SCARECROW)
    @CommonTestService.test(CommonSpecies.FOX, CommonAge.ADULT, CommonOccultType.WEREWOLF, CommonSimType.ADULT_FOX_WEREWOLF)
    @CommonTestService.test(CommonSpecies.HORSE, CommonAge.ADULT, CommonOccultType.NON_OCCULT, CommonSimType.ADULT_HORSE)
    @CommonTestService.test(CommonSpecies.HORSE, CommonAge.ADULT, CommonOccultType.VAMPIRE, CommonSimType.ADULT_HORSE_VAMPIRE)
    @CommonTestService.test(CommonSpecies.HORSE, CommonAge.ADULT, CommonOccultType.GHOST, CommonSimType.ADULT_HORSE_GHOST)
    @CommonTestService.test(CommonSpecies.HORSE, CommonAge.ADULT, CommonOccultType.ALIEN, CommonSimType.ADULT_HORSE_ALIEN)
    @CommonTestService.test(CommonSpecies.HORSE, CommonAge.ADULT, CommonOccultType.FAIRY, CommonSimType.ADULT_HORSE_FAIRY)
    @CommonTestService.test(CommonSpecies.HORSE, CommonAge.ADULT, CommonOccultType.MERMAID, CommonSimType.ADULT_HORSE_MERMAID)
    @CommonTestService.test(CommonSpecies.HORSE, CommonAge.ADULT, CommonOccultType.WITCH, CommonSimType.ADULT_HORSE_WITCH)
    @CommonTestService.test(CommonSpecies.HORSE, CommonAge.ADULT, CommonOccultType.ROBOT, CommonSimType.ADULT_HORSE_ROBOT)
    @CommonTestService.test(CommonSpecies.HORSE, CommonAge.ADULT, CommonOccultType.SCARECROW, CommonSimType.ADULT_HORSE_SCARECROW)
    @CommonTestService.test(CommonSpecies.HORSE, CommonAge.ADULT, CommonOccultType.WEREWOLF, CommonSimType.ADULT_HORSE_WEREWOLF)
    def _s4cl_determine_sim_type(species: CommonSpecies, age: CommonAge, occult_type: CommonOccultType, expected_sim_type: CommonSimType):
        result = CommonSimTypeUtils.determine_sim_type_for_species_age_occult(species, age, occult_type)
        CommonAssertionUtils.are_equal(result, expected_sim_type)
