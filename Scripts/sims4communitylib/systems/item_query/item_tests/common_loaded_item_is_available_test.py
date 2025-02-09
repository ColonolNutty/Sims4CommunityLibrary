"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.systems.item_query.dtos.common_loaded_item import CommonLoadedItem
from sims4communitylib.systems.item_query.item_tests.common_loaded_item_test import CommonLoadedItemTest
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo


class CommonLoadedItemIsAvailableTest(CommonLoadedItemTest[CommonLoadedItem]):
    """ Test for an item is available. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_loaded_item_is_available'

    # noinspection PyMissingOrEmptyDocstring
    def test_item(self, item: CommonLoadedItem) -> CommonTestResult:
        if not item.is_available:
            return CommonTestResult(False, reason=f'Item is not available. {self.__class__.__name__}', hide_tooltip=True)
        return CommonTestResult.TRUE
