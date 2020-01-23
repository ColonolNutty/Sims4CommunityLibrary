"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import TypeVar, Type

ServiceType = TypeVar('ServiceType', bound=object)


class CommonService:
    """A class used as a common structure for singleton services.

    """
    @classmethod
    def get(cls: Type[ServiceType]) -> ServiceType:
        """Retrieve an instance of the service

        :return: An instance of the service
        """
        if getattr(cls, '_SERVICE', None) is None:
            setattr(cls, '_SERVICE', cls())
        return getattr(cls, '_SERVICE')

    def __new__(cls, *args, **kwargs) -> 'CommonService':
        if getattr(cls, '_SERVICE', None) is None:
            setattr(cls, '_SERVICE', super().__new__(cls))
        return getattr(cls, '_SERVICE')
