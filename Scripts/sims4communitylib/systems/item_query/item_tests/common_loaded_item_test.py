"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import TypeVar, Generic

from sims4communitylib.systems.item_query.dtos.common_loaded_item import CommonLoadedItem
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


CommonLoadedItemType = TypeVar('CommonLoadedItemType', bound=CommonLoadedItem)


class CommonLoadedItemTest(HasClassLog, Generic[CommonLoadedItemType]):
    """ A test that is run to test a loaded item. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    def test_item(self, item: CommonLoadedItemType) -> CommonTestResult:
        """Test an item for a match."""
        raise NotImplementedError()
