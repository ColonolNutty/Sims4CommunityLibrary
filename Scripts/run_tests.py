"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyUnresolvedReferences
import s4cl_tests.enums.enumtypes.int_enum_tests
# noinspection PyUnresolvedReferences
import s4cl_tests.enums.enumtypes.float_enum_tests
# noinspection PyUnresolvedReferences
import s4cl_tests.enums.enumtypes.string_enum_tests
# noinspection PyUnresolvedReferences
import s4cl_tests.enums.enumtypes.general_enum_tests
# noinspection PyUnresolvedReferences
import s4cl_tests.utils.common_collection_utils_tests
from sims4communitylib.testing.common_test_service import CommonTestService

CommonTestService.get().run_tests()
