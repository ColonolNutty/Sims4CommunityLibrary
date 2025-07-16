"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonMotiveId(CommonInt):
    """Identifiers for vanilla sim motives.

    """
    INVALID: 'CommonMotiveId' = 0
    BLADDER: 'CommonMotiveId' = 16652  # motive_Bladder
    ANIMAL_FOX_BLADDER: 'CommonMotiveId' = 270467  # commodity_Motive_Fox_Bladder
    PET_CAT_BLADDER: 'CommonMotiveId' = 151036  # commodity_Motive_PetCat_Bladder
    PET_DOG_BLADDER: 'CommonMotiveId' = 151032  # commodity_Motive_PetDog_Bladder
    PET_HORSE_BLADDER: 'CommonMotiveId' = 312267  # motive_Horse_Bladder
    # This motive doesn't actually exist, it is used when mapping motives. The value is arbitrary.
    BOWEL: 'CommonMotiveId' = INVALID
    PET_CAT_BOWEL: 'CommonMotiveId' = 157949  # commodity_Motive_PetCat_Bowel
    PET_DOG_BOWEL: 'CommonMotiveId' = 158698  # commodity_Motive_PetDog_Bowel
    ENERGY: 'CommonMotiveId' = 16654  # motive_Energy
    PET_CAT_ENERGY: 'CommonMotiveId' = 151037  # commodity_Motive_PetCat_Energy
    PET_DOG_ENERGY: 'CommonMotiveId' = 151033  # commodity_Motive_PetDog_Energy
    PET_HORSE_ENERGY: 'CommonMotiveId' = 312266  # motive_Horse_Energy
    SERVO_CHARGE: 'CommonMotiveId' = 218484  # motive_Robots_Charge
    FUN: 'CommonMotiveId' = 16655  # motive_Fun
    PET_CAT_PLAY: 'CommonMotiveId' = 157718  # commodity_Motive_PetCat_Play
    PET_DOG_PLAY: 'CommonMotiveId' = 158699  # commodity_Motive_PetDog_Play
    PET_HORSE_FUN: 'CommonMotiveId' = 312268  # motive_Horse_Fun
    HUNGER: 'CommonMotiveId' = 16656  # motive_Hunger
    PET_CAT_HUNGER: 'CommonMotiveId' = 151035  # commodity_Motive_PetCat_Hunger
    PET_DOG_HUNGER: 'CommonMotiveId' = 151031  # commodity_Motive_PetDog_Hunger
    PET_HORSE_HUNGER: 'CommonMotiveId' = 312265  # motive_Horse_Hunger
    HYGIENE: 'CommonMotiveId' = 16657  # motive_Hygiene
    ANIMAL_FOX_HYGIENE: 'CommonMotiveId' = 270701  # motive_Hygiene_Fox
    PET_CAT_HYGIENE: 'CommonMotiveId' = 157055  # commodity_Motive_PetCat_Hygiene
    PET_DOG_HYGIENE: 'CommonMotiveId' = 157056  # commodity_Motive_PetDog_Hygiene
    PET_HORSE_HYGIENE: 'CommonMotiveId' = 312269  # motive_Horse_Hygiene
    SOCIAL: 'CommonMotiveId' = 16658  # motive_Social
    PET_CAT_AFFECTION: 'CommonMotiveId' = 151038  # commodity_Motive_PetCat_Affection
    PET_DOG_AFFECTION: 'CommonMotiveId' = 151034  # commodity_Motive_PetDog_Affection
    PET_HORSE_SOCIAL: 'CommonMotiveId' = 312270  # motive_Horse_Social
    VAMPIRE_POWER: 'CommonMotiveId' = 150238  # commodity_Motive_Visible_Vampire_Power
    VAMPIRE_THIRST: 'CommonMotiveId' = 149541  # commodity_Motive_Visible_Vampire_Thirst
    PLANT_SIM_WATER: 'CommonMotiveId' = 162675  # motive_PlantSim_Water
    SERVO_DURABILITY: 'CommonMotiveId' = 218485  # motive_Robots_Durability
    MERMAID_HYDRATION: 'CommonMotiveId' = HYGIENE
    WITCH_MAGIC: 'CommonMotiveId' = 213024  # commodity_Motive_WitchOccult_Charge
    WEREWOLF_FURY: 'CommonMotiveId' = 276223  # commodity_Motive_Werewolf_Fury
    FAIRY_EMOTIONAL_FORCE: 'CommonMotiveId' = 420035  # commodity_Motive_FairyOccult_EmotionalAppetite
