"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from event_testing.resolver import RESOLVER_PARTICIPANT, Resolver
from typing import Any, Dict, Tuple

from event_testing.test_base import BaseTest
from interactions import ParticipantType
from sims.sim_info import SimInfo
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit, TunableEnumEntry, Tunable
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest, HasClassLog):
    """A tunable test"""
    FACTORY_TUNABLES = {
        'invert': Tunable(
            description='\n            If checked, this test will return the opposite of what it\'s tuned to\n            return. For instance, if "invert" is set to True and the test "fails",\n            the test will return true instead.\n            ',
            tunable_type=bool,
            default=False
        )
    }

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    __slots__ = {'invert'}

    def get_expected_args(self) -> Dict[str, Any]:
        """The values expected to be passed to the test."""
        return {}

    def __call__(self, *args, tooltip=None, **kwargs) -> CommonTestResult:
        try:
            return self._run_test(*args, tooltip=tooltip, **kwargs)
        except Exception as ex:
            self.log.error('Error occurred while running test.', exception=ex)
            return CommonTestResult(False, reason=f'An error occurred. {ex}', hide_tooltip=True)

    def _run_test(self, *args, tooltip=None, **kwargs) -> CommonTestResult:
        raise NotImplementedError


class CommonSubjectTest(CommonTest):
    """A tunable test with a Subject"""
    FACTORY_TUNABLES = {
        'subject': TunableEnumEntry(
            description='\n            The Sim we want to test with.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.Actor
        )
    }

    __slots__ = {'subject'}

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    def get_expected_args(self) -> Dict[str, Any]:
        return {**super().get_expected_args(), 'subjects': self.subject}

    # noinspection PyMethodOverriding
    def _run_test(self, subjects: Tuple[Any], *args, tooltip=None, **kwargs) -> CommonTestResult:
        has_subjects = False
        for subject in subjects:
            if subject is None or not CommonTypeUtils.is_sim_or_sim_info(subject):
                self.log.format_with_message('Subject is not a Sim, skipping.', subject=subjects)
                continue

            sim_info = CommonSimUtils.get_sim_info(subject)
            has_subjects = True

            sim_test_result = self._run_subject_sim_test(sim_info, *args, tooltip=tooltip, **kwargs)
            if not sim_test_result:
                return sim_test_result

        if not has_subjects:
            self.log.format_with_message('No Subjects were found for subject type.', subject=self.subject, subjects=subjects)
            return CommonTestResult(False, reason=f'No Subjects were found for type {self.subject}.', tooltip_text=CommonStringId.S4CL_NO_SUBJECTS_FOUND_FOR_TYPE, tooltip_tokens=(str(self.subject),))

        return CommonTestResult(True, tooltip_text=tooltip)

    def _run_subject_sim_test(self, sim_info: SimInfo, *args, tooltip=None, **kwargs) -> CommonTestResult:
        raise NotImplementedError()


