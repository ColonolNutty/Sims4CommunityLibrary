"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union
from routing.walkstyle.walkstyle_tuning import Walkstyle
from sims.sim_info import SimInfo
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimWalkstyleUtils(_HasS4CLClassLog):
    """Utilities for manipulating the Walkstyle of Sims.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_sim_walkstyle_utils'

    @classmethod
    def get_default_walkstyle(cls, sim_info: SimInfo) -> Union[Walkstyle, None]:
        """get_default_walkstyle(sim_info)

        Retrieve the default walkstyle of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The default walkstyle of a Sim or None if the Sim is not available or has no default walk style.
        :rtype: Union[Walkstyle, None]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        return sim.routing_component.get_default_walkstyle()

    @classmethod
    def get_current_walkstyle(cls, sim_info: SimInfo) -> Union[Walkstyle, None]:
        """get_current_walkstyle(sim_info)

        Retrieve the current walkstyle of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The current walkstyle of the Sim or None when not found.
        :rtype: Union[Walkstyle, None]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        routing_component = sim.routing_component
        if routing_component is None:
            return None
        path = routing_component.current_path
        if path:
            return routing_component.get_walkstyle_for_path(routing_component.current_path)

        return cls.get_default_walkstyle(sim_info)
