"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import TypeVar, Type

ServiceType = TypeVar('ServiceType', bound=object)


class CommonService:
    """An inheritable class that turns a class into a singleton, create an instance by invoking :func:`~get`.


    :Example usage:

    .. highlight:: python
    .. code-block:: python

        class ExampleService(CommonService):
            @property
            def first_value(self) -> str:
                return 'yes'

        # ExampleService.get() returns an instance of ExampleService.
        # Calling ExampleService.get() again, will return the same instance.
        ExampleService.get().first_value

    """
    @classmethod
    def get(cls: Type[ServiceType]) -> ServiceType:
        """get()

        Retrieve an instance of the service

        :return: An instance of the service
        :rtype: The type of the inheriting class
        """
        if getattr(cls, '_SERVICE', None) is None:
            setattr(cls, '_SERVICE', cls())
        return getattr(cls, '_SERVICE')

    def __new__(cls, *args, **kwargs) -> 'CommonService':
        if getattr(cls, '_SERVICE', None) is None:
            setattr(cls, '_SERVICE', super().__new__(cls))
        return getattr(cls, '_SERVICE')
