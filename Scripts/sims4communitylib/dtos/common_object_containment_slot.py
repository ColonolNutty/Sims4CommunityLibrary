"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from objects.slots import SlotType


class CommonObjectContainmentSlot:
    """CommonObjectContainmentSlot(slot_name_hash, slot_types)

    A slot used for containing other objects within an object.

    .. note:: A place that other objects can be placed at on an object.

    :param slot_name_hash: The hashed name of the slot.
    :type slot_name_hash: int
    :param slot_types: A collection of slot types within this containment slot.
    :type slot_types: Tuple[SlotType]
    """
    def __init__(self, slot_name_hash: int, slot_types: Tuple[SlotType]):
        self._slot_name_hash = slot_name_hash
        self._slot_types = slot_types

    @property
    def slot_name_hash(self) -> int:
        """The hashed name of the slot."""
        return self._slot_name_hash

    @property
    def slot_types(self) -> Tuple[SlotType]:
        """The types of slots."""
        return self._slot_types
