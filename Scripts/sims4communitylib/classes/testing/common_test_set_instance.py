"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyUnresolvedReferences
from _sims4_collections import frozendict
from typing import Any, Dict, Type

from event_testing.tests import TestSetInstance, CompoundTestList, \
    CompoundTestListLoadingMixin, _get_debug_loaded_tuning_callbak, _verify_tooltip_tuning, TunableTestVariant
from sims4.tuning.tunable import TunableList


class CommonTunableTestVariant(TunableTestVariant):
    """A tunable test variant."""

    def __init__(self, description='A single tunable test.', test_locked_args=None, **kwargs) -> None:
        if test_locked_args is None:
            test_locked_args = dict()
        kwargs.update((test_name, self.__class__.cached_tunable_test(test_factory, frozendict(test_locked_args))) for (test_name, test_factory) in self._get_test_variants().items())
        super().__init__(description=description, test_locked_args=test_locked_args, **kwargs)

    def _get_test_variants(self) -> Dict[str, Any]:
        return {}


class CommonTunableTestSetBase(CompoundTestListLoadingMixin):
    """A tunable test set base."""
    DEFAULT_LIST = CompoundTestList()

    def __init__(self, tunable_test_variant_class: Type[CommonTunableTestVariant] = CommonTunableTestVariant, description=None, callback=None, test_locked_args=None, **kwargs) -> None:
        self._tunable_test_variant_class = tunable_test_variant_class
        if test_locked_args is None:
            test_locked_args = dict()
        if description is None:
            description = '\n                A list of tests groups.  At least one must pass all its sub-\n                tests to pass the TestSet.\n                \n                ORs of ANDs\n                '
        super().__init__(
            description=description,
            callback=_get_debug_loaded_tuning_callbak(self._on_tunable_loaded_callback, callback),
            tunable=TunableList(
                description='\n                             A list of tests.  All of these must pass for the\n                             group to pass.\n                             ',
                tunable=self._get_tunable_test_variant_class()(
                    test_locked_args=test_locked_args
                )
            ),
            **kwargs
        )
        self.cache_key = '{}_{}'.format(self.__class__.__name__, self._template.cache_key)

    def _get_tunable_test_variant_class(self) -> Type[CommonTunableTestVariant]:
        return self._tunable_test_variant_class

    def _on_tunable_loaded_callback(self, instance_class, tunable_name, source, value) -> Any:
        for test_set in value:
            _verify_tooltip_tuning(instance_class, tunable_name, source, test_set)


class CommonTunableTestSet(CommonTunableTestSetBase, is_fragment=True):
    """A tunable set of tests."""
    def __init__(self, tunable_test_variant_class: Type[CommonTunableTestVariant] = CommonTunableTestVariant, test_locked_args=None, **kwargs) -> None:
        super().__init__(tunable_test_variant_class=tunable_test_variant_class, test_locked_args=test_locked_args, **kwargs)


class CommonTunableTestSetWithTooltip(CommonTunableTestSetBase):
    """A tunable set of tests with a tooltip."""
    DEFAULT_LIST = CompoundTestList()


class CommonTestSetInstance(TestSetInstance):
    """A tunable instance set of tests."""
    INSTANCE_TUNABLES = {'test': CommonTunableTestSetWithTooltip(CommonTunableTestVariant)}


class S4CLTunableTestVariant(CommonTunableTestVariant):
    """A tunable test variant with common tests available for use in TestSetInstance tunables."""

    def _get_test_variants(self) -> Dict[str, Any]:
        from sims4communitylib.classes.testing.common_tests import _S4CLSimHasNextCareerLevelTest, \
            _S4CLSimHasPreviousCareerLevelTest, _S4CLSimHasCareerLevelPositionTargetTest, _S4CLSimIsHumanTest, \
            _S4CLSimIsInActiveHouseholdTest
        items = {
            'sim_is_human': _S4CLSimIsHumanTest.TunableFactory,
            'sim_is_in_active_household': _S4CLSimIsInActiveHouseholdTest.TunableFactory,
            'sim_has_next_career_level': _S4CLSimHasNextCareerLevelTest.TunableFactory,
            'sim_has_previous_career_level': _S4CLSimHasPreviousCareerLevelTest.TunableFactory,
            'sim_has_career_level_position_to_sim': _S4CLSimHasCareerLevelPositionTargetTest.TunableFactory
        }
        items.update(super()._get_test_variants())
        return items


class S4CLTunableTestSet(CommonTunableTestSet):
    """A tunable test set for S4CL. This instance is used within other types of custom Tunables, such as custom LootActions."""
    def __init__(self, tunable_test_variant_class: Type[S4CLTunableTestVariant] = S4CLTunableTestVariant, test_locked_args=None, **kwargs) -> None:
        super().__init__(tunable_test_variant_class=tunable_test_variant_class, test_locked_args=test_locked_args, **kwargs)


class S4CLTestSetInstance(CommonTestSetInstance):
    """A tunable test set instance. This instance provides extra tests that can be used in TestSetInstance tunable snippets."""
    INSTANCE_TUNABLES = {'test': CommonTunableTestSetWithTooltip(S4CLTunableTestVariant)}
