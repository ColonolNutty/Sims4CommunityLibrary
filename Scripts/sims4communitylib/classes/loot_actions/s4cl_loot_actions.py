"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Tuple, Union

import services
from event_testing.resolver import DoubleSimResolver
from interactions import ParticipantTypeSingle
from interactions.utils.loot import LootActions, LootActionVariant
from interactions.utils.success_chance import SuccessChance
from sims.pregnancy.pregnancy_enums import PregnancyOrigin
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4.tuning.tunable import TunableList, TunableEnumEntry, TunableVariant, \
    HasTunableSingletonFactory, AutoFactoryInit, Tunable, TunableReference
from sims4communitylib.classes.loot_actions.common_loot_actions import CommonSubjectLootOperation
from sims4communitylib.classes.testing.common_test_set_instance import CommonTunableTestSet, S4CLTunableTestSet
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_loot_actions')


class _S4CLStartPregnancyLootOp(CommonSubjectLootOperation):
    """Start a Pregnancy in a Sim."""

    class _S4CLPregnancyParentParticipant(HasTunableSingletonFactory, AutoFactoryInit):
        FACTORY_TUNABLES = {
            'subject': TunableEnumEntry(
                description='\n                The participant that is to be the\n                one impregnating.\n                ',
                tunable_type=ParticipantTypeSingle,
                default=ParticipantTypeSingle.TargetSim
            ),
            'single_sim_is_allowed': Tunable(
                description='\n                The participant can be the same Sim as the Sim becoming\n                pregnant. This allows single Sim pregnancy.\n                ',
                tunable_type=bool,
                default=False
            )
        }

        __slots__ = {'subject', 'single_sim_is_allowed'}

        # noinspection PyMissingOrEmptyDocstring
        def get_parent(self, resolver, pregnancy_subject_sim_info) -> Tuple[Union[SimInfo, None], bool]:
            parent = resolver.get_participant(self.subject)
            if parent is None:
                return None, self.single_sim_is_allowed
            return parent.sim_info, self.single_sim_is_allowed

    class _S4CLPregnancyParentFilter(HasTunableSingletonFactory, AutoFactoryInit):
        FACTORY_TUNABLES = {
            'filter': TunableReference(
                description='\n                The filter to use to find a parent.\n                ',
                manager=services.get_instance_manager(Types.SIM_FILTER),
                class_restrictions=('TunableSimFilter',)
            ),
            'sim_tests': S4CLTunableTestSet(
                description='\n                Tests that determine if a Sim from the filter can be chosen.'
            ),
        }

        __slots__ = {'filter', 'sim_tests'}

        # noinspection PyMissingOrEmptyDocstring
        def get_sim_filter_gsi_name(self) -> str:
            return str(self)

        # noinspection PyMissingOrEmptyDocstring
        def get_parent(self, resolver, pregnancy_subject_sim_info) -> Tuple[Union[SimInfo, None], bool]:
            filter_results = services.sim_filter_service().submit_matching_filter(
                sim_filter=self.filter,
                allow_yielding=False,
                requesting_sim_info=pregnancy_subject_sim_info,
                gsi_source_fn=self.get_sim_filter_gsi_name
            )
            if filter_results:
                if self.sim_tests:
                    tested_filter_results = list()
                    for result in filter_results:
                        resolver = DoubleSimResolver(pregnancy_subject_sim_info, result.sim_info)
                        if self.sim_tests.run_tests(resolver):
                            tested_filter_results.append(result)
                else:
                    tested_filter_results = list(filter_results)
                sims = [filter_result.sim_info for filter_result in tested_filter_results]
                if not sims:
                    return None, False
                # noinspection PyTypeChecker
                parent = random.choice(sims)
                return parent, False
            return None, False

    FACTORY_TUNABLES = {
        'subject': TunableEnumEntry(
            description='\n            The participant that is to be impregnated. There\n            are no age or gender restrictions on this Sim, so ensure that you\n            are tuning the appropriate tests to avoid unwanted pregnancies.\n            ',
            tunable_type=ParticipantTypeSingle,
            default=ParticipantTypeSingle.Actor
        ),
        'pregnancy_parent': TunableVariant(
            description='\n            The participant that is to be the one impregnating.\n            ',
            from_participant=_S4CLPregnancyParentParticipant.TunableFactory(),
            from_filter=_S4CLPregnancyParentFilter.TunableFactory(),
            default='from_participant'
        ),
        'pregnancy_origin': TunableEnumEntry(
            description='\n            Define the origin of this pregnancy. This value is used to determine\n            some of the random elements at birth.\n            ',
            tunable_type=PregnancyOrigin,
            default=PregnancyOrigin.DEFAULT
        ),
        'success_chance': SuccessChance.TunableFactory(description='\n            The percentage chance that this action will be applied.\n            ')
    }

    __slots__ = {'subject', 'pregnancy_parent', 'pregnancy_origin', 'success_chance'}

    def __init__(self, *_, subject=ParticipantTypeSingle.Actor, pregnancy_parent=None, pregnancy_origin=PregnancyOrigin.DEFAULT, success_chance=None, **__) -> None:
        super().__init__(*_, **__)
        self.subject = subject
        self.pregnancy_parent = pregnancy_parent
        self.pregnancy_origin = pregnancy_origin
        self.success_chance = success_chance

    def _apply_to_subject_and_target(self, subject, target, resolver) -> None:
        if self._tests:
            test_result = self._tests.run_tests(resolver)
            if not test_result:
                log.format_with_message('Ran tests and they failed.', me=self, subject=subject, target=target, result=test_result)
                return test_result
            log.format_with_message('Ran tests and they passed.', me=self, subject=subject, target=target)

        subject_sim_info = CommonSimUtils.get_sim_info(subject)
        if subject is None:
            return None
        if not CommonHouseholdUtils.has_free_household_slots(subject_sim_info):
            log.format_with_message('No free household slot.', sim=subject_sim_info)
            return
        from interactions.utils.death import get_death_interaction
        death_interaction = get_death_interaction(subject)
        if death_interaction is not None:
            log.format_with_message('No death interaction found for Sim', sim=subject)
            return
        (parent_sim_info, single_sim_is_allowed) = self.pregnancy_parent.get_parent(resolver, subject_sim_info)
        if parent_sim_info is None:
            log.format_with_message('No parent Sim found to impregnate.', sim=subject_sim_info)
            return
        if not single_sim_is_allowed and subject_sim_info is parent_sim_info:
            log.format_with_message('Single Sim not allowed and the parent found was the same Sim.', sim=subject_sim_info)
            return
        success_chance = self.success_chance.get_chance(resolver)
        dice_roll = random.random()
        if dice_roll <= success_chance:
            log.format_with_message('Applying pregnancy to Sim.', subject=subject, parent_sim=parent_sim_info, success_chance=success_chance, dice_roll=dice_roll)
            CommonSimPregnancyUtils.start_pregnancy(
                subject_sim_info,
                parent_sim_info,
                pregnancy_origin=self.pregnancy_origin
            )
        else:
            log.format_with_message('Not applying pregnancy to Sim.', subject=subject, parent_sim=parent_sim_info, success_chance=success_chance, dice_roll=dice_roll)


class S4CLLootActionVariant(LootActionVariant):
    """Loot actions."""
    def __init__(self, *args, statistic_pack_safe=False, **kwargs) -> None:
        super().__init__(
            *args,
            statistic_pack_safe=statistic_pack_safe,
            start_pregnancy=_S4CLStartPregnancyLootOp.TunableFactory(),
            **kwargs
        )


class S4CLLootActions(LootActions):
    """Loot actions."""
    INSTANCE_TUNABLES = {
        'loot_actions': TunableList(
            description='\n           List of loots operations that will be awarded.\n           ',
            tunable=S4CLLootActionVariant(statistic_pack_safe=True)
        ),
        'tests': CommonTunableTestSet(
            description='\n           Tests to run before applying any of the loot actions.\n           \n           These are run before run_test_first is evaluated so it will not\n           affect these tests.\n           '
        )
    }
