"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.int_enum import CommonEnumIntBase
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService


# noinspection PyMissingOrEmptyDocstring
class TestEnum(CommonEnumIntBase):
    TEST_VALUE_ONE = 1
    TEST_VALUE_TWO = 2
    TEST_VALUE_THREE = 3


# noinspection PyMissingOrEmptyDocstring
@CommonTestService.test_class(ModInfo.MOD_NAME)
class CommonGeneralEnumTests:
    @staticmethod
    @CommonTestService.test()
    def enum_should_have_name():
        CommonAssertionUtils.is_true(hasattr(TestEnum.TEST_VALUE_ONE, 'name'), message='Enum did not have attribute \'name\'')
        CommonAssertionUtils.are_equal(getattr(TestEnum.TEST_VALUE_ONE, 'name'), 'TEST_VALUE_ONE')

    @staticmethod
    @CommonTestService.test()
    def enum_should_have_value():
        CommonAssertionUtils.is_true(hasattr(TestEnum.TEST_VALUE_ONE, 'value'), message='Enum did not have attribute \'value\'')
        CommonAssertionUtils.are_equal(getattr(TestEnum.TEST_VALUE_ONE, 'value'), 1)

    @staticmethod
    @CommonTestService.test()
    def enum_items_result_should_be_correct():
        expected_list = [TestEnum.TEST_VALUE_ONE, TestEnum.TEST_VALUE_TWO, TestEnum.TEST_VALUE_THREE]
        result_values = []
        for enum_thing in TestEnum.items():
            result_values.append(enum_thing)
        CommonAssertionUtils.list_contents_are_same(result_values, expected_list)

    @staticmethod
    @CommonTestService.test()
    def enum_values_result_should_be_correct():
        expected_list = [1, 2, 3]
        result_values = []
        for enum_thing in TestEnum.values():
            result_values.append(enum_thing)
        CommonAssertionUtils.list_contents_are_same(result_values, expected_list)

    @staticmethod
    @CommonTestService.test()
    def enum_names_result_should_be_correct():
        expected_list = ['TEST_VALUE_ONE', 'TEST_VALUE_TWO', 'TEST_VALUE_THREE']
        result_values = []
        for enum_thing in TestEnum.names():
            result_values.append(enum_thing)
        CommonAssertionUtils.list_contents_are_same(result_values, expected_list)

    @staticmethod
    @CommonTestService.test()
    def enum_should_be_iterable():
        expected_list = ['TEST_VALUE_ONE', 'TEST_VALUE_TWO', 'TEST_VALUE_THREE']
        result_values = []
        for enum_thing in TestEnum:
            result_values.append(enum_thing)
        CommonAssertionUtils.list_contents_are_same(result_values, expected_list)

    @staticmethod
    @CommonTestService.test('TEST_VALUE_ONE', TestEnum.TEST_VALUE_ONE)
    @CommonTestService.test('TEST_VALUE_TWO', TestEnum.TEST_VALUE_TWO)
    @CommonTestService.test('TEST_VALUE_THREE', TestEnum.TEST_VALUE_THREE)
    def enum_should_be_gained_via_calling_the_enum_class_by_name(value, expected_value):
        CommonAssertionUtils.are_equal(TestEnum(value), expected_value)

    @staticmethod
    @CommonTestService.test(1, TestEnum.TEST_VALUE_ONE)
    @CommonTestService.test(2, TestEnum.TEST_VALUE_TWO)
    @CommonTestService.test(3, TestEnum.TEST_VALUE_THREE)
    def enum_should_be_gained_via_calling_the_enum_class_by_value(value, expected_value):
        CommonAssertionUtils.are_equal(TestEnum(value), expected_value)

    @staticmethod
    @CommonTestService.test(80)
    @CommonTestService.test('NOT_IN_THERE')
    def enum_call_should_throw_when_value_not_found(value):
        exception = CommonAssertionUtils.throws(lambda: TestEnum(value), value)
        CommonAssertionUtils.is_true(isinstance(exception, KeyError), message='Exception was not of type KeyError, it was type \'{}\''.format(type(exception)))
        CommonAssertionUtils.has_length(exception.args, 1)
        exception_message = exception.args[0]
        CommonAssertionUtils.are_equal(exception_message, 'Value: \'{}\' not found within class \'TestEnum\''.format(value))
