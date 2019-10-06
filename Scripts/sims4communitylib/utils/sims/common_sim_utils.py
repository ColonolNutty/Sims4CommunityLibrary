"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
import sims4.commands
from typing import Iterator, Callable, Union
from sims.sim import Sim
from sims.sim_info import SimInfo
from objects import ALL_HIDDEN_REASONS


class CommonSimUtils:
    """ Utilities for retrieving sims in different ways. """
    @staticmethod
    def get_active_sim() -> Sim:
        """
            Retrieve a Sim object of the Currently Active Sim.
        """
        client = services.client_manager().get_first_client()
        return client.active_sim

    @staticmethod
    def get_active_sim_info() -> SimInfo:
        """
            Retrieve a SimInfo object of the Currently Active Sim.
        """
        return CommonSimUtils.get_active_sim().sim_info

    @staticmethod
    def get_all_sims_generator(include_sim_callback: Callable[[SimInfo], bool]=None) -> Iterator[Sim]:
        """
            Retrieve a Sim object for each and every sim (including hidden sims).
        :param include_sim_callback: If the result of this callback is True, the sim will be included in the results. If set to None, All sims will be included.
        """
        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback):
            sim_instance = sim_info.get_sim_instance(allow_hidden_flags=ALL_HIDDEN_REASONS)
            if sim_instance is None:
                continue
            yield sim_instance

    @staticmethod
    def get_sim_info_for_all_sims_generator(include_sim_callback: Callable[[SimInfo], bool]=None) -> Iterator[SimInfo]:
        """
            Retrieve a SimInfo object for each and every sim.
        :param include_sim_callback: If the result of this callback is True, the sim will be included in the results. If set to None, All sims will be included.
        """
        sim_info_list = list(services.sim_info_manager().get_all())
        for sim_info in sim_info_list:
            if sim_info is None:
                continue
            if include_sim_callback is not None and include_sim_callback(sim_info) is False:
                continue
            yield sim_info

    @staticmethod
    def get_instanced_sim_info_for_all_sims_generator(include_sim_callback: Callable[[SimInfo], bool]=None) -> Iterator[SimInfo]:
        """
            Retrieve a SimInfo object for each and every sim.

            Note: Only SimInfo with a Sim instance (get_sim_instance) will be returned.
        :param include_sim_callback: If the result of this callback is True, the sim will be included in the results. If set to None, All sims will be included.
        """
        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback):
            sim_instance = sim_info.get_sim_instance(allow_hidden_flags=ALL_HIDDEN_REASONS)
            if sim_instance is None:
                continue
            yield sim_info

    @staticmethod
    def get_sim_id(sim_identifier: Union[int, Sim, SimInfo]) -> int:
        """
            Retrieve a SimId (int) from a sim identifier.
        """
        if sim_identifier is None:
            return 0
        if isinstance(sim_identifier, int):
            return sim_identifier
        if isinstance(sim_identifier, Sim):
            return sim_identifier.sim_id
        if isinstance(sim_identifier, SimInfo):
            return sim_identifier.id
        return sim_identifier

    @staticmethod
    def get_sim_info(sim_identifier: Union[int, Sim, SimInfo]) -> Union[SimInfo, None]:
        """
            Retrieve a SimInfo instance from a sim identifier.
        """
        if sim_identifier is None or isinstance(sim_identifier, SimInfo):
            return sim_identifier
        if isinstance(sim_identifier, Sim):
            return sim_identifier.sim_info
        if isinstance(sim_identifier, int):
            return services.sim_info_manager().get(sim_identifier)
        return sim_identifier

    @staticmethod
    def get_sim_instance(sim_identifier: Union[int, Sim, SimInfo]) -> Union[Sim, None]:
        """
            Retrieve a Sim instance from a sim identifier.
        """
        if sim_identifier is None or isinstance(sim_identifier, Sim):
            return sim_identifier
        if isinstance(sim_identifier, SimInfo):
            return sim_identifier.get_sim_instance(allow_hidden_flags=ALL_HIDDEN_REASONS)
        if isinstance(sim_identifier, int):
            sim_info = services.sim_info_manager().get(sim_identifier)
            if sim_info is None:
                return None
            return CommonSimUtils.get_sim_instance(sim_info)
        return sim_identifier


@sims4.commands.Command('s4clib_testing.display_name_of_currently_active_sim', command_type=sims4.commands.CommandType.Live)
def _s4clib_testing_display_name_of_currently_active_sim(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    sim_info = CommonSimUtils.get_active_sim_info()
    # noinspection PyPropertyAccess
    output('Currently Active Sim: {} {}'.format(sim_info.first_name, sim_info.last_name))


@sims4.commands.Command('s4clib_testing.display_names_of_all_sims', command_type=sims4.commands.CommandType.Live)
def _s4clib_testing_display_names_of_all_sims(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing the names of all sims (This may take awhile).')
    current_count = 1
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
        # noinspection PyPropertyAccess
        output('{}: {} {}'.format(str(current_count), sim_info.first_name, sim_info.last_name))
        current_count += 1
    output('Done showing the names of all sims.')
