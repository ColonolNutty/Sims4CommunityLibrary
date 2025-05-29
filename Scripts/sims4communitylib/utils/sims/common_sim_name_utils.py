"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims.sim_info import SimInfo
from sims.sim_spawner import SimSpawner
from sims.sim_spawner_enums import SimNameType
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.common_sim_name_type import CommonSimNameType
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.misc.common_text_utils import CommonTextUtils


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
        if full_name == ' ':
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
    def create_random_first_name(gender: CommonGender, species: CommonSpecies=CommonSpecies.HUMAN, sim_name_type: CommonSimNameType=CommonSimNameType.DEFAULT) -> str:
        """create_random_first_name(gender, species=CommonSpecies.HUMAN, sim_name_type=CommonSimNameType.DEFAULT)

        Create a random first name.

        :param gender: A gender.
        :type gender: CommonGender
        :param species: A species. Default is HUMAN.
        :type species: CommonSpecies, optional
        :param sim_name_type: The Sim Name Type determines from which list of names to randomize the name from. Default is CommonSimNameType.DEFAULT.
        :type sim_name_type: CommonSimNameType, optional
        :return: A random first name.
        :rtype: str
        """
        vanilla_gender = CommonGender.convert_to_vanilla(gender)
        vanilla_species = CommonSpecies.convert_to_vanilla(species)
        vanilla_sim_name_type = CommonSimNameType.convert_to_vanilla(sim_name_type)
        return SimSpawner.get_random_first_name(vanilla_gender, species=vanilla_species, sim_name_type_override=vanilla_sim_name_type)

    @staticmethod
    def create_random_last_name(gender: CommonGender, species: CommonSpecies=CommonSpecies.HUMAN, sim_name_type: CommonSimNameType=CommonSimNameType.DEFAULT) -> str:
        """create_random_last_name(gender, species=CommonSpecies.HUMAN, sim_name_type=CommonSimNameType.DEFAULT)

        Create a random last name.

        :param gender: A gender.
        :type gender: CommonGender
        :param species: A species. Default is HUMAN.
        :type species: CommonSpecies, optional
        :param sim_name_type: The Sim Name Type determines from which list of names to randomize the name from. Default is CommonSimNameType.DEFAULT.
        :type sim_name_type: CommonSimNameType, optional
        :return: A random last name.
        :rtype: str
        """
        account = SimSpawner._get_default_account()
        vanilla_gender = CommonGender.convert_to_vanilla(gender)
        vanilla_species = CommonSpecies.convert_to_vanilla(species)
        vanilla_sim_name_type = CommonSimNameType.convert_to_vanilla(sim_name_type)
        language = SimSpawner._get_language_for_locale(account.locale)
        family_name = SimSpawner._get_random_last_name(language, sim_name_type=vanilla_sim_name_type)
        if sim_name_type == SimNameType.DEFAULT:
            last_name = SimSpawner.get_last_name(family_name, vanilla_gender, species=vanilla_species)
        else:
            from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
            last_name = SimSpawner._get_family_name_for_gender(language, family_name, CommonGenderUtils.is_female_gender(gender), sim_name_type=vanilla_sim_name_type)
        return last_name


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.randomize_name', 'Randomize the first and last names of a Sim.', command_arguments=(
    CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to change the first and last names of.'),
    CommonConsoleCommandArgument('sim_name_type', 'CommonSimNameType', f'Determines from which list of names to randomize the name from. Valid Values: {CommonSimNameType.get_comma_separated_names_string()}'),
))
def _common_randomize_name(output: CommonConsoleCommandOutput, sim_info: SimInfo=None, sim_name_type: CommonSimNameType=CommonSimNameType.DEFAULT):
    if sim_info is None:
        return
    gender = CommonGender.get_gender(sim_info)
    species = CommonSpecies.get_species(sim_info)
    first_name = CommonSimNameUtils.create_random_first_name(gender, species=species, sim_name_type=sim_name_type)
    first_name = CommonTextUtils.capitalize(first_name)
    output(f'Setting the first name of Sim {sim_info} to {first_name}')
    CommonSimNameUtils.set_first_name(sim_info, first_name)
    last_name = CommonSimNameUtils.create_random_last_name(gender, species=species, sim_name_type=sim_name_type)
    last_name = CommonTextUtils.capitalize(last_name)
    output(f'Setting the last name of Sim {sim_info} to {last_name}')
    CommonSimNameUtils.set_last_name(sim_info, last_name)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.set_first_name', 'Set the first name of a Sim.', command_arguments=(
    CommonConsoleCommandArgument('first_name', 'Text', 'The first name to give to the Sim.'),
    CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to change the first name of.'),
))
def _common_set_first_name(output: CommonConsoleCommandOutput, first_name: str, sim_info: SimInfo=None):
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    if not first_name:
        output(f'Failed, \'{first_name}\' is not a valid first name.')
        return
    first_name = CommonTextUtils.capitalize(first_name)
    output(f'Setting the first name of Sim {sim_info} to {first_name}')
    CommonSimNameUtils.set_first_name(sim_info, first_name)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.randomize_first_name', 'Randomize the first name of a Sim.', command_arguments=(
    CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to change the first name of.'),
    CommonConsoleCommandArgument('sim_name_type', 'CommonSimNameType', f'Determines from which list of names to randomize the name from. Valid Values: {CommonSimNameType.get_comma_separated_names_string()}'),
))
def _common_randomize_first_name(output: CommonConsoleCommandOutput, sim_info: SimInfo=None, sim_name_type: CommonSimNameType=CommonSimNameType.DEFAULT):
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    gender = CommonGender.get_gender(sim_info)
    species = CommonSpecies.get_species(sim_info)
    first_name = CommonSimNameUtils.create_random_first_name(gender, species=species, sim_name_type=sim_name_type)
    first_name = CommonTextUtils.capitalize(first_name)
    output(f'Setting the first name of Sim {sim_info} to {first_name}')
    CommonSimNameUtils.set_first_name(sim_info, first_name)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.set_last_name', 'Set the last name of a Sim.', command_arguments=(
    CommonConsoleCommandArgument('last_name', 'Text', 'The last name to give to the Sim.'),
    CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to change the last name of.'),
))
def _common_set_last_name(output: CommonConsoleCommandOutput, last_name: str, sim_info: SimInfo=None):
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    last_name = CommonTextUtils.capitalize(last_name)
    output(f'Setting the last name of Sim {sim_info} to {last_name}')
    CommonSimNameUtils.set_last_name(sim_info, last_name)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.randomize_last_name', 'Randomize the last name of a Sim.', command_arguments=(
    CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to change the last name of.'),
    CommonConsoleCommandArgument('sim_name_type', 'CommonSimNameType', f'Determines from which list of names to randomize the name from. Valid Values: {CommonSimNameType.get_comma_separated_names_string()}'),
))
def _common_randomize_last_name(output: CommonConsoleCommandOutput, sim_info: SimInfo=None, sim_name_type: CommonSimNameType=CommonSimNameType.DEFAULT):
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    gender = CommonGender.get_gender(sim_info)
    species = CommonSpecies.get_species(sim_info)
    last_name = CommonSimNameUtils.create_random_last_name(gender, species=species, sim_name_type=sim_name_type)
    last_name = CommonTextUtils.capitalize(last_name)
    output(f'Setting the last name of Sim {sim_info} to {last_name}')
    CommonSimNameUtils.set_last_name(sim_info, last_name)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.set_name', 'Set the full name of a Sim.', command_arguments=(
    CommonConsoleCommandArgument('first_name', 'Text', 'The first name to give to the Sim.'),
    CommonConsoleCommandArgument('last_name', 'Text', 'The last name to give to the Sim.'),
    CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to change the first and last name of.'),
))
def _common_set_name(output: CommonConsoleCommandOutput, first_name: str, last_name: str, sim_info: SimInfo=None):
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    if not first_name:
        output(f'Failed, \'{first_name}\' is not a valid first name.')
        return
    if not last_name:
        output(f'Failed, \'{last_name}\' is not a valid last name.')
        return
    first_name = CommonTextUtils.capitalize(first_name)
    last_name = CommonTextUtils.capitalize(last_name)
    output(f'Setting the name of Sim {sim_info} to {first_name} {last_name}')
    CommonSimNameUtils.set_first_name(sim_info, first_name)
    CommonSimNameUtils.set_last_name(sim_info, last_name)