class CommonSubjectTargetTest(CommonSubjectTest):
    """A tunable test with a target and subject."""
    FACTORY_TUNABLES = {
        'target': TunableEnumEntry(
            description='\n            The Target we want to test with.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.Object
        )
    }

    __slots__ = {'target'}

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    def get_expected_args(self) -> Dict[str, Any]:
        return {**super().get_expected_args(), 'targets': self.target}

    # noinspection PyMethodOverriding
    def _run_test(self, subjects: Tuple[Any], targets: Tuple[Any], *args, tooltip=None, **kwargs) -> CommonTestResult:
        has_subjects = False
        has_targets = False

        for subject in subjects:
            if subject is None or not CommonTypeUtils.is_sim_or_sim_info(subject):
                continue

            source_sim_info = CommonSimUtils.get_sim_info(subject)
            has_subjects = True

            sim_test_result = self._run_subject_sim_test(source_sim_info, *args, tooltip=tooltip, **kwargs)
            if not sim_test_result:
                self.log.format_with_message('Sim cannot.', subject=source_sim_info)
                return sim_test_result

            for target in targets:
                if target is None or not CommonTypeUtils.is_sim_or_sim_info(target):
                    self.log.format_with_message('Target is not a Sim, skipping.', subject=subjects)
                    continue

                target_sim_info = CommonSimUtils.get_sim_info(target)
                sim_target_test_result = self._run_subject_sim_and_target_test(source_sim_info, target_sim_info)
                if not sim_target_test_result:
                    self.log.format_with_message('Sim cannot with Target.', sim=source_sim_info, target_sim=target_sim_info, result=sim_target_test_result)
                    return sim_target_test_result

                has_targets = True
                break

        if not has_subjects:
            self.log.format_with_message('No Subjects were found for subject type.', subject=self.subject, subjects=subjects)
            return CommonTestResult(False, reason=f'No Subjects were found for type {self.subject}.', tooltip_text=CommonStringId.S4CL_NO_SUBJECTS_FOUND_FOR_TYPE, tooltip_tokens=(str(self.subject),))

        if not has_targets:
            self.log.format_with_message('No Targets were found for subject type.', target=self.target, targets=targets)
            return CommonTestResult(False, reason=f'No Targets were found for type {self.target}.', tooltip_text=CommonStringId.S4CL_NO_TARGETS_FOUND_FOR_TYPE, tooltip_tokens=(str(self.target),))
        self.log.format_with_message('Success, Sim can do with Target.', subjects=subjects, target=targets)
        return CommonTestResult.TRUE

    def _run_subject_sim_test(self, sim_info: SimInfo, *args, tooltip=None, **kwargs) -> CommonTestResult:
        raise NotImplementedError()

    def _run_subject_sim_and_target_test(self, source_sim_info: SimInfo, target_sim_info: SimInfo, *args, tooltip=None, **kwargs) -> CommonTestResult:
        raise NotImplementedError()


class CommonResolverTest(CommonTest):
    """A tunable test with a resolver."""
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    def get_expected_args(self) -> Dict[str, Any]:
        return {**super().get_expected_args(), 'resolver': RESOLVER_PARTICIPANT}

    # noinspection PyMethodOverriding
    def _run_test(self, resolver: Resolver, *args, tooltip=None, **kwargs) -> CommonTestResult:
        raise NotImplementedError


class _S4CLSimIsHumanTest(CommonSubjectTest):
    """Tests if a Sim is species Human."""
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cl_sim_is_human'

    def _run_subject_sim_test(self, sim_info: SimInfo, *args, tooltip=None, **kwargs) -> CommonTestResult:
        self.log.format_with_message('Got sim', sim=sim_info)
        from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
        result = CommonSpeciesUtils.is_human(sim_info)
        if self.invert:
            if result:
                return CommonTestResult(False, reason=f'{sim_info} is Human', tooltip_text=tooltip, tooltip_tokens=(sim_info,), hide_tooltip=True)
        else:
            if not result:
                return CommonTestResult(False, reason=f'{sim_info} is not Human', tooltip_text=tooltip, tooltip_tokens=(sim_info,), hide_tooltip=True)
        return CommonTestResult.TRUE


class _S4CLSimIsInActiveHouseholdTest(CommonSubjectTest):
    """Tests if a Sim is in the active household."""
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cl_sim_is_in_active_household'

    def _run_subject_sim_test(self, sim_info: SimInfo, *args, tooltip=None, **kwargs) -> CommonTestResult:
        self.log.format_with_message('Got sim', sim=sim_info)
        result = CommonHouseholdUtils.is_part_of_active_household(sim_info)
        if self.invert:
            if result:
                return CommonTestResult(False, reason=f'{sim_info} is part of the active household.', tooltip_text=tooltip, tooltip_tokens=(sim_info,), hide_tooltip=True)
        else:
            if not result:
                return CommonTestResult(False, reason=f'{sim_info} is not part of the active household.', tooltip_text=tooltip, tooltip_tokens=(sim_info,), hide_tooltip=True)
        return CommonTestResult.TRUE
