"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sys
from pprint import pformat
from typing import Dict, Any
from typing import Union
from objects.game_object import GameObject
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils


class _CommonGameObjectDataStorageMetaclass(type):
    _game_object_storage_instances: Dict[str, Dict[int, '_CommonGameObjectDataStorageMetaclass']] = dict()

    def __call__(cls, game_object: GameObject) -> Union['_CommonGameObjectDataStorageMetaclass', None]:
        mod_identity = cls.get_mod_identity()
        game_object_id = CommonObjectUtils.get_object_id(game_object)
        mod_name = mod_identity.name
        if mod_name is None:
            return None
        if mod_name not in cls._game_object_storage_instances:
            cls._game_object_storage_instances[mod_name] = dict()
        if game_object_id not in cls._game_object_storage_instances[mod_name]:
            cls._game_object_storage_instances[mod_name][game_object_id] = super(_CommonGameObjectDataStorageMetaclass, cls).__call__(game_object)
        return cls._game_object_storage_instances[mod_name][game_object_id]

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(mcs) -> CommonModIdentity:
        raise NotImplementedError()


class _CommonGameObjectDataStorage(HasClassLog, metaclass=_CommonGameObjectDataStorageMetaclass):
    def __init__(self, game_object: GameObject):
        super().__init__()
        self._game_object_id = CommonObjectUtils.get_object_id(game_object)
        self._game_object = game_object
        self._data = dict()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError('Missing \'{}\' inside {}.'.format(cls.get_mod_identity.__name__, cls.__class__))

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return '{}_game_object_data_storage'.format(cls.get_mod_identity().base_namespace)

    @property
    def game_object(self) -> GameObject:
        """The GameObject the storage applies to.

        :return: An instance of an Object.
        :rtype: GameObject
        """
        return self._game_object

    @property
    def game_object_id(self) -> int:
        """The decimal identifier of the GameObject.

        :return: The decimal identifier of the GameObject.
        :rtype: int
        """
        return self._game_object_id

    def get_data(self, default: Any=None, key: str=None) -> Union[Any, None]:
        """get_data(default=None, key=None)

        Retrieve stored data.

        :param default: The default data to return. The default value is None.
        :type default: Dict[Any, Any], optional
        :param key: The key for the data. If None, the name of the calling function will be used.
        :type key: str, optional
        :return: The stored data.
        :rtype: Dict[Any, Any]
        """
        key = key or str(sys._getframe(1).f_code.co_name)
        if key not in self._data:
            self.log.format_with_message('Key not found in data.', key=key, data=self._data)
            self._data[key] = default
        return self._data.get(key)

    def set_data(self, value: Any, key: str=None):
        """set_data(value, key=None)

        Set stored data.

        :param value: The value of the data.
        :type value: Any
        :param key: The key for the data. If None, the name of the calling function will be used.
        :type key: str, optional
        """
        key = key or str(sys._getframe(1).f_code.co_name)
        self._data[key] = value

    def remove_data(self, key: str=None):
        """remove_data(key=None)

        Remove stored data.

        :param key: The key for the data. If None, the name of the calling function will be used.
        :type key: str, optional
        """
        key = key or str(sys._getframe(1).f_code.co_name)
        if key not in self._data:
            self.log.format_with_message('Key not found in data.', key=key, data=self._data)
            return
        del self._data[key]

    def __repr__(self) -> str:
        return ''.join(['{}: {}\n'.format(pformat(key), pformat(value)) for (key, value) in self._data.items()])

    def __str__(self) -> str:
        return self.__repr__()


class CommonGameObjectDataStorage(_CommonGameObjectDataStorage):
    """CommonGameObjectDataStorage(game_object)

    A wrapper for Object instances that allows storing of data.

    .. warning:: Data stored within is not persisted when closing and reopening the game!
    .. warning:: DO NOT CREATE THIS CLASS DIRECTLY, IT IS ONLY MEANT TO INHERIT FROM!

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        # Inherit from CommonGameObjectDataStorage
        class _ExampleGameObjectDataStorage(CommonGameObjectDataStorage):
            # noinspection PyMissingOrEmptyDocstring
            @classmethod
            def get_mod_identity(cls) -> CommonModIdentity:
                # !!!Override with the CommonModIdentity of your own mod!!!
                from sims4communitylib.modinfo import ModInfo
                return ModInfo.get_identity()

            @property
            def example_property_one(self) -> bool:
                # Could also be written self.get_data(default=False, key='example_property_one') and it would do the same thing.
                return self.get_data(default=False)

            @example_property_one.setter
            def example_property_one(self, value: bool):
                # Could also be written self.set_data(value, key='example_property_one') and it would do the same thing.
                self.set_data(value)

    :param game_object: An instance of an Object.
    :type game_object: GameObject
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError('Missing \'{}\' inside {}.'.format(cls.get_mod_identity.__name__, cls.__class__))

    def __init__(self, game_object: GameObject):
        super().__init__(game_object)
        if self.__class__.__name__ is CommonGameObjectDataStorage.__name__:
            raise RuntimeError('{} cannot be created directly. You must inherit from it to create an instance of it.'.format(self.__class__.__name__))


# noinspection PyMissingOrEmptyDocstring
class _ExampleGameObjectDataStorage(CommonGameObjectDataStorage):
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        # !!!Override with the CommonModIdentity of your own mod!!!
        from sims4communitylib.modinfo import ModInfo
        return ModInfo.get_identity()

    @property
    def example_property_one(self) -> bool:
        # Could also be written self.get_data(default=False, key='example_property_one') and it would do the same thing.
        return self.get_data(default=False)

    @example_property_one.setter
    def example_property_one(self, value: bool):
        # Could also be written self.set_data(value, key='example_property_one') and it would do the same thing.
        self.set_data(value)
