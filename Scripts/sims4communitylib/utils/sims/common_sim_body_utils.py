"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims.sim_info import SimInfo
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimBodyUtils:
    """Utilities for manipulating the body of Sims.

    """

    @staticmethod
    def get_wading_size(sim_info: SimInfo) -> Tuple[int, int]:
        """get_wading_size(sim_info)

        Retrieve the size of a Sim if they were to wade in an Ocean of water.

        .. note:: This function is obsolete. Please use :func:`~get_ocean_wading_size` instead.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A tuple indicating the x and y wading size of a Sim from their origin point.
        :rtype: Tuple[int, int]
        """
        return CommonSimBodyUtils.get_ocean_wading_size(sim_info)

    @staticmethod
    def get_ocean_wading_size(sim_info: SimInfo) -> Tuple[int, int]:
        """get_ocean_wading_size(sim_info)

        Retrieve the size of a Sim if they were to wade in an Ocean of water.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A tuple indicating the x and y Ocean wading size of a Sim from their origin point.
        :rtype: Tuple[int, int]
        """
        # noinspection PyBroadException
        try:
            from world.ocean_tuning import OceanTuning
        except:
            return 0, 0
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return 0, 0
        wading_interval = OceanTuning.get_actor_wading_interval(sim)
        if wading_interval is None:
            return 0, 0
        return wading_interval.lower_bound, wading_interval.upper_bound

    @staticmethod
    def get_pond_wading_size(sim_info: SimInfo) -> Tuple[int, int]:
        """get_wading_size(sim_info)

        Retrieve the size of a Sim if they were to wade in a pond of water.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A tuple indicating the x and y Pond wading size of a Sim from their origin point.
        :rtype: Tuple[int, int]
        """
        # noinspection PyBroadException
        try:
            from objects.pools.pond_utils import PondUtils
        except:
            return 0, 0
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return 0, 0
        wading_interval = PondUtils.get_actor_wading_interval(sim)
        if wading_interval is None:
            return 0, 0
        return wading_interval.lower_bound, wading_interval.upper_bound

    @classmethod
    def set_fit_level(cls, sim_info: SimInfo, level: float):
        """set_fit_level(sim_info, level)

        Set the Fit level of a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param level: The Fit level to set the Sim to.
        :type level: float
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        from objects.components.consumable_component import ConsumableComponent
        sim.commodity_tracker.set_value(ConsumableComponent.FIT_COMMODITY, level)
        sim_info._sim_ref().needs_fitness_update = True
        sim_info.update_fitness_state()

    @classmethod
    def get_fit_level(cls, sim_info: SimInfo) -> float:
        """get_fit_level(sim_info)

        Get the Fit level of a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :return: The Fit level of the Sim.
        :rtype: float
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        from objects.components.consumable_component import ConsumableComponent
        return sim.commodity_tracker.get_value(ConsumableComponent.FIT_COMMODITY)

    @classmethod
    def set_fat_level(cls, sim_info: SimInfo, level: float):
        """set_fat_level(sim_info, level)

        Set the Fat level of a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param level: The Fat level to set the Sim to.
        :type level: float
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        from objects.components.consumable_component import ConsumableComponent
        sim.commodity_tracker.set_value(ConsumableComponent.FAT_COMMODITY, level)
        sim_info._sim_ref().needs_fitness_update = True
        sim_info.update_fitness_state()

    @classmethod
    def get_fat_level(cls, sim_info: SimInfo) -> float:
        """get_fat_level(sim_info)

        Get the Fat level of a Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :return: The Fat level of the Sim.
        :rtype: float
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        from objects.components.consumable_component import ConsumableComponent
        return sim.commodity_tracker.get_value(ConsumableComponent.FAT_COMMODITY)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4cl.set_fit',
    'Set the Fit level of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('level', 'Number', 'The Fit level to set the Sim to.', is_optional=False),
        CommonConsoleCommandArgument('sim_info', 'Name or ID', 'The name or ID of the Sim to modify.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4cl.set_fit_level',
    )
)
def _common_set_fit_level(output: CommonConsoleCommandOutput, level: float, sim_info: SimInfo = None):
    if sim_info is None:
        output(f'No Sim found with {sim_info}')
        return
    output(f'Setting Fit level of {sim_info} to {level}.')
    CommonSimBodyUtils.set_fit_level(sim_info, level)
    output('Done')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4cl.set_fat',
    'Set the Fat level of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('level', 'Number', 'The Fat level to set the Sim to.', is_optional=False),
        CommonConsoleCommandArgument('sim_info', 'Name or ID', 'The name or ID of the Sim to modify.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4cl.set_fat_level',
    )
)
def _common_set_fat_level(output: CommonConsoleCommandOutput, level: float, sim_info: SimInfo = None):
    if sim_info is None:
        output(f'No Sim found with {sim_info}')
        return
    output(f'Setting Fat level of {sim_info} to {level}.')
    CommonSimBodyUtils.set_fat_level(sim_info, level)
    output('Done')
