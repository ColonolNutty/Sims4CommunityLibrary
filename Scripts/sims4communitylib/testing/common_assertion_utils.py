"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, List, Union, Tuple, Callable

from sims4communitylib.utils.common_collection_utils import CommonCollectionUtils


class CommonAssertionUtils:
    """
        Utilities for use when asserting data within tests. However, they can be used outside tests.
    """
    @staticmethod
    def are_equal(value_one: Any, value_two: Any, message: str= '') -> bool:
        """
            Assert the two values are equal to each other.

            If the values are both collections, then the values contained within will be asserted to be equal.
            Note: The order of the values in each collection is asserted.
        :param value_one: The first value.
        :param value_two: The second value.
        :param message: A custom message to include when the assertion fails.
        :return: True if the assertion succeeds.
        :exception AssertionError when the assertion fails.
        """
        if CommonCollectionUtils.is_collection(value_one) or CommonCollectionUtils.is_collection(value_two):
            return CommonAssertionUtils.lists_are_equal(value_one, value_two, message=message)
        if value_one != value_two:
            raise AssertionError('{}: expected\n  {}\n  to be equal to\n  {}'.format(message, value_one, value_two))
        return True

    @staticmethod
    def are_similar(value_one: Any, value_two: Any, message: str='') -> bool:
        """
            Assert the two values are similar.

            If the values are both collections, then the values contained within will be asserted to be similar.
            Note: The order of the values in each collection is ignored.
        :param value_one: The first value.
        :param value_two: The second value.
        :param message: A custom message to include when the assertion fails.
        :return: True if the assertion succeeds.
        :exception AssertionError when the assertion fails.
        """
        if CommonCollectionUtils.is_collection(value_one) or CommonCollectionUtils.is_collection(value_two):
            return CommonAssertionUtils.list_contents_are_same(value_one, value_two, message=message)
        if value_one != value_two:
            raise AssertionError('{}: expected\n  {}\n  to be similar to\n  {}'.format(message, value_one, value_two))
        return True

    @staticmethod
    def lists_are_equal(list_one: Union[Tuple[Any], List[Any]], list_two: Union[Tuple[Any], List[Any]], message: str='') -> bool:
        """
            Assert the collections contain exactly the same values.
            Note: The order of the values in each collection is asserted.
        :param list_one: The first list. (Can be any collection type)
        :param list_two: The second list. (Can be any collection type)
        :param message: A custom message to include when the assertion fails.
        :return: True if the assertion succeeds.
        :exception AssertionError when the assertion fails.
        """
        if not CommonCollectionUtils.is_collection(list_one):
            raise AssertionError('{}: expected\n  {}\n  to be equal to\n  {}'.format(message, list_one, list_two))
        if not CommonCollectionUtils.is_collection(list_two):
            raise AssertionError('{}: expected\n  {}\n  to be equal to\n  {}'.format(message, list_one, list_two))
        if len(list_one) != len(list_two):
            raise AssertionError('{}: expected\n  {}\n  to be equal to\n  {}'.format(message, list_one, list_two))
        current_idx = 0
        while current_idx < len(list_one):
            item_one = list_one[current_idx]
            item_two = list_two[current_idx]
            if item_one != item_two:
                raise AssertionError('{}:  expected\n  {}\n  to be equal to\n  {}\n  Difference:\n  {}\n  should be\n  {}\n  at index {}'.format(message, list_one, list_two, item_one, item_two, current_idx))
            current_idx += 1
        return True

    @staticmethod
    def list_contents_are_same(list_one: Union[Tuple[Any], List[Any]], list_two: Union[Tuple[Any], List[Any]], message: str='') -> bool:
        """
            Assert the values contained within the specified collections are the same.
            Note: The order of the values in each collection is ignored.
        :param list_one: The first collection. (Can be any collection type)
        :param list_two: The second collection. (Can be any collection type)
        :param message: A custom message to include when the assertion fails.
        :return: True if the assertion succeeds.
        :exception AssertionError when the assertion fails.
        """
        if not CommonCollectionUtils.is_collection(list_one):
            raise AssertionError('{}: {} is not a collection'.format(message, list_one))
        if not CommonCollectionUtils.is_collection(list_two):
            raise AssertionError('{}: {} is not a collection'.format(message, list_two))
        if len(list_one) != len(list_two):
            raise AssertionError('{}: expected\n  {}\n  to be equal to\n  {}'.format(message, list_one, list_two))
        for item_one in list_one:
            if item_one not in list_two:
                raise AssertionError('{}: expected\n  {}\n  contents to be equal to\n  {}\n  {} not found in\n  {}'.format(message, list_one, list_two, item_one, list_two))
        for item_one in list_two:
            if item_one not in list_one:
                raise AssertionError('{}: expected\n  {}\n  contents to be equal to\n  {}\n  {} not found in\n  {}'.format(message, list_one, list_two, item_one, list_one))
        return True

    @staticmethod
    def is_true(value: bool, message: str='') -> bool:
        """
            Assert value is True.
        :param value: The value being asserted.
        :param message: A custom message to include when the assertion fails.
        :return: True if the value is True.
        :exception AssertionError when the assertion fails.
        """
        if value is not True:
            raise AssertionError('{}: expected True, but was {}'.format(message, value))
        return True

    @staticmethod
    def is_false(value: bool, message: str='') -> bool:
        """
            Assert value is False.
        :param value: The value being asserted.
        :param message: A custom message to include when the assertion fails.
        :return: True if the value is False.
        :exception AssertionError when the assertion fails.
        """
        if value is not False:
            raise AssertionError('{}: expected False, but was {}'.format(message, value))
        return True

    @staticmethod
    def has_length(value, expected_length: int, message: str='') -> bool:
        """
            Assert a collection has the specified length.
        :param expected_length: The length expected of the collection.
        :param value: The collection being asserted.
        :param message: A custom message to include when the assertion fails.
        :return: True if the length matches.
        :exception AssertionError when the assertion fails.
        """
        if not CommonCollectionUtils.is_collection(value):
            raise AssertionError('{}: expected collection {} to have length {}, but was not a collection'.format(message, value, expected_length))
        if len(value) != expected_length:
            raise AssertionError('{}: expected collection {} to have length {}, but was {}'.format(message, value, expected_length, len(value)))
        return True

    @staticmethod
    def contains(collection: Union[Tuple[Any], List[Any]], value: Any, message: str='') -> bool:
        """
            Assert the value is contained within the collection
        :param collection: The collection being checked.
        :param value: The value being located.
        :param message: A custom message to include when the assertion fails.
        :return: True if the value is contained within the collection.
        :exception AssertionError when the assertion fails.
        """
        if value not in collection:
            raise AssertionError('{}: expected {} to contain {}, but it did not'.format(message, collection, value))
        return True

    @staticmethod
    def throws(callback: Callable[..., Any], message: str='') -> Exception:
        """
            Assert calling a function will raise an Exception.
        :param callback: The function to invoke.
        :param message: A custom message to include when the assertion fails.
        :return: The exception that was thrown.
        """
        try:
            callback()
        except Exception as ex:
            return ex
        raise AssertionError('{}: expected function to throw an exception, but it did not.'.format(message))
