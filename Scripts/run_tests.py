"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyUnresolvedReferences
import tests.enums.enumtypes.int_enum_tests
# noinspection PyUnresolvedReferences
import tests.enums.enumtypes.float_enum_tests
# noinspection PyUnresolvedReferences
import tests.enums.enumtypes.string_enum_tests
# noinspection PyUnresolvedReferences
import tests.enums.enumtypes.general_enum_tests
# noinspection PyUnresolvedReferences
import tests.utils.common_collection_utils_tests
from sims4communitylib.testing.common_test_service import CommonTestService

CommonTestService.get().run_tests()
