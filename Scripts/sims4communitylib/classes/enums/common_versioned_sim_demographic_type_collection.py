"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Type, Iterator

from sims4communitylib.classes.enums.common_versioned_enum_value_collection import CommonVersionedEnumValueCollection
from sims4communitylib.enums.common_sim_demographic_types import CommonSimDemographicType


class CommonVersionedSimDemographicTypeCollection(CommonVersionedEnumValueCollection[CommonSimDemographicType]):
    """CommonVersionedSimDemographicTypeCollection(\
        demographic_types,\
        version=None\
    )

    A collection of demographic types with a version.

    :param demographic_types: A collection of demographic types.
    :type demographic_types: Iterator[CommonSimDemographicType]
    :param version: The version of the data. Default is the version of CommonSimDemographicType.
    :type version: str, optional
    """

    def __init__(self, demographic_types: Iterator[CommonSimDemographicType], version: str = None):
        super().__init__(demographic_types, version=version)

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_enum_type(cls) -> Type[CommonSimDemographicType]:
        return CommonSimDemographicType

    @property
    def demographic_types(self) -> Tuple[CommonSimDemographicType]:
        """Types of demographics."""
        return self.enum_values
