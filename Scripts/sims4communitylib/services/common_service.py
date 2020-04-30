"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import TypeVar, Any

ServiceType = TypeVar('ServiceType', bound=object)


class _Singleton(type):
    def __init__(cls, *args, **kwargs) -> None:
        super(_Singleton, cls).__init__(*args, **kwargs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs) -> 'CommonService':
        if cls.__instance is None:
            cls.__instance = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls.__instance


class CommonService(metaclass=_Singleton):
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
    def get(cls: Any, *_, **__) -> 'CommonService':
        """get()

        Retrieve an instance of the service

        :return: An instance of the service
        :rtype: The type of the inheriting class
        """
        return cls(*_, **__)
