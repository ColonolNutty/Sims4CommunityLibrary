"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

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
@CommonTestService.test_class(ModInfo.get_identity().name)
class CommonStringEnumTests:
    @staticmethod
    @CommonTestService.test(TestEnum.TEST_VALUE_ONE, 'TestEnum.TEST_VALUE_ONE')
    @CommonTestService.test(TestEnum.TEST_VALUE_TWO, 'TestEnum.TEST_VALUE_TWO')
    @CommonTestService.test(TestEnum.TEST_VALUE_THREE, 'TestEnum.TEST_VALUE_THREE')
    def enum_should_convert_properly(enum_val, expected_value):
        CommonAssertionUtils.are_equal(expected_value, str(enum_val))
