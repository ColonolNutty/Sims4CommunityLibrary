"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from distributor.shared_messages import IconInfoData
from event_testing.results import TestResult
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.resources.common_situation_utils import CommonSituationUtils
from sims4communitylib.utils.sims.common_sim_situation_utils import CommonSimSituationUtils


class S4CLDebugShowRunningSituationsInteraction(CommonImmediateSuperInteraction):
    """S4CLDebugShowRunningSituationsInteraction(*_, **__)

    Show the currently running Situations of a Sim.
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cl_debug_show_running_situations'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().format_with_message(
            'Running \'{}\' on_test.'.format(cls.__name__),
            interaction_sim=interaction_sim,
            interaction_target=interaction_target,
            interaction_context=interaction_context,
            kwargles=kwargs
        )
        if interaction_target is None or not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            cls.get_log().debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        cls.get_log().debug('Success, can show active Buffs.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        self.log.format_with_message(
            'Running \'{}\' on_started.'.format(self.__class__.__name__),
            interaction_sim=interaction_sim,
            interaction_target=interaction_target
        )
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        target_sim_name = CommonSimNameUtils.get_full_name(target_sim_info)
        sim_situations = ', '.join(CommonSituationUtils.get_situation_names(CommonSimSituationUtils.get_situations(target_sim_info)))
        text = ''
        text += 'Running Situations:\n{}\n\n'.format(sim_situations)
        CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string('{} Running Situations'.format(target_sim_name)),
            CommonLocalizationUtils.create_localized_string(text)
        ).show(
            icon=IconInfoData(obj_instance=interaction_target)
        )
        return True
