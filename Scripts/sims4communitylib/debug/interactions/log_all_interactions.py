"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Any, List, Tuple
from interactions import ParticipantType
from interactions.base.interaction import Interaction
from interactions.context import InteractionContext
from objects.game_object import GameObject
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_log_utils import CommonLogUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
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
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, picked_item_ids: Tuple[int] = (), **kwargs) -> CommonTestResult:
        if interaction_target is None and not picked_item_ids:
            cls.get_log().debug('Failed, No Target was found.')
            return cls.create_test_result(False)
        cls.get_log().format_with_message(
            'Success, can show Log All Interactions interaction.',
            interaction_sim=interaction_sim,
            interaction_target=interaction_target,
            picked_item_ids=picked_item_ids
        )
        return cls.create_test_result(True)

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> CommonExecutionResult:
        self.log.enable()
        # noinspection PyUnresolvedReferences
        picked_item_id = self.get_participant(ParticipantType.PickedItemId)
        self.log.format_with_message('Got picked item ids', picked_item_id=picked_item_id)
        if picked_item_id is not None:
            new_target = CommonSimUtils.get_sim_info(picked_item_id)
            if new_target is None:
                self.log.format_with_message('No Sim with the identifier found.', picked_item_id=picked_item_id)
                new_target = CommonObjectUtils.get_game_object(picked_item_id)
                if new_target is None:
                    self.log.format_with_message('No object with the identifier found.', picked_item_id=picked_item_id)
                    return CommonExecutionResult(False, reason=f'Picked Item {picked_item_id} was not found.', hide_tooltip=True)
                else:
                    self.log.format_with_message('Found object target using picked item id.', new_target=new_target)
                    interaction_target = new_target
            else:
                self.log.format_with_message('Found Sim target using picked item id.', new_target=new_target)
                new_target = CommonSimUtils.get_sim_instance(new_target)
                if new_target is None:
                    self.log.format_with_message('Had Sim Info, but did not have Sim instance.', new_target=new_target)
                else:
                    self.log.format_with_message('Had Sim Instance.', new_target=new_target)
                    interaction_target = new_target
        object_id = CommonObjectUtils.get_object_id(interaction_target) if interaction_target is not None else -1
        object_tuning_name = None
        definition_id = -1
        if CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
            object_id = CommonSimUtils.get_sim_id(interaction_target)
            target_sim = CommonSimUtils.get_sim_instance(interaction_target)
            object_tuning_name = target_sim.__name__ if hasattr(target_sim, '__name__') else target_sim.__class__.__name__
            rig_hash64 = target_sim.rig.hash64
            rig_instance = target_sim.rig.instance
            self.log.format_with_message('All things on rig', rig64=rig_hash64, rig_instance=rig_instance, target_rig_key=target_sim_info.rig_key)
            definition = CommonObjectUtils.get_game_object_definition(target_sim)
            if definition is not None:
                definition_id = definition.id
        elif CommonTypeUtils.is_game_object(interaction_target):
            object_tuning_name = interaction_target.__name__ if hasattr(interaction_target, '__name__') else interaction_target.__class__.__name__
            rig_hash64 = interaction_target.rig.hash64
            rig_instance = interaction_target.rig.instance
            self.log.format_with_message('All things on rig', rig64=rig_hash64, rig_instance=rig_instance)
            definition = CommonObjectUtils.get_game_object_definition(interaction_target)
            if definition is not None:
                definition_id = definition.id
        self.log.debug(f'Interactions that can be performed on \'{interaction_target}\' id:{object_id} def_id:{definition_id} tuning_name:{object_tuning_name}:')
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
        return CommonExecutionResult.TRUE
