"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, TypeVar, Type

from objects.components import ComponentContainer, Component
from sims4communitylib.enums.types.component_types import CommonComponentType


CommonExpectedReturnType = TypeVar('CommonExpectedReturnType', bound=Component)


class CommonComponentUtils:
    """Utilities for handling components of component containers.

    """
    @staticmethod
    def has_component(component_container: ComponentContainer, component_type: CommonComponentType) -> bool:
        """has_component(component_container, component_type)

        Determine if a ComponentContainer has a component of the specified type.

        :param component_container: The ComponentContainer to check.
        :type component_container: ComponentContainer
        :param component_type: The type of component to locate.
        :type component_type: CommonComponentType
        :return: True, if the ComponentContainer contains a component of the specified type. False, if not.
        :rtype: bool
        """
        if component_type is None or not isinstance(component_container, ComponentContainer) or not hasattr(component_container, 'has_component'):
            return False
        return component_container.has_component(component_type)

    # noinspection PyUnusedLocal
    @staticmethod
    def get_component(component_container: ComponentContainer, component_type: CommonComponentType, add_dynamic: bool = False, return_type: Type[CommonExpectedReturnType] = Component) -> Union[CommonExpectedReturnType, None]:
        """get_component(component_container, component_type, add_dynamic=False, return_type=Component)

        Retrieve a component from a ComponentContainer.

        :param component_container: The ComponentContainer to retrieve a component from.
        :type component_container: ComponentContainer
        :param component_type: The type of component being retrieved.
        :type component_type: CommonComponentType
        :param add_dynamic: If True, the component will be added dynamically. If False, the component will not be added dynamically. Default is False.
        :type add_dynamic: bool, optional
        :param return_type: The type of the returned value. (This is to make type hinting more accurate). It is not actually used in the function. Default is Component.
        :type return_type: Type[CommonExpectedReturnType], optional
        :return: An object of type Component, or None if the specified component type is not found.
        :rtype: Union[CommonExpectedReturnType, None]
        """
        if component_type is None or not isinstance(component_container, ComponentContainer) or not hasattr(component_container, 'get_component'):
            return None
        if add_dynamic and not component_container.has_component(component_type):
            return CommonComponentUtils.add_dynamic_component(component_container, component_type)
        return component_container.get_component(component_type)

    @staticmethod
    def add_dynamic_component(component_container: ComponentContainer, component_type: CommonComponentType) -> Union[Component, None]:
        """add_dynamic_component(component_container, component_type)

        Add a dynamic component to a ComponentContainer.

        :param component_container: The ComponentContainer to add to.
        :type component_container: ComponentContainer
        :param component_type: The type of component being added.
        :type component_type: CommonComponentType
        :return: The added Component or None
        :rtype: Union[Component, None]
        """
        if component_type is None or not hasattr(component_container, 'add_dynamic_component') or not hasattr(component_container, 'get_component'):
            return None
        if not component_container.add_dynamic_component(component_type):
            return None
        return component_container.get_component(component_type)
