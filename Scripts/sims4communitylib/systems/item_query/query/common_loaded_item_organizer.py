"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple, Generic, TypeVar

from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.enumtypes.common_int_flags import CommonIntFlags
from sims4communitylib.systems.item_query.dtos.common_loaded_item import CommonLoadedItem

CommonLoadedItemKeyType = TypeVar('CommonLoadedItemKeyType', int, CommonInt, CommonIntFlags)
CommonLoadedItemType = TypeVar('CommonLoadedItemType', bound=CommonLoadedItem)


class CommonLoadedItemOrganizer(Generic[CommonLoadedItemKeyType, CommonLoadedItemType]):
    """ An organizer of items. """
    def __init__(self, key_type: CommonLoadedItemKeyType):
        self._key_type = key_type

    @property
    def key_type(self) -> CommonLoadedItemKeyType:
        """ The type of keys this organizer produces. """
        return self._key_type

    def get_key_values(self, item: CommonLoadedItemType) -> Tuple[Any]:
        """ Retrieve key values for this organizer. """
        raise NotImplementedError

    # noinspection PyUnusedLocal
    def applies(self, item: CommonLoadedItemType) -> bool:
        """ Determine if this organizer applies to an item. """
        return True
