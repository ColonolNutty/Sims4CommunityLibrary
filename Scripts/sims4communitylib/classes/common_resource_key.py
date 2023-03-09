"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Union
from sims4communitylib.enums.enumtypes.common_int import CommonInt

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

if ON_RTD:
    # noinspection PyMissingOrEmptyDocstring
    class Types(CommonInt):
        pass

    # noinspection PyMissingOrEmptyDocstring
    class Groups(CommonInt):
        pass

    # noinspection PyMissingOrEmptyDocstring
    class Key:
        # noinspection PyPropertyDefinition
        @property
        def type(self) -> str:
            pass

        # noinspection PyPropertyDefinition
        @property
        def instance(self) -> str:
            pass

        # noinspection PyPropertyDefinition
        @property
        def group(self) -> str:
            pass

        # noinspection PyUnusedLocal
        def __init__(self, res_type: int, res_instance: int, *args, **kwargs):
            pass

if not ON_RTD:
    try:
        # noinspection PyUnresolvedReferences
        from _resourceman import Key
        from sims4.resources import Types, Groups
    except:
        class Key:
            pass

        class Types:
            pass

        class Groups:
            pass


class CommonResourceKey:
    """CommonResourceKey(resource_key_type, resource_key_instance, resource_key_group)

    A wrapper for a resource key.

    :param resource_key_type: An identifier that indicates the tuning type of the resource.
    :type resource_key_type: Union[int, str, Types]
    :param resource_key_instance: An identifier that indicates what tuning instance the resource key is for.
    :type resource_key_instance: Union[int, str]
    :param resource_key_group: An identifier that indicates what tuning group the resource key is for. In most cases a group of "0" is sufficient.
    :type resource_key_group: Union[int, str, Group]
    """

    @property
    def type(self) -> Union[int, str, Types]:
        """ The type identifier of the resource. """
        return self._resource_key_type

    @property
    def instance(self) -> Union[int, str]:
        """ The instance identifier of the resource. """
        return self._resource_key_instance

    @property
    def group(self) -> Union[int, str, Groups]:
        """ The group identifier of the resource. """
        return self._resource_key_group

    def __init__(self, resource_key_type: Union[int, str, Types], resource_key_instance: Union[int, str], resource_key_group: Union[int, str, Groups]):
        self._resource_key_type = resource_key_type
        self._resource_key_instance = resource_key_instance
        self._resource_key_group = resource_key_group

    def __new__(cls, resource_key_type: Union[int, str, Types], resource_key_instance: Union[int, str], resource_key_group: Union[int, str, Groups]) -> 'CommonResourceKey':
        # noinspection PyTypeChecker
        return Key(resource_key_type, resource_key_instance, resource_key_group)

    @staticmethod
    def empty() -> 'CommonResourceKey':
        """empty()

        Create an empty resource key.

        :return: An empty resource key.
        :rtype: CommonResourceKey
        """
        return CommonResourceKey(0, 0, 0)

    @staticmethod
    def from_resource_key(resource_key: Union[Key, 'CommonResourceKey']) -> Union['CommonResourceKey', None]:
        """from_resource_key(resource_key)

        Convert a vanilla Key object into a CommonResourceKey.

        :param resource_key: An instance of a Resource Key.
        :type resource_key: Union[Key, CommonResourceKey]
        :return: An instance of a CommonResourceKey or None if the object failed to convert.
        :rtype: Union[CommonResourceKey, None]
        """
        if resource_key is None:
            return None
        if isinstance(resource_key, CommonResourceKey):
            return resource_key
        if not isinstance(resource_key, Key):
            raise Exception('Failed to convert {} with type {}, it was not of type {}.'.format(resource_key, type(resource_key), type(Key)))
        return CommonResourceKey(resource_key.type, resource_key.instance, resource_key.group)

    def __repr__(self) -> str:
        if not self.group or self.group == 0:
            return '{}!{}'.format(self.type, self.instance)
        return '{}!{}!{}'.format(self.type, self.instance, self.group)

    def __str__(self) -> str:
        return self.__repr__()
