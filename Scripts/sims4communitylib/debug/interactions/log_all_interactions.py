"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Any, List
from event_testing.results import TestResult
from interactions.base.interaction import Interaction
from interactions.context import InteractionContext
from objects.game_object import GameObject
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_log_utils import CommonLogUtils
from sims4communitylib.utils.objects.common_object_interaction_utils import CommonObjectInteractionUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class S4CLDebugLogAllInteractionsInteraction(CommonImmediateSuperInteraction):
    """ Log All Interactions of an object. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cl_debug_log_all_interactions'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        if interaction_target is None:
            cls.get_log().debug('Failed, No Target was found.')
            return TestResult.NONE
        cls.get_log().debug('Success, can show Log All Interactions interaction.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.enable()
        object_id = CommonObjectUtils.get_object_id(interaction_target) if interaction_target is not None else -1
        definition_id = -1
        if isinstance(interaction_target, Sim):
            object_id = CommonSimUtils.get_sim_id(interaction_target)
        elif isinstance(interaction_target, GameObject):
            definition = CommonObjectUtils.get_game_object_definition(interaction_target)
            if definition is not None:
                definition_id = definition.id
        self.log.debug('Interactions that can be performed on \'{}\' id:{} def_id:{}:'.format(interaction_target, object_id, definition_id))
        interactions = CommonObjectInteractionUtils.get_all_interactions_registered_to_object_gen(interaction_target)
        interaction_target: GameObject = interaction_target
        interaction_short_names: List[str] = list()
        for interaction in interactions:
            interaction: Interaction = interaction
            try:
                interaction_short_names.append('{} ({})'.format(CommonInteractionUtils.get_interaction_short_name(interaction), CommonInteractionUtils.get_interaction_id(interaction)))
            except Exception as ex:
                self.log.error('Problem while attempting to handle interaction {}'.format(pformat(interaction)), exception=ex)
                continue
        for component in interaction_target.components:
            if not hasattr(component, 'component_super_affordances_gen'):
                continue
            for affordance in component.component_super_affordances_gen():
                try:
                    interaction_short_names.append('{} ({})'.format(CommonInteractionUtils.get_interaction_short_name(affordance), CommonInteractionUtils.get_interaction_id(affordance)))
                except Exception as ex:
                    self.log.error('Problem while attempting to handle affordance {}'.format(pformat(affordance)), exception=ex)
                    continue

        sorted_short_names = sorted(interaction_short_names, key=lambda x: x)
        self.log.format(interactions=sorted_short_names)
        self.log.debug('Done Logging Available Interactions.')
        self.log.disable()
        CommonBasicNotification(
            CommonStringId.S4CL_LOG_ALL_INTERACTIONS,
            CommonStringId.S4CL_DONE_LOGGING_ALL_INTERACTIONS,
            description_tokens=(CommonLogUtils.get_message_file_path(self.mod_identity), )
        ).show()
        return True
