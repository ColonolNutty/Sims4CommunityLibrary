"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.events.build_buy.events.build_buy_enter import S4CLBuildBuyEnterEvent
from sims4communitylib.events.build_buy.events.build_buy_exit import S4CLBuildBuyExitEvent
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from zone import Zone


class CommonBuildBuyEventDispatcherService(CommonService):
    """A service for dispatching Build/Buy events.

    """

    def _on_build_buy_enter(self, zone: Zone, *_, **__):
        return CommonEventRegistry.get().dispatch(S4CLBuildBuyEnterEvent(zone))

    def _on_build_buy_exit(self, zone: Zone, *_, **__):
        return CommonEventRegistry.get().dispatch(S4CLBuildBuyExitEvent(zone))


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, Zone, Zone.on_build_buy_enter.__name__)
def _common_build_buy_enter(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    CommonBuildBuyEventDispatcherService.get()._on_build_buy_enter(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, Zone, Zone.on_build_buy_exit.__name__)
def _common_build_buy_exit(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    CommonBuildBuyEventDispatcherService.get()._on_build_buy_exit(self, *args, **kwargs)
    return result
