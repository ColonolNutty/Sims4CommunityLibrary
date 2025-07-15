"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Iterator, Dict, Set

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.enums.enumtypes.common_versioned_int_flags import CommonVersionedIntFlags
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.math.common_bitwise_utils import CommonBitwiseUtils


class CommonSimDemographicType(CommonVersionedIntFlags):
    """ Various demographics of Sims. """
    NONE: 'CommonSimDemographicType' = ...
    HOUSEHOLD: 'CommonSimDemographicType' = ...
    NON_HOUSEHOLD: 'CommonSimDemographicType' = ...
    CURRENTLY_CONTROLLED: 'CommonSimDemographicType' = ...

    # Gender
    MALE: 'CommonSimDemographicType' = ...
    FEMALE: 'CommonSimDemographicType' = ...

    # Age
    BABY: 'CommonSimDemographicType' = ...
    INFANT: 'CommonSimDemographicType' = ...
    CHILD: 'CommonSimDemographicType' = ...
    TODDLER: 'CommonSimDemographicType' = ...
    TEEN: 'CommonSimDemographicType' = ...
    ADULT: 'CommonSimDemographicType' = ...
    YOUNG_ADULT: 'CommonSimDemographicType' = ...
    ELDER: 'CommonSimDemographicType' = ...

    # Occult
    ALIEN: 'CommonSimDemographicType' = ...
    FAIRY: 'CommonSimDemographicType' = ...
    GHOST: 'CommonSimDemographicType' = ...
    MERMAID: 'CommonSimDemographicType' = ...
    NON_OCCULT: 'CommonSimDemographicType' = ...
    PLANT: 'CommonSimDemographicType' = ...
    ROBOT: 'CommonSimDemographicType' = ...
    SKELETON: 'CommonSimDemographicType' = ...
    VAMPIRE: 'CommonSimDemographicType' = ...
    WEREWOLF: 'CommonSimDemographicType' = ...
    WITCH: 'CommonSimDemographicType' = ...

    # Species
    HUMAN: 'CommonSimDemographicType' = ...
    SMALL_DOG: 'CommonSimDemographicType' = ...
    LARGE_DOG: 'CommonSimDemographicType' = ...
    CAT: 'CommonSimDemographicType' = ...
    FOX: 'CommonSimDemographicType' = ...
    HORSE: 'CommonSimDemographicType' = ...

    # Obsolete
    PLAYER_SIMS: 'CommonSimDemographicType' = ...
    NPC_SIMS: 'CommonSimDemographicType' = ...
    ACTIVE_SIM: 'CommonSimDemographicType' = ...
    CONTROLLED: 'CommonSimDemographicType' = ...

    @classmethod
    def get_version(cls) -> str:
        """The version of the enum. If this changes, it means values have changed and should be updated."""
        return 'v1.2'

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonSimDemographicType'] = None) -> Tuple['CommonSimDemographicType']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, NONE will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonTypesOfSims], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonSimDemographicType]
        """
        if exclude_values is None:
            exclude_values = (cls.NONE,)
        obsolete_values = cls.get_obsolete_values()
        # noinspection PyTypeChecker
        result: Tuple[CommonSimDemographicType, ...] = tuple([val for val in cls.values if val not in exclude_values and val not in obsolete_values])
        return result

    @classmethod
    def get_all_flags(cls, exclude_values: Iterator['CommonSimDemographicType'] = None) -> 'CommonSimDemographicType':
        """get_all_flags(exclude_values=None)

        Get a flag containing all values.

        :param exclude_values: These values will be excluded. If set to None, NONE will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonTypesOfSims], optional
        :return: A flag containing all values.
        :rtype: CommonSimDemographicType
        """
        value_flags = CommonSimDemographicType.NONE
        for value in cls.get_all(exclude_values=exclude_values):
            if value_flags == CommonSimDemographicType.NONE:
                value_flags = value
            else:
                value_flags = CommonBitwiseUtils.add_flags(value_flags, value)
        return value_flags

    @staticmethod
    def to_display_name(value: 'CommonSimDemographicType') -> Union[int, LocalizedString]:
        """Convert a value to a display name."""
        mappings = {
            CommonSimDemographicType.HOUSEHOLD: CommonStringId.S4CL_HOUSEHOLD,
            CommonSimDemographicType.NON_HOUSEHOLD: CommonStringId.S4CL_NON_HOUSEHOLD,
            CommonSimDemographicType.CURRENTLY_CONTROLLED: CommonStringId.S4CL_CURRENTLY_CONTROLLED,
            # Gender
            CommonSimDemographicType.MALE: CommonStringId.MALE,
            CommonSimDemographicType.FEMALE: CommonStringId.FEMALE,
            # Age
            CommonSimDemographicType.BABY: CommonStringId.BABY,
            CommonSimDemographicType.TODDLER: CommonStringId.TODDLER,
            CommonSimDemographicType.CHILD: CommonStringId.CHILD,
            CommonSimDemographicType.TEEN: CommonStringId.TEEN,
            CommonSimDemographicType.ADULT: CommonStringId.ADULT,
            CommonSimDemographicType.YOUNG_ADULT: CommonStringId.YOUNG_ADULT,
            CommonSimDemographicType.ELDER: CommonStringId.ELDER,
            # Occult
            CommonSimDemographicType.ALIEN: CommonStringId.S4CL_ALIEN,
            CommonSimDemographicType.GHOST: CommonStringId.S4CL_GHOST,
            CommonSimDemographicType.MERMAID: CommonStringId.S4CL_MERMAID,
            CommonSimDemographicType.NON_OCCULT: CommonStringId.S4CL_NON_OCCULT,
            CommonSimDemographicType.PLANT: CommonStringId.S4CL_PLANT_SIM,
            CommonSimDemographicType.ROBOT: CommonStringId.S4CL_ROBOT,
            CommonSimDemographicType.SKELETON: CommonStringId.S4CL_SKELETON,
            CommonSimDemographicType.VAMPIRE: CommonStringId.S4CL_VAMPIRE,
            CommonSimDemographicType.WEREWOLF: CommonStringId.S4CL_WEREWOLF,
            CommonSimDemographicType.WITCH: CommonStringId.S4CL_WITCH,
            # Species
            CommonSimDemographicType.HUMAN: CommonStringId.HUMAN,
            CommonSimDemographicType.SMALL_DOG: CommonStringId.SMALL_DOG,
            CommonSimDemographicType.LARGE_DOG: CommonStringId.LARGE_DOG,
            CommonSimDemographicType.CAT: CommonStringId.CAT,
            CommonSimDemographicType.FOX: CommonStringId.FOX,
            CommonSimDemographicType.HORSE: CommonStringId.HORSE,
        }
        return mappings.get(value, value.name if hasattr(value, 'name') else str(value))

    @staticmethod
    def to_display_description(value: 'CommonSimDemographicType') -> Union[int, LocalizedString]:
        """Convert a value to a display description."""
        mappings = {
            CommonSimDemographicType.HOUSEHOLD: CommonStringId.S4CL_HOUSEHOLD_DESCRIPTION,
            CommonSimDemographicType.NON_HOUSEHOLD: CommonStringId.S4CL_NON_HOUSEHOLD_DESCRIPTION,
            CommonSimDemographicType.CURRENTLY_CONTROLLED: CommonStringId.S4CL_CURRENTLY_CONTROLLED_DESCRIPTION,
        }
        return mappings.get(value, 0)

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_obsolete_values(cls) -> Set['CommonSimDemographicType']:
        return {
            CommonSimDemographicType.ACTIVE_SIM,
            CommonSimDemographicType.PLAYER_SIMS,
            CommonSimDemographicType.NPC_SIMS,
            CommonSimDemographicType.CONTROLLED
        }

    @classmethod
    def _get_obsolete_conversion_mapping(cls) -> Dict['CommonSimDemographicType', 'CommonSimDemographicType']:
        mapping: Dict[CommonSimDemographicType, CommonSimDemographicType] = {
            CommonSimDemographicType.ACTIVE_SIM: CommonSimDemographicType.CURRENTLY_CONTROLLED,
            CommonSimDemographicType.CONTROLLED: CommonSimDemographicType.CURRENTLY_CONTROLLED,
            CommonSimDemographicType.NPC_SIMS: CommonSimDemographicType.NON_HOUSEHOLD,
            CommonSimDemographicType.PLAYER_SIMS: CommonSimDemographicType.HOUSEHOLD
        }
        return mapping
