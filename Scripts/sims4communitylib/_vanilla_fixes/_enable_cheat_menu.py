"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

import services
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.enums.interactions_enum import CommonInteractionId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_keyboard_utils import CommonKeyboardUtils, CommonKey
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_extra_cheat_menu_log')


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), InteractionContext, '__init__')
def _common_ensure_shift_held_is_true_when_it_should_be(original, self: InteractionContext, *_, **__):
    from sims4communitylib.s4cl_configuration import S4CLConfiguration
    cheat_service = services.get_cheat_service()
    if cheat_service.cheats_enabled and S4CLConfiguration().enable_extra_shift_click_menus and ('shift_held' not in __ or not __['shift_held']):
        log.format_with_message('Enabling shift click because SHIFT was held down.')
        __['shift_held'] = CommonKeyboardUtils.is_holding_key_down(CommonKey.SHIFT)
    return original(self, *_, **__)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Sim, Sim.potential_relation_panel_interactions.__name__)
def _common_ensure_proper_interactions_appear_in_relationship_panel(original, self: Sim, *args, **kwargs):
    # noinspection PyTypeChecker
    context: InteractionContext = None
    if len(args) == 1:
        context: InteractionContext = args[0]
    elif len(args) == 2:
        context: InteractionContext = args[1]
    cheat_service = services.get_cheat_service()
    from sims4communitylib.s4cl_configuration import S4CLConfiguration
    if not S4CLConfiguration().enable_extra_shift_click_menus or not cheat_service.cheats_enabled:
        yield from original(self, *args, **kwargs)
    elif context is not None:
        original_result = original(self, *args, **kwargs)
        # noinspection PyBroadException
        try:
            for aop in original_result:
                affordance = aop.affordance
                affordance_id = CommonInteractionUtils.get_interaction_id(affordance)
                if affordance_id == CommonInteractionId.TOGGLE_PHONE_SILENCE:
                    # We do this to account for a bug in Wicked Whims that is literally there solely to annoy those who use S4CL.
                    yield aop
                    continue
                if context.shift_held:
                    if not affordance.cheat:
                        log.format_with_message('Excluding affordance because not a cheat with shift held down.', affordance=affordance, is_cheat=affordance.cheat, shift_held=context.shift_held, me=self)
                        continue
                else:
                    if affordance.cheat:
                        log.format_with_message('Excluding affordance because it is a cheat with shift held down.', affordance=affordance, is_cheat=affordance.cheat, shift_held=context.shift_held, me=self)
                        continue
                log.format_with_message('Allowing affordance because it works.', affordance=affordance, is_cheat=affordance.cheat, shift_held=context.shift_held, me=self)
                yield aop
        except:
            yield from original_result
    else:
        yield from original(self, *args, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Sim, Sim.potential_phone_interactions.__name__)
def _common_ensure_proper_interactions_appear_in_phone_panel(original, self: Sim, *args, **kwargs):
    # noinspection PyTypeChecker
    context = None
    if len(args) == 1:
        context: InteractionContext = args[0]
    elif len(args) == 2:
        context: InteractionContext = args[1]
    cheat_service = services.get_cheat_service()
    from sims4communitylib.s4cl_configuration import S4CLConfiguration
    if not S4CLConfiguration().enable_extra_shift_click_menus or not cheat_service.cheats_enabled:
        yield from original(self, *args, **kwargs)
    elif context is not None:
        original_result = original(self, *args, **kwargs)
        # noinspection PyBroadException
        try:
            for aop in original_result:
                affordance = aop.affordance
                affordance_id = CommonInteractionUtils.get_interaction_id(affordance)
                if affordance_id == CommonInteractionId.TOGGLE_PHONE_SILENCE:
                    # We do this to account for a bug in Wicked Whims that is literally there solely to annoy those who use S4CL.
                    yield aop
                    continue
                if context.shift_held:
                    if not affordance.cheat:
                        log.format_with_message('Excluding affordance because not a cheat with shift held down.', affordance=affordance, is_cheat=affordance.cheat, shift_held=context.shift_held, me=self)
                        continue
                else:
                    if affordance.cheat:
                        log.format_with_message('Excluding affordance because it is a cheat with shift held down.', affordance=affordance, is_cheat=affordance.cheat, shift_held=context.shift_held, me=self)
                        continue
                log.format_with_message('Allowing affordance because it works.', affordance=affordance, is_cheat=affordance.cheat, shift_held=context.shift_held, me=self)
                yield aop
        except:
            yield from original_result
    else:
        yield from original(self, *args, **kwargs)
