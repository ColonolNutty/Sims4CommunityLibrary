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
    _MOTIVE_MAPPINGS: Dict[CommonMotiveId, Dict[Species, CommonMotiveId]] = None

    @staticmethod
    def has_motive(sim_info: SimInfo, motive_id: CommonMotiveId) -> bool:
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
        mapped_motive_id: int = CommonSimMotiveUtils._map_motive_id(sim_info, motive_id)
        if mapped_motive_id == -1:
            return False
        return CommonSimStatisticUtils.has_statistic(sim_info, mapped_motive_id)

    @staticmethod
    def set_motive_level(sim_info: SimInfo, motive_id: CommonMotiveId, amount: float) -> bool:
        """set_motive_level(sim_info, motive_id, amount)

        Set the current level of a Motive of a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to change.
        :type motive_id: CommonMotiveId
        :param amount: The amount to set the motive level to.
        :type amount: float
        :return: True, if the specified Motive was changed successfully. False, if not.
        :rtype: bool
        """
        if not CommonSimMotiveUtils.has_motive(sim_info, motive_id):
            return False
        mapped_motive_id: int = CommonSimMotiveUtils._map_motive_id(sim_info, motive_id)
        CommonSimStatisticUtils.set_statistic_value(sim_info, mapped_motive_id, amount, add=True)
        return True

    @staticmethod
    def get_motive_level(sim_info: SimInfo, motive_id: CommonMotiveId) -> float:
        """get_motive_level(sim_info, motive_id, amount)

        Retrieve the current level of a Motive of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to get.
        :type motive_id: CommonMotiveId
        :return: True, if the specified Motive was changed successfully. False, if not.
        :rtype: bool
        """
        return CommonSimMotiveUtils._get_motive_level(sim_info, motive_id)

    @staticmethod
    def increase_motive_level(sim_info: SimInfo, motive_id: CommonMotiveId, amount: float) -> bool:
        """increase_motive_level(sim_info, motive_id, amount)

        Increase the current level of a Motive of a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to change.
        :type motive_id: CommonMotiveId
        :param amount: The amount to increase the motive by.
        :type amount: float
        :return: True, if the specified Motive was changed successfully. False, if not.
        :rtype: bool
        """
        if not CommonSimMotiveUtils.has_motive(sim_info, motive_id):
            return False
        mapped_motive_id: int = CommonSimMotiveUtils._map_motive_id(sim_info, motive_id)
        CommonSimStatisticUtils.add_statistic_value(sim_info, mapped_motive_id, amount, add=True)
        return True

    @staticmethod
    def decrease_motive_level(sim_info: SimInfo, motive_id: CommonMotiveId, amount: float) -> bool:
        """decrease_motive_level(sim_info, motive_id, amount)

        Decrease the current level of a Motive of a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to change.
        :type motive_id: CommonMotiveId
        :param amount: The amount to decrease the motive by.
        :type amount: float
        :return: True, if the specified Motive was changed successfully. False, if not.
        :rtype: bool
        """
        if not CommonSimMotiveUtils.has_motive(sim_info, motive_id):
            return False
        mapped_motive_id: int = CommonSimMotiveUtils._map_motive_id(sim_info, motive_id)
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
    def has_bowels(sim_info: SimInfo) -> bool:
        """has_bowels(sim_info)

        Determine if a Sim has bowels.

        .. note:: Human Sims do not have Bowels.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has bowels. False, if not.
        :rtype: bool
        """
        return CommonSimMotiveUtils.has_motive(sim_info, CommonMotiveId.BOWEL)

    @staticmethod
    def get_bowels_level(sim_info: SimInfo) -> float:
        """get_bowels_level(sim_info)

        Retrieve the bowel level of a Sim.

        .. note:: Human Sims do not have Bowels. (As hard as that is to believe)

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        if CommonSpeciesUtils.is_human(sim_info):
            return -1.0
        return CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.BOWEL)

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
    def get_robot_charge_level(sim_info: SimInfo) -> float:
        """get_robot_charge_level(sim_info)

        Retrieve the charge level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim or `-1.0` if the Sim is not a Robot.
        :rtype: float
        """
        if not CommonOccultUtils.is_robot(sim_info):
            return -1.0
        return CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.SERVO_CHARGE)

    @staticmethod
    def get_robot_durability_level(sim_info: SimInfo) -> float:
        """get_robot_durability_level(sim_info)

        Retrieve the durability level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim or `-1.0` if the Sim is not a Robot.
        :rtype: float
        """
        if not CommonOccultUtils.is_robot(sim_info):
            return -1.0
        return CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.SERVO_DURABILITY)

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
    def get_mermaid_hydration_level(sim_info: SimInfo) -> float:
        """get_mermaid_hydration_level(sim_info)

        Retrieve the hydration level of a Sim.

        .. note:: This level is basically the Hygiene motive.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim or `-1.0` if the Sim is not a Mermaid.
        :rtype: float
        """
        if not CommonOccultUtils.is_mermaid(sim_info):
            return -1.0
        return CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.MERMAID_HYDRATION)

    @staticmethod
    def get_witch_magic_level(sim_info: SimInfo) -> float:
        """get_witch_magic_level(sim_info)

        Retrieve the magic level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim or `-1.0` if the Sim is not a Witch.
        :rtype: float
        """
        if not CommonOccultUtils.is_witch(sim_info):
            return -1.0
        return CommonSimMotiveUtils._get_motive_level(sim_info, CommonMotiveId.WITCH_MAGIC)

    @staticmethod
    def _get_motive_level(sim_info: SimInfo, motive_id: CommonMotiveId) -> float:
        motive_id: int = CommonSimMotiveUtils._map_motive_id(sim_info, motive_id)
        if motive_id == -1:
            return 0.0
        return CommonSimStatisticUtils.get_statistic_value(sim_info, motive_id)

    @staticmethod
    def _map_motive_id(sim_info: SimInfo, motive_id: CommonMotiveId) -> CommonMotiveId:
        motive_mappings = CommonSimMotiveUtils._get_motive_mappings()
        if motive_id not in motive_mappings:
            return motive_id
        motive_species_mapping: Dict[Species, CommonMotiveId] = motive_mappings[motive_id]

        species = CommonSpeciesUtils.get_species(sim_info)
        if species not in motive_species_mapping:
            return motive_id
        return motive_species_mapping[species]

    @staticmethod
    def _get_motive_mappings() -> Dict[CommonMotiveId, Dict[Species, CommonMotiveId]]:
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
                CommonMotiveId.MERMAID_HYDRATION: {
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
                CommonMotiveId.BOWEL: {
                    Species.HUMAN: CommonMotiveId.BOWEL,
                    Species.CAT: CommonMotiveId.PET_CAT_BOWEL,
                    Species.DOG: CommonMotiveId.PET_DOG_BOWEL
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
