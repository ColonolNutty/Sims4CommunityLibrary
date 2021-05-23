"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple
from interactions.context import InteractionContext
from objects.script_object import ScriptObject
from sims.sim import Sim
from sims4communitylib.enums.interactions_enum import CommonInteractionId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.interactions.interaction_registration_service import CommonInteractionRegistry, \
    CommonInteractionType, CommonScriptObjectInteractionHandler, CommonInteractionHandler
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_keyboard_utils import CommonKeyboardUtils, CommonKey
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
            CommonInteractionId.S4CL_DEBUG_INDUCE_LABOR
        )
        return result

    # noinspection PyMissingOrEmptyDocstring
    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        return CommonTypeUtils.is_sim_instance(script_object)


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
class _S4CLDebugEverywhereObjectInteractionHandler(CommonScriptObjectInteractionHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        result: Tuple[int] = (
            CommonInteractionId.S4CL_DEBUG_LOG_ALL_INTERACTIONS,
        )
        return result

    # noinspection PyMissingOrEmptyDocstring
    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        return True


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_TERRAIN_LOAD)
class _S4CLDebugEverywhereTerrainInteractionHandler(CommonInteractionHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        result: Tuple[int] = (
            CommonInteractionId.S4CL_DEBUG_LOG_ALL_INTERACTIONS,
        )
        return result


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ADD_TO_SIM_RELATIONSHIP_PANEL_INTERACTIONS)
class _S4CLDebugSimRelationshipPanelInteractionHandler(CommonScriptObjectInteractionHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        result: Tuple[int] = (
            CommonInteractionId.S4CL_DEBUG_LOG_ALL_INTERACTIONS,
        )
        return result

    # noinspection PyMissingOrEmptyDocstring
    def should_add(self, script_object: Sim, *args, **kwargs) -> bool:
        return CommonTypeUtils.is_sim_instance(script_object)


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ADD_TO_SIM_PHONE_INTERACTIONS)
class _S4CLDebugSimPhoneInteractionHandler(CommonScriptObjectInteractionHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        result: Tuple[int] = (
            CommonInteractionId.S4CL_DEBUG_LOG_ALL_INTERACTIONS,
        )
        return result

    # noinspection PyMissingOrEmptyDocstring
    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        return CommonTypeUtils.is_sim_instance(script_object)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), InteractionContext, InteractionContext.__init__.__name__)
def _common_ensure_shift_held_is_true_when_it_should_be(original, self: InteractionContext, *_, **__):
    if 'shift_held' not in __ or not __['shift_held']:
        __['shift_held'] = CommonKeyboardUtils.is_holding_key_down(CommonKey.SHIFT)
    return original(self, *_, **__)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Sim, Sim.potential_relation_panel_interactions.__name__)
def _common_ensure_proper_interactions_appear_in_relationship_panel(original, self: Sim, context: InteractionContext, **kwargs):
    # noinspection PyBroadException
    try:
        for aop in original(self, context, **kwargs):
            if not self._can_show_affordance(context.shift_held, aop.affordance):
                continue
            yield aop
    except:
        yield from original(self, context, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Sim, Sim.potential_phone_interactions.__name__)
def _common_ensure_proper_interactions_appear_in_phone_panel(original, self: Sim, context: InteractionContext, **kwargs):
    # noinspection PyBroadException
    try:
        for aop in original(self, context, **kwargs):
            if not self._can_show_affordance(context.shift_held, aop.affordance):
                continue
            yield aop
    except:
        yield from original(self, context, **kwargs)
