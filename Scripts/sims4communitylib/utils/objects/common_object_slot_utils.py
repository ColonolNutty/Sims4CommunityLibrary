"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union, List, Callable, Iterator

from objects.base_object import BaseObject
from objects.components.slot_component import SlotComponent
from objects.game_object import GameObject
from objects.script_object import ScriptObject
from objects.slots import SlotType
from sims4communitylib.dtos.common_object_containment_slot import CommonObjectContainmentSlot
from sims4communitylib.enums.common_slot_type import CommonSlotType
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils

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
        # noinspection PyTypeChecker
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
        # noinspection PyTypeChecker
        slot_component: SlotComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.SLOT)
        return slot_component

    @classmethod
    def get_slot_name(cls, slot: SlotType) -> str:
        """get_slot_name(slot)

        Retrieve the name of a slot.

        :param slot: The slot to use.
        :type slot: SlotType
        :return: The name of the slot or 'No Slot Name' if a problem occurs.
        :rtype: str
        """
        if slot is None:
            return 'No Slot Name'
        return slot.__name__

    @classmethod
    def get_first_connected_object_by_slot_name(
        cls,
        script_object: ScriptObject,
        slot_name: CommonSlotType,
        include_object_callback: Callable[[ScriptObject], bool] = None
    ) -> Union[ScriptObject, None]:
        """get_first_connected_object_by_slot_name(script_object, slot_name, include_object_callback=None)

        Get the first connected object by slot.

        .. note:: If only the first object found matching the slot type will be returned.

        :param script_object: The Object to locate connections with.
        :type script_object: ScriptObject
        :param slot_name: The name of the slot to locate a connected object at.
        :type slot_name: CommonSlotType
        :param include_object_callback: If the result of this callback is True, the Object will be included in the results. If set to None, All Objects will be included. Default is None.
        :type include_object_callback: Callable[[ScriptObject], bool], optional
        :return: The object connected to the specified object at the specified slot or None if no object is found.
        :rtype: Union[ScriptObject, None]
        """
        for child in cls.get_connected_objects_by_slot_name_gen(
            script_object,
            slot_name,
            include_object_callback=include_object_callback
        ):
            return child
        return None

    @classmethod
    def get_connected_objects_by_slot_name_gen(
        cls,
        script_object: ScriptObject,
        slot_name: CommonSlotType,
        include_object_callback: Callable[[ScriptObject], bool] = None
    ) -> Iterator[ScriptObject]:
        """get_connected_objects_by_slot_generator(script_object, slot_name, include_object_callback=None)

        Get all connected objects by slot.

        :param script_object: The Object to locate connections with.
        :type script_object: ScriptObject
        :param slot_name: The name of the slot to locate a connected objects at.
        :type slot_name: CommonSlotType
        :param include_object_callback: If the result of this callback is True, the Object will be included in the results. If set to None, All Objects will be included. Default is None.
        :type include_object_callback: Callable[[ScriptObject], bool], optional
        :return: An iterator of objects connected to the specified object at the specified slot.
        :rtype: Iterator[ScriptObject]
        """
        if script_object is None:
            return tuple()

        slot_name_str = str(slot_name)
        with_slot_in_front_of_name = f'slot_{slot_name}'

        def _has_slot_name(_connected_object: ScriptObject) -> bool:
            if not _connected_object.parent_slot:
                return False
            for _connected_object_slot_type in _connected_object.parent_slot.slot_types:
                if cls.get_slot_name(_connected_object_slot_type) in (slot_name_str, with_slot_in_front_of_name):
                    return True
            return False

        if include_object_callback is not None:
            include_object_callback = CommonFunctionUtils.run_predicates_as_one((_has_slot_name, include_object_callback))
        else:
            include_object_callback = _has_slot_name

        for connected_object in CommonObjectSlotUtils.get_all_connected_objects_gen(
            script_object,
            include_object_callback=include_object_callback
        ):
            yield connected_object

    @classmethod
    def get_all_connected_objects_gen(
        cls,
        script_object: ScriptObject,
        include_self: bool = False,
        direct_connections_only: bool = False,
        include_object_callback: Callable[[ScriptObject], bool] = None
    ) -> Iterator[BaseObject]:
        """get_all_connected_objects_generator(\
            script_object,\
            include_self=False,\
            direct_connections_only=False,\
            include_object_callback=None\
        )

        Retrieve all objects connected to the specified Object.

        :param script_object: The Object to locate connections with.
        :type script_object: ScriptObject
        :param include_self: If True, then script_object will be included in the results. If False, script_object will not be included in the results. Default is False.
        :type include_self: bool, optional
        :param direct_connections_only: If True, then only directly connected objects will be included in the results. If False, all connected objects as well as all objects connected to those objects recursively will be included in the results.
        :type direct_connections_only: bool, optional
        :param include_object_callback: If the result of this callback is True, the Object will be included in the results. If set to None, All Objects will be included. Default is None.
        :type include_object_callback: Callable[[ScriptObject], bool], optional
        :return: An iterator of Objects connected to the specified Object.
        :rtype: Iterator[BaseObject]
        """
        if direct_connections_only:
            if include_self:
                yield script_object
            for connected_object in script_object.children:
                if connected_object is None:
                    continue
                if include_object_callback is not None and not include_object_callback(connected_object):
                    continue
                yield connected_object
        else:
            for connected_object in script_object.children_recursive_gen(include_self=include_self):
                if connected_object is None:
                    continue
                if include_object_callback is not None and not include_object_callback(connected_object):
                    continue
                yield connected_object
