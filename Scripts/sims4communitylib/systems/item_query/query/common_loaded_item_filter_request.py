"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Tuple, Callable, List

from sims4communitylib.systems.item_query.enums.common_query_method_type import CommonQueryMethodType
from sims4communitylib.systems.item_query.query.common_loaded_item_key import CommonLoadedItemKey
from sims4communitylib.systems.item_query.query.common_loaded_item_filter import CommonLoadedItemFilter


class CommonLoadedItemFilterRequest:
    """ A request used to locate things. """
    def __init__(
        self,
        item_filters: Tuple[CommonLoadedItemFilter],
        query_type: CommonQueryMethodType = CommonQueryMethodType.ALL_INTERSECT_ANY
    ):
        self._item_filters = item_filters
        self._query_type = query_type
        self._include_all_keys = None
        self._include_any_keys = None
        self._exclude_keys = None
        self._must_match_at_least_one_key_sets = None

    @property
    def query_type(self) -> CommonQueryMethodType:
        """ The method used to query items. """
        return self._query_type

    @property
    def include_all_keys(self) -> Tuple[CommonLoadedItemKey]:
        """ Must have all these keys to match. """
        if self._include_all_keys is not None:
            return self._include_all_keys

        def _include_item_filter(_item_filter: CommonLoadedItemFilter) -> bool:
            return _item_filter.match_all and not _item_filter.exclude

        self._include_all_keys = self._get_item_keys(_include_item_filter)
        return self._include_all_keys

    @property
    def include_any_keys(self) -> Tuple[CommonLoadedItemKey]:
        """ Must have any of these keys to match. """
        if self._include_any_keys is not None:
            return self._include_any_keys

        def _include_item_filter(_item_filter: CommonLoadedItemFilter) -> bool:
            return not _item_filter.match_all and not _item_filter.exclude and not _item_filter.match_at_least_one

        self._include_any_keys = self._get_item_keys(_include_item_filter)
        return self._include_any_keys

    @property
    def exclude_keys(self) -> Tuple[CommonLoadedItemKey]:
        """ Must NOT have any of these keys to match. """
        if self._exclude_keys is not None:
            return self._exclude_keys

        def _include_item_filter(_item_filter: CommonLoadedItemFilter) -> bool:
            return _item_filter.exclude

        self._exclude_keys = self._get_item_keys(_include_item_filter)
        return self._exclude_keys

    @property
    def must_match_at_least_one_key_sets(self) -> Tuple[Tuple[CommonLoadedItemKey]]:
        """ Must match at least one of these keys. """
        if self._must_match_at_least_one_key_sets is not None:
            return self._must_match_at_least_one_key_sets

        def _get_match_at_least_one_item_filter_sets() -> Tuple[Tuple[CommonLoadedItemKey]]:
            item_keys: List[Tuple[CommonLoadedItemKey]] = list()
            for _item_filter in self._item_filters:
                if _item_filter.exclude or not _item_filter.match_at_least_one:
                    continue
                item_keys.append(_item_filter.get_keys())
            return tuple(item_keys)

        self._must_match_at_least_one_key_sets = _get_match_at_least_one_item_filter_sets()
        return self._must_match_at_least_one_key_sets

    def _get_item_keys(self, include_item_filter_callback: Callable[[CommonLoadedItemFilter], bool]) -> Tuple[CommonLoadedItemKey]:
        item_keys: List[CommonLoadedItemKey] = []
        for _item_filter in self._item_filters:
            if not include_item_filter_callback(_item_filter):
                continue
            for item_key in _item_filter.get_keys():
                item_keys.append(item_key)
        return tuple(item_keys)

    def __repr__(self) -> str:
        return '{}:\n' \
               'Include All: {}\n' \
               'Include Any: {}\n' \
               'Exclude All: {}\n' \
               'Match One Sets: {}\n' \
               'Query Type: {}'\
            .format(
                self.__class__.__name__,
                pformat(self.include_all_keys),
                pformat(self.include_any_keys),
                pformat(self.exclude_keys),
                pformat(self.must_match_at_least_one_key_sets),
                pformat(self.query_type)
            )

    def __str__(self) -> str:
        return self.__repr__()
