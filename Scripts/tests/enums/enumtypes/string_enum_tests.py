"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.string_enum import CommonEnumStringBase
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService


# noinspection PyMissingOrEmptyDocstring
class TestEnum(CommonEnumStringBase):
    TEST_VALUE_ONE = 'One'
    TEST_VALUE_TWO = 'Two'
    TEST_VALUE_THREE = 'Three'


# noinspection PyMissingOrEmptyDocstring
@CommonTestService.test_class(ModInfo.MOD_NAME)
class CommonStringEnumTests:
    @staticmethod
    @CommonTestService.test(TestEnum.TEST_VALUE_ONE, 1.0)
    @CommonTestService.test(TestEnum.TEST_VALUE_TWO, 2.0)
    @CommonTestService.test(TestEnum.TEST_VALUE_THREE, 3.0)
    def enum_should_convert_properly(enum_val, expected_value):
        CommonAssertionUtils.are_equal(str(enum_val), expected_value)
