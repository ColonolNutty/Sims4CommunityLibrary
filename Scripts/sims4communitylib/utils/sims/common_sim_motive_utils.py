"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Union

import services
from server_commands.argument_helpers import TunableInstanceParam, OptionalTargetParam
from sims.sim_info import SimInfo
from sims4 import commands
from sims4.commands import Command, CommandType, CheatOutput
from sims4.resources import Types
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.enums.motives_enum import CommonMotiveId


class CommonSimMotiveUtils(_HasS4CLClassLog):
    """Utilities for Sim motives.

    .. note:: Motives are just another name for Sim Needs (Bladder, Hunger, Energy, etc.)

    """
    _MOTIVE_MAPPINGS: Dict[Union[CommonMotiveId, CommonInt, int], Dict[CommonSpecies, Union[CommonMotiveId, CommonInt, int]]] = None

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_sim_motive_utils'

    @classmethod
    def has_motive(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int]) -> bool:
        """has_motive(sim_info, motive_id)

        Determine if a Sim has the specified Motive.

        .. note:: For example, you could use this to determine if a Sim has a vampire power level.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to look for.
        :type motive_id: Union[CommonMotiveId, CommonInt, int]
        :return: True, if the Sim has the specified Motive. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', motive_id=motive_id, sim=sim_info)
            return False
        mapped_motive_id: int = cls._map_motive_id(sim_info, motive_id)
        if mapped_motive_id == -1:
            cls.get_log().format_with_message('Failed to map motive id!', motive_id=motive_id, sim=sim_info)
            return False
        cls.get_log().format_with_message('Mapped motive id, checking if Sim has the motive.', motive_id=motive_id, mapped_motive_id=mapped_motive_id, sim=sim_info)
        return CommonSimStatisticUtils.has_statistic(sim_info, mapped_motive_id)

    @classmethod
    def set_motive_level(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int], level: float) -> bool:
        """set_motive_level(sim_info, motive_id, level)

        Set the current level of a Motive on a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to change.
        :type motive_id: Union[CommonMotiveId, CommonInt, int]
        :param level: The amount to set the motive level to.
        :type level: float
        :return: True, if the specified Motive was changed successfully. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', motive_id=motive_id, sim=sim_info)
            return False
        if not cls.has_motive(sim_info, motive_id):
            cls.get_log().format_with_message('Sim did not have the motive.', motive_id=motive_id, sim=sim_info)
            return False
        mapped_motive_id: int = cls._map_motive_id(sim_info, motive_id)
        if mapped_motive_id == -1:
            cls.get_log().format_with_message('Failed to map motive id!', motive_id=motive_id, sim=sim_info)
            return False
        cls.get_log().format_with_message('Mapped motive id, setting the level for it on Sim.', motive_id=motive_id, mapped_motive_id=mapped_motive_id, level=level, sim=sim_info)
        return CommonSimStatisticUtils.set_statistic_value(sim_info, mapped_motive_id, level, add=True)

    @classmethod
    def get_motive_level(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int]) -> float:
        """get_motive_level(sim_info, motive_id, amount)

        Retrieve the current level of a Motive of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to get.
        :type motive_id: Union[CommonMotiveId, CommonInt, int]
        :return: True, if the specified Motive was changed successfully. False, if not.
        :rtype: bool
        """
        return cls._get_motive_level(sim_info, motive_id)

    @classmethod
    def increase_motive_level(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int], amount: float) -> bool:
        """increase_motive_level(sim_info, motive_id, amount)

        Increase the current level of a Motive of a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to change.
        :type motive_id: Union[CommonMotiveId, CommonInt, int]
        :param amount: The amount to increase the motive by.
        :type amount: float
        :return: True, if the specified Motive was changed successfully. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', motive_id=motive_id, sim=sim_info)
            return False
        if not cls.has_motive(sim_info, motive_id):
            cls.get_log().format_with_message('Sim did not have the motive.', motive_id=motive_id, sim=sim_info)
            return False
        mapped_motive_id: int = cls._map_motive_id(sim_info, motive_id)
        if mapped_motive_id == -1:
            cls.get_log().format_with_message('Failed to map motive id!', motive_id=motive_id, sim=sim_info)
            return False
        cls.get_log().format_with_message('Mapped motive id, Adding to it for Sim.', motive_id=motive_id, mapped_motive_id=mapped_motive_id, amount=amount, sim=sim_info)
        return CommonSimStatisticUtils.add_statistic_value(sim_info, mapped_motive_id, amount, add=True)

    @classmethod
    def decrease_motive_level(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int], amount: float) -> bool:
        """decrease_motive_level(sim_info, motive_id, amount)

        Decrease the current level of a Motive of a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to change.
        :type motive_id: Union[CommonMotiveId, CommonInt, int]
        :param amount: The amount to decrease the motive by.
        :type amount: float
        :return: True, if the specified Motive was changed successfully. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', motive_id=motive_id, sim=sim_info)
            return False
        if not cls.has_motive(sim_info, motive_id):
            cls.get_log().format_with_message('Sim did not have the motive.', motive_id=motive_id, sim=sim_info)
            return False
        mapped_motive_id: int = cls._map_motive_id(sim_info, motive_id)
        if mapped_motive_id == -1:
            cls.get_log().format_with_message('Failed to map motive id!', motive_id=motive_id, sim=sim_info)
            return False
        cls.get_log().format_with_message('Mapped motive id, Subtracting from it for Sim.', motive_id=motive_id, mapped_motive_id=mapped_motive_id, amount=amount, sim=sim_info)
        return CommonSimStatisticUtils.add_statistic_value(sim_info, mapped_motive_id, amount * -1.0, add=True)

    @classmethod
    def get_hunger_level(cls, sim_info: SimInfo) -> float:
        """get_hunger_level(sim_info)

        Retrieve the hunger level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', sim=sim_info)
            return False
        motive_level = cls._get_motive_level(sim_info, CommonMotiveId.HUNGER)
        if motive_level is None:
            cls.get_log().format_with_message('Sim did not have motive HUNGER.', sim=sim_info)
            return 0.0
        return motive_level

    @classmethod
    def get_hygiene_level(cls, sim_info: SimInfo) -> float:
        """get_hygiene_level(sim_info)

        Retrieve the hygiene level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', sim=sim_info)
            return False
        motive_level = cls._get_motive_level(sim_info, CommonMotiveId.HYGIENE)
        if motive_level is None:
            cls.get_log().format_with_message('Sim did not have motive HYGIENE.', sim=sim_info)
            return 0.0
        return motive_level

    @classmethod
    def get_energy_level(cls, sim_info: SimInfo) -> float:
        """get_energy_level(sim_info)

        Retrieve the energy level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', sim=sim_info)
            return False
        motive_level = cls._get_motive_level(sim_info, CommonMotiveId.ENERGY)
        if motive_level is None:
            cls.get_log().format_with_message('Sim did not have motive ENERGY.', sim=sim_info)
            return 0.0
        return motive_level

    @classmethod
    def get_bladder_level(cls, sim_info: SimInfo) -> float:
        """get_bladder_level(sim_info)

        Retrieve the bladder level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', sim=sim_info)
            return False
        motive_level = cls._get_motive_level(sim_info, CommonMotiveId.BLADDER)
        if motive_level is None:
            return 0.0
        return motive_level

    @classmethod
    def has_bowels(cls, sim_info: SimInfo) -> bool:
        """has_bowels(sim_info)

        Determine if a Sim has bowels.

        .. note:: Human Sims do not have Bowels.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has bowels. False, if not.
        :rtype: bool
        """
        return cls.has_motive(sim_info, CommonMotiveId.BOWEL)

    @classmethod
    def get_bowels_level(cls, sim_info: SimInfo) -> float:
        """get_bowels_level(sim_info)

        Retrieve the bowel level of a Sim.

        .. note:: Human Sims do not have Bowels. (As hard as that is to believe)

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        if CommonSpeciesUtils.is_human(sim_info):
            cls.get_log().format_with_message('Sim did not have motive BOWELS.', sim=sim_info)
            return 0.0
        return cls._get_motive_level(sim_info, CommonMotiveId.BOWEL)

    @classmethod
    def get_social_level(cls, sim_info: SimInfo) -> float:
        """get_social_level(sim_info)

        Retrieve the social level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        motive_level = cls._get_motive_level(sim_info, CommonMotiveId.SOCIAL)
        if motive_level is None:
            cls.get_log().format_with_message('Sim did not have motive SOCIAL.', sim=sim_info)
            return 0.0
        return motive_level

    @classmethod
    def get_fun_level(cls, sim_info: SimInfo) -> float:
        """get_fun_level(sim_info)

        Retrieve the fun level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim.
        :rtype: float
        """
        motive_level = cls._get_motive_level(sim_info, CommonMotiveId.FUN)
        if motive_level is None:
            cls.get_log().format_with_message('Sim did not have motive FUN.', sim=sim_info)
            return 0.0
        return motive_level

    @classmethod
    def get_robot_charge_level(cls, sim_info: SimInfo) -> float:
        """get_robot_charge_level(sim_info)

        Retrieve the charge level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim or `0.0` if the Sim is not a Robot.
        :rtype: float
        """
        if not CommonOccultUtils.is_robot(sim_info):
            cls.get_log().format_with_message('Sim is not a Robot.', sim=sim_info)
            return 0.0
        return cls._get_motive_level(sim_info, CommonMotiveId.SERVO_CHARGE)

    @classmethod
    def get_robot_durability_level(cls, sim_info: SimInfo) -> float:
        """get_robot_durability_level(sim_info)

        Retrieve the durability level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim or `0.0` if the Sim is not a Robot.
        :rtype: float
        """
        if not CommonOccultUtils.is_robot(sim_info):
            cls.get_log().format_with_message('Sim is not a Robot.', sim=sim_info)
            return 0.0
        return cls._get_motive_level(sim_info, CommonMotiveId.SERVO_DURABILITY)

    @classmethod
    def get_vampire_power_level(cls, sim_info: SimInfo) -> float:
        """get_vampire_power_level(sim_info)

        Retrieve the vampire power level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim or `0.0` if the Sim is not a Vampire.
        :rtype: float
        """
        if not CommonOccultUtils.is_vampire(sim_info):
            cls.get_log().format_with_message('Sim is not a Vampire.', sim=sim_info)
            return 0.0
        return cls._get_motive_level(sim_info, CommonMotiveId.VAMPIRE_POWER)

    @classmethod
    def get_vampire_thirst_level(cls, sim_info: SimInfo) -> float:
        """get_vampire_thirst_level(sim_info)

        Retrieve the vampire thirst level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim or `0.0` if the Sim is not a Vampire.
        :rtype: float
        """
        if not CommonOccultUtils.is_vampire(sim_info):
            cls.get_log().format_with_message('Sim is not a Vampire.', sim=sim_info)
            return 0.0
        return cls._get_motive_level(sim_info, CommonMotiveId.VAMPIRE_THIRST)

    @classmethod
    def get_plant_sim_water_level(cls, sim_info: SimInfo) -> float:
        """get_plant_sim_water_level(sim_info)

        Retrieve the plant sim water level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim or `0.0` if the Sim is not a Plant Sim.
        :rtype: float
        """
        if not CommonOccultUtils.is_plant_sim(sim_info):
            cls.get_log().format_with_message('Sim is not a Plant Sim.', sim=sim_info)
            return 0.0
        return cls._get_motive_level(sim_info, CommonMotiveId.PLANT_SIM_WATER)

    @classmethod
    def get_mermaid_hydration_level(cls, sim_info: SimInfo) -> float:
        """get_mermaid_hydration_level(sim_info)

        Retrieve the hydration level of a Sim.

        .. note:: This level is basically the Hygiene motive.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim or `0.0` if the Sim is not a Mermaid.
        :rtype: float
        """
        if not CommonOccultUtils.is_mermaid(sim_info):
            cls.get_log().format_with_message('Sim is not a Mermaid.', sim=sim_info)
            return 0.0
        return cls._get_motive_level(sim_info, CommonMotiveId.MERMAID_HYDRATION)

    @classmethod
    def get_witch_magic_level(cls, sim_info: SimInfo) -> float:
        """get_witch_magic_level(sim_info)

        Retrieve the magic level of a Sim.

        :param sim_info: The Sim to get the level of.
        :type sim_info: SimInfo
        :return: The current level of the Motive of the Sim or `0.0` if the Sim is not a Witch.
        :rtype: float
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', sim=sim_info)
            return 0.0
        if not CommonOccultUtils.is_witch(sim_info):
            cls.get_log().format_with_message('Sim is not a Witch.', sim=sim_info)
            return 0.0
        return cls._get_motive_level(sim_info, CommonMotiveId.WITCH_MAGIC)

    @classmethod
    def is_motive_locked(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int]) -> bool:
        """is_motive_locked(sim_info, motive_id)

        Determine if a Motive is locked for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the motive to check.
        :type motive_id: Union[CommonMotiveId, CommonInt, int]
        :return: True, if the specified Motive is locked for the Sim. False, if not.
        :rtype: bool
        """
        mapped_motive_id: int = cls._map_motive_id(sim_info, motive_id)
        return CommonSimStatisticUtils.is_statistic_locked(sim_info, mapped_motive_id)

    @classmethod
    def set_all_motives_max(cls, sim_info: SimInfo) -> bool:
        """set_all_motives_max(sim_info)

        Set all Motives for a Sim to their maximum values.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        client_id = services.client_manager().get_first_client_id()
        commands.execute('stats.fill_commodities {}'.format(CommonSimUtils.get_sim_id(sim_info)), client_id)
        return True

    @classmethod
    def _get_motive_level(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int]) -> float:
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', motive_id=motive_id, sim=sim_info)
            return 0.0
        mapped_motive_id: int = cls._map_motive_id(sim_info, motive_id)
        if mapped_motive_id == -1:
            cls.get_log().format_with_message('Failed to map the motive id.', motive_id=motive_id, sim=sim_info)
            return 0.0
        cls.get_log().format_with_message('Mapped motive id, attempting to get motive value.', motive_id=motive_id, mapped_motive_id=mapped_motive_id, sim=sim_info)
        return CommonSimStatisticUtils.get_statistic_value(sim_info, mapped_motive_id)

    @classmethod
    def _map_motive_id(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int]) -> Union[CommonMotiveId, CommonInt, int]:
        motive_mappings = CommonSimMotiveUtils._get_motive_mappings()
        if motive_id not in motive_mappings:
            return motive_id
        motive_species_mapping: Dict[CommonSpecies, CommonMotiveId] = motive_mappings[motive_id]

        species = CommonSpecies.get_species(sim_info)
        return motive_species_mapping.get(species, motive_id)

    @staticmethod
    def _get_motive_mappings() -> Dict[Union[CommonMotiveId, CommonInt, int], Dict[CommonSpecies, Union[CommonMotiveId, CommonInt, int]]]:
        if CommonSimMotiveUtils._MOTIVE_MAPPINGS is not None:
            return CommonSimMotiveUtils._MOTIVE_MAPPINGS

        CommonSimMotiveUtils._MOTIVE_MAPPINGS = {
            CommonMotiveId.HUNGER: {
                CommonSpecies.HUMAN: CommonMotiveId.HUNGER,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_HUNGER,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_HUNGER,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_HUNGER,
                CommonSpecies.FOX: CommonMotiveId.HUNGER
            },
            CommonMotiveId.HYGIENE: {
                CommonSpecies.HUMAN: CommonMotiveId.HYGIENE,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_HYGIENE,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_HYGIENE,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_HYGIENE,
                CommonSpecies.FOX: CommonMotiveId.ANIMAL_FOX_HYGIENE
            },
            CommonMotiveId.MERMAID_HYDRATION: {
                CommonSpecies.HUMAN: CommonMotiveId.HYGIENE,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_HYGIENE,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_HYGIENE,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_HYGIENE,
                CommonSpecies.FOX: CommonMotiveId.HYGIENE
            },
            CommonMotiveId.ENERGY: {
                CommonSpecies.HUMAN: CommonMotiveId.ENERGY,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_ENERGY,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_ENERGY,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_ENERGY,
                CommonSpecies.FOX: CommonMotiveId.ENERGY
            },
            CommonMotiveId.BLADDER: {
                CommonSpecies.HUMAN: CommonMotiveId.BLADDER,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_BLADDER,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_BLADDER,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_BLADDER,
                CommonSpecies.FOX: CommonMotiveId.ANIMAL_FOX_BLADDER
            },
            CommonMotiveId.BOWEL: {
                CommonSpecies.HUMAN: CommonMotiveId.BOWEL,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_BOWEL,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_BOWEL,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_BOWEL,
                CommonSpecies.FOX: CommonMotiveId.BOWEL
            },
            CommonMotiveId.SOCIAL: {
                CommonSpecies.HUMAN: CommonMotiveId.SOCIAL,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_AFFECTION,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_AFFECTION,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_AFFECTION,
                CommonSpecies.FOX: CommonMotiveId.SOCIAL
            },
            CommonMotiveId.FUN: {
                CommonSpecies.HUMAN: CommonMotiveId.FUN,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_PLAY,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_PLAY,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_PLAY,
                CommonSpecies.FOX: CommonMotiveId.FUN
            }
        }
        return CommonSimMotiveUtils._MOTIVE_MAPPINGS


