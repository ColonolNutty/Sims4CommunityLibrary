"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Tuple, Iterator, Union, Generic, TypeVar

from sims4communitylib.systems.item_query.item_tests.common_loaded_item_test import CommonLoadedItemTest
from sims4communitylib.systems.item_query.item_tests.common_loaded_item_is_available_test import \
    CommonLoadedItemIsAvailableTest
from sims4communitylib.systems.item_query.query.common_loaded_item_filter import CommonLoadedItemFilter

from sims4communitylib.systems.item_query.enums.common_query_method_type import CommonQueryMethodType
from sims4communitylib.systems.item_query.dtos.common_loaded_item import CommonLoadedItem
from sims4communitylib.systems.item_query.common_loaded_item_query_registry import CommonLoadedItemQueryRegistry
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.systems.item_query.query.common_loaded_item_filter_request import CommonLoadedItemFilterRequest

CommonLoadedItemType = TypeVar('CommonLoadedItemType', bound=CommonLoadedItem)


class CommonLoadedItemQueryUtils(HasLog, Generic[CommonLoadedItemType]):
    """ Query for items using various filter configurations. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        raise NotImplementedError()

    @property
    def _query_registry(self) -> CommonLoadedItemQueryRegistry:
        raise NotImplementedError()

    def get_all(self) -> Tuple[CommonLoadedItemType]:
        """ Get all items. """
        return self._query_registry.get_all()

    def locate_by_identifier(self, identifier: str) -> Union[CommonLoadedItemType, None]:
        """ Locate a CAS Part by its identifier. """
        return self._query_registry._registry.locate_by_identifier(identifier)

    def create_filter_request(
        self,
        item_filters: Tuple[CommonLoadedItemFilter],
        item_tests: Iterator[CommonLoadedItemTest],
        query_type: CommonQueryMethodType = CommonQueryMethodType.ALL_INTERSECT_ANY
    ) -> CommonLoadedItemFilterRequest:
        """ Create a filter request for items. """
        return CommonLoadedItemFilterRequest(item_filters, item_tests, query_type=query_type)

    def has_for_filters(
        self,
        item_filters: Tuple[CommonLoadedItemFilter],
        item_tests: Iterator[CommonLoadedItemTest],
        query_type: CommonQueryMethodType = CommonQueryMethodType.ALL_INTERSECT_ANY
    ) -> bool:
        """Determine if any items are available that match filters."""
        filter_request = self.create_filter_request(item_filters, item_tests, query_type=query_type)
        return self._query_registry.has_items((filter_request, ))

    def get_for_filters_gen(
        self,
        item_filters: Tuple[CommonLoadedItemFilter],
        item_tests: Iterator[CommonLoadedItemTest],
        query_type: CommonQueryMethodType = CommonQueryMethodType.ALL_INTERSECT_ANY
    ) -> Iterator[CommonLoadedItemType]:
        """ Get all items matching filters. """
        self.log.format_with_message(
            'Getting items that match filters',
            item_filters=item_filters,
            item_tests=item_tests,
            query_type=query_type
        )
        filter_request = self.create_filter_request(item_filters, item_tests, query_type=query_type)
        query_result = self._query_registry.get_items_gen((filter_request,))
        had_items = False
        for item in query_result:
            had_items = True
            yield item
        if not had_items:
            self.log.debug('No items found matching filters.')

    def get_random_for_filters(
        self,
        item_filters: Tuple[CommonLoadedItemFilter],
        item_tests: Tuple[CommonLoadedItemTest],
        query_type: CommonQueryMethodType = CommonQueryMethodType.ALL_INTERSECT_ANY
    ) -> Union[CommonLoadedItemType, None]:
        """Get a random item that matches filters."""
        if not self.has_for_filters(
            item_filters,
            item_tests,
            query_type=query_type
        ):
            return None

        items = tuple(self.get_for_filters_gen(
            item_filters,
            item_tests,
            query_type=query_type
        ))
        if not items:
            return None
        return random.choice(items)

    def has_available_for_filters(
        self,
        item_filters: Tuple[CommonLoadedItemFilter],
        item_tests: Iterator[CommonLoadedItemTest],
        query_type: CommonQueryMethodType = CommonQueryMethodType.ALL_INTERSECT_ANY
    ) -> bool:
        """Determine if any items are available that match filters and are marked as being available."""
        item_tests: Tuple[CommonLoadedItemTest, ...] = (
            CommonLoadedItemIsAvailableTest(),
            *item_tests
        )
        return self.has_for_filters(
            item_filters,
            item_tests,
            query_type=query_type
        )

    def get_available_for_filters_gen(
        self,
        item_filters: Tuple[CommonLoadedItemFilter],
        item_tests: Tuple[CommonLoadedItemTest],
        query_type: CommonQueryMethodType = CommonQueryMethodType.ALL_INTERSECT_ANY
    ) -> Iterator[CommonLoadedItemType]:
        """Get all items matching filters that are marked as being available."""
        item_tests: Tuple[CommonLoadedItemTest, ...] = (
            CommonLoadedItemIsAvailableTest(),
            *item_tests
        )
        yield from self.get_for_filters_gen(
            item_filters,
            item_tests,
            query_type=query_type
        )

    def get_random_from_available_for_filters(
        self,
        item_filters: Tuple[CommonLoadedItemFilter],
        item_tests: Tuple[CommonLoadedItemTest],
        query_type: CommonQueryMethodType = CommonQueryMethodType.ALL_INTERSECT_ANY
    ) -> Union[CommonLoadedItemType, None]:
        """Get a random item that matches filters and is marked as being available."""
        item_tests: Tuple[CommonLoadedItemTest, ...] = (
            CommonLoadedItemIsAvailableTest(),
            *item_tests
        )
        return self.get_random_for_filters(item_filters, item_tests, query_type=query_type)
