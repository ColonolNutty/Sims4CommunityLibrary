"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Iterator

from sims.occult.occult_enums import OccultType
from sims.sim_info import SimInfo
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonOccultType(CommonInt):
    """Custom Occult Types enum containing all occults. DLC not required.

    """
    NONE: 'CommonOccultType' = ...
    ALIEN: 'CommonOccultType' = ...
    GHOST: 'CommonOccultType' = ...
    MERMAID: 'CommonOccultType' = ...
    NON_OCCULT: 'CommonOccultType' = ...
    PLANT_SIM: 'CommonOccultType' = ...
    ROBOT: 'CommonOccultType' = ...
    SKELETON: 'CommonOccultType' = ...
    VAMPIRE: 'CommonOccultType' = ...
    WEREWOLF: 'CommonOccultType' = ...
    WITCH: 'CommonOccultType' = ...

    @classmethod
    def get_all(cls, exclude_occult_types: Iterator['CommonOccultType'] = ()) -> Tuple['CommonOccultType']:
        """get_all(exclude_occult_types=())

        Retrieve a collection of all CommonOccultType, excluding CommonOccultType.NONE.

        :param exclude_occult_types: An iterable of occult types to exclude from the result. Default is to exclude none of them.
        :type exclude_occult_types: Iterator[CommonOccultType], optional
        :return: A collection of all CommonOccultType, without CommonOccultType.NONE.
        :rtype: Tuple[CommonOccultType]
        """
        value_list: Tuple[CommonOccultType] = tuple([value for value in cls.values if value != cls.NONE and (not exclude_occult_types or value not in exclude_occult_types)])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_occult_types: Iterator['CommonOccultType']=()) -> Tuple[str]:
        """get_all_names(exclude_occult_types=())

        Retrieve a collection of the names of all CommonOccultType, excluding CommonOccultType.NONE.

        :param exclude_occult_types: An iterable of occult types to exclude from the result.
        :type exclude_occult_types: CommonOccultType
        :return: A collection of the names of all CommonOccultType, without CommonOccultType.NONE.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_occult_types=exclude_occult_types)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_occult_types: Iterator['CommonOccultType']=()) -> str:
        """get_comma_separated_names_string(exclude_occult_types=())

        Create a string containing all names of all CommonOccultType values (excluding CommonOccultType.NONE), separated by a comma.

        :param exclude_occult_types: An iterable of occult types to exclude from the result.
        :type exclude_occult_types: CommonOccultType
        :return: A string containing all names of all CommonOccultType values (excluding CommonOccultType.NONE), separated by a comma.
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
