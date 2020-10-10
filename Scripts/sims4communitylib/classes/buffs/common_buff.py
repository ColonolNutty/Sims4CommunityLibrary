"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union
from buffs.buff import Buff
from sims.sim import Sim
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonBuff(Buff, HasClassLog):
    """CommonBuff(...)

    An inheritable class that provides a way to create Custom Buffs.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_buff'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError('Missing \'{}\'.'.format(cls.get_mod_identity.__name__))

    @property
    def sim(self) -> Union[Sim, None]:
        """Retrieve the Sim that owns the Buff.

        :return: An instance of the Sim that owns the Buff
        :rtype: Sim
        """
        return CommonSimUtils.get_sim_instance(self._owner)

    # noinspection PyMissingOrEmptyDocstring
    def on_add(self, from_load: bool=False, apply_buff_loot: bool=True):
        """on_add(from_load=False, apply_buff_loot=True)

        A function that occurs upon a Buff being added to a Sim.

        :param from_load: True, if the Buff is being added from a load. Default is False.
        :type from_load: bool, optional
        :param apply_buff_loot: If True, Loot will be applied when the Buff is added. Default is True.
        :type apply_buff_loot: bool, optional
        """
        super().on_add(from_load=from_load, apply_buff_loot=apply_buff_loot)
        try:
            self.on_added(self.sim, from_load=from_load, apply_buff_loot=apply_buff_loot)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while running buff \'{}\' on_added.'.format(self.__class__.__name__), exception=ex)

    def on_remove(self, apply_loot_on_remove: bool=True):
        """on_remove(apply_loot_on_remove=True)

        A function that occurs upon a Buff being removed from a Sim.

        :param apply_loot_on_remove: If True, Loot will be applied after the Buff is removed. If False, it won't. Default is True.
        :type apply_loot_on_remove: bool, optional
        """
        super().on_remove(apply_loot_on_remove=apply_loot_on_remove)
        try:
            self.on_removed(self.sim, apply_loot_on_remove=apply_loot_on_remove)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while running buff \'{}\' on_removed.'.format(self.__class__.__name__), exception=ex)

    # The following functions are hooks into various parts of a buff, override them in your own buff to provide custom functionality.

    def on_added(self, owner: Sim, from_load: bool=False, apply_buff_loot: bool=True):
        """on_added(owner, from_load=False, apply_buff_loot=True)

        A hook that occurs upon the Buff being added to the Sim.

        :param owner: The Sim that owns the Buff.
        :type owner: Sim
        :param from_load: True, if the Buff was added from a load. Default is False.
        :type from_load: bool, optional
        :param apply_buff_loot: If True, Loot was applied when the Buff was added. Default is True.
        :type apply_buff_loot: bool, optional
        """
        pass

    def on_removed(self, owner: Sim, apply_loot_on_remove: bool=True):
        """on_removed(owner, apply_loot_on_remove=True)

        A hook that occurs upon the Buff being removed from the Sim.

        :param owner: The Sim that owns the Buff.
        :type owner: Sim
        :param apply_loot_on_remove: If True, Loot will be applied after the Buff is removed. If False, it won't. Default is True.
        :type apply_loot_on_remove: bool, optional
        """
        pass
