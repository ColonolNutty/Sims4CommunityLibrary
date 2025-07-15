"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Union, Dict, Callable

from sims.occult.occult_enums import OccultType
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.common_occult_type import CommonOccultType
from sims4communitylib.enums.strings_enum import CommonStringId
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
        :return: An iterator of Occult Types for all occults of the Sim.
        :rtype: Iterator[CommonOccultType]
        """
        if sim_info is None:
            return tuple()
        yield CommonOccultType.NON_OCCULT
        for occult_type in CommonOccultType.get_all(exclude_occult_types=(CommonOccultType.NONE, CommonOccultType.NON_OCCULT)):
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
    def is_occult_type(sim_info: SimInfo, occult_type: CommonOccultType) -> CommonTestResult:
        """is_occult_type(sim_info, occult_type)

        Determine if a Sim is an Occult Type.

        .. note:: To check if a Sim is currently an occult type use :func:`~is_currently_occult_type` instead.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param occult_type: The Occult Type to check.
        :type occult_type: OccultType
        :return: The result of the test. True, if the Sim is the specified Occult Type. False, if not.
        :rtype: CommonTestResult
        """
        if occult_type == CommonOccultType.NONE:
            raise AssertionError('Cannot check if Sim is a NONE occult!'.format(CommonSimNameUtils.get_full_name(sim_info)))
        if occult_type == CommonOccultType.NON_OCCULT:
            # Every Sim is always a Non-Occult
            return CommonTestResult.TRUE
        from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
        occult_type_mappings: Dict[CommonOccultType, Callable[[SimInfo], CommonTestResult]] = {
            CommonOccultType.ALIEN: CommonOccultUtils.is_alien,
            CommonOccultType.FAIRY: CommonOccultUtils.is_fairy,
            CommonOccultType.MERMAID: CommonOccultUtils.is_mermaid,
            CommonOccultType.ROBOT: CommonOccultUtils.is_robot,
            CommonOccultType.SCARECROW: CommonOccultUtils.is_scarecrow,
            CommonOccultType.SKELETON: CommonOccultUtils.is_skeleton,
            CommonOccultType.VAMPIRE: CommonOccultUtils.is_vampire,
            CommonOccultType.WITCH: CommonOccultUtils.is_witch,
            CommonOccultType.PLANT_SIM: CommonOccultUtils.is_plant_sim,
            CommonOccultType.GHOST: CommonOccultUtils.is_ghost,
            CommonOccultType.WEREWOLF: CommonOccultUtils.is_werewolf
        }
        if occult_type not in occult_type_mappings:
            return CommonTestResult(False, reason=f'A check for the specified occult type was not found. {occult_type}.', tooltip_text=CommonStringId.S4CL_OCCULT_TYPE_IS_NOT_AVAILABLE_OR_SUPPORT_FOR_IT_HAS_NOT_BEEN_IMPLEMENTED, tooltip_tokens=(CommonOccultType.convert_to_localized_string_id(occult_type),))
        return occult_type_mappings[occult_type](sim_info)

    @staticmethod
    def is_currently_occult_type(sim_info: SimInfo, occult_type: CommonOccultType) -> CommonTestResult:
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
        occult_type_mappings: Dict[CommonOccultType, Callable[[SimInfo], CommonTestResult]] = {
            CommonOccultType.ALIEN: CommonOccultUtils.is_currently_an_alien,
            CommonOccultType.FAIRY: CommonOccultUtils.is_currently_a_fairy,
            CommonOccultType.MERMAID: CommonOccultUtils.is_currently_a_mermaid,
            CommonOccultType.ROBOT: CommonOccultUtils.is_currently_a_robot,
            CommonOccultType.SCARECROW: CommonOccultUtils.is_currently_a_scarecrow,
            CommonOccultType.SKELETON: CommonOccultUtils.is_currently_a_skeleton,
            CommonOccultType.VAMPIRE: CommonOccultUtils.is_currently_a_vampire,
            CommonOccultType.WITCH: CommonOccultUtils.is_currently_a_witch,
            CommonOccultType.PLANT_SIM: CommonOccultUtils.is_currently_a_plant_sim,
            CommonOccultType.GHOST: CommonOccultUtils.is_currently_a_ghost,
            CommonOccultType.WEREWOLF: CommonOccultUtils.is_currently_a_werewolf
        }
        if occult_type not in occult_type_mappings:
            return CommonTestResult(False, reason=f'A check for the specified occult type was not found. {occult_type}.', tooltip_text=CommonStringId.S4CL_OCCULT_TYPE_IS_NOT_AVAILABLE_OR_SUPPORT_FOR_IT_HAS_NOT_BEEN_IMPLEMENTED, tooltip_tokens=(CommonOccultType.convert_to_localized_string_id(occult_type),))
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
        elif CommonOccultUtils.is_scarecrow(sim_info):
            return CommonOccultType.SCARECROW
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
        elif CommonOccultUtils.is_werewolf(sim_info):
            return CommonOccultType.WEREWOLF
        elif CommonOccultUtils.is_fairy(sim_info):
            return CommonOccultType.FAIRY
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
        elif CommonOccultUtils.is_currently_a_scarecrow(sim_info):
            return CommonOccultType.SCARECROW
        elif CommonOccultUtils.is_currently_a_vampire(sim_info):
            return CommonOccultType.VAMPIRE
        elif CommonOccultUtils.is_currently_a_werewolf(sim_info):
            return CommonOccultType.WEREWOLF
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
        elif CommonOccultUtils.is_currently_a_fairy(sim_info):
            return CommonOccultType.FAIRY
        return CommonOccultType.NON_OCCULT

    @staticmethod
    def convert_to_vanilla(occult_type: CommonOccultType) -> Union[OccultType, None]:
        """convert_to_vanilla(occult_type)

        Convert CommonOccultType into OccultType.

        .. note:: Not all CommonOccultTypes have an OccultType to convert to! They will return None in those cases! (Ghost, Plant Sim, Robot, Skeleton)

        :param occult_type: An instance of a CommonOccultType
        :type occult_type: CommonOccultType
        :return: The specified CommonOccultType translated to OccultType, or None if the value could not be translated.
        :rtype: Union[OccultType, None]
        """
        return CommonSimOccultTypeUtils.convert_custom_type_to_vanilla(occult_type)

    @staticmethod
    def convert_from_vanilla(occult_type: OccultType) -> Union[CommonOccultType, None]:
        """convert_from_vanilla(occult_type)

        Convert an OccultType into CommonOccultType.

        :param occult_type: An instance of an OccultType
        :type occult_type: OccultType
        :return: The specified OccultType translated to CommonOccultType, or None if the value could not be translated.
        :rtype: Union[CommonOccultType, None]
        """
        return CommonSimOccultTypeUtils.convert_custom_type_from_vanilla(occult_type)

    @staticmethod
    def convert_custom_type_to_vanilla(occult_type: CommonOccultType) -> Union[OccultType, None]:
        """convert_custom_type_to_vanilla(occult_type)

        Convert a CommonOccultType into OccultType.

        .. note:: Not all CommonOccultType values have a matching OccultType! None will be returned in these cases! (Ghost, Plant Sim, Robot, Skeleton)

        :param occult_type: An instance of a CommonOccultType
        :type occult_type: CommonOccultType
        :return: The specified CommonOccultType translated to OccultType, or None if the value could not be translated.
        :rtype: Union[OccultType, None]
        """
        if occult_type is None or occult_type == CommonOccultType.NONE:
            return None
        if isinstance(occult_type, OccultType):
            return occult_type
        conversion_mapping: Dict[CommonOccultType, OccultType] = {
            CommonOccultType.NON_OCCULT: OccultType.HUMAN,
            CommonOccultType.ALIEN: OccultType.ALIEN if hasattr(OccultType, 'ALIEN') else None,
            CommonOccultType.FAIRY: OccultType.FAIRY if hasattr(OccultType, 'FAIRY') else None,
            CommonOccultType.MERMAID: OccultType.MERMAID if hasattr(OccultType, 'MERMAID') else None,
            CommonOccultType.VAMPIRE: OccultType.VAMPIRE if hasattr(OccultType, 'VAMPIRE') else None,
            CommonOccultType.WITCH: OccultType.WITCH if hasattr(OccultType, 'WITCH') else None,
            CommonOccultType.WEREWOLF: OccultType.WEREWOLF if hasattr(OccultType, 'WEREWOLF') else None
        }
        return conversion_mapping.get(occult_type, None)

    @staticmethod
    def convert_custom_type_from_vanilla(occult_type: OccultType) -> Union[CommonOccultType, None]:
        """convert_custom_type_from_vanilla(occult_type)

        Convert an OccultType into CommonOccultType.

        :param occult_type: An instance of an OccultType
        :type occult_type: OccultType
        :return: The specified OccultType translated to CommonOccultType, or None if the value could not be translated.
        :rtype: Union[CommonOccultType, None]
        """
        if occult_type is None or occult_type == CommonOccultType.NONE:
            return None
        if isinstance(occult_type, CommonOccultType):
            return occult_type
        mapping: Dict[OccultType, CommonOccultType] = dict()
        if hasattr(OccultType, 'HUMAN'):
            mapping[OccultType.HUMAN] = CommonOccultType.NON_OCCULT
        if hasattr(OccultType, 'ALIEN'):
            mapping[OccultType.ALIEN] = CommonOccultType.ALIEN
        if hasattr(OccultType, 'FAIRY'):
            mapping[OccultType.FAIRY] = CommonOccultType.FAIRY
        if hasattr(OccultType, 'VAMPIRE'):
            mapping[OccultType.VAMPIRE] = CommonOccultType.VAMPIRE
        if hasattr(OccultType, 'MERMAID'):
            mapping[OccultType.MERMAID] = CommonOccultType.MERMAID
        if hasattr(OccultType, 'WITCH'):
            mapping[OccultType.WITCH] = CommonOccultType.WITCH
        if hasattr(OccultType, 'WEREWOLF'):
            mapping[OccultType.WEREWOLF] = CommonOccultType.WEREWOLF
        return mapping.get(occult_type, occult_type)


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
def _common_print_custom_occult_types_for_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        return
    occult_types_str = ', '.join([occult_type.name if hasattr(occult_type, 'name') else str(occult_type) for occult_type in CommonSimOccultTypeUtils.get_all_occult_types_for_sim_gen(sim_info)])
    output(f'Occult Types: {occult_types_str}')
    current_occult_type = CommonSimOccultTypeUtils.determine_current_occult_type(sim_info)
    current_occult_type_str = current_occult_type.name if hasattr(current_occult_type, 'name') else str(current_occult_type)
    output(f'Current Occult Type: {current_occult_type_str}')