@Command('s4clib.get_motive_level', command_type=CommandType.Live)
def _common_get_motive_level(motive: TunableInstanceParam(Types.STATISTIC), opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    if motive is None:
        output('Failed, Motive not specified or Motive did not exist! s4clib.set_motive_level <motive_name_or_id> <level> [opt_sim=None]')
        return
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    sim_name = CommonSimNameUtils.get_full_name(sim_info)
    output('Setting motive {} to Sim {}'.format(str(motive), sim_name))
    try:
        motive_level = CommonSimMotiveUtils.get_motive_level(sim_info, motive)
        output('Motive Level of {}: {}'.format(motive, motive_level))
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to get motive {} to Sim {}.'.format(str(motive), sim_name), exception=ex)
        output('Failed to get motive {} to Sim {}. {}'.format(str(motive), sim_name, str(ex)))


@Command('s4clib.set_motive_level', command_type=CommandType.Live)
def _common_set_motive_level(motive: TunableInstanceParam(Types.STATISTIC), level: float, opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    if motive is None:
        output('Failed, Motive not specified or Motive did not exist! s4clib.set_motive_level <motive_name_or_id> <level> [opt_sim=None]')
        return
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    sim_name = CommonSimNameUtils.get_full_name(sim_info)
    output('Setting motive {} to Sim {}'.format(str(motive), sim_name))
    try:
        if CommonSimMotiveUtils.set_motive_level(sim_info, motive, level):
            output('Successfully set motive level.')
        else:
            output('Failed to set motive level.')
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to set motive {} to Sim {}.'.format(str(motive), sim_name), exception=ex)
        output('Failed to set motive {} to Sim {}. {}'.format(str(motive), sim_name, str(ex)))


@Command('s4clib.max_all_motives', command_type=CommandType.Live)
def _common_max_all_motives(opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    try:
        CommonSimMotiveUtils.set_all_motives_max(sim_info)
        output('Maxed the motives of {}.'.format(CommonSimNameUtils.get_full_name(sim_info)))
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to max the motives of {}.'.format(CommonSimNameUtils.get_full_name(sim_info)), exception=ex)
        output('Failed to max the motives of {}. {}'.format(CommonSimNameUtils.get_full_name(sim_info), str(ex)))


@Command('s4clib.max_world_motives', command_type=CommandType.Live)
def _common_max_world_motives(_connection: int=None):
    output = CheatOutput(_connection)
    try:
        sim_count = 0
        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
            CommonSimMotiveUtils.set_all_motives_max(sim_info)
            sim_count += 1
        output('Maxed the motives of {} Sim(s).'.format(sim_count))
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to max the motives of all Sims.', exception=ex)
        output('Failed to max the motives of all Sims. {}'.format(str(ex)))
