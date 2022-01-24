"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.proxy import ProxyObject
from objects.script_object import ScriptObject
from sims4communitylib.classes.filters.common_match_object_filter import CommonMatchObjectFilterBase
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class CommonMatchAllNonSimsObjectFilter(CommonMatchObjectFilterBase):
    """An object filter that will match on all non-Sim objects."""

    # noinspection PyMissingOrEmptyDocstring
    def matches(self, obj: ScriptObject) -> bool:
        return not CommonTypeUtils.is_sim_or_sim_info(obj) and CommonTypeUtils.is_game_object(obj) and not isinstance(obj, ProxyObject)
