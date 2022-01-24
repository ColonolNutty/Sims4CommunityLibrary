"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from interactions.utils.object_definition_or_tags import TunableObjectFilter
from objects.script_object import ScriptObject
from sims4communitylib.enums.common_object_filter_type import CommonObjectFilterType


class CommonMatchObjectFilterBase(TunableObjectFilter):
    """A filter that will match on objects."""

    def get_filter_type(self) -> CommonObjectFilterType:
        """Indicates the type of filter."""
        return CommonObjectFilterType.CUSTOM

    def _intersect_dissimilar(self, other) -> TunableObjectFilter:
        return self

    def _intersect_similar(self, other) -> TunableObjectFilter:
        return self

    def matches(self, obj: ScriptObject) -> bool:
        """matches(obj)

        Whether or not the specified object matches this filter.

        :param obj: An instance of an object.
        :type obj: ScriptObject
        :return: True, if the object matches the filter. False, if not.
        :rtype: bool
        """
        raise NotImplementedError()
