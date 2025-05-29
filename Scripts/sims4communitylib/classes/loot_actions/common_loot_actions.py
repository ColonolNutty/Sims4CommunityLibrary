"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from event_testing.resolver import Resolver
from interactions import ParticipantType
from interactions.utils.loot import LootActions, LootActionVariant
from interactions.utils.loot_basic_op import BaseLootOperation, \
    LootOperationTargetFilterTestMixin
from objects.game_object import GameObject
from sims.sim_info import SimInfo
from sims4.tuning.tunable import TunableList, TunableEnumEntry, TunableFactory
from sims4communitylib.classes.testing.common_test_set_instance import S4CLTunableTestSet
from singletons import DEFAULT


class CommonSubjectLootOperation(BaseLootOperation):
    """A loot operation with a subject."""
    FACTORY_TUNABLES = {
        'subject': TunableEnumEntry(
            description='\n            The Sim we want to use.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.Actor
        ),
        'tests': S4CLTunableTestSet(description='\n            The test to decide whether the loot action can be applied.\n            '),
        'subject_filter_tests': S4CLTunableTestSet(description='\n            These tests will be run once per subject. If the subject \n            participant of this loot action resolves to multiple objects, each \n            of those objects will be tested individually. Any subject that \n            fails this test will be ignored by this loot. This will have no \n            effect on whether we consider the loot to have passed testing on\n            on other subjects or targets. We can use this in cases where we \n            want to give loot based on some criteria like "All active household\n            members that are dogs get this loot".\n            \n            These tests will have no effect on "run tests first" as they are\n            only used for participant filtering and not to determine loot \n            success.\n            \n            The resolver used for these tests is a SingleObjectResolver based \n            on subject sim. This means that test should generally be \n            testing against "Actor" and should not assume the presence of \n            additional participants that may be present in the containing loot.\n            Ask a GPE if you have questions.\n            '),
    }

    __slots__ = {'tests', 'subject_filter_tests', 'chance'}

    # noinspection PyMethodParameters,PyMissingTypeHints,PyMissingOrEmptyDocstring
    @TunableFactory.factory_option
    def subject_participant_type_options(description=DEFAULT, **kwargs):
        if description is DEFAULT:
            # noinspection PyMethodFirstArgAssignment
            description = 'The sim(s) the operation is applied to.'
        return BaseLootOperation.get_participant_tunable(*('subject',), description=description, **kwargs)

    def __init__(self, *_, subject=ParticipantType.Actor, **__) -> None:
        super().__init__(*_, subject=subject, **__)

    def _apply_to_subject_and_target(self, subject: Union[SimInfo, GameObject, None], target: Union[SimInfo, GameObject, None], resolver: Resolver) -> None:
        """Apply the loot operation."""
        raise NotImplementedError()


class CommonSubjectTargetLootOperation(LootOperationTargetFilterTestMixin, CommonSubjectLootOperation):
    """A loot operation with a subject and target."""
    FACTORY_TUNABLES = {
        'target': TunableEnumEntry(
            description='\n            The Target Sim we want to use.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.Object
        ),
        'tests': S4CLTunableTestSet(description='\n            The test to decide whether the loot action can be applied.\n            '),
        'subject_filter_tests': S4CLTunableTestSet(description='\n            These tests will be run once per subject. If the subject \n            participant of this loot action resolves to multiple objects, each \n            of those objects will be tested individually. Any subject that \n            fails this test will be ignored by this loot. This will have no \n            effect on whether we consider the loot to have passed testing on\n            on other subjects or targets. We can use this in cases where we \n            want to give loot based on some criteria like "All active household\n            members that are dogs get this loot".\n            \n            These tests will have no effect on "run tests first" as they are\n            only used for participant filtering and not to determine loot \n            success.\n            \n            The resolver used for these tests is a SingleObjectResolver based \n            on subject sim. This means that test should generally be \n            testing against "Actor" and should not assume the presence of \n            additional participants that may be present in the containing loot.\n            Ask a GPE if you have questions.\n            '),
        'target_filter_tests': S4CLTunableTestSet(description='\n            As subject filter tests, except per target object. See description\n            of subject filter tests.\n            ')
    }

    __slots__ = {'subject', 'target_participant_type', 'tests', 'subject_filter_tests', 'target_filter_tests', 'chance'}

    # noinspection PyMethodParameters,PyMissingTypeHints,PyMissingOrEmptyDocstring
    @TunableFactory.factory_option
    def target_participant_type_options(description=DEFAULT, default_participant=ParticipantType.Object, **kwargs):
        if description is DEFAULT:
            # noinspection PyMethodFirstArgAssignment
            description = 'Participant(s) that target will apply operations on.'
        return CommonSubjectLootOperation.get_participant_tunable(*('target',), description=description, default_participant=default_participant, **kwargs)

    def __init__(self, *_, subject=ParticipantType.Actor, target=ParticipantType.Object, **__) -> None:
        super().__init__(*_, subject=subject, target_participant_type=target, **__)

    def _apply_to_subject_and_target(self, subject: Union[SimInfo, GameObject, None], target: Union[SimInfo, GameObject, None], resolver: Resolver) -> None:
        """Apply the loot operation."""
        raise NotImplementedError()


class CommonLootActionVariant(LootActionVariant):
    """Loot actions variants, where the different loots are."""
    def __init__(self, *args, statistic_pack_safe=False, **kwargs) -> None:
        super().__init__(
            *args,
            statistic_pack_safe=statistic_pack_safe,
            **kwargs
        )


class CommonLootActions(LootActions):
    """Loot actions."""
    INSTANCE_TUNABLES = {
        'loot_actions': TunableList(
            description='\n           List of loots operations that will be awarded.\n           ',
            tunable=CommonLootActionVariant(statistic_pack_safe=True)
        ),
        'tests': S4CLTunableTestSet(
            description='\n           Tests to run before applying any of the loot actions.\n           \n           These are run before run_test_first is evaluated so it will not\n           affect these tests.\n           '
        )
    }
