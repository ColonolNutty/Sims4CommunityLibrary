"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from interactions.utils.plumbbob import unslot_plumbbob, reslot_plumbbob
from sims.sim_info import SimInfo
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimPlumbobSlot:
    """CommonSimPlumbobSlot(offset_position, bone_name='b__ROOT__', balloon_offset_position=CommonVector3.empty())

    Used to place a Plumbob.

    :param offset_position: The position of the plumbob.
    :type offset_position: CommonVector3
    :param bone_name: The name of the bone to slot the Plumbob to. Default is 'b__ROOT__'
    :type bone_name: str, optional
    :param balloon_offset_position: The position of the Balloon above Sims heads. Default is CommonVector3.empty().
    :type balloon_offset_position: CommonVector3, optional
    """
    def __init__(self, offset_position: CommonVector3, bone_name: str='b__ROOT__', balloon_offset_position: CommonVector3=CommonVector3.empty()):
        self._offset_position = offset_position
        self._bone_name = bone_name
        self._balloon_offset_position = balloon_offset_position

    @property
    def bone_name(self) -> str:
        """ The name of a Bone.

        :return: The name of a Bone.
        :rtype: str
        """
        return self._bone_name

    @property
    def offset(self) -> CommonVector3:
        """ The offset position of the Plumbob.

        :return: The offset of the Plumbob
        :rtype: CommonVector3
        """
        return self._offset_position

    @property
    def balloon_offset(self) -> CommonVector3:
        """ The offset position of the Balloon.

        :return: The offset of the Balloon
        :rtype: CommonVector3
        """
        return self._balloon_offset_position


class CommonSimPlumbobUtils:
    """ Utilities for manipulating the Plumbob of a Sim. """
    @staticmethod
    def hide_plumbob(sim_info: SimInfo):
        """hide_plumbob(sim_info)

        Hide the plumbob of a Sim.

        .. note:: If the plumbob of the Sim is already hidden, this function will do nothing.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        """
        CommonSimPlumbobUtils.set_plumbob_position(sim_info, CommonVector3(-1000, -1000, -1000))

    @staticmethod
    def show_plumbob(sim_info: SimInfo):
        """show_plumbob(sim_info)

        Show the plumbob of a Sim.

        .. note:: If the plumbob of the Sim is already shown, this function will do nothing.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        """
        CommonSimPlumbobUtils.reset_plumbob_position(sim_info)

    @staticmethod
    def set_plumbob_position(sim_info: SimInfo, position: CommonVector3, bone_name: str='b__ROOT__', balloon_position: CommonVector3=CommonVector3.empty()):
        """set_plumbob_position(sim_info, position, bone_name='b__ROOT__', balloon_position=CommonVector3.empty())

        Set the position of the Plumbob for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param position: The position to set the plumbob to.
        :type position: CommonVector3
        :param bone_name: The name of the bone to slot the Plumbob to. Default is 'b__ROOT__'
        :type bone_name: str, optional
        :param balloon_position: The position of the Balloon above Sims heads. Default is CommonVector3.empty().
        :type balloon_position: CommonVector3, optional
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return
        reslot_plumbbob(sim, CommonSimPlumbobSlot(position, bone_name=bone_name, balloon_offset_position=balloon_position))

    @staticmethod
    def reset_plumbob_position(sim_info: SimInfo):
        """reset_plumbob_position(sim_info)

        Reset the position of the Plumbob for a Sim to it's original position.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return
        unslot_plumbbob(sim)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.hide_plumbob', 'Hide the plumbob above a Sim.', command_arguments=(
    CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to hide the plumbob of.', is_optional=True, default_value='Active Sim'),
))
def _common_hide_plumbob(output: CommonConsoleCommandOutput, sim_info: SimInfo=None):
    if sim_info is None:
        return
    output(f'Hiding plumbob for Sim {sim_info}')
    CommonSimPlumbobUtils().hide_plumbob(sim_info)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.show_plumbob', 'Show the plumbob above a Sim.', command_arguments=(
    CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to show the plumbob of.', is_optional=True, default_value='Active Sim'),
))
def _common_show_plumbob(output: CommonConsoleCommandOutput, sim_info: SimInfo=None):
    if sim_info is None:
        return
    output(f'Showing plumbob for Sim {sim_info}')
    CommonSimPlumbobUtils().show_plumbob(sim_info)
