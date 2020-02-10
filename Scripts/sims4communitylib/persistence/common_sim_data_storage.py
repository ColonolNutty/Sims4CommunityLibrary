"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sys
from sims4.commands import Command, CommandType, CheatOutput
from pprint import pformat
from typing import Dict, Any
from typing import Union
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class _CommonSimDataStorage:
    _instances: Dict[int, '_CommonSimDataStorage'] = {}

    def __init__(self, sim_info: SimInfo):
        self._sim_id = CommonSimUtils.get_sim_id(sim_info)
        self._sim_info = sim_info
        self._data = dict()

    def __new__(cls, sim_info: SimInfo) -> '_CommonSimDataStorage':
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        if sim_id not in cls._instances:
            cls._instances[sim_id] = super(_CommonSimDataStorage, cls).__new__(cls)
        return cls._instances[sim_id]

    @property
    def sim_info(self) -> SimInfo:
        """The SimInfo of a Sim.

        :return: The SimInfo of a Sim.
        :rtype: SimInfo
        """
        return self._sim_info

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
            self._data[key] = default
        return self._data.get(key, default)

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

    :param sim_info: The SimInfo of a Sim.
    :type sim_info: SimInfo
    """
    def __init__(self, sim_info: SimInfo):
        super().__init__(sim_info)


@Command('s4clib.print_sim_data', command_type=CommandType.Live)
def _common_command_print_sim_data(_connection=None):
    output = CheatOutput(_connection)
    sim_info = CommonSimUtils.get_active_sim_info()
    output('Sim Data for Sim: Name: \'{}\' Id: \'{}\''.format(CommonSimNameUtils.get_full_name(sim_info), CommonSimUtils.get_sim_id(sim_info)))
    sim_storage = CommonSimDataStorage(sim_info)
    for (key, value) in sim_storage._data.items():
        output(' > {}: {}'.format(pformat(key), pformat(value)))
