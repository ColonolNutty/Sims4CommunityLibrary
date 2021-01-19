"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyUnresolvedReferences
from _resourceman import Key


class CommonResourceKey:
    """A resource key wrapper."""

    def __init__(self, resource_type: str, instance: str, group: str):
        self._type = resource_type
        self._instance = instance
        self._group = group

    # noinspection PyMissingOrEmptyDocstring
    @property
    def type(self) -> str:
        return self._type

    # noinspection PyMissingOrEmptyDocstring
    @property
    def instance(self) -> str:
        return self._instance

    # noinspection PyMissingOrEmptyDocstring
    @property
    def group(self) -> str:
        return self._group

    def __repr__(self) -> str:
        return '{}!{}!{}'.format(self._type, self._group, self._instance)

    def __str__(self) -> str:
        return self.__repr__()
