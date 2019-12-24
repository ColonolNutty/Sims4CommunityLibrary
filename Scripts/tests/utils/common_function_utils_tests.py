"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


# noinspection PyMissingOrEmptyDocstring
@CommonTestService.test_class(ModInfo.get_identity().name)
class CommonFunctionUtilsTests:
    @staticmethod
    @CommonTestService.test(True, True, True, True)
    @CommonTestService.test(True, False, True, False)
    @CommonTestService.test(True, False, False, True)
    @CommonTestService.test(False, False, False, False)
    def run_predicates_as_one_should_work_properly(func_result_one: bool, func_result_two: bool, all_must_pass: bool, expected_result: bool):
        def _function_one(*_, **__):
            return func_result_one

        def _function_two(*_, **__):
            return func_result_two

        result = CommonFunctionUtils.run_predicates_as_one((_function_one, _function_two), all_must_pass=all_must_pass)()
        CommonAssertionUtils.are_equal(result, expected_result)

    @staticmethod
    @CommonTestService.test(True, False)
    @CommonTestService.test(False, True)
    def run_predicate_with_reversed_result_should_work_properly(func_result: bool, expected_result: bool):
        def _function(*_, **__):
            return func_result

        result = CommonFunctionUtils.run_predicate_with_reversed_result(_function)()
        CommonAssertionUtils.are_equal(result, expected_result)

    @staticmethod
    @CommonTestService.test()
    def run_with_arguments_should_work_properly():

        _additional_value = 'No'
        _additional_key_word_value = 'What'
        normal_val = 'one'
        normal_key_val = 'two'

        def _function(normal_arg: str, value_one: str, normal_key_arg: str=None, key_value: str=None):
            CommonAssertionUtils.are_equal(value_one, _additional_value)
            CommonAssertionUtils.are_equal(key_value, _additional_key_word_value)
            CommonAssertionUtils.are_equal(normal_arg, normal_val)
            CommonAssertionUtils.are_equal(normal_key_arg, normal_key_val)
            if normal_arg == normal_val and normal_key_arg == normal_key_val and value_one == _additional_value and key_value == _additional_key_word_value:
                return True

        result = CommonFunctionUtils.run_with_arguments(_function, _additional_value, key_value=_additional_key_word_value)(normal_val, normal_key_arg=normal_key_val)
        CommonAssertionUtils.is_true(result, message='Failed to send proper arguments: {}'.format(result))
