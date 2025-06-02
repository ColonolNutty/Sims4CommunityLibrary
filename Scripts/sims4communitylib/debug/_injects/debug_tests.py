"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from event_testing.tests import CompoundTestList, TestList
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_run_tests')
# log.enable()


# @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CompoundTestList, CompoundTestList.run_tests.__name__)
def _s4cl_compound_test_list(original, self, *_, **__) -> Any:
    try:
        return original(self, *_, **__)
    except Exception as ex:
        group_number = 1
        for test_group in self:
            log.format_with_message(f'Test group {group_number}', test_group=test_group)
            test_number = 1
            for test in test_group:
                log.format_with_message(f'Test group test {test_number}', test=test)
                test_number += 1
            group_number += 1
        log.format_with_message('Done')
        raise ex


# @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), TestList, TestList.run_tests.__name__)
def _s4cl_test_list(original, self, *_, **__) -> Any:
    try:
        return original(self, *_, **__)
    except Exception as ex:
        test_number = 1
        for test in self:
            log.format_with_message(f'Test {test_number}', test=test)
            test_number += 1
        log.format_with_message('Done')
        raise ex
