"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from objects.game_object import GameObject
from server.client import Client
from sims.sim_info import SimInfo
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonCameraUtils:
    """ Utilities for controlling the camera. """
    @classmethod
    def start_focus(cls, target: Union[SimInfo, GameObject, CommonVector3], follow: bool=True, client: Client=None) -> bool:
        """start_focus(target, follow=True, client=None)

        Focus the player camera on something.

        :param target: The Target SimInfo, Game Object, or Position to focus the camera on.
        :type target: Union[Sim, GameObject, CommonVector3]
        :param follow: If True, the camera will follow the object after focusing on it. If False, the camera will not follow the object after focusing on it. Default is True.
        :type follow: bool, optional
        :param client: The client to focus on the Sim. If None, the active client will be used. Default is None.
        :type client: Client, optional
        :return: True, if the camera was focused on the specified target.
        """
        if CommonTypeUtils.is_sim_or_sim_info(target):
            cls.start_focus_on_sim(target, follow=follow, client=client)
        elif CommonTypeUtils.is_game_object(target):
            cls.start_focus_on_object(target, follow=follow)
        elif isinstance(target, CommonVector3):
            cls.start_focus_on_position(target, client=client)
        else:
            return False
        return True

    @classmethod
    def start_focus_on_sim(cls, sim_info: SimInfo, follow: bool=True, client: Client=None) -> None:
        """start_focus_on_sim(sim_info, follow=True, client=None)

        Focus the player camera on a Sim.

        :param sim_info: The SimInfo of the Sim to focus the camera on.
        :type sim_info: SimInfo
        :param follow: If True, the camera will follow the object after focusing on it. If False, the camera will not follow the object after focusing on it. Default is True.
        :type follow: bool, optional
        :param client: The client to focus on the Sim. If None, the active client will be used. Default is None.
        :type client: Client, optional
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return
        from camera import focus_on_sim
        focus_on_sim(sim=sim, follow=follow, client=client)

    @classmethod
    def start_focus_on_position(cls, position: CommonVector3, client: Client=None) -> None:
        """start_focus_on_position(position, client=None)

        Focus the player camera on a position.

        :param position: The position to focus the camera on.
        :type position: CommonVector3
        :param client: The client to focus on the position. If None, the active client will be used. Default is None.
        :type client: Client, optional
        """
        from camera import focus_on_position
        focus_on_position(position, client=client)

    @classmethod
    def start_focus_on_object(cls, game_object: GameObject, follow: bool=True) -> None:
        """start_focus_on_object(game_object, follow=True)

        Focus the player camera on a game object.

        :param game_object: The object to focus on.
        :type game_object: GameObject
        :param follow: If True, the camera will follow the object after focusing on it. If False, the camera will not follow the object after focusing on it. Default is True.
        :type follow: bool, optional
        """
        from camera import focus_on_object
        focus_on_object(object=game_object, follow=follow)

    @classmethod
    def stop_focus_on_object(cls, game_object: GameObject):
        """stop_focus_on_object(game_object)

        Stop focusing the player camera on a game object.

        :param game_object: The object to stop focusing on.
        :type game_object: GameObject
        """
        from camera import cancel_focus
        cancel_focus(object=game_object)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.focus_on_object',
    'Move the camera to focus on an object.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Game Object Id', 'The instance id of the object to focus on.'),
    )
)
def _common_focus_on_object_command(output: CommonConsoleCommandOutput, game_object: GameObject):
    if game_object is None:
        return
    output(f'Attempting to focus the camera on object {game_object}.')
    if CommonCameraUtils.start_focus(game_object):
        output(f'SUCCESS: Successfully focused the camera on object {game_object}.')
    else:
        output(f'FAILED: Failed to focus the camera on object {game_object}.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.focus_on_sim',
    'Move the camera to focus on a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Name or Id', 'The instance id of the Sim to focus on.'),
    )
)
def _common_focus_on_sim_command(output: CommonConsoleCommandOutput, sim_info: SimInfo):
    if sim_info is None:
        return
    output(f'Attempting to focus the camera on Sim {sim_info}.')
    if CommonCameraUtils.start_focus(sim_info):
        output(f'SUCCESS: Successfully focused the camera on Sim {sim_info}.')
    else:
        output(f'FAILED: Failed to focus the camera on Sim {sim_info}.')
