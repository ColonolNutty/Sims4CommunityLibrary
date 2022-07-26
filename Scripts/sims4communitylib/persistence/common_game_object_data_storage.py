"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sys
from pprint import pformat
from typing import Dict, Any, Callable
from typing import Union
from objects.game_object import GameObject
from sims4communitylib.classes.serialization.common_serializable import CommonSerializable
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils


class _CommonGameObjectDataStorageMetaclass(type):
    _game_object_storage_instances: Dict[str, Dict[int, '_CommonGameObjectDataStorageMetaclass']] = dict()

    def __call__(cls, game_object: GameObject):
        mod_identity = cls.get_mod_identity()
        game_object_id = CommonObjectUtils.get_object_id(game_object)
        mod_name = mod_identity.name
        if mod_name is None:
            return None
        identifier = f'{mod_name}_{cls.__name__}'
        if identifier not in cls._game_object_storage_instances:
            cls._game_object_storage_instances[identifier] = dict()
        if game_object_id not in cls._game_object_storage_instances[identifier]:
            cls._game_object_storage_instances[identifier][game_object_id] = super(_CommonGameObjectDataStorageMetaclass, cls).__call__(game_object)
        stored_obj = cls._game_object_storage_instances[identifier][game_object_id]
        if stored_obj.__class__.__name__ != cls.__name__:
            cls._game_object_storage_instances[identifier][game_object_id] = super(_CommonGameObjectDataStorageMetaclass, cls).__call__(game_object)
        return cls._game_object_storage_instances[identifier][game_object_id]

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(mcs) -> CommonModIdentity:
        raise NotImplementedError()

    @classmethod
    def clear_instances(mcs, mod_identity: CommonModIdentity) -> None:
        """Clear the cached instances of this type of Object Storage."""
        mod_name = mod_identity.name
        if mod_name is None:
            return
        identifier = f'{mod_name}_{mcs.__name__}'
        if identifier in _CommonGameObjectDataStorageMetaclass._game_object_storage_instances:
            del _CommonGameObjectDataStorageMetaclass._game_object_storage_instances[identifier]


class _CommonGameObjectDataStorage(HasClassLog, metaclass=_CommonGameObjectDataStorageMetaclass):
    def __init__(self, game_object: GameObject):
        super().__init__()
        if not CommonTypeUtils.is_game_object(game_object):
            raise AssertionError('game_object was not of type GameObject! {}'.format(game_object))
        self._game_object_id = CommonObjectUtils.get_object_id(game_object)
        self._game_object = game_object
        self._data: Dict[str, Any] = dict()

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

    def get_data(self, default: Any=None, key: str=None, encode: Callable[[Any], Any]=None, decode: Callable[[Any], Any]=None) -> Union[Any, None]:
        """get_data(default=None, key=None, encode=None, decode=None)

        Retrieve stored data.

        :param default: The default data to return. The default value is None.
        :type default: Dict[Any, Any], optional
        :param key: The key for the data. If None, the name of the calling function will be used.
        :type key: str, optional
        :param encode: If specified, the data will be encoded using this function and the result will be the new data stored. Default is None.
        :type encode: Callable[[Any], Any], optional
        :param decode: If specified, the data will be decoded using this function and the result will be the new result of "get_data". Default is None.
        :type decode: Callable[[Any], Any], optional
        :return: The stored data.
        :rtype: Union[Any, None]
        """
        # noinspection PyUnresolvedReferences
        key = key or str(sys._getframe(1).f_code.co_name)
        if key not in self._data:
            self.log.format_with_message('Key not found in data.', key=key, data=self._data)
            if default is not None:
                if encode is not None:
                    self._data[key] = encode(default)
                else:
                    self._data[key] = default
            return default
        data = self._data.get(key)
        if decode is not None and not isinstance(data, CommonSerializable):
            decoded = decode(data)
            if isinstance(data, CommonSerializable):
                self._data[key] = decoded
            return decoded
        return data

    def set_data(self, value: Any, key: str=None, encode: Callable[[Any], Any]=None):
        """set_data(value, key=None, encode=None)

        Set stored data.

        :param value: The value of the data.
        :type value: Any
        :param key: The key for the data. If None, the name of the calling function will be used.
        :type key: str, optional
        :param encode: If specified, the data will be encoded using this function and the result will be the new data stored. Default is None.
        :type encode: Callable[[Any], Any], optional
        """
        # noinspection PyUnresolvedReferences
        key = key or str(sys._getframe(1).f_code.co_name)
        if encode is not None:
            value = encode(value)
        self._data[key] = value

    def remove_data(self, key: str=None):
        """remove_data(key=None)

        Remove stored data.

        :param key: The key for the data. If None, the name of the calling function will be used.
        :type key: str, optional
        """
        # noinspection PyUnresolvedReferences
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
