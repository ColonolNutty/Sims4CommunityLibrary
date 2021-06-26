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
from sims.sim_info import SimInfo
from sims4communitylib.classes.serialization.common_serializable import CommonSerializable
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class _CommonSimDataStorageMetaclass(type):
    _sim_storage_instances: Dict[str, Dict[int, '_CommonSimDataStorageMetaclass']] = {}

    def __call__(cls, sim_info: SimInfo) -> Union['_CommonSimDataStorageMetaclass', None]:
        mod_identity = cls.get_mod_identity()
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        mod_name = mod_identity.name
        if mod_name is None:
            return None
        if mod_name not in cls._sim_storage_instances:
            cls._sim_storage_instances[mod_name] = dict()
        if sim_id not in cls._sim_storage_instances[mod_name]:
            cls._sim_storage_instances[mod_name][sim_id] = super(_CommonSimDataStorageMetaclass, cls).__call__(sim_info)
        return cls._sim_storage_instances[mod_name][sim_id]

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(mcs) -> CommonModIdentity:
        raise NotImplementedError()


class _CommonSimDataStorage(HasClassLog, metaclass=_CommonSimDataStorageMetaclass):
    def __init__(self, sim_info: SimInfo):
        super().__init__()
        self._sim_id = CommonSimUtils.get_sim_id(sim_info)
        self._sim_info = sim_info
        self._data: Dict[str, Any] = dict()
        if sim_info is not None:
            from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
            sim_name = CommonSimNameUtils.get_full_name(sim_info)
            if sim_name is not None:
                self._data['sim_name'] = sim_name

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError('Missing \'{}\' inside {}.'.format(cls.get_mod_identity.__name__, cls.__class__))

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return '{}_sim_data_storage'.format(cls.get_mod_identity().base_namespace)

    @property
    def sim_info(self) -> SimInfo:
        """The SimInfo of a Sim.

        :return: The SimInfo of a Sim.
        :rtype: SimInfo
        """
        return self._sim_info

    @property
    def sim_id(self) -> int:
        """The decimal identifier of a Sim.

        :return: The decimal identifier of a Sim.
        :rtype: int
        """
        return self._sim_id

    def get_data(self, default: Any=None, key: str=None, encode: Callable[[Any], Any]=None, decode: Callable[[Any], CommonSerializable]=None) -> Union[Any, None]:
        """get_data(default=None, key=None, encode=None, decode=None)

        Retrieve stored data.

        :param default: The default data to return. The default value is None.
        :type default: Dict[Any, Any], optional
        :param key: The key for the data. If None, the name of the calling function will be used.
        :type key: str, optional
        :param encode: If specified, the data will be encoded using this function and the result will be the new data stored. Default is None.
        :type encode: Callable[[Any], Any], optional
        :param decode: If specified, the data will be decoded using this function and the result will be the new result of "get_data". Default is None.
        :type decode: Callable[[Any], CommonSerializable], optional
        :return: The stored data.
        :rtype: Union[Any, None]
        """
        key = key or str(sys._getframe(1).f_code.co_name)
        if key not in self._data:
            self.log.format_with_message('Key not found in data.', key=key, data=self._data)
            if encode is not None:
                self._data[key] = encode(default)
            else:
                self._data[key] = default
            return default
        data = self._data.get(key)
        if decode is not None and not isinstance(data, CommonSerializable):
            self._data[key] = decode(data)
            return self._data[key]
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
        key = key or str(sys._getframe(1).f_code.co_name)
        if key not in self._data:
            self.log.format_with_message('Key not found in data.', key=key, data=self._data)
            return
        del self._data[key]

    def __repr__(self) -> str:
        return ''.join(['{}: {}\n'.format(pformat(key), pformat(value)) for (key, value) in self._data.items()])

    def __str__(self) -> str:
        return self.__repr__()


class CommonSimDataStorage(_CommonSimDataStorage):
    """CommonSimDataStorage(sim_info)

    A wrapper for Sim instances that allows storing of data.

    .. warning:: Data stored within is not persisted when closing and reopening the game!
    .. warning:: DO NOT CREATE THIS CLASS DIRECTLY, IT IS ONLY MEANT TO INHERIT FROM!

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        # Inherit from CommonSimDataStorage
        class _ExampleSimDataStorage(CommonSimDataStorage):
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

    :param sim_info: The SimInfo of a Sim.
    :type sim_info: SimInfo
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError('Missing \'{}\' inside {}.'.format(cls.get_mod_identity.__name__, cls.__class__))

    def __init__(self, sim_info: SimInfo):
        super().__init__(sim_info)
        if self.__class__.__name__ is CommonSimDataStorage.__name__:
            raise RuntimeError('{} cannot be created directly. You must inherit from it to create an instance of it.'.format(self.__class__.__name__))


# noinspection PyMissingOrEmptyDocstring
class _ExampleSimDataStorage(CommonSimDataStorage):
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
