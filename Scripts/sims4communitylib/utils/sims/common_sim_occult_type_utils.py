"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Union, Dict, Callable

from sims.occult.occult_enums import OccultType
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_occult_type import CommonOccultType
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils


class CommonSimOccultTypeUtils:
    """Utilities for determining the type of Occult a Sim is. i.e. Alien, Vampire, Ghost, etc.

    """
    @staticmethod
    def get_all_occult_types_for_sim_gen(sim_info: SimInfo) -> Iterator[CommonOccultType]:
        """get_all_occult_types_for_sim_gen(sim_info)

        Retrieve a generator of CommonOccultType for all Occults of a Sim.

        .. note:: Results include the occult type of the sim_info specified.\
            If they are Human by default, the Human occult type will be included.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :return: An iterable of Occult Types for all occults of the Sim.
        :rtype: Iterator[CommonOccultType]
        """
        if sim_info is None:
            return tuple()
        yield CommonOccultType.NON_OCCULT
        for occult_type in CommonOccultType.values:
            if occult_type in (CommonOccultType.NONE, CommonOccultType.NON_OCCULT):
                continue
            if CommonSimOccultTypeUtils.is_occult_type(sim_info, occult_type):
                yield occult_type

    @staticmethod
    def has_any_occult(sim_info: SimInfo) -> bool:
        """has_any_occult(sim_info)

        Determine if a Sim has any Occult Types. (Not including NON_OCCULT)

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :return: True, if the specified Sim has any Non-Human Occult Types. False, if not.
        :rtype: bool
        """
        for occult_type in CommonSimOccultTypeUtils.get_all_occult_types_for_sim_gen(sim_info):
            if occult_type in (CommonOccultType.NONE, CommonOccultType.NON_OCCULT):
                continue
            return True
        return False

    @staticmethod
    def is_occult_type(sim_info: SimInfo, occult_type: CommonOccultType) -> bool:
        """is_occult_type(sim_info, occult_type)

        Determine if a Sim is an Occult Type.

        .. note:: To check if a Sim is currently an occult type use :func:`~is_currently_occult_type` instead.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param occult_type: The Occult Type to check.
        :type occult_type: OccultType
        :return: True, if the Sim is the specified Occult Type. False, if not.
        :rtype: bool
        """
        if occult_type == CommonOccultType.NONE:
            raise AssertionError('Cannot check if Sim is a NONE occult!'.format(CommonSimNameUtils.get_full_name(sim_info)))
        if occult_type == CommonOccultType.NON_OCCULT:
            # Every Sim is always a Non-Occult
            return True
        from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
        occult_type_mappings: Dict[CommonOccultType, Callable[[SimInfo], bool]] = {
            CommonOccultType.ALIEN: CommonOccultUtils.is_alien,
            CommonOccultType.MERMAID: CommonOccultUtils.is_mermaid,
            CommonOccultType.ROBOT: CommonOccultUtils.is_robot,
            CommonOccultType.SKELETON: CommonOccultUtils.is_skeleton,
            CommonOccultType.VAMPIRE: CommonOccultUtils.is_vampire,
            CommonOccultType.WITCH: CommonOccultUtils.is_witch,
            CommonOccultType.PLANT_SIM: CommonOccultUtils.is_plant_sim,
            CommonOccultType.GHOST: CommonOccultUtils.is_ghost
        }
        if occult_type not in occult_type_mappings:
            return False
        return occult_type_mappings[occult_type](sim_info)

    @staticmethod
    def is_currently_occult_type(sim_info: SimInfo, occult_type: CommonOccultType) -> bool:
        """is_currently_occult_type(sim_info, occult_type)

        Determine if a Sim is currently an Occult Type.

        .. note:: To check if a Sim is an occult type (Whether current or not) use :func:`~is_occult_type` instead.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param occult_type: The Occult Type to check.
        :type occult_type: OccultType
        :return: True, if the Sim is currently the specified Occult Type. False, if not.
        :rtype: bool
        """
        if occult_type == CommonOccultType.NONE:
            raise AssertionError('Cannot check if Sim is currently a NONE occult!'.format(CommonSimNameUtils.get_full_name(sim_info)))
        from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
        occult_type_mappings: Dict[CommonOccultType, Callable[[SimInfo], bool]] = {
            CommonOccultType.ALIEN: CommonOccultUtils.is_currently_an_alien,
            CommonOccultType.MERMAID: CommonOccultUtils.is_currently_a_mermaid,
            CommonOccultType.ROBOT: CommonOccultUtils.is_currently_a_robot,
            CommonOccultType.SKELETON: CommonOccultUtils.is_currently_a_skeleton,
            CommonOccultType.VAMPIRE: CommonOccultUtils.is_currently_a_vampire,
            CommonOccultType.WITCH: CommonOccultUtils.is_currently_a_witch,
            CommonOccultType.PLANT_SIM: CommonOccultUtils.is_currently_a_plant_sim,
            CommonOccultType.GHOST: CommonOccultUtils.is_currently_a_ghost
        }
        if occult_type not in occult_type_mappings:
            return False
        return occult_type_mappings[occult_type](sim_info)

    @staticmethod
    def determine_occult_type(sim_info: SimInfo) -> CommonOccultType:
        """determine_occult_type(sim_info)

        Determine the type of Occult a Sim is.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The CommonOccultType that represents what a Sim is.
        :rtype: CommonOccultType
        """
        from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
        if CommonOccultUtils.is_robot(sim_info):
            return CommonOccultType.ROBOT
        elif CommonOccultUtils.is_skeleton(sim_info):
            return CommonOccultType.SKELETON
        elif CommonOccultUtils.is_alien(sim_info):
            return CommonOccultType.ALIEN
        elif CommonOccultUtils.is_ghost(sim_info):
            return CommonOccultType.GHOST
        elif CommonOccultUtils.is_mermaid(sim_info):
            return CommonOccultType.MERMAID
        elif CommonOccultUtils.is_plant_sim(sim_info):
            return CommonOccultType.PLANT_SIM
        elif CommonOccultUtils.is_vampire(sim_info):
            return CommonOccultType.VAMPIRE
        elif CommonOccultUtils.is_witch(sim_info):
            return CommonOccultType.WITCH
        return CommonOccultType.NON_OCCULT

    @staticmethod
    def determine_current_occult_type(sim_info: SimInfo) -> CommonOccultType:
        """determine_current_occult_type(sim_info)

        Determine the type of Occult a Sim is currently appearing as.
        i.e. A mermaid with their tail out would currently be a MERMAID. But a Mermaid Sim with no tail out would currently be a CommonOccultType.NONE

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The CommonOccultType the Sim is currently appearing as, or CommonOccultType.NONE if they are not appearing as any Occult or are appearing as their HUMAN disguise/occult.
        :rtype: CommonOccultType
        """
        from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
        if CommonOccultUtils.is_currently_a_mermaid(sim_info) or CommonOccultUtils.is_mermaid_in_mermaid_form(sim_info):
            return CommonOccultType.MERMAID
        elif CommonOccultUtils.is_robot(sim_info):
            return CommonOccultType.ROBOT
        elif CommonOccultUtils.is_currently_a_vampire(sim_info):
            return CommonOccultType.VAMPIRE
        elif CommonOccultUtils.is_currently_a_witch(sim_info):
            return CommonOccultType.WITCH
        elif CommonOccultUtils.is_currently_an_alien(sim_info):
            return CommonOccultType.ALIEN
        elif CommonOccultUtils.is_plant_sim(sim_info):
            return CommonOccultType.PLANT_SIM
        elif CommonOccultUtils.is_ghost(sim_info):
            return CommonOccultType.GHOST
        elif CommonOccultUtils.is_skeleton(sim_info):
            return CommonOccultType.SKELETON
        return CommonOccultType.NON_OCCULT

    @staticmethod
    def convert_custom_type_to_vanilla(occult_type: 'CommonOccultType') -> Union[OccultType, None]:
        """convert_custom_type_to_vanilla(occult_type)

        Convert a CommonOccultType into the vanilla OccultType enum.

        .. note:: Not all CommonOccultTypes have an OccultType to convert to! They will return None in those cases! (Ghost, Plant Sim, Robot, Skeleton)

        :param occult_type: An instance of a CommonOccultType
        :type occult_type: CommonOccultType
        :return: The specified CommonOccultType translated to a OccultType or None if the CommonOccultType could not be translated.
        :rtype: Union[OccultType, None]
        """
        if occult_type is None or occult_type == CommonOccultType.NONE:
            return None
        if isinstance(occult_type, OccultType):
            return occult_type
        conversion_mapping: Dict[CommonOccultType, OccultType] = {
            CommonOccultType.NON_OCCULT: OccultType.HUMAN,
            CommonOccultType.ALIEN: OccultType.ALIEN,
            CommonOccultType.MERMAID: OccultType.MERMAID if hasattr(OccultType, 'MERMAID') else None,
            CommonOccultType.VAMPIRE: OccultType.VAMPIRE,
            CommonOccultType.WITCH: OccultType.WITCH if hasattr(OccultType, 'WITCH') else None
        }
        return conversion_mapping.get(occult_type, None)


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_custom_occults',
    'Print a list of all custom CommonOccultTypes a Sim has.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance Id or name of the Sim to print the occult types of.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.printcustomoccults',
    )
)
def _common_print_custom_occult_types_for_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo=None):
    if sim_info is None:
        return
    occult_types_str = ', '.join([occult_type.name if hasattr(occult_type, 'name') else str(occult_type) for occult_type in CommonSimOccultTypeUtils.get_all_occult_types_for_sim_gen(sim_info)])
    output(f'Occult Types: {occult_types_str}')
    current_occult_type = CommonSimOccultTypeUtils.determine_current_occult_type(sim_info)
    current_occult_type_str = current_occult_type.name if hasattr(current_occult_type, 'name') else str(current_occult_type)
    output(f'Current Occult Type: {current_occult_type_str}')
