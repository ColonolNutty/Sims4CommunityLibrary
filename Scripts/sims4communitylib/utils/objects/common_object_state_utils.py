"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple
from objects.components.state import StateComponent, ObjectStateValue
from objects.game_object import GameObject
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.utils.common_component_utils import CommonComponentUtils


class CommonObjectStateUtils:
    """ Utilities for manipulating the state of Objects. """
    @staticmethod
    def is_object_usable(game_object: GameObject) -> bool:
        """is_object_usable(game_object)

        Determine if an Object is in a usable state.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the specified Object is in a usable state. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return False
        state_component: StateComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.STATE)
        if state_component is None:
            return False
        return state_component.is_object_usable

    @staticmethod
    def get_object_states(game_object: GameObject) -> Tuple[ObjectStateValue]:
        """get_object_states(game_object)

        Retrieve the state values of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: A collection of ObjectStateValues.
        :rtype: Tuple[ObjectStateValue]
        """
        if game_object is None:
            return tuple()
        state_component: StateComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.STATE)
        if state_component is None:
            return tuple()
        return tuple(state_component.values())

    @staticmethod
    def has_any_object_states(game_object: GameObject, object_state_ids: Tuple[int]) -> bool:
        """has_any_object_states(game_object, object_state_ids)

        Determine if an Object has any of the specified object states.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param object_state_ids: A collection of decimal identifiers for object states.
        :type object_state_ids: Tuple[int]
        :return: True, if the object has any of the specified object states. False, if not.
        :rtype: bool
        """
        state_component: StateComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.STATE)
        if state_component is None:
            return False
        if not object_state_ids:
            return False
        for state_value in state_component.values():
            if CommonObjectStateUtils.get_object_state_value_id(state_value) in object_state_ids:
                return True
        return False

    @staticmethod
    def has_all_object_states(game_object: GameObject, object_state_ids: Tuple[int]) -> bool:
        """has_all_object_states(game_object, object_state_ids)

        Determine if an Object has all of the specified object states.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param object_state_ids: A collection of decimal identifiers for object states.
        :type object_state_ids: Tuple[int]
        :return: True, if the object has all of the specified object states. False, if not.
        :rtype: bool
        """
        state_component: StateComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.STATE)
        if state_component is None:
            return False
        if not object_state_ids:
            return False
        for state_value in state_component.values():
            if CommonObjectStateUtils.get_object_state_value_id(state_value) not in object_state_ids:
                return False
        return True

    @staticmethod
    def get_object_state_value_id(object_state_value: ObjectStateValue) -> Union[int, None]:
        """get_object_state_id(state_value)

        Retrieve the decimal identifier of an object state.

        :param object_state_value: An instance of an object state.
        :type object_state_value: ObjectStateValue
        :return: The identifier of the state value or None if no identifier is found.
        :rtype: Union[int, None]
        """
        if object_state_value is None:
            return None
        return getattr(object_state_value, 'guid64', None)

    @staticmethod
    def get_object_state_component(game_object: GameObject) -> Union[StateComponent, None]:
        """get_object_state_component(game_object)

        Retrieve the State Component of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The State Component of the specified Object or None if no state component is found.
        :rtype: Union[StateComponent, None]
        """
        if game_object is None:
            return None
        return CommonComponentUtils.get_component(game_object, CommonComponentType.STATE)
