"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Iterator, Dict

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.occult.occult_enums import OccultType
from sims.sim_info import SimInfo
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.strings_enum import CommonStringId


class CommonOccultType(CommonInt):
    """Custom Occult Types enum containing all occults. DLC not required.

    """
    NONE: 'CommonOccultType' = ...
    ALIEN: 'CommonOccultType' = ...
    FAIRY: 'CommonOccultType' = ...
    GHOST: 'CommonOccultType' = ...
    MERMAID: 'CommonOccultType' = ...
    NON_OCCULT: 'CommonOccultType' = ...
    PLANT_SIM: 'CommonOccultType' = ...
    ROBOT: 'CommonOccultType' = ...
    SCARECROW: 'CommonOccultType' = ...
    SKELETON: 'CommonOccultType' = ...
    VAMPIRE: 'CommonOccultType' = ...
    WEREWOLF: 'CommonOccultType' = ...
    WITCH: 'CommonOccultType' = ...

    @classmethod
    def get_all(cls, exclude_occult_types: Iterator['CommonOccultType'] = None) -> Tuple['CommonOccultType']:
        """get_all(exclude_occult_types=None)

        Get a collection of all values.

        :param exclude_occult_types: These values will be excluded. If set to None, NONE will be excluded automatically. Default is None.
        :type exclude_occult_types: Iterator[CommonOccultType], optional
        :return: A collection of all CommonOccultType, without CommonOccultType.NONE.
        :rtype: Tuple[CommonOccultType]
        """
        if exclude_occult_types is None:
            exclude_occult_types = (cls.NONE,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonOccultType] = tuple([value for value in cls.values if value not in exclude_occult_types])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_occult_types: Iterator['CommonOccultType'] = None) -> Tuple[str]:
        """get_all_names(exclude_occult_types=None)

        Retrieve a collection of the names of all values.

        :param exclude_occult_types: These values will be excluded. If set to None, NONE will be excluded automatically. Default is None.
        :type exclude_occult_types: Iterator[CommonOccultType], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_occult_types=exclude_occult_types)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_occult_types: Iterator['CommonOccultType'] = None) -> str:
        """get_comma_separated_names_string(exclude_occult_types=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_occult_types: These values will be excluded. If set to None, NONE will be excluded automatically. Default is None.
        :type exclude_occult_types: Iterator[CommonOccultType], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_occult_types=exclude_occult_types))

    @staticmethod
    def determine_occult_type(sim_info: SimInfo) -> 'CommonOccultType':
        """determine_occult_type(sim_info)

        Determine the type of Occult a Sim is.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The CommonOccultType that represents what a Sim is.
        :rtype: CommonOccultType
        """
        from sims4communitylib.utils.sims.common_sim_occult_type_utils import CommonSimOccultTypeUtils
        return CommonSimOccultTypeUtils.determine_occult_type(sim_info)

    @staticmethod
    def determine_current_occult_type(sim_info: SimInfo) -> 'CommonOccultType':
        """determine_current_occult_type(sim_info)

        Determine the type of Occult a Sim is currently appearing as.
        i.e. A mermaid with their tail out would currently be a MERMAID. But a Mermaid Sim with no tail out would currently be a CommonOccultType.NONE

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The CommonOccultType the Sim is currently appearing as, or CommonOccultType.NONE if they are not appearing as any Occult or are appearing as their HUMAN disguise/occult.
        :rtype: CommonOccultType
        """
        from sims4communitylib.utils.sims.common_sim_occult_type_utils import CommonSimOccultTypeUtils
        return CommonSimOccultTypeUtils.determine_current_occult_type(sim_info)

    @staticmethod
    def convert_to_vanilla(occult_type: 'CommonOccultType') -> Union[OccultType, None]:
        """convert_to_vanilla(occult_type)

        Convert a CommonOccultType into the vanilla OccultType enum.

        .. note:: Not all CommonOccultTypes have an OccultType to convert to! They will return None in those cases! (Ghost, Plant Sim, Robot, Skeleton)

        :param occult_type: An instance of CommonOccultType
        :type occult_type: CommonOccultType
        :return: The specified CommonOccultType translated to OccultType, or None if the value could not be translated.
        :rtype: Union[OccultType, None]
        """
        from sims4communitylib.utils.sims.common_sim_occult_type_utils import CommonSimOccultTypeUtils
        return CommonSimOccultTypeUtils.convert_custom_type_to_vanilla(occult_type)

    @staticmethod
    def convert_from_vanilla(value: Union[OccultType, 'CommonOccultType', int]) -> Union['CommonOccultType', OccultType, int]:
        """convert_from_vanilla(value)

        Convert a vanilla value into this enum.

        :param value: The value to convert.
        :type value: Union[OccultType, 'CommonOccultType', int]
        :return: The specified value translated to CommonOccultType. The value will be returned if it cannot be translated.
        :rtype: Union['CommonOccultType', OccultType, int]
        """
        from sims4communitylib.utils.sims.common_sim_occult_type_utils import CommonSimOccultTypeUtils
        return CommonSimOccultTypeUtils.convert_custom_type_from_vanilla(value)

    @staticmethod
    def convert_to_localized_string_id(value: Union['CommonOccultType', OccultType]) -> Union[int, str, CommonStringId, LocalizedString]:
        """convert_to_localized_string_id(value)

        Convert a CommonOccultType into a Localized String identifier.

        :param value: An instance of a CommonOccultType
        :type value: Union[CommonOccultType, OccultType]
        :return: The specified CommonOccultType translated to a localized string identifier. If no localized string id is found, the name property of the value will be used instead.
        :rtype: Union[int, str, CommonStringId, LocalizedString]
        """
        value = CommonOccultType.convert_from_vanilla(value)
        mapping: Dict[CommonOccultType, CommonStringId] = {
            CommonOccultType.NONE: CommonStringId.S4CL_NONE,
            CommonOccultType.ALIEN: CommonStringId.S4CL_ALIEN,
            CommonOccultType.FAIRY: CommonStringId.S4CL_FAIRY,
            CommonOccultType.MERMAID: CommonStringId.S4CL_MERMAID,
            CommonOccultType.ROBOT: CommonStringId.S4CL_ROBOT,
            CommonOccultType.SCARECROW: CommonStringId.S4CL_SCARECROW,
            CommonOccultType.SKELETON: CommonStringId.S4CL_SKELETON,
            CommonOccultType.VAMPIRE: CommonStringId.S4CL_VAMPIRE,
            CommonOccultType.WITCH: CommonStringId.S4CL_WITCH,
            CommonOccultType.PLANT_SIM: CommonStringId.S4CL_PLANT_SIM,
            CommonOccultType.GHOST: CommonStringId.S4CL_GHOST,
            CommonOccultType.WEREWOLF: CommonStringId.S4CL_WEREWOLF,
            CommonOccultType.NON_OCCULT: CommonStringId.S4CL_NON_OCCULT,
        }

        return mapping.get(value, value.name if hasattr(value, 'name') else str(value))
