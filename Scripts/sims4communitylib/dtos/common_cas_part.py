"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims.outfits.outfit_enums import BodyType
from sims4communitylib.enums.common_body_slot import CommonBodySlot


class CommonCASPart:
    """CommonCASPart(\
        cas_part_id,\
        body_type=None,\
    )

    A class that contains information about a CAS Part.

    :param cas_part_id: The decimal identifier of a CAS Part.
    :type cas_part_id: int
    :param body_type: The place on a Sims person the CAS Part gets applied to. If not specified, then the Body Type of the CAS Part itself will be used. Default is None.
    :type body_type: Union[CommonBodySlot, BodyType, int, None], optional
    """

    def __init__(self, cas_part_id: int, body_type: Union[CommonBodySlot, BodyType, int, None] = None) -> None:
        self._cas_part_id = cas_part_id
        from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
        self._body_type = body_type or CommonCASUtils.get_body_type_of_cas_part(cas_part_id)

    @property
    def cas_part_id(self) -> int:
        """The decimal identifier of a CAS Part."""
        return self._cas_part_id

    @property
    def body_type(self) -> Union[CommonBodySlot, BodyType, int]:
        """The place on a Sims person the CAS Part gets applied to."""
        return self._body_type

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'<CommonCASPart cas_part: {self.cas_part_id} body_type: {self.body_type}>'
