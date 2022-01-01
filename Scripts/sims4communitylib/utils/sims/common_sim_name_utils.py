"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from server_commands.argument_helpers import OptionalTargetParam
from sims.sim_info import SimInfo
from sims.sim_spawner import SimSpawner
from sims.sim_spawner_enums import SimNameType
from sims4.commands import Command, CommandType, CheatOutput
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimNameUtils:
    """Utilities for manipulating the name of Sims.

    """
    @staticmethod
    def has_name(sim_info: SimInfo) -> bool:
        """has_name(sim_info)

        Determine if a Sim has a name.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the specified Sim has a name. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        return CommonSimNameUtils.get_full_name(sim_info) != ''

    @staticmethod
    def set_first_name(sim_info: SimInfo, first_name: str):
        """set_first_name(sim_info, first_name)

        Retrieve the First Name of a Sim.

        :param sim_info: The Sim to set the first name of.
        :type sim_info: SimInfo
        :param first_name: The first name you want the Sim to have.
        :type first_name: str
        """
        if sim_info is None or not hasattr(sim_info, 'first_name'):
            return
        sim_info.first_name = first_name

    @staticmethod
    def set_last_name(sim_info: SimInfo, last_name: str):
        """set_last_name(sim_info, last_name)

        Retrieve the Last Name of a Sim.

        :param sim_info: The Sim to set the last name of.
        :type sim_info: SimInfo
        :param last_name: The last name you want the Sim to have.
        :type last_name: str
        """
        if sim_info is None or not hasattr(sim_info, 'last_name'):
            return
        sim_info.last_name = last_name

    @staticmethod
    def get_first_name(sim_info: SimInfo) -> str:
        """get_first_name(sim_info)

        Retrieve the First Name of a Sim.

        :param sim_info: The Sim to retrieve the first name of.
        :type sim_info: SimInfo
        :return: The first name of the specified Sim.
        :rtype: str
        """
        if sim_info is None or not hasattr(sim_info, 'first_name'):
            return ''
        return getattr(sim_info, 'first_name')

    @staticmethod
    def get_last_name(sim_info: SimInfo) -> str:
        """get_last_name(sim_info)

        Retrieve the Last Name of a Sim.

        :param sim_info: The Sim to retrieve the last name of.
        :type sim_info: SimInfo
        :return: The last name of the specified Sim.
        :rtype: str
        """
        if sim_info is None or not hasattr(sim_info, 'last_name'):
            return ''
        return getattr(sim_info, 'last_name')

    @staticmethod
    def get_full_name(sim_info: SimInfo) -> str:
        """get_full_name(sim_info)

        Retrieve the full name of a Sim.

        .. note:: Resulting Full Name: '{First} {Last}'

        :param sim_info: The Sim to retrieve the full name of.
        :type sim_info: SimInfo
        :return: The full name of the specified Sim.
        :rtype: str
        """
        full_name = '{} {}'.format(CommonSimNameUtils.get_first_name(sim_info), CommonSimNameUtils.get_last_name(sim_info)).strip()
        if full_name == '':
            full_name = 'No Name'
        return full_name

    @staticmethod
    def get_full_names(sim_info_list: Tuple[SimInfo]) -> Tuple[str]:
        """get_full_names(sim_info_list)

        Retrieve a collection of full names for the specified Sims.

        .. note:: Resulting Full Names: ('{First} {Last}', '{First} {Last}', '{First} {Last}', ...)

        :param sim_info_list: A collection of Sims
        :type sim_info_list: Tuple[SimInfo]
        :return: A collection of full names of the specified Sims.
        :rtype: Tuple[str]
        """
        result: Tuple[str] = tuple([CommonSimNameUtils.get_full_name(sim_info) for sim_info in sim_info_list])
        return result

    @staticmethod
    def create_random_first_name(gender: CommonGender, species: CommonSpecies=CommonSpecies.HUMAN, sim_name_type: SimNameType=SimNameType.DEFAULT) -> str:
        """create_random_first_name(gender, species=CommonSpecies.HUMAN, sim_name_type=SimNameType.DEFAULT)

        Create a random first name.

        :param gender: A gender.
        :type gender: CommonGender
        :param species: A species. Default is HUMAN.
        :type species: CommonSpecies, optional
        :param sim_name_type: An override for Sim Name Type. Default is SimNameType.DEFAULT.
        :type sim_name_type: SimNameType, optional
        :return: A random first name.
        :rtype: str
        """
        vanilla_gender = CommonGender.convert_to_vanilla(gender)
        vanilla_species = CommonSpecies.convert_to_vanilla(species)
        return SimSpawner.get_random_first_name(vanilla_gender, species=vanilla_species, sim_name_type_override=sim_name_type)

    @staticmethod
    def create_random_last_name(gender: CommonGender, species: CommonSpecies=CommonSpecies.HUMAN, sim_name_type: SimNameType=SimNameType.DEFAULT) -> str:
        """create_random_last_name(gender, species=CommonSpecies.HUMAN, sim_name_type=SimNameType.DEFAULT)

        Create a random last name.

        :param gender: A gender.
        :type gender: CommonGender
        :param species: A species. Default is HUMAN.
        :type species: CommonSpecies, optional
        :param sim_name_type: An override for Sim Name Type. Default is None.
        :type sim_name_type: Any, optional
        :return: A random last name.
        :rtype: str
        """
        account = SimSpawner._get_default_account()
        vanilla_gender = CommonGender.convert_to_vanilla(gender)
        vanilla_species = CommonSpecies.convert_to_vanilla(species)
        language = SimSpawner._get_language_for_locale(account.locale)
        family_name = SimSpawner._get_random_last_name(language, sim_name_type=sim_name_type)
        if sim_name_type == SimNameType.DEFAULT:
            last_name = SimSpawner.get_last_name(family_name, vanilla_gender, species=vanilla_species)
        else:
            from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
            last_name = SimSpawner._get_family_name_for_gender(language, family_name, CommonGenderUtils.is_female_gender(gender), sim_name_type=sim_name_type)
        return last_name


@Command('s4clib.set_first_name', command_type=CommandType.Live)
def _common_set_first_name(first_name: str=None, opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    if not first_name:
        output(f'Failed, {first_name} is not a valid first name.')
        return
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    CommonSimNameUtils.set_first_name(sim_info, first_name)


@Command('s4clib.set_last_name', command_type=CommandType.Live)
def _common_set_last_name(last_name: str=None, opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    if not last_name:
        output(f'Failed, {last_name} is not a valid last name.')
        return
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    CommonSimNameUtils.set_last_name(sim_info, last_name)


@Command('s4clib.set_name', command_type=CommandType.Live)
def _common_set_name(first_name: str=None, last_name: str=None, opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    if not first_name:
        output(f'Failed, {first_name} is not a valid first name.')
        return
    if not last_name:
        output(f'Failed, {last_name} is not a valid last name.')
        return
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    CommonSimNameUtils.set_first_name(sim_info, first_name)
    CommonSimNameUtils.set_last_name(sim_info, last_name)
