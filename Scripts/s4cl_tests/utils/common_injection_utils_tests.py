"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from sims4communitylib.modinfo import ModInfo
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


# noinspection PyMissingOrEmptyDocstring
class FakeClassToBeOverridden:
    # noinspection PyMissingOrEmptyDocstring
    @property
    def the_property(self) -> bool:
        return False

    # noinspection PyMissingOrEmptyDocstring
    @staticmethod
    def the_static_method() -> bool:
        return False

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def the_class_method(cls) -> bool:
        return False

    # noinspection PyMissingOrEmptyDocstring
    def the_instance_method(self) -> bool:
        return False


# noinspection PyMissingOrEmptyDocstring
@CommonTestService.test_class(ModInfo.get_identity())
class CommonInjectionUtilsTests:
    @staticmethod
    @CommonTestService.test()
    def _should_override_property() -> None:
        @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), FakeClassToBeOverridden, 'the_property')
        def _overridden_property(*_: Any, **__: Any) -> bool:
            return True

        CommonAssertionUtils.is_true(FakeClassToBeOverridden().the_property)

    @staticmethod
    @CommonTestService.test()
    def _should_override_static_method() -> None:
        @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), FakeClassToBeOverridden, FakeClassToBeOverridden.the_static_method.__name__)
        def _overridden_static_method(*_: Any, **__: Any) -> bool:
            return True

        CommonAssertionUtils.is_true(FakeClassToBeOverridden.the_static_method())

    @staticmethod
    @CommonTestService.test()
    def _should_override_class_method() -> None:
        @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), FakeClassToBeOverridden, FakeClassToBeOverridden.the_class_method.__name__)
        def _overridden_class_method(*_: Any, **__: Any) -> bool:
            return True

        CommonAssertionUtils.is_true(FakeClassToBeOverridden.the_class_method())

    @staticmethod
    @CommonTestService.test()
    def _should_override_instance_method() -> None:
        @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), FakeClassToBeOverridden, FakeClassToBeOverridden.the_instance_method.__name__)
        def _overridden_instance_method(*_: Any, **__: Any) -> bool:
            return True

        CommonAssertionUtils.is_true(FakeClassToBeOverridden().the_instance_method())
