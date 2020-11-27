"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import List, Set, Tuple, Dict, Any

from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_collection_utils import CommonCollectionUtils
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService


# noinspection PyMissingOrEmptyDocstring
@CommonTestService.test_class(ModInfo.get_identity())
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

    @staticmethod
    @CommonTestService.test({'a': 1, 'b': 2, 'test_coll': (1, 2, 3)}, {'a': 5, 'c': 6, 'test_coll': (3, 4, 5, 6), 'test_other_coll': (24, 25)})
    def _should_merge_dictionaries(dictionary_one: Dict[str, Any], dictionary_two: Dict[str, Any]) -> None:
        result_dict = CommonCollectionUtils.merge_dict(dictionary_one, dictionary_two)
        CommonAssertionUtils.contains(result_dict, 'a', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'b', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'c', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'test_coll', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'test_other_coll', message=pformat(result_dict))
        a_val = result_dict['a']
        CommonAssertionUtils.are_equal(a_val, 5, message=pformat(result_dict))
        b_val = result_dict['b']
        CommonAssertionUtils.are_equal(b_val, 2, message=pformat(result_dict))
        c_val = result_dict['c']
        CommonAssertionUtils.are_equal(c_val, 6, message=pformat(result_dict))
        test_coll_val = result_dict['test_coll']
        CommonAssertionUtils.contains(test_coll_val, 1, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 2, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 3, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 4, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 5, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 6, message=pformat(result_dict))
        count_of_test_val = 0
        for val in test_coll_val:
            if val == 3:
                count_of_test_val += 1
        CommonAssertionUtils.are_equal(count_of_test_val, 2, message='The number of 3s were not correct! {}'.format(pformat(result_dict)))
        test_other_coll_val = result_dict['test_other_coll']
        CommonAssertionUtils.contains(test_other_coll_val, 24, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_other_coll_val, 25, message=pformat(result_dict))

    @staticmethod
    @CommonTestService.test({'a': 1, 'b': 2, 'test_coll': (1, 2, 3)}, {'a': 5, 'c': 6, 'test_coll': (3, 4, 5, 6), 'test_other_coll': (24, 25)})
    def _should_merge_dictionaries_allow_duplicates_false(dictionary_one: Dict[str, Any], dictionary_two: Dict[str, Any]) -> None:
        result_dict = CommonCollectionUtils.merge_dict(dictionary_one, dictionary_two, allow_duplicates_in_collections=False)
        CommonAssertionUtils.contains(result_dict, 'a', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'b', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'c', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'test_coll', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'test_other_coll', message=pformat(result_dict))
        a_val = result_dict['a']
        CommonAssertionUtils.are_equal(a_val, 5, message=pformat(result_dict))
        b_val = result_dict['b']
        CommonAssertionUtils.are_equal(b_val, 2, message=pformat(result_dict))
        c_val = result_dict['c']
        CommonAssertionUtils.are_equal(c_val, 6, message=pformat(result_dict))
        test_coll_val = result_dict['test_coll']
        CommonAssertionUtils.contains(test_coll_val, 1, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 2, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 3, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 4, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 5, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 6, message=pformat(result_dict))
        count_of_test_val = 0
        for val in test_coll_val:
            if val == 3:
                count_of_test_val += 1
        CommonAssertionUtils.are_equal(count_of_test_val, 1, message='The number of 3s were not correct! {}'.format(pformat(result_dict)))
        test_other_coll_val = result_dict['test_other_coll']
        CommonAssertionUtils.contains(test_other_coll_val, 24, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_other_coll_val, 25, message=pformat(result_dict))

    @staticmethod
    @CommonTestService.test({'a': 1, 'b': 2, 'test_coll': (1, 2, 3)}, {'a': 5, 'c': 6, 'test_coll': (3, 4, 5, 6), 'test_other_coll': (24, 25)})
    def _should_merge_dictionaries_prefer_source_false(dictionary_one: Dict[str, Any], dictionary_two: Dict[str, Any]) -> None:
        result_dict = CommonCollectionUtils.merge_dict(dictionary_one, dictionary_two, prefer_source_values=False)
        CommonAssertionUtils.contains(result_dict, 'a', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'b', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'c', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'test_coll', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'test_other_coll', message=pformat(result_dict))
        a_val = result_dict['a']
        CommonAssertionUtils.are_equal(a_val, 1, message=pformat(result_dict))
        b_val = result_dict['b']
        CommonAssertionUtils.are_equal(b_val, 2, message=pformat(result_dict))
        c_val = result_dict['c']
        CommonAssertionUtils.are_equal(c_val, 6, message=pformat(result_dict))
        test_coll_val = result_dict['test_coll']
        CommonAssertionUtils.contains(test_coll_val, 1, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 2, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 3, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 4, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 5, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 6, message=pformat(result_dict))
        count_of_test_val = 0
        for val in test_coll_val:
            if val == 3:
                count_of_test_val += 1
        CommonAssertionUtils.are_equal(count_of_test_val, 2, message='The number of 3s were not correct! {}'.format(pformat(result_dict)))
        test_other_coll_val = result_dict['test_other_coll']
        CommonAssertionUtils.contains(test_other_coll_val, 24, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_other_coll_val, 25, message=pformat(result_dict))

    @staticmethod
    @CommonTestService.test({'a': 1, 'b': 2, 'test_coll': (1, 2, 3)}, {'a': 5, 'c': 6, 'test_coll': (3, 4, 5, 6), 'test_other_coll': (24, 25)})
    def _should_merge_dictionaries_prefer_source_false_allow_duplicates_false(dictionary_one: Dict[str, Any], dictionary_two: Dict[str, Any]) -> None:
        result_dict = CommonCollectionUtils.merge_dict(dictionary_one, dictionary_two, prefer_source_values=False, allow_duplicates_in_collections=False)
        CommonAssertionUtils.contains(result_dict, 'a', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'b', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'c', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'test_coll', message=pformat(result_dict))
        CommonAssertionUtils.contains(result_dict, 'test_other_coll', message=pformat(result_dict))
        a_val = result_dict['a']
        CommonAssertionUtils.are_equal(a_val, 1, message=pformat(result_dict))
        b_val = result_dict['b']
        CommonAssertionUtils.are_equal(b_val, 2, message=pformat(result_dict))
        c_val = result_dict['c']
        CommonAssertionUtils.are_equal(c_val, 6, message=pformat(result_dict))
        test_coll_val = result_dict['test_coll']
        CommonAssertionUtils.contains(test_coll_val, 1, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 2, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 3, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 4, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 5, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_coll_val, 6, message=pformat(result_dict))
        count_of_test_val = 0
        for val in test_coll_val:
            if val == 3:
                count_of_test_val += 1
        CommonAssertionUtils.are_equal(count_of_test_val, 1, message='The number of 3s were not correct! {}'.format(pformat(result_dict)))
        test_other_coll_val = result_dict['test_other_coll']
        CommonAssertionUtils.contains(test_other_coll_val, 24, message=pformat(result_dict))
        CommonAssertionUtils.contains(test_other_coll_val, 25, message=pformat(result_dict))
