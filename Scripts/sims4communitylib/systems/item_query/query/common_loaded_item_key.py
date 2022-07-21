"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple, TypeVar, Generic

from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.enumtypes.common_int_flags import CommonIntFlags

ItemKeyType = TypeVar('ItemKeyType', int, CommonInt, CommonIntFlags)


class CommonLoadedItemKey(Generic[ItemKeyType]):
    """ A key for a loaded item. """
    def __init__(self, key_type: ItemKeyType, value: Any):
        self._key_type = key_type
        self._value = value
        self._key = (key_type, value)

    @property
    def key_type(self) -> ItemKeyType:
        """ The type of key. """
        return self._key_type

    @property
    def value(self) -> Any:
        """ The value. """
        return self._value

    @property
    def key(self) -> Tuple[ItemKeyType, Any]:
        """ The combination of the type and value. """
        return self._key

    def __repr__(self) -> str:
        return str(self.key)

    def __str__(self) -> str:
        return self.__repr__()
