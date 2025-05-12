"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Union

import services
from server_commands.argument_helpers import TunableInstanceParam
from sims.sim_info import SimInfo
from sims4 import commands
from sims4.resources import Types
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
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
    def has_motive(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int]) -> CommonTestResult:
        """has_motive(sim_info, motive_id)

        Determine if a Sim has the specified Motive.

        .. note:: For example, you could use this to determine if a Sim has a vampire power level.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to look for.
        :type motive_id: Union[CommonMotiveId, CommonInt, int]
        :return: The result of testing if the Sim has the motive. True, if the Sim has the specified Motive. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', motive_id=motive_id, sim=sim_info)
            return CommonTestResult(False, reason='sim_info was None.', hide_tooltip=True)
        mapped_motive_id: int = cls._map_motive_id(sim_info, motive_id)
        if mapped_motive_id == -1:
            cls.get_log().format_with_message('Failed to map motive id!', motive_id=motive_id, sim=sim_info)
            return CommonTestResult(False, reason=f'{sim_info} did not have a mapped motive {motive_id}', tooltip_text=CommonStringId.S4CL_SIM_DID_NOT_HAVE_A_MAPPED_MOTIVE, tooltip_tokens=(sim_info, str(motive_id)))
        cls.get_log().format_with_message('Mapped motive id, checking if Sim has the motive.', motive_id=motive_id, mapped_motive_id=mapped_motive_id, sim=sim_info)
        return CommonSimStatisticUtils.has_statistic(sim_info, mapped_motive_id)

    @classmethod
    def set_motive_level(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int], level: float) -> CommonExecutionResult:
        """set_motive_level(sim_info, motive_id, level)

        Set the current level of a Motive on a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to change.
        :type motive_id: Union[CommonMotiveId, CommonInt, int]
        :param level: The amount to set the motive level to.
        :type level: float
        :return: The result of setting the motive level. True, if the specified Motive was changed successfully. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', motive_id=motive_id, sim=sim_info)
            return CommonExecutionResult(False, reason='sim_info was None.', hide_tooltip=True)
        mapped_motive_id: int = cls._map_motive_id(sim_info, motive_id)
        if mapped_motive_id == -1:
            cls.get_log().format_with_message('Failed to map motive id!', motive_id=motive_id, sim=sim_info)
            return CommonTestResult(False, reason=f'{sim_info} did not have a mapped motive {motive_id}', tooltip_text=CommonStringId.S4CL_SIM_DID_NOT_HAVE_A_MAPPED_MOTIVE, tooltip_tokens=(sim_info, str(motive_id)))
        if not cls.has_motive(sim_info, motive_id):
            return CommonExecutionResult(False, reason=f'{sim_info} does not have motive {motive_id}.', tooltip_text=CommonStringId.S4CL_SIM_DID_NOT_HAVE_MOTIVE, tooltip_tokens=(sim_info, str(motive_id)))
        if cls.is_motive_locked(sim_info, motive_id):
            return CommonExecutionResult(True, reason='The motive is currently locked.', hide_tooltip=True)
        cls.get_log().format_with_message('Mapped motive id, setting the level for it on Sim.', motive_id=motive_id, mapped_motive_id=mapped_motive_id, level=level, sim=sim_info)
        return CommonSimStatisticUtils.set_statistic_value(sim_info, mapped_motive_id, level, add=True)

    @classmethod
    def get_motive_level(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int]) -> float:
        """get_motive_level(sim_info, motive_id, amount)

        Retrieve the current level of a Motive of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to get the value of.
        :type motive_id: Union[CommonMotiveId, CommonInt, int]
        :return: The current level of the motive for the specified Sim.
        :rtype: float
        """
        return cls._get_motive_level(sim_info, motive_id)

    @classmethod
    def increase_motive_level(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int], amount: float) -> CommonExecutionResult:
        """increase_motive_level(sim_info, motive_id, amount)

        Increase the current level of a Motive of a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to change.
        :type motive_id: Union[CommonMotiveId, CommonInt, int]
        :param amount: The amount to increase the motive by.
        :type amount: float
        :return: The result of increasing motive level. True, if the specified Motive was changed successfully. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', motive_id=motive_id, sim=sim_info)
            return CommonExecutionResult(False, reason='sim_info was None.', hide_tooltip=True)
        mapped_motive_id: int = cls._map_motive_id(sim_info, motive_id)
        if mapped_motive_id == -1:
            cls.get_log().format_with_message('Failed to map motive id!', motive_id=motive_id, sim=sim_info)
            return CommonTestResult(False, reason=f'{sim_info} did not have a mapped motive {motive_id}', tooltip_text=CommonStringId.S4CL_SIM_DID_NOT_HAVE_A_MAPPED_MOTIVE, tooltip_tokens=(sim_info, str(motive_id)))
        cls.get_log().format_with_message('Mapped motive id, Adding to it for Sim.', motive_id=motive_id, mapped_motive_id=mapped_motive_id, amount=amount, sim=sim_info)
        return CommonSimStatisticUtils.add_statistic_value(sim_info, mapped_motive_id, amount, add=True)

    @classmethod
    def decrease_motive_level(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int], amount: float) -> CommonExecutionResult:
        """decrease_motive_level(sim_info, motive_id, amount)

        Decrease the current level of a Motive of a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the Motive to change.
        :type motive_id: Union[CommonMotiveId, CommonInt, int]
        :param amount: The amount to decrease the motive by.
        :type amount: float
        :return: The result of decreasing motive level. True, if the specified Motive was changed successfully. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            cls.get_log().format_with_message('sim_info was None!', motive_id=motive_id, sim=sim_info)
            return CommonExecutionResult(False, reason='sim_info was None.', hide_tooltip=True)
        mapped_motive_id: int = cls._map_motive_id(sim_info, motive_id)
        if mapped_motive_id == -1:
            cls.get_log().format_with_message('Failed to map motive id!', motive_id=motive_id, sim=sim_info)
            return CommonTestResult(False, reason=f'{sim_info} did not have a mapped motive {motive_id}', tooltip_text=CommonStringId.S4CL_SIM_DID_NOT_HAVE_A_MAPPED_MOTIVE, tooltip_tokens=(sim_info, str(motive_id)))
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
    def has_bowels(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_bowels(sim_info)

        Determine if a Sim has bowels.

        .. note:: Human Sims do not have Bowels.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the Sim has bowels. False, if not.
        :rtype: CommonTestResult
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
    def is_motive_locked(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int]) -> CommonTestResult:
        """is_motive_locked(sim_info, motive_id)

        Determine if a Motive is locked for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param motive_id: The identifier of the motive to check.
        :type motive_id: Union[CommonMotiveId, CommonInt, int]
        :return: The result of the test. True, if the specified Motive is locked for the Sim. False, if not.
        :rtype: CommonTestResult
        """
        mapped_motive_id: int = cls._map_motive_id(sim_info, motive_id)
        if mapped_motive_id == -1:
            cls.get_log().format_with_message('Failed to map motive id!', motive_id=motive_id, sim=sim_info)
            return CommonTestResult(False, reason=f'{sim_info} did not have a mapped motive {motive_id}', tooltip_text=CommonStringId.S4CL_SIM_DID_NOT_HAVE_A_MAPPED_MOTIVE, tooltip_tokens=(sim_info, str(motive_id)))
        motive_instance = CommonSimStatisticUtils.get_statistic(sim_info, mapped_motive_id)
        if motive_instance is None:
            return CommonTestResult(False, reason=f'No motive found for id {mapped_motive_id}.', tooltip_text=CommonStringId.S4CL_NO_MOTIVE_FOUND_FOR_ID, tooltip_tokens=(str(mapped_motive_id),))
        if not cls.has_motive(sim_info, motive_id):
            return CommonTestResult(False, reason=f'{sim_info} does not have motive {motive_id}.', tooltip_text=CommonStringId.S4CL_SIM_DID_NOT_HAVE_MOTIVE, tooltip_tokens=(sim_info, str(motive_id)))
        if sim_info.is_locked(motive_instance):
            return CommonTestResult(True, reason=f'Motive {mapped_motive_id} is locked for Sim {sim_info}', tooltip_text=CommonStringId.S4CL_MOTIVE_IS_LOCKED_FOR_SIM, tooltip_tokens=(str(mapped_motive_id), sim_info))
        return CommonTestResult(False, reason=f'Motive {mapped_motive_id} is not locked for Sim {sim_info}', tooltip_text=CommonStringId.S4CL_MOTIVE_IS_NOT_LOCKED_FOR_SIM, tooltip_tokens=(str(mapped_motive_id), sim_info))

    @classmethod
    def set_all_motives_max(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """set_all_motives_max(sim_info)

        Set all Motives for a Sim to their maximum values.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of setting all motives to max. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            return CommonExecutionResult(False, reason='sim_info was None.', hide_tooltip=True)
        client_id = services.client_manager().get_first_client_id()
        commands.execute('stats.fill_commodities {}'.format(CommonSimUtils.get_sim_id(sim_info)), client_id)
        return CommonExecutionResult(True, reason=f'Successfully set all motives to their max levels for Sim {sim_info}', tooltip_text=CommonStringId.S4CL_SUCCESSFULLY_SET_ALL_MOTIVES_TO_MAX_FOR_SIM, tooltip_tokens=(sim_info,))

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
    def get_motive_id_for_sim(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int]) -> Union[CommonMotiveId, CommonInt, int]:
        """get_motive_id_for_sim(sim_info, motive_id)

        Translate a motive ID to one that the Sim would have.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param motive_id: The motive to translate.
        :type motive_id: Union[CommonMotiveId, CommonInt, int]
        :return: The mapped motive id.
        :rtype: Union[CommonMotiveId, CommonInt, int]
        """
        result = cls._map_motive_id(sim_info, motive_id)
        if result == -1:
            return motive_id
        return result

    @classmethod
    def _map_motive_id(cls, sim_info: SimInfo, motive_id: Union[CommonMotiveId, CommonInt, int]) -> Union[CommonMotiveId, CommonInt, int]:
        motive_mappings = cls._get_motive_mappings()
        if motive_id not in motive_mappings:
            return motive_id
        motive_species_mapping: Dict[CommonSpecies, CommonMotiveId] = motive_mappings[motive_id]

        species = CommonSpecies.get_species(sim_info)
        mapped_motive_id = motive_species_mapping.get(species, motive_id)

        if mapped_motive_id == CommonMotiveId.HUNGER:
            if CommonOccultUtils.is_vampire(sim_info):
                mapped_motive_id = CommonMotiveId.VAMPIRE_THIRST
            elif CommonOccultUtils.is_plant_sim(sim_info):
                mapped_motive_id = CommonMotiveId.PLANT_SIM_WATER
        if mapped_motive_id == CommonMotiveId.HYGIENE:
            if CommonOccultUtils.is_mermaid(sim_info):
                mapped_motive_id = CommonMotiveId.MERMAID_HYDRATION
        return mapped_motive_id

    @classmethod
    def _get_motive_mappings(cls) -> Dict[Union[CommonMotiveId, CommonInt, int], Dict[CommonSpecies, Union[CommonMotiveId, CommonInt, int]]]:
        if CommonSimMotiveUtils._MOTIVE_MAPPINGS is not None:
            return CommonSimMotiveUtils._MOTIVE_MAPPINGS

        CommonSimMotiveUtils._MOTIVE_MAPPINGS = {
            CommonMotiveId.HUNGER: {
                CommonSpecies.HUMAN: CommonMotiveId.HUNGER,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_HUNGER,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_HUNGER,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_HUNGER,
                CommonSpecies.FOX: CommonMotiveId.HUNGER,
                CommonSpecies.HORSE: CommonMotiveId.PET_HORSE_HUNGER
            },
            CommonMotiveId.HYGIENE: {
                CommonSpecies.HUMAN: CommonMotiveId.HYGIENE,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_HYGIENE,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_HYGIENE,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_HYGIENE,
                CommonSpecies.FOX: CommonMotiveId.ANIMAL_FOX_HYGIENE,
                CommonSpecies.HORSE: CommonMotiveId.PET_HORSE_HYGIENE
            },
            CommonMotiveId.MERMAID_HYDRATION: {
                CommonSpecies.HUMAN: CommonMotiveId.HYGIENE,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_HYGIENE,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_HYGIENE,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_HYGIENE,
                CommonSpecies.FOX: CommonMotiveId.HYGIENE,
                CommonSpecies.HORSE: CommonMotiveId.PET_HORSE_HYGIENE
            },
            CommonMotiveId.ENERGY: {
                CommonSpecies.HUMAN: CommonMotiveId.ENERGY,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_ENERGY,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_ENERGY,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_ENERGY,
                CommonSpecies.FOX: CommonMotiveId.ENERGY,
                CommonSpecies.HORSE: CommonMotiveId.PET_HORSE_ENERGY
            },
            CommonMotiveId.BLADDER: {
                CommonSpecies.HUMAN: CommonMotiveId.BLADDER,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_BLADDER,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_BLADDER,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_BLADDER,
                CommonSpecies.FOX: CommonMotiveId.ANIMAL_FOX_BLADDER,
                CommonSpecies.HORSE: CommonMotiveId.PET_HORSE_BLADDER
            },
            CommonMotiveId.BOWEL: {
                CommonSpecies.HUMAN: CommonMotiveId.BOWEL,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_BOWEL,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_BOWEL,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_BOWEL,
                CommonSpecies.FOX: CommonMotiveId.BOWEL,
                CommonSpecies.HORSE: CommonMotiveId.BOWEL
            },
            CommonMotiveId.SOCIAL: {
                CommonSpecies.HUMAN: CommonMotiveId.SOCIAL,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_AFFECTION,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_AFFECTION,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_AFFECTION,
                CommonSpecies.FOX: CommonMotiveId.SOCIAL,
                CommonSpecies.HORSE: CommonMotiveId.PET_HORSE_SOCIAL
            },
            CommonMotiveId.FUN: {
                CommonSpecies.HUMAN: CommonMotiveId.FUN,
                CommonSpecies.CAT: CommonMotiveId.PET_CAT_PLAY,
                CommonSpecies.LARGE_DOG: CommonMotiveId.PET_DOG_PLAY,
                CommonSpecies.SMALL_DOG: CommonMotiveId.PET_DOG_PLAY,
                CommonSpecies.FOX: CommonMotiveId.FUN,
                CommonSpecies.HORSE: CommonMotiveId.PET_HORSE_FUN
            }
        }
        return CommonSimMotiveUtils._MOTIVE_MAPPINGS


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_motive_level',
    'Print the current level of a Motive for a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('motive', 'Motive Id or Tuning Name', 'The tuning name or decimal identifier of a Motive.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to check.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_print_motive_level(output: CommonConsoleCommandOutput, motive: TunableInstanceParam(Types.STATISTIC), sim_info: SimInfo = None):
    if motive is None:
        output('ERROR: No Motive specified or Motive did not exist!')
        return
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    output(f'Printing motive level of Motive {motive} for Sim {sim_info}')
    motive_level = CommonSimMotiveUtils.get_motive_level(sim_info, motive)
    output(f'Motive Level of {motive}: {motive_level}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_motive_level',
    'Set the current level of a Motive for a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('motive', 'Motive Id or Tuning Name', 'The tuning name or decimal identifier of a Motive.'),
        CommonConsoleCommandArgument('level', 'Decimal Number', 'The amount to set the motive level to between -100 and 100.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to change.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_set_motive_level(output: CommonConsoleCommandOutput, motive: TunableInstanceParam(Types.STATISTIC), level: float, sim_info: SimInfo = None):
    if motive is None:
        output('ERROR: Failed, Motive not specified or Motive did not exist! s4clib.set_motive_level <motive_name_or_id> <level> [opt_sim=None]')
        return
    if sim_info is None:
        return
    output(f'Attempting to set motive {motive} for Sim {sim_info} to {level}')
    if CommonSimMotiveUtils.set_motive_level(sim_info, motive, level):
        output(f'SUCCESS: Successfully set the motive level of motive {motive} for Sim {sim_info} to {level}.')
    else:
        output(f'FAILED: Failed to set motive level of motive {motive} for Sim {sim_info} to {level}.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.max_all_motives',
    'Set all Motive Levels to their maximum for a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to change.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_max_all_motives(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        return
    CommonSimMotiveUtils.set_all_motives_max(sim_info)
    output(f'SUCCESS: Maxed the motives of {sim_info}.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.max_world_motives',
    'Set all Motive Levels to their maximum for all Sims.'
)
def _common_max_world_motives(output: CommonConsoleCommandOutput):
    sim_count = 0
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
        CommonSimMotiveUtils.set_all_motives_max(sim_info)
        sim_count += 1
    output('Maxed the motives of {} Sim(s).'.format(sim_count))
