"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple
from objects.script_object import ScriptObject
from sims4communitylib.enums.interactions_enum import CommonInteractionId
from sims4communitylib.services.interactions.interaction_registration_service import CommonInteractionRegistry, \
    CommonInteractionType, CommonScriptObjectInteractionHandler
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
class _S4CLDebugInteractionHandler(CommonScriptObjectInteractionHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        result: Tuple[int] = (
            CommonInteractionId.S4CL_DEBUG_SHOW_RUNNING_AND_QUEUED_INTERACTIONS,
            CommonInteractionId.S4CL_DEBUG_SHOW_ACTIVE_BUFFS,
            CommonInteractionId.S4CL_DEBUG_SHOW_TRAITS,
            CommonInteractionId.S4CL_DEBUG_SHOW_RUNNING_SITUATIONS,
        )
        return result

    # noinspection PyMissingOrEmptyDocstring
    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        return CommonTypeUtils.is_sim_instance(script_object)
