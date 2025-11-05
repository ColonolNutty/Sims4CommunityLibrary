"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from typing import Iterator, Callable, Union

from objects import HiddenReasonFlag, ALL_HIDDEN_REASONS
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims.sim_info_manager import SimInfoManager
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.misc.common_game_client_utils import CommonGameClientUtils


class CommonSimUtils:
    """Utilities for retrieving Sims in different ways.

    .. note::

        Available commands:

        - `s4clib_testing.display_name_of_currently_active_sim`
        - `s4clib_testing.display_names_of_all_sims`

    """
    @classmethod
    def get_active_sim(cls) -> Union[Sim, None]:
        """get_active_sim()

        Retrieve a Sim object of the Currently Active Sim.

        .. note:: The Active Sim is the Sim with the Plumbob above their head.

        :return: An instance of the Active Sim or None if not found.
        :rtype: Union[Sim, None]
        """
        client = CommonGameClientUtils.get_first_game_client()
        if client is None:
            return None
        return client.active_sim

    @classmethod
    def get_active_sim_id(cls) -> int:
        """get_active_sim_id()

        Retrieve the decimal identifier for the Currently Active Sim.

        .. note:: The Active Sim is the Sim with the Plumbob above their head.

        :return: The decimal identifier of the active Sim or -1 if the active Sim does not have an id or if no active Sim was found.
        :rtype: int
        """
        active_sim_info = cls.get_active_sim_info()
        if active_sim_info is None:
            return -1
        return cls.get_sim_id(active_sim_info)

    @classmethod
    def get_active_sim_info(cls) -> Union[SimInfo, None]:
        """get_active_sim_info()

        Retrieve a SimInfo object of the Currently Active Sim.

        :return: The SimInfo of the Active Sim or None if not found.
        :rtype: Union[SimInfo, None]
        """
        client = CommonGameClientUtils.get_first_game_client()
        if client is None:
            return None
        # noinspection PyPropertyAccess
        return client.active_sim_info

    @classmethod
    def is_active_sim(cls, sim_info: SimInfo) -> bool:
        """is_active_sim(sim_info)

        Determine if a Sim is the active Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the specified Sim is the active Sim. False, if not.
        :rtype: bool
        """
        return cls.get_active_sim_info() is sim_info

    @classmethod
    def is_instanced(cls, sim_info: SimInfo, allow_hidden_flags: HiddenReasonFlag = ALL_HIDDEN_REASONS) -> bool:
        """is_instanced(\
            sim_info,\
            allow_hidden_flags=ALL_HIDDEN_REASONS\
         )

        Determine if a Sim is instanced.

        .. note:: Only SimInfo with a Sim instance (:func:`~get_sim_instance`) are considered as instanced. In other words, if a Sim does not have a Sim instance, it means they are not loaded on the current lot.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param allow_hidden_flags: Flags to indicate the types of hidden Sims to consider as being instanced. Default is ALL_HIDDEN_REASONS
        :type allow_hidden_flags: HiddenReasonFlag, optional
        :return: True, if the Sim is instanced. False, if not.
        :rtype: bool
        """
        return cls.get_sim_instance(sim_info, allow_hidden_flags=allow_hidden_flags) is not None

    @classmethod
    def get_sim_info_of_sim_with_name(cls, first_name: str, last_name: str) -> Union[SimInfo, None]:
        """get_sim_info_of_sim_with_name(first_name, last_name)

        Retrieve a SimInfo object for the first Sim with the specified First and Last Name.

        :param first_name: A first name to look for.
        :type first_name: str
        :param last_name: A last name to look for.
        :type last_name: str
        :return: The first Sim found with the specified first and last name or None if no Sim is found.
        :rtype: Union[SimInfo, None]
        """
        for sim_info in cls.get_sim_info_for_all_sims_with_name_generator(first_name, last_name):
            return sim_info
        return None

    @classmethod
    def get_sim_info_for_all_sims_with_last_name_generator(cls, last_name: str) -> Iterator[SimInfo]:
        """get_sim_info_for_all_sims_with_last_name_generator(last_name)

        Retrieve a SimInfo object for each and every Sim with the specified Last Name.

        :param last_name: A last name to look for.
        :type last_name: str
        :return: An iterator of Sims found with the specified last name.
        :rtype: Iterator[SimInfo]
        """
        from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
        last_name = last_name.lower()

        def _has_last_name(sim_info: SimInfo) -> bool:
            return CommonSimNameUtils.get_last_name(sim_info).lower() == last_name

        return cls.get_sim_info_for_all_sims_generator(include_sim_callback=_has_last_name)

    @classmethod
    def get_sim_info_for_all_sims_with_first_name_generator(cls, first_name: str) -> Iterator[SimInfo]:
        """get_sim_info_for_all_sims_with_first_name_generator(first_name)

        Retrieve a SimInfo object for each and every Sim with the specified First Name.

        :param first_name: A first name to look for.
        :type first_name: str
        :return: An iterator of Sims found with the specified first name.
        :rtype: Iterator[SimInfo]
        """
        from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
        first_name = first_name.lower()

        def _has_first_name(sim_info: SimInfo) -> bool:
            return CommonSimNameUtils.get_first_name(sim_info).lower() == first_name

        return cls.get_sim_info_for_all_sims_generator(include_sim_callback=_has_first_name)

    @classmethod
    def get_sim_info_for_all_sims_with_name_generator(cls, first_name: str, last_name: str) -> Iterator[SimInfo]:
        """get_sim_info_for_all_sims_with_name_generator(first_name, last_name)

        Retrieve a SimInfo object for each and every Sim with the specified First and Last Name.

        :param first_name: A first name to look for.
        :type first_name: str
        :param last_name: A last name to look for.
        :type last_name: str
        :return: An iterator of Sims found with the specified first and last name.
        :rtype: Iterator[SimInfo]
        """
        from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
        first_name = first_name.lower()
        last_name = last_name.lower()

        def _has_first_and_last_name(sim_info: SimInfo) -> bool:
            return CommonSimNameUtils.get_first_name(sim_info).lower() == first_name and CommonSimNameUtils.get_last_name(sim_info).lower() == last_name

        return cls.get_sim_info_for_all_sims_generator(include_sim_callback=_has_first_and_last_name)

    @classmethod
    def get_all_sims_generator(
        cls,
        include_sim_callback: Callable[[SimInfo], Union[bool, CommonExecutionResult, CommonTestResult]] = None,
        allow_hidden_flags: HiddenReasonFlag = ALL_HIDDEN_REASONS
    ) -> Iterator[Sim]:
        """get_all_sims_generator(include_sim_callback=None, allow_hidden_flags=ALL_HIDDEN_REASONS)

        Retrieve a Sim object for each and every Sim (including hidden Sims).

        :param include_sim_callback: If the result of this callback is True, the Sim will be included in the results. If set to None, All Sims will be included.
        :type include_sim_callback: Callable[[SimInfo], bool], optional
        :param allow_hidden_flags: Flags to indicate the types of hidden Sims to consider as being instanced. Default is ALL_HIDDEN_REASONS
        :type allow_hidden_flags: HiddenReasonFlag, optional
        :return: An iterator of all Sims matching the `include_sim_callback` filter.
        :rtype: Iterator[Sim]
        """
        for sim_info in cls.get_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback):
            sim_instance = sim_info.get_sim_instance(allow_hidden_flags=allow_hidden_flags)
            if sim_instance is None:
                continue
            yield sim_instance

    @classmethod
    def get_sim_info_for_all_sims_generator(
        cls,
        include_sim_callback: Callable[[SimInfo], Union[bool, CommonExecutionResult, CommonTestResult]] = None
    ) -> Iterator[SimInfo]:
        """get_sim_info_for_all_sims_generator(include_sim_callback=None)

        Retrieve a SimInfo object for each and every Sim.

        :param include_sim_callback: If the result of this callback is True, the Sim will be included in the results. If set to None, All Sims will be included.
        :type include_sim_callback: Callable[[SimInfo], bool], optional
        :return: An iterator of all Sims matching the `include_sim_callback` filter.
        :rtype: Iterator[SimInfo]
        """
        sim_info_list = tuple(cls.get_sim_info_manager().get_all())
        for sim_info in sim_info_list:
            if sim_info is None:
                continue
            if include_sim_callback is not None and not include_sim_callback(sim_info):
                continue
            yield sim_info

    @classmethod
    def get_instanced_sim_info_for_all_sims_generator(
        cls,
        include_sim_callback: Callable[[SimInfo], Union[bool, CommonExecutionResult, CommonTestResult]] = None,
        allow_hidden_flags: HiddenReasonFlag = ALL_HIDDEN_REASONS
    ) -> Iterator[SimInfo]:
        """get_instanced_sim_info_for_all_sims_generator(\
            include_sim_callback=None,\
            allow_hidden_flags=ALL_HIDDEN_REASONS\
         )

        Retrieve a SimInfo object for each and every Sim.

        .. note:: Only SimInfo with a Sim instance (:func:`~get_sim_instance`) will be returned.

        :param include_sim_callback: If the result of this callback is True, the Sim will be included in the results. If set to None, All Sims will be included.
        :type include_sim_callback: Callable[[SimInfo], bool], optional
        :param allow_hidden_flags: Flags to indicate the types of hidden Sims to consider as being instanced. Default is ALL_HIDDEN_REASONS
        :type allow_hidden_flags: HiddenReasonFlag, optional
        :return: An iterator of all Sims matching the `include_sim_callback` filter.
        :rtype: Iterator[SimInfo]
        """
        def _is_instanced(_sim_info: SimInfo) -> bool:
            return cls.is_instanced(_sim_info, allow_hidden_flags=allow_hidden_flags)

        include_sim_callback = CommonFunctionUtils.run_predicates_as_one((_is_instanced, include_sim_callback))
        for sim_info in cls.get_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback):
            yield sim_info

    @classmethod
    def get_sim_id(cls, sim_identifier: Union[int, Sim, SimInfo, SimInfoBaseWrapper]) -> int:
        """get_sim_id(sim_identifier)

        Retrieve a SimId (int) from a Sim identifier.

        :param sim_identifier: The identifier or instance of a Sim.
        :type sim_identifier: Union[int, Sim, SimInfo, SimInfoBaseWrapper]
        :return: The decimal identifier for the Sim instance or 0 if a problem occurs.
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
        if isinstance(sim_identifier, SimInfoBaseWrapper):
            return sim_identifier.id
        return 0

    @classmethod
    def get_sim_info(
        cls,
        sim_identifier: Union[int, Sim, SimInfo, SimInfoBaseWrapper]
    ) -> Union[SimInfo, SimInfoBaseWrapper, None]:
        """get_sim_info(sim_identifier)

        Retrieve a SimInfo instance from a Sim identifier.

        :param sim_identifier: The identifier or instance of a Sim to use.
        :type sim_identifier: Union[int, Sim, SimInfo, SimInfoBaseWrapper]
        :return: The SimInfo of the specified Sim instance or None if SimInfo is not found.
        :rtype: Union[SimInfo, SimInfoBaseWrapper, None]
        """
        if sim_identifier is None or isinstance(sim_identifier, SimInfo):
            return sim_identifier
        if isinstance(sim_identifier, SimInfoBaseWrapper):
            return sim_identifier.get_sim_info()
        if isinstance(sim_identifier, Sim):
            return sim_identifier.sim_info
        if isinstance(sim_identifier, int):
            return cls.get_sim_info_manager().get(sim_identifier)
        return sim_identifier

    @classmethod
    def get_sim_instance(
        cls,
        sim_identifier: Union[int, Sim, SimInfo],
        allow_hidden_flags: HiddenReasonFlag = ALL_HIDDEN_REASONS
    ) -> Union[Sim, None]:
        """get_sim_instance(sim_identifier, allow_hidden_flags=HiddenReasonFlag.NONE)

        Retrieve a Sim instance from a Sim identifier.

        :param sim_identifier: The identifier or instance of a Sim to use.
        :type sim_identifier: Union[int, Sim, SimInfo]
        :param allow_hidden_flags: Flags to indicate the types of hidden Sims to consider as being instanced. Default is ALL_HIDDEN_REASONS
        :type allow_hidden_flags: HiddenReasonFlag, optional
        :return: The instance of the specified Sim or None if no instance was found.
        :rtype: Union[Sim, None]
        """
        if sim_identifier is None or isinstance(sim_identifier, Sim):
            return sim_identifier
        if isinstance(sim_identifier, SimInfo):
            return sim_identifier.get_sim_instance(allow_hidden_flags=allow_hidden_flags)
        if isinstance(sim_identifier, int):
            sim_info = cls.get_sim_info_manager().get(sim_identifier)
            if sim_info is None:
                return None
            return cls.get_sim_instance(sim_info, allow_hidden_flags=allow_hidden_flags)
        if isinstance(sim_identifier, SimInfoBaseWrapper):
            return sim_identifier.get_sim_instance(allow_hidden_flags=allow_hidden_flags)
        return sim_identifier

    @classmethod
    def get_sim_info_manager(cls) -> SimInfoManager:
        """get_sim_info_manager()

        Retrieve the manager that manages the Sim Info of all Sims in a game world.

        :return: The manager that manages the Sim Info of all Sims in a game world.
        :rtype: SimInfoManager
        """
        return services.sim_info_manager()


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_name_of_sim',
    'Print the first and last name of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance identifier of a Sim.', is_optional=True, default_value='Active Sim'),
    )
)
def _s4clib_testing_print_name_of_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    # noinspection PyPropertyAccess
    output(f'First Name: {sim_info.first_name}  Last Name: \'{sim_info.last_name}\'')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_names_of_all_sims',
    'Print a list of the first and last names of all Sims.'
)
def _s4clib_testing_print_names_of_all_sims(output: CommonConsoleCommandOutput):
    output('Printing the names of all Sims (This may take awhile).')
    current_count = 1
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
        # noinspection PyPropertyAccess
        output(f'{current_count}: First: \'{sim_info.first_name}\' Last: \'{sim_info.last_name}\'')
        current_count += 1
    output('Done showing the names of all Sims.')
