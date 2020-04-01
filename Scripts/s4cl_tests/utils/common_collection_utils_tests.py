"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import List, Set, Tuple

from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_collection_utils import CommonCollectionUtils
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService


# noinspection PyMissingOrEmptyDocstring
@CommonTestService.test_class(ModInfo.get_identity().name)
class CommonCollectionUtilsTests:
    @staticmethod
    @CommonTestService.test((1, 2, 3), (2,))
    @CommonTestService.test((1, 2, 3), (4,), (2,))
    @CommonTestService.test((1, 2, 3), (4, 7), (5, 6), (3,))
    def _should_intersect_true(list_one, *list_items) -> None:
        result = CommonCollectionUtils.intersects(list_one, *list_items)
        CommonAssertionUtils.is_true(result)

    @staticmethod
    @CommonTestService.test((1, 2, 3), (4, 8))
    @CommonTestService.test((1, 2, 3), (5, 9,), (10, 4))
    def _should_intersect_false(list_one: List[int], *list_items: int) -> None:
        result = CommonCollectionUtils.intersects(list_one, *list_items)
        CommonAssertionUtils.is_false(result)

    @staticmethod
    @CommonTestService.test([1, 2, 3], 2, {(1, 2), (1, 3), (2, 3)})
    def _should_combine(items: List[int], combination_length: int, expected_outcome: Set[Tuple[int]]) -> None:
        result = CommonCollectionUtils.create_possible_combinations(items, combination_length)
        CommonAssertionUtils.are_equal(result, expected_outcome)
