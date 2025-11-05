"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, TYPE_CHECKING
from buffs.buff import Buff
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from interactions.utils.loot import Interaction, Loot, LootAction


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
        raise NotImplementedError(f'Missing \'{cls.get_mod_identity.__name__}\'.')

    @property
    def sim(self) -> Union[Sim, None]:
        """Retrieve the Sim that owns the Buff.

        :return: An instance of the Sim that owns the Buff
        :rtype: Sim
        """
        return CommonSimUtils.get_sim_instance(self._owner)

    @property
    def sim_info(self) -> Union[SimInfo, None]:
        """Retrieve the SimInfo that owns the Buff.

        :return: The info of the Sim that owns the Buff.
        :rtype: SimInfo
        """
        return CommonSimUtils.get_sim_info(self._owner)

    # noinspection PyMissingOrEmptyDocstring
    def on_add(self, *_, from_load: bool = False, apply_buff_loot: bool = True, buff_source: Union['Interaction', 'Loot', 'LootAction'] = None, **__):
        """on_add(from_load=False, apply_buff_loot=True, buff_source=None)

        A function that occurs upon a Buff being added to a Sim.

        :param from_load: True, if the Buff is being added from a load. Default is False.
        :type from_load: bool, optional
        :param apply_buff_loot: If True, Loot will be applied when the Buff is added. Default is True.
        :type apply_buff_loot: bool, optional
        :param buff_source: The source of the buff. Default is No Source.
        :type buff_source: Union[Interaction, Loot, LootAction], optional
        """
        super().on_add(*_, from_load=from_load, apply_buff_loot=apply_buff_loot, buff_source=buff_source, **__)
        try:
            self.on_added(self.sim, *_, from_load=from_load, apply_buff_loot=apply_buff_loot, buff_source=buff_source)
        except Exception as ex:
            self.log.error(f'Error occurred while running buff \'{self.__class__.__name__}\' on_added.', exception=ex)

    def on_remove(self, *_, apply_loot_on_remove: bool = True, **__):
        """on_remove(apply_loot_on_remove=True)

        A function that occurs upon a Buff being removed from a Sim.

        :param apply_loot_on_remove: If True, Loot will be applied after the Buff is removed. If False, it won't. Default is True.
        :type apply_loot_on_remove: bool, optional
        """
        super().on_remove(*_, apply_loot_on_remove=apply_loot_on_remove, **__)
        try:
            self.on_removed(self.sim, *_, apply_loot_on_remove=apply_loot_on_remove, **__)
        except Exception as ex:
            self.log.error(f'Error occurred while running buff \'{self.__class__.__name__}\' on_removed.', exception=ex)

    # The following functions are hooks into various parts of a buff, override them in your own buff to provide custom functionality.

    def on_added(self, owner: Sim, *_, from_load: bool = False, apply_buff_loot: bool = True, buff_source: Union['Interaction', 'Loot', 'LootAction'] = None, **__):
        """on_added(owner, *_, from_load=False, apply_buff_loot=True, buff_source=None, **__)

        A hook that occurs upon the Buff being added to the Sim.

        :param owner: The Sim that owns the Buff.
        :type owner: Sim
        :param from_load: True, if the Buff was added from a load. Default is False.
        :type from_load: bool, optional
        :param apply_buff_loot: If True, Loot was applied when the Buff was added. Default is True.
        :type apply_buff_loot: bool, optional
        :param buff_source: The source of the buff. Default is No Source.
        :type buff_source: Union[Interaction, Loot, LootAction], optional
        """
        pass

    def on_removed(self, owner: Sim, *_, apply_loot_on_remove: bool = True, **__):
        """on_removed(owner, *_, apply_loot_on_remove=True, **__)

        A hook that occurs upon the Buff being removed from the Sim.

        :param owner: The Sim that owns the Buff.
        :type owner: Sim
        :param apply_loot_on_remove: If True, Loot will be applied after the Buff is removed. If False, it won't. Default is True.
        :type apply_loot_on_remove: bool, optional
        """
        pass
