"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from objects.components.ownable_component import OwnableComponent
from objects.game_object import GameObject
from sims.sim_info import SimInfo
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonObjectOwnershipUtils:
    """Utilities for manipulating the ownership of Objects.

    """

    @staticmethod
    def set_owning_household_id(game_object: GameObject, household_id: int) -> bool:
        """set_owning_household_id(game_object, household_id)

        Set the Household that owns the Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param household_id: The decimal identifier of a Household.
        :type household_id: int
        :return: True, if the Household was successfully set as the owner. False, if not.
        :rtype: bool
        """
        if game_object is None or household_id == -1:
            return False
        game_object.set_household_owner_id(household_id)
        return True

    @staticmethod
    def get_owning_household_id(game_object: GameObject) -> int:
        """get_owning_household_id(game_object)

        Retrieve the decimal identifier of the Household that owns the Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The decimal identifier of the Household that owns the object.
        :rtype: int
        """
        if game_object is None:
            return -1
        return game_object.get_household_owner_id()

    @staticmethod
    def set_owning_sim(game_object: GameObject, sim_info: SimInfo, make_sim_sole_owner: bool = True) -> bool:
        """set_owning_sim(game_object, sim_info, make_sim_sole_owner=True)

        Change the ownership of an Object to become owned by the household of a Sim and optional by the Sim themselves.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param make_sim_sole_owner: If True, the Sim will become the sole owner in their household of the Object (In addition to the household owning it). If False, only the household will own the Object. Default is True.
        :type make_sim_sole_owner: bool, optional
        :return: True, if ownership was transferred successfully. False, if not.
        :rtype: bool
        """
        if game_object is None or sim_info is None:
            return False
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return False
        game_object.update_ownership(sim, make_sim_owner=make_sim_sole_owner)
        return True

    @staticmethod
    def get_owning_sim(game_object: GameObject) -> Union[SimInfo, None]:
        """get_owning_sim(game_object)

        Retrieve the Sim that owns an Object, if a Sim owns the Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The SimInfo of the Sim that owns the specified Object or None if no Sim owns the Object.
        :rtype: Union[SimInfo, None]
        """
        if game_object is None:
            return None
        ownable_component: OwnableComponent = CommonObjectOwnershipUtils.get_ownable_component(game_object)
        if ownable_component is None:
            return None
        return CommonSimUtils.get_sim_info(ownable_component.get_sim_owner_id())

    @staticmethod
    def get_ownable_component(game_object: GameObject) -> Union[OwnableComponent, None]:
        """get_ownable_component(game_object)

        Retrieve the Ownable Component of an Object if it has one.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The OwnableComponent of the Object or None if no OwnableComponent was found.
        :rtype: Union[OwnableComponent, None]
        """
        if game_object is None:
            return None
        if not hasattr(game_object, 'ownable_component'):
            return None
        return game_object.ownable_component


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.change_ownership',
    'Change the owner of an object to a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Game Object Instance Id', 'The instance id of a game object to change.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to become the new owner.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.changeownership',
    )
)
def _common_change_ownership(output: CommonConsoleCommandOutput, game_object: GameObject, sim_info: SimInfo = None):
    if sim_info is None:
        output('ERROR: No Sim was specified or the specified Sim was not found!')
        return
    if game_object is None:
        output('ERROR: No object was specified or the specified Game Object was not found.')
        return
    output(f'Attempting to change the owner of object {game_object} to Sim {sim_info}.')
    if CommonObjectOwnershipUtils.set_owning_sim(game_object, sim_info, make_sim_sole_owner=True):
        output(f'SUCCESS: Object {game_object} successfully owned by Sim {sim_info}.')
    else:
        output(f'FAILED: Object {game_object} failed to change ownership to Sim {sim_info}.')
    output(f'Done changing the ownership of object {game_object}.')
