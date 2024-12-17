"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

import services
from sims4.resources import Types
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from statistics.commodity_tracker import CommodityTracker

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_commodity_tracker_error_catcher')


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CommodityTracker, CommodityTracker.save.__name__, handle_exceptions=True)
def _common_fix_missing_name_hash(original, self: CommodityTracker, *_, **__) -> Any:
    try:
        return original(self, *_, **__)
    except Exception as ex:
        commodities = []
        skills = []
        ranked_statistics = []
        for stat in tuple(self._statistics_values_gen()):
            if not stat.persisted:
                pass
            else:
                try:
                    stat.save_statistic(commodities, skills, ranked_statistics, self)
                except Exception as e:
                    log.format_error_with_message('Failed to save statistic', statistic=stat, sim=self.owner, exception=e)
                    continue
        if self._delayed_active_lod_statistics is not None:
            statistic_manager = services.get_instance_manager(Types.STATISTIC)
            for commodity_proto in self._delayed_active_lod_statistics:
                # noinspection PyBroadException
                try:
                    from protocolbuffers.SimObjectAttributes_pb2 import Commodity
                    commodity_class = statistic_manager.get(commodity_proto.name_hash)
                    commodity_class.save_for_delayed_active_lod(commodity_proto, commodities, skills, ranked_statistics)
                except:
                    try:
                        commodity_id = commodity_proto[0]
                        commodity_class = statistic_manager.get(commodity_id)
                        sim_info = CommonSimUtils.get_sim_info(self.owner)
                        commodity_tracker: CommodityTracker = sim_info.get_tracker(commodity_class)
                        commodity = commodity_tracker.get_statistic(commodity_class, add=False)
                        proto = commodity.get_save_message(commodity_tracker)
                        commodity_class.save_for_delayed_active_lod(proto, commodities, skills, ranked_statistics)
                    except Exception as ex:
                        log.format_error_with_message('Failed to save commodity', commodity_proto=commodity_proto, sim=self.owner, exception=ex)
        return commodities, skills, ranked_statistics
