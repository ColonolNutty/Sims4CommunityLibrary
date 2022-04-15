"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, List, Union, Tuple, Callable, Dict

from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.utils.common_collection_utils import CommonCollectionUtils


class CommonAssertionUtils:
    """Utilities for used to assert within tests. They can be used outside tests if need be.

    """
    @staticmethod
    def are_equal(value_one: Any, value_two: Any, message: str='') -> bool:
        """are_equal(value_one, value_two, message='')

        Assert two values are equal to each other.

        If the values are both collections, then the values contained within will be asserted to be equal.

        .. note:: The order of the values in each collection is asserted.

        :param value_one: The first value.
        :type value_one: Any
        :param value_two: The second value.
        :type value_two: Any
        :param message: A custom message to include when the assertion fails. Default is Empty String.
        :type message: str, optional
        :return: True, if the assertion succeeds.
        :rtype: bool
        :exception AssertionError: when the assertion fails.
        """
        if CommonCollectionUtils.is_collection(value_one) or CommonCollectionUtils.is_collection(value_two):
            return CommonAssertionUtils.lists_are_equal(value_one, value_two, message=message)
        if value_one != value_two:
            raise AssertionError(f'{message}: expected\n  {value_one}\n  to be equal to\n  {value_two}')
        return True

    @staticmethod
    def are_similar(value_one: Any, value_two: Any, message: str='') -> bool:
        """are_similar(value_one, value_two, message='')

        Assert two values are similar.

        If the values are both collections, then the values contained within will be asserted to be similar.

        .. note:: The order of the values in each collection is ignored.

        :param value_one: The first value.
        :type value_one: Any
        :param value_two: The second value.
        :type value_two: Any
        :param message: A custom message to include when the assertion fails. Default is Empty String.
        :type message: str, optional
        :return: True, if the assertion succeeds.
        :rtype: bool
        :exception AssertionError: when the assertion fails.
        """
        if CommonCollectionUtils.is_collection(value_one) or CommonCollectionUtils.is_collection(value_two):
            return CommonAssertionUtils.list_contents_are_same(value_one, value_two, message=message)
        if value_one != value_two:
            raise AssertionError(f'{message}: expected\n  {value_one}\n  to be similar to\n  {value_two}')
        return True

    @staticmethod
    def lists_are_equal(list_one: Union[Tuple[Any], List[Any]], list_two: Union[Tuple[Any], List[Any]], message: str='') -> bool:
        """lists_are_equal(list_one, list_two, message='')

        Assert two collections contain tbe exact same values.

        .. note:: The order of the values in each collection will be asserted.

        :param list_one: The first value. (Can be any collection type)
        :type list_one: Union[Tuple[Any], List[Any]]
        :param list_two: The second value. (Can be any collection type)
        :type list_two: Union[Tuple[Any], List[Any]]
        :param message: A custom message to include when the assertion fails. Default is Empty String.
        :type message: str, optional
        :return: True, if the assertion succeeds.
        :rtype: bool
        :exception AssertionError: when the assertion fails.
        """
        if not CommonCollectionUtils.is_collection(list_one):
            raise AssertionError(f'{message}: expected\n  {list_one}\n  to be equal to\n  {list_two}')
        if not CommonCollectionUtils.is_collection(list_two):
            raise AssertionError(f'{message}: expected\n  {list_one}\n  to be equal to\n  {list_two}')
        if len(list_one) != len(list_two):
            raise AssertionError(f'{message}: expected\n  {list_one}\n  to be equal to\n  {list_two}')
        if isinstance(list_one, set) or isinstance(list_two, set):
            return list_one == list_two
        current_idx = 0
        while current_idx < len(list_one):
            item_one = list_one[current_idx]
            item_two = list_two[current_idx]
            if item_one != item_two:
                raise AssertionError(f'{message}:  expected\n  {list_one}\n  to be equal to\n  {list_two}\n  Difference:\n  {item_one}\n  should be\n  {item_two}\n  at index {current_idx}')
            current_idx += 1
        return True

    @staticmethod
    def list_contents_are_same(list_one: Union[Tuple[Any], List[Any]], list_two: Union[Tuple[Any], List[Any]], message: str='') -> bool:
        """list_contents_are_same(list_one, list_two, message='')

        Assert the values contained within two collections are the same.

        .. note:: The order of the values in each collection is ignored.

        :param list_one: The first value. (Can be any collection type)
        :type list_one: Union[Tuple[Any], List[Any]]
        :param list_two: The second value. (Can be any collection type)
        :type list_two: Union[Tuple[Any], List[Any]]
        :param message: A custom message to include when the assertion fails. Default is Empty String.
        :type message: str, optional
        :return: True, if the assertion succeeds.
        :rtype: bool
        :exception AssertionError: when the assertion fails.
        """
        if not CommonCollectionUtils.is_collection(list_one):
            raise AssertionError(f'{message}: {list_one} is not a collection')
        if not CommonCollectionUtils.is_collection(list_two):
            raise AssertionError(f'{message}: {list_two} is not a collection')
        if len(list_one) != len(list_two):
            raise AssertionError(f'{message}: expected\n  {list_one}\n  to be equal to\n  {list_two}')
        for item_one in list_one:
            if item_one not in list_two:
                raise AssertionError(f'{message}: expected\n  {list_one}\n  contents to be equal to\n  {list_two}\n  {item_one} not found in\n  {list_two}')
        for item_one in list_two:
            if item_one not in list_one:
                raise AssertionError(f'{message}: expected\n  {list_one}\n  contents to be equal to\n  {list_two}\n  {item_one} not found in\n  {list_one}')
        return True

    @staticmethod
    def is_true(value: Union[bool, CommonTestResult, CommonExecutionResult], message: str='') -> bool:
        """is_true(value, message='')

        Assert a value is True.

        :param value: The value being asserted.
        :type value: Union[bool, CommonTestResult, CommonExecutionResult]
        :param message: A custom message to include when the assertion fails. Default is Empty String.
        :type message: str, optional
        :return: True if the value is True.
        :rtype: bool
        :exception AssertionError: when the assertion fails.
        """
        if isinstance(value, CommonTestResult) or isinstance(value, CommonExecutionResult):
            if value.result is not True:
                raise AssertionError(f'{message} {value.reason}: expected True, but was {value.result}')
            return True
        if value is not True:
            raise AssertionError(f'{message}: expected True, but was {value}')
        return True

    @staticmethod
    def is_false(value: Union[bool, CommonTestResult, CommonExecutionResult], message: str='') -> bool:
        """is_false(value, message='')

        Assert value is False.

        :param value: The value being asserted.
        :type value: Union[bool, CommonTestResult, CommonExecutionResult]
        :param message: A custom message to include when the assertion fails.
        :type message: str, optional
        :return: True if the value is False.
        :rtype: bool
        :exception AssertionError: when the assertion fails.
        """
        if isinstance(value, CommonTestResult) or isinstance(value, CommonExecutionResult):
            if value.result is not False:
                raise AssertionError(f'{message} {value.reason}: expected False, but was {value.result}')
            return True
        if value is not False:
            raise AssertionError(f'{message}: expected False, but was {value}')
        return True

    @staticmethod
    def has_length(value: Union[Tuple[Any], List[Any]], expected_length: int, message: str='') -> bool:
        """has_length(value, expected_length, message='')

        Assert a collection has the specified length.

        :param value: The collection being asserted. (Any collection that works with `len()` can be used)
        :type value: Union[Tuple[Any], List[Any]]
        :param expected_length: The length expected of the collection.
        :type expected_length: int
        :param message: A custom message to include when the assertion fails. Default is Empty String.
        :type message: str, optional
        :return: True if the length matches.
        :rtype: bool
        :exception AssertionError: when the assertion fails.
        """
        if not CommonCollectionUtils.is_collection(value):
            raise AssertionError(f'{message}: expected collection {value} to have length {expected_length}, but was not a collection')
        if len(value) != expected_length:
            raise AssertionError(f'{message}: expected collection {value} to have length {expected_length}, but was {len(value)}')
        return True

    @staticmethod
    def contains(collection: Union[Tuple[Any], List[Any], Dict[Any, Any]], value: Any, message: str='') -> bool:
        """contains(collection, value, message='')

        Assert a value is contained within a collection

        :param collection: The collection being checked (Any collection that works with `len()` can be used)
        :type collection: Union[Tuple[Any], List[Any], Dict[Any, Any]]
        :param value: The value being located.
        :type value: Any
        :param message: A custom message to include when the assertion fails. Default is Empty String.
        :type message: str, optional
        :return: True, if the value is contained within the collection. False, if it is not.
        :rtype: bool
        :exception AssertionError: when the assertion fails.
        """
        if value not in collection:
            raise AssertionError(f'{message}: expected {collection} to contain {value}, but it did not.')
        return True

    @staticmethod
    def not_contains(collection: Union[Tuple[Any], List[Any], Dict[Any, Any]], value: Any, message: str='') -> bool:
        """not_contains(collection, value, message='')

        Assert a value is NOT contained within a collection

        :param collection: The collection being checked (Any collection that works with `len()` can be used)
        :type collection: Union[Tuple[Any], List[Any], Dict[Any, Any]]
        :param value: The value being located.
        :type value: Any
        :param message: A custom message to include when the assertion fails. Default is Empty String.
        :type message: str, optional
        :return: True, if the value is NOT contained within the collection. False, if it is.
        :rtype: bool
        :exception AssertionError: when the assertion fails.
        """
        if value in collection:
            raise AssertionError(f'{message}: expected {collection} to not contain {value}, but it did.')
        return True

    @staticmethod
    def throws(callback: Callable[..., Any], message: str='') -> Exception:
        """throws(callback, message='')

        Assert calling a function will raise an Exception.

        :param callback: The function to invoke.
        :type callback: Callable[..., Any]
        :param message: A custom message to include when the assertion fails. Default is Empty String.
        :type message: str, optional
        :return: The exception that was thrown.
        :rtype: Exception
        :exception AssertionError: when the assertion fails.
        """
        try:
            callback()
        except Exception as ex:
            return ex
        raise AssertionError(f'{message}: expected function to throw an exception, but it did not.')

    @staticmethod
    def not_throws(callback: Callable[..., Any], message: str='') -> bool:
        """not_throws(callback, message='')

        Assert calling a function will not raise an Exception.

        :param callback: The function to invoke.
        :type callback: Callable[..., Any]
        :param message: A custom message to include when the assertion fails. Default is Empty String.
        :type message: str, optional
        :return: True, if the assertion was successful.
        :rtype: bool
        :exception AssertionError: when the assertion fails.
        """
        try:
            callback()
        except Exception as ex:
            raise AssertionError(f'{message}: expected function to not throw an exception, but it did. Exception: {ex}')
        return True
