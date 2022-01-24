"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.classes.filters.common_match_object_filter import CommonMatchObjectFilterBase
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class CommonMatchAllSimsObjectFilter(CommonMatchObjectFilterBase):
    """A filter that will match on all Sims."""
    # noinspection PyMissingOrEmptyDocstring
    def matches(self, obj) -> bool:
        return CommonTypeUtils.is_sim_or_sim_info(obj)
