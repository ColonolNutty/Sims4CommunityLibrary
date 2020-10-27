"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
try:
    # The purpose of this file is to fix the fact that when trying to access the "full_name" attribute on Sims, nothing is returned.
    import sims.sim_info_mixin
    import sims.sim_info_base_wrapper
    from sims.sim import Sim
    from sims.sim_info import SimInfo
    from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils


    @property
    def _sim_full_name(self: Sim) -> str:
        return CommonSimNameUtils.get_full_name(self.sim_info)

    @property
    def _sim_info_full_name(self: SimInfo) -> str:
        return CommonSimNameUtils.get_full_name(self)


    # noinspection PyPropertyAccess
    sims.sim_info_mixin.HasSimInfoBasicMixin.full_name = _sim_full_name
    # noinspection PyPropertyAccess
    sims.sim_info_base_wrapper.SimInfoBaseWrapper.full_name = _sim_info_full_name
except:
    pass
