"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple
from interactions.context import InteractionContext
from objects.game_object import GameObject
from objects.script_object import ScriptObject
from sims.sim import Sim
from sims4communitylib.enums.interactions_enum import CommonInteractionId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.interactions.interaction_registration_service import CommonInteractionRegistry, \
    CommonInteractionType, CommonScriptObjectInteractionHandler, CommonInteractionHandler
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_keyboard_utils import CommonKeyboardUtils, CommonKey
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.objects.common_object_state_utils import CommonObjectStateUtils


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
class _S4CLObjectBrokennessDebugInteractionHandler(CommonScriptObjectInteractionHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        result: Tuple[int] = (
            CommonInteractionId.S4CL_DEBUG_OBJECT_BREAK,
            CommonInteractionId.S4CL_DEBUG_OBJECT_FIX
        )
        return result

    # noinspection PyMissingOrEmptyDocstring
    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        if not CommonTypeUtils.is_game_object(script_object):
            return False
        script_object: GameObject = script_object
        return CommonObjectStateUtils.can_become_broken(script_object)


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
class _S4CLObjectDirtinessDebugInteractionHandler(CommonScriptObjectInteractionHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        result: Tuple[int] = (
            CommonInteractionId.S4CL_DEBUG_OBJECT_MAKE_DIRTY,
            CommonInteractionId.S4CL_DEBUG_OBJECT_MAKE_CLEAN
        )
        return result

    # noinspection PyMissingOrEmptyDocstring
    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        if not CommonTypeUtils.is_game_object(script_object):
            return False
        script_object: GameObject = script_object
        return CommonObjectStateUtils.can_become_dirty(script_object)


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
        return not CommonTypeUtils.is_sim_or_sim_info(script_object)


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
    from sims4communitylib.s4cl_configuration import S4CLConfiguration
    if S4CLConfiguration().enable_extra_shift_click_menus and ('shift_held' not in __ or not __['shift_held']):
        __['shift_held'] = CommonKeyboardUtils.is_holding_key_down(CommonKey.SHIFT)
    return original(self, *_, **__)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Sim, Sim.potential_relation_panel_interactions.__name__)
def _common_ensure_proper_interactions_appear_in_relationship_panel(original, self: Sim, context: InteractionContext, **kwargs):
    from sims4communitylib.s4cl_configuration import S4CLConfiguration
    if not S4CLConfiguration().enable_extra_shift_click_menus:
        yield from original(self, context, **kwargs)
    else:
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
    from sims4communitylib.s4cl_configuration import S4CLConfiguration
    if not S4CLConfiguration().enable_extra_shift_click_menus:
        yield from original(self, context, **kwargs)
    else:
        # noinspection PyBroadException
        try:
            for aop in original(self, context, **kwargs):
                if not self._can_show_affordance(context.shift_held, aop.affordance):
                    continue
                yield aop
        except:
            yield from original(self, context, **kwargs)
