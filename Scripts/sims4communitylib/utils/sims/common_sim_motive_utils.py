"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict
from sims.sim_info import SimInfo
from sims.sim_info_types import Species
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.enums.motives_enum import CommonMotiveId


class CommonSimMotiveUtils:
    """Utilities for Sim motives.

    .. note:: Motives are just another name for Sim Needs (Bladder, Hunger, Energy, etc.)

    """
    _MOTIVE_MAPPINGS: Dict[int, Dict[Species, int]] = None

    @staticmethod
    def has_motive(sim_info: SimInfo, motive_id: int) -> bool:
        """has_motive(sim_info, motive_id)

        Determine if a Sim has the specified Motive.

        .. note:: For example, you could use this to determine if a Sim has a vampire power level.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to look for.
        :type motive_id: int
        :return: True, if the Sim has the specified Motive. False, if not.
        :rtype: bool
        """
        mapped_motive_id = CommonSimMotiveUtils._map_motive_id(sim_info, motive_id)
        return CommonSimStatisticUtils.has_statistic(sim_info, mapped_motive_id)

    @staticmethod
    def set_motive_level(sim_info: SimInfo, motive_id: int, amount: float) -> bool:
        """set_motive_level(sim_info, motive_id, amount)

        Set the current level of a Motive of a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to change.
        :type motive_id: int
        :param amount: The amount to set the motive level to.
        :type amount: float
        :return: True, if the specified Motive was changed successfully. False, if not.
        :rtype: bool
        """
        mapped_motive_id = CommonSimMotiveUtils._map_motive_id(sim_info, motive_id)
        if not CommonSimMotiveUtils.has_motive(sim_info, mapped_motive_id):
            return False
        CommonSimStatisticUtils.set_statistic_value(sim_info, mapped_motive_id, amount, add=True)
        return True

    @staticmethod
    def increase_motive_level(sim_info: SimInfo, motive_id: int, amount: float) -> bool:
        """increase_motive_level(sim_info, motive_id, amount)

        Increase the current level of a Motive of a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to change.
        :type motive_id: int
        :param amount: The amount to increase the motive by.
        :type amount: float
        :return: True, if the specified Motive was changed successfully. False, if not.
        :rtype: bool
        """
        mapped_motive_id = CommonSimMotiveUtils._map_motive_id(sim_info, motive_id)
        if not CommonSimMotiveUtils.has_motive(sim_info, mapped_motive_id):
            return False
        CommonSimStatisticUtils.add_statistic_value(sim_info, mapped_motive_id, amount, add=True)
        return True

    @staticmethod
    def decrease_motive_level(sim_info: SimInfo, motive_id: int, amount: float) -> bool:
        """decrease_motive_level(sim_info, motive_id, amount)

        Decrease the current level of a Motive of a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to change.
        :type motive_id: int
        :param amount: The amount to decrease the motive by.
        :type amount: float
        :return: True, if the specified Motive was changed successfully. False, if not.
        :rtype: bool
        """
        mapped_motive_id = CommonSimMotiveUtils._map_motive_id(sim_info, motive_id)
        if not CommonSimMotiveUtils.has_motive(sim_info, mapped_motive_id):
            return False
        CommonSimStatisticUtils.add_statistic_value(sim_info, mapped_motive_id, amount * -1.0, add=True)
        return True

    @staticmethod
    def get_hunger_level(sim_info: SimInfo) -> float:
        """get_hunger_level(sim_info)

        Retrieve the hunger level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        motive_level = CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.HUNGER)
        if motive_level is None:
            return -1.0
        return motive_level

    @staticmethod
    def get_hygiene_level(sim_info: SimInfo) -> float:
        """get_hygiene_level(sim_info)

        Retrieve the hygiene level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        motive_level = CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.HYGIENE)
        if motive_level is None:
            return -1.0
        return motive_level

    @staticmethod
    def get_energy_level(sim_info: SimInfo) -> float:
        """get_energy_level(sim_info)

        Retrieve the energy level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        motive_level = CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.ENERGY)
        if motive_level is None:
            return -1.0
        return motive_level

    @staticmethod
    def get_bladder_level(sim_info: SimInfo) -> float:
        """get_bladder_level(sim_info)

        Retrieve the bladder level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        motive_level = CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.BLADDER)
        if motive_level is None:
            return -1.0
        return motive_level

    @staticmethod
    def get_bowels_level(sim_info: SimInfo) -> float:
        """get_bowels_level(sim_info)

        Retrieve the bowels level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        if CommonSpeciesUtils.is_human(sim_info):
            return -1.0
        elif CommonSpeciesUtils.is_dog(sim_info):
            return CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.PET_DOG_BOWEL)
        elif CommonSpeciesUtils.is_cat(sim_info):
            return CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.PET_CAT_BOWEL)
        return -1.0

    @staticmethod
    def get_social_level(sim_info: SimInfo) -> float:
        """get_social_level(sim_info)

        Retrieve the social level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        motive_level = CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.SOCIAL)
        if motive_level is None:
            return -1.0
        return motive_level

    @staticmethod
    def get_fun_level(sim_info: SimInfo) -> float:
        """get_fun_level(sim_info)

        Retrieve the fun level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        motive_level = CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.FUN)
        if motive_level is None:
            return -1.0
        return motive_level

    @staticmethod
    def get_vampire_power_level(sim_info: SimInfo) -> float:
        """get_vampire_power_level(sim_info)

        Retrieve the vampire power level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim or `-1.0` if the Sim is not a Vampire.
        :rtype: float
        """
        if not CommonOccultUtils.is_vampire(sim_info):
            return -1.0
        return CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.VAMPIRE_POWER)

    @staticmethod
    def get_vampire_thirst_level(sim_info: SimInfo) -> float:
        """get_vampire_thirst_level(sim_info)

        Retrieve the vampire thirst level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim or `-1.0` if the Sim is not a Vampire.
        :rtype: float
        """
        if not CommonOccultUtils.is_vampire(sim_info):
            return -1.0
        return CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.VAMPIRE_THIRST)

    @staticmethod
    def get_plant_sim_water_level(sim_info: SimInfo) -> float:
        """get_plant_sim_water_level(sim_info)

        Retrieve the plant sim water level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim or `-1.0` if the Sim is not a Plant Sim.
        :rtype: float
        """
        if not CommonOccultUtils.is_plant_sim(sim_info):
            return -1.0
        return CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.PLANT_SIM_WATER)

    @staticmethod
    def _get_motive_level(sim_info: SimInfo, motive_id: int) -> float:
        motive_id = CommonSimMotiveUtils._map_motive_id(sim_info, motive_id)
        return CommonSimStatisticUtils.get_statistic_value(sim_info, motive_id)

    @staticmethod
    def _map_motive_id(sim_info: SimInfo, motive_id: int) -> int:
        motive_mappings = CommonSimMotiveUtils._get_motive_mappings()
        if motive_id not in motive_mappings:
            return motive_id
        motive_species_mapping: Dict[Species, CommonMotiveId] = motive_mappings[motive_id]

        species = CommonSpeciesUtils.get_species(sim_info)
        if species not in motive_species_mapping:
            return motive_id
        return motive_species_mapping[species]

    @staticmethod
    def _get_motive_mappings() -> Dict[int, Dict[Species, int]]:
        if CommonSimMotiveUtils._MOTIVE_MAPPINGS is None:
            CommonSimMotiveUtils._MOTIVE_MAPPINGS = {
                CommonMotiveId.HUNGER: {
                    Species.HUMAN: CommonMotiveId.HUNGER,
                    Species.CAT: CommonMotiveId.PET_CAT_HUNGER,
                    Species.DOG: CommonMotiveId.PET_DOG_HUNGER
                },
                CommonMotiveId.HYGIENE: {
                    Species.HUMAN: CommonMotiveId.HYGIENE,
                    Species.CAT: CommonMotiveId.PET_CAT_HYGIENE,
                    Species.DOG: CommonMotiveId.PET_DOG_HYGIENE
                },
                CommonMotiveId.ENERGY: {
                    Species.HUMAN: CommonMotiveId.ENERGY,
                    Species.CAT: CommonMotiveId.PET_CAT_ENERGY,
                    Species.DOG: CommonMotiveId.PET_DOG_ENERGY
                },
                CommonMotiveId.BLADDER: {
                    Species.HUMAN: CommonMotiveId.BLADDER,
                    Species.CAT: CommonMotiveId.PET_CAT_BLADDER,
                    Species.DOG: CommonMotiveId.PET_DOG_BLADDER
                },
                CommonMotiveId.SOCIAL: {
                    Species.HUMAN: CommonMotiveId.SOCIAL,
                    Species.CAT: CommonMotiveId.PET_CAT_AFFECTION,
                    Species.DOG: CommonMotiveId.PET_DOG_AFFECTION
                },
                CommonMotiveId.FUN: {
                    Species.HUMAN: CommonMotiveId.FUN,
                    Species.CAT: CommonMotiveId.PET_CAT_PLAY,
                    Species.DOG: CommonMotiveId.PET_DOG_PLAY
                }
            }
        return CommonSimMotiveUtils._MOTIVE_MAPPINGS
