"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union, List

from objects.components.slot_component import SlotComponent
from objects.game_object import GameObject
from sims4communitylib.dtos.common_object_containment_slot import CommonObjectContainmentSlot
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.utils.common_component_utils import CommonComponentUtils


from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils


class CommonObjectSlotUtils:
    """Utilities for manipulating object slots."""
    @classmethod
    def get_containment_slots(cls, game_object: GameObject) -> Tuple[CommonObjectContainmentSlot]:
        """get_containment_slots(game_object)

        Retrieve the containment slots of an object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: A collection of containment slots on the specified object.
        :rtype: Tuple[CommonObjectContainmentSlot]
        """
        game_object: GameObject = CommonObjectUtils.get_root_parent(game_object)
        slot_component = cls.get_slot_component(game_object)
        if slot_component is None:
            return tuple()
        containment_slot_list: List[CommonObjectContainmentSlot] = list()
        for (slot_hash, slot_types) in tuple(slot_component.get_containment_slot_infos()):
            containment_slot_list.append(CommonObjectContainmentSlot(slot_hash, slot_types))
        return tuple(containment_slot_list)

    @classmethod
    def get_slot_component(cls, game_object: GameObject) -> Union[SlotComponent, None]:
        """get_slot_component(game_object)

        Retrieve the SlotComponent of an Object.

        :param game_object: An instance of an object.
        :type game_object: GameObject
        :return: The SlotComponent of the object or None if not found.
        :rtype: bool
        """
        if not CommonComponentUtils.has_component(game_object, CommonComponentType.SLOT):
            return None
        slot_component: SlotComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.SLOT)
        return slot_component
