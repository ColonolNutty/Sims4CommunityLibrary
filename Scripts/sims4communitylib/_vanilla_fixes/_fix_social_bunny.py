"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_early_load import S4CLZoneEarlyLoadEvent
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from social_media.social_media_tuning import SocialMediaTunables


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _common_fix_social_bunny_on_zone_load(event_data: S4CLZoneEarlyLoadEvent):
    if event_data.game_loaded:
        return True

    social_media_post_feed_stat = SocialMediaTunables.NPC_POSTING_COMMODITY
    if social_media_post_feed_stat is not None:
        social_media_post_feed_stat._add_if_not_in_tracker = False
        active_sim_infos = CommonHouseholdUtils.get_sim_info_of_all_sims_in_active_household_generator()
        all_social_media_sim_infos = set()
        active_sim_social_media_friends = set()
        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
            social_media_friends = sim_info.get_social_media_friends()
            if social_media_friends:
                all_social_media_sim_infos.add(sim_info)
                all_social_media_sim_infos.update(social_media_friends)
                if sim_info in active_sim_infos:
                    active_sim_social_media_friends.update(social_media_friends)
        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
            if sim_info not in all_social_media_sim_infos or sim_info not in active_sim_social_media_friends:
                tracker = sim_info.get_tracker(social_media_post_feed_stat)
                if tracker is not None:
                    tracker.remove_statistic(social_media_post_feed_stat)
            elif sim_info in active_sim_social_media_friends:
                tracker = sim_info.get_tracker(social_media_post_feed_stat)
                if tracker is not None and not tracker.has_statistic(social_media_post_feed_stat):
                    tracker.set_value(social_media_post_feed_stat, value=0, add=True)
    return True
