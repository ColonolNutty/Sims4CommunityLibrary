"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Any, List
from event_testing.results import TestResult
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_log_utils import CommonLogUtils
from sims4communitylib.utils.objects.common_object_interaction_utils import CommonObjectInteractionUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils


class S4CLDebugLogAllInteractionsInteraction(CommonImmediateSuperInteraction):
    """ Log All Interactions of an object. """
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cl_debug_log_all_interactions'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context, kwargles=kwargs)
        if interaction_target is None:
            cls.get_log().debug('Failed, No Target was found.')
            return TestResult.NONE
        cls.get_log().debug('Success, can show Log All Interactions interaction.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.format_with_message('Running \'{}\' on_started.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        self.log.enable()
        self.log.debug('Interactions that can be performed on \'{}\':'.format(interaction_target))
        interactions = CommonObjectInteractionUtils.get_all_interactions_registered_to_object_gen(interaction_target)
        interaction_short_names: List[str] = list()
        for interaction in interactions:
            try:
                interaction_short_names.append(CommonInteractionUtils.get_interaction_short_name(interaction))
            except Exception as ex:
                self.log.error('Problem while attempting to handle interaction {}'.format(pformat(interaction)), exception=ex)
                continue
        sorted_short_names = sorted(interaction_short_names, key=lambda x: x)
        self.log.debug(pformat(sorted_short_names))
        self.log.debug('Done Logging Available Interactions.'.format())
        self.log.disable()
        CommonBasicNotification(
            CommonStringId.S4CL_LOG_ALL_INTERACTIONS,
            CommonStringId.S4CL_DONE_LOGGING_ALL_INTERACTIONS,
            description_tokens=(CommonLogUtils.get_message_file_path(self.mod_identity), )
        ).show()
        return True
