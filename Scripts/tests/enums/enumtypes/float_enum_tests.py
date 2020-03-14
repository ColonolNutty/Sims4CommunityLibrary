"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.float_enum import CommonEnumFloatBase
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService


# noinspection PyMissingOrEmptyDocstring
class TestEnum(CommonEnumFloatBase):
    TEST_VALUE_ONE = 1.0
    TEST_VALUE_TWO = 2.0
    TEST_VALUE_THREE = 3.0


# noinspection PyMissingOrEmptyDocstring
@CommonTestService.test_class(ModInfo.get_identity().name)
class CommonFloatEnumTests:
    @staticmethod
    @CommonTestService.test(TestEnum.TEST_VALUE_ONE, 1.0)
    @CommonTestService.test(TestEnum.TEST_VALUE_TWO, 2.0)
    @CommonTestService.test(TestEnum.TEST_VALUE_THREE, 3.0)
    def _enum_should_convert_properly(enum_val, expected_value) -> None:
        CommonAssertionUtils.are_equal(float(enum_val), expected_value)
