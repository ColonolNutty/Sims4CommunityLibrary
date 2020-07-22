"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from typing import Callable, Iterator, Union
from sims.sim_info import SimInfo
from sims4communitylib.enums.situations_enum import CommonSituationId
from sims4communitylib.utils.resources.common_situation_utils import CommonSituationUtils
from situations.situation import Situation
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimSituationUtils:
    """Utilities for manipulating the Situations of Sims.

    """
    @staticmethod
    def has_situations(sim_info: SimInfo, situation_ids: Iterator[Union[int, CommonSituationId]]) -> bool:
        """has_situations(sim_info, situation_ids)

        Determine if a Sim is involved in any of the specified Situations.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param situation_ids: The decimal identifiers of Situations.
        :type situation_ids: Iterator[Union[int, CommonSituationId]]
        :return: True, if the Sim has any of the specified buffs. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        for situation in CommonSimSituationUtils.get_situations(sim_info):
            situation_id = CommonSituationUtils.get_situation_id(situation)
            if situation_id in situation_ids:
                return True
        return False

    @staticmethod
    def get_situations(sim_info: SimInfo, include_situation_callback: Callable[[Situation], bool]=None) -> Iterator[Situation]:
        """get_situations(sim_info, include_situation_callback=None)

        Retrieve all Situations that a Sim is currently involved in.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param include_situation_callback: If the result of this callback is True, the Situation will be included in the results. If set to None, All situations will be included. Default is None.
        :type include_situation_callback: Callable[[Situation], bool], optional
        :return: An iterable of Situations that pass the include callback filter.
        :rtype: Iterator[Situation]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        situations = tuple(services.get_zone_situation_manager().get_situations_sim_is_in(sim))
        if sim is None or not situations:
            return tuple()
        for situation in situations:
            if include_situation_callback is not None and not include_situation_callback(situation):
                continue
            yield situation
