"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
import sims4.commands
from typing import Iterator, Callable, Union
from sims.sim import Sim
from sims.sim_info import SimInfo
from objects import ALL_HIDDEN_REASONS
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


class CommonSimUtils:
    """Utilities for retrieving sims in different ways.

    .. note::

        Available commands:

        - `s4clib_testing.display_name_of_currently_active_sim`
        - `s4clib_testing.display_names_of_all_sims`

    """
    @staticmethod
    def get_active_sim() -> Sim:
        """get_active_sim()

        Retrieve a Sim object of the Currently Active Sim.

        .. note:: The Active Sim is the Sim with the Plumbob above their head.

        :return: An instance of the Active Sim.
        :rtype: Sim
        """
        client = services.client_manager().get_first_client()
        return client.active_sim

    @staticmethod
    def get_active_sim_info() -> SimInfo:
        """get_active_sim_info()

        Retrieve a SimInfo object of the Currently Active Sim.

        :return: The SimInfo of the Active Sim.
        :rtype: SimInfo
        """
        client = services.client_manager().get_first_client()
        return client.active_sim_info

    @staticmethod
    def get_sim_info_of_sim_with_name(first_name: str, last_name: str) -> Union[SimInfo, None]:
        """get_sim_info_of_sim_with_name(first_name, last_name)

        Retrieve a SimInfo object for the first Sim with the specified First and Last Name.

        :param first_name: A first name to look for.
        :type first_name: str
        :param last_name: A last name to look for.
        :type last_name: str
        :return: The first Sim found with the specified first and last name or None if no Sim is found.
        :rtype: Union[SimInfo, None]
        """
        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_with_name_generator(first_name, last_name):
            return sim_info
        return None

    @staticmethod
    def get_sim_info_for_all_sims_with_name_generator(first_name: str, last_name: str) -> Iterator[SimInfo]:
        """get_sim_info_for_all_sims_with_name_generator(first_name, last_name)

        Retrieve a SimInfo object for each and every Sim with the specified First and Last Name.

        :param first_name: A first name to look for.
        :type first_name: str
        :param last_name: A last name to look for.
        :type last_name: str
        :return: An iterable of Sims found with the specified first and last name.
        :rtype: Iterator[SimInfo]
        """
        from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
        first_name = first_name.lower()
        last_name = last_name.lower()

        def _first_and_last_name(sim_info: SimInfo) -> bool:
            return CommonSimNameUtils.get_first_name(sim_info).lower() == first_name and CommonSimNameUtils.get_last_name(sim_info).lower() == last_name

        return CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=_first_and_last_name)

    @staticmethod
    def get_all_sims_generator(include_sim_callback: Callable[[SimInfo], bool]=None) -> Iterator[Sim]:
        """get_all_sims_generator(include_sim_callback=None)

        Retrieve a Sim object for each and every Sim (including hidden Sims).

        :param include_sim_callback: If the result of this callback is True, the sim will be included in the results. If set to None, All sims will be included.
        :type include_sim_callback: Callable[[SimInfo], bool], optional
        :return: An iterable of all Sims matching the `include_sim_callback` filter.
        :rtype: Iterator[Sim]
        """
        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback):
            sim_instance = sim_info.get_sim_instance(allow_hidden_flags=ALL_HIDDEN_REASONS)
            if sim_instance is None:
                continue
            yield sim_instance

    @staticmethod
    def get_sim_info_for_all_sims_generator(include_sim_callback: Callable[[SimInfo], bool]=None) -> Iterator[SimInfo]:
        """get_sim_info_for_all_sims_generator(include_sim_callback=None)

        Retrieve a SimInfo object for each and every sim.

        :param include_sim_callback: If the result of this callback is True, the sim will be included in the results. If set to None, All sims will be included.
        :type include_sim_callback: Callable[[SimInfo], bool], optional
        :return: An iterable of all Sims matching the `include_sim_callback` filter.
        :rtype: Iterator[SimInfo]
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
        """get_instanced_sim_info_for_all_sims_generator(include_sim_callback=None)

        Retrieve a SimInfo object for each and every sim.

        .. note:: Only SimInfo with a Sim instance (:func:`~get_sim_instance`) will be returned.

        :param include_sim_callback: If the result of this callback is True, the sim will be included in the results. If set to None, All sims will be included.
        :type include_sim_callback: Callable[[SimInfo], bool], optional
        :return: An iterable of all Sims matching the `include_sim_callback` filter.
        :rtype: Iterator[SimInfo]
        """
        def _is_instanced(_sim_info: SimInfo) -> bool:
            return _sim_info.get_sim_instance(allow_hidden_flags=ALL_HIDDEN_REASONS) is not None

        include_sim_callback = CommonFunctionUtils.run_predicates_as_one((_is_instanced, include_sim_callback))
        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback):
            yield sim_info

    @staticmethod
    def get_sim_id(sim_identifier: Union[int, Sim, SimInfo]) -> int:
        """get_sim_id(sim_identifier)

        Retrieve a SimId (int) from a Sim identifier.

        :param sim_identifier: The identifier or instance of a Sim.
        :type sim_identifier: Union[int, Sim, SimInfo]
        :return: An identifier for the Sim instance.
        :rtype: int
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
        """get_sim_info(sim_identifier)

        Retrieve a SimInfo instance from a sim identifier.

        :param sim_identifier: The identifier or instance of a Sim to use.
        :type sim_identifier: Union[int, Sim, SimInfo]
        :return: The SimInfo of the specified Sim instance or None if SimInfo is not found.
        :rtype: Union[SimInfo, None]
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
        """get_sim_instance(sim_identifier)

        Retrieve a Sim instance from a sim identifier.

        :param sim_identifier: The identifier or instance of a Sim to use.
        :type sim_identifier: Union[int, Sim, SimInfo]
        :return: The instance of the specified Sim or None if no instance was found.
        :rtype: Union[Sim, None]
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
