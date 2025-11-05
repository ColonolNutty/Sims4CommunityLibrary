"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from relationships.relationship_track import RelationshipTrack, ObjectRelationshipTrack
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_missing_visible_test_set')


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), RelationshipTrack, RelationshipTrack._update_visiblity.__name__, handle_exceptions=False)
def _common_fix_update_visibility_with_missing_visible_test_set_relationship_track(original, self: RelationshipTrack, *_, **__):
    # Known broken relationship tracks
    relationship_track_id = getattr(self, 'guid64')
    if relationship_track_id in (
        362100,  # URT_RelSat_Main
    ):
        return original(self, *_, **__)
    # noinspection PyUnresolvedReferences
    if not self.visible_to_client and (not hasattr(self, 'visible_test_set') or not self.visible_test_set or not hasattr(self.visible_test_set, 'run_tests')):
        log.format_error_with_message('Relationship Track is missing visible_test_set', relationship_track=self, me_id=getattr(self, 'guid64', None), visible_test_set=getattr(self, 'visible_test_set', None))
        self.visible_to_client = True
        return
    return original(self, *_, **__)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), ObjectRelationshipTrack, ObjectRelationshipTrack._update_visiblity.__name__, handle_exceptions=False)
def _common_fix_update_visibility_with_missing_visible_test_set_object_relationship_track(original, self: ObjectRelationshipTrack, *_, **__):
    relationship_track_id = getattr(self, 'guid64')
    # Known broken relationship tracks
    if relationship_track_id in (
        362100,  # URT_RelSat_Main
    ):
        return original(self, *_, **__)

    # noinspection PyUnresolvedReferences
    if not self.visible_to_client and (not hasattr(self, 'visible_test_set') or not self.visible_test_set or not hasattr(self.visible_test_set, 'run_tests')):
        log.format_error_with_message('Object Relationship Track is missing visible_test_set', relationship_track=self, me_id=getattr(self, 'guid64', None), visible_test_set=getattr(self, 'visible_test_set', None))
        self.visible_to_client = True
        return
    return original(self, *_, **__)
