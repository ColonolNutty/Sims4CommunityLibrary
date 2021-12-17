"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator, Tuple, List

from sims4communitylib.enums.situations_enum import CommonSituationId
from situations.situation import Situation


class CommonSituationUtils:
    """Utilities for manipulating Situations.

    """

    @staticmethod
    def get_situation_id(situation_identifier: Union[int, Situation]) -> Union[int, None]:
        """get_situation_id(situation_identifier)

        Retrieve the decimal identifier of a Situation.

        :param situation_identifier: The identifier or instance of a Situation.
        :type situation_identifier: Union[int, Situation]
        :return: The decimal identifier of the Situation or None if the Situation does not have an id.
        :rtype: Union[int, None]
        """
        if isinstance(situation_identifier, int):
            return situation_identifier
        if not hasattr(situation_identifier, 'id'):
            return -1
        return situation_identifier.id or getattr(situation_identifier, 'id', -1)

    @staticmethod
    def get_situation_guid(situation_identifier: Union[int, Situation]) -> int:
        """get_situation_guid(situation_identifier)

        Retrieve the GUID of a Situation.

        :param situation_identifier: The identifier or instance of a Situation.
        :type situation_identifier: Union[int, Situation]
        :return: The GUID of the specified Situation or -1 if it does not have one.
        :rtype: int
        """
        if situation_identifier is None:
            return -1
        if isinstance(situation_identifier, int):
            return situation_identifier
        if not hasattr(situation_identifier, 'guid64'):
            return -1
        return getattr(situation_identifier, 'guid64', -1)

    @staticmethod
    def get_situation_name(situation: Situation) -> Union[str, None]:
        """get_situation_name(situation)

        Retrieve the Name of a Situation.

        :param situation: An instance of a Situation.
        :type situation: Situation
        :return: The short name of a Situation or None if a problem occurs.
        :rtype: Union[str, None]
        """
        if situation is None:
            return None
        # noinspection PyBroadException
        try:
            return situation.__class__.__name__ or ''
        except:
            return ''

    @staticmethod
    def get_situation_names(situations: Iterator[Situation]) -> Tuple[str]:
        """get_situation_names(situations)

        Retrieve the Names of a collection of Situation.

        :param situations: A collection of Situation instances.
        :type situations: Iterator[Situation]
        :return: A collection of names for all specified Situations.
        :rtype: Tuple[str]
        """
        if situations is None or not situations:
            return tuple()
        names: List[str] = []
        for situation in situations:
            # noinspection PyBroadException
            try:
                name = CommonSituationUtils.get_situation_name(situation)
                if not name:
                    continue
            except:
                continue
            names.append(name)
        return tuple(names)

    @staticmethod
    def load_situation_by_id(situation_id: Union[int, CommonSituationId, Situation]) -> Union[Situation, None]:
        """load_situation_by_id(situation_id)

        Load an instance of a Situation by its decimal identifier.

        :param situation_id: The decimal identifier of a Situation.
        :type situation_id: Union[int, CommonSituationId, Situation]
        :return: An instance of a Situation matching the decimal identifier or None if not found.
        :rtype: Union[Situation, None]
        """
        if isinstance(situation_id, Situation):
            return situation_id
        # noinspection PyBroadException
        try:
            situation_id: int = int(situation_id)
        except:
            situation_id: Situation = situation_id
            return situation_id

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.SITUATION, situation_id)
