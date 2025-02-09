"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple

from interactions import ParticipantType
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.objects.common_object_tag_utils import CommonObjectTagUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class S4CLDebugLogAllGameTagsInteraction(CommonImmediateSuperInteraction):
    """ Log All Game Tags of a Target. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cl_debug_log_all_game_tags'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, picked_item_ids: Tuple[int] = (), **kwargs) -> CommonTestResult:
        if interaction_target is None and not picked_item_ids:
            cls.get_log().debug('Failed, Target is not valid.')
            return CommonTestResult.NONE
        cls.get_log().debug('Success, can show active Buffs.')
        return CommonTestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> CommonExecutionResult:
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
        CommonObjectTagUtils._print_game_tags(interaction_target)
        return CommonExecutionResult.TRUE
