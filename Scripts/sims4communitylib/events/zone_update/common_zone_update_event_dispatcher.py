"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import math
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_update.events.zone_update_event import S4CLZoneUpdateEvent
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from zone import Zone


class CommonZoneUpdateEventDispatcherService(CommonService, HasLog):
    """A service that dispatches zone update events.

    .. warning:: Do not use this service directly to listen for events!\
        Use the :class:`.CommonEventRegistry` to listen for dispatched events.

    """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    def __init__(self: 'CommonZoneUpdateEventDispatcherService'):
        super().__init__()
        self._last_absolute_ticks = 0
        self._ticks_since_last_zone_update = 0
        self._ticks_since_last_zone_update_error = 0

    @property
    def ticks_since_last_zone_update(self) -> int:
        """The amount of time that has passed since the last zone update.

        :return: The amount of time that has passed in milliseconds
        :rtype: int
        """
        return self._ticks_since_last_zone_update

    @ticks_since_last_zone_update.setter
    def ticks_since_last_zone_update(self, val: int):
        self._ticks_since_last_zone_update = val

    def _update_ticks(self, diff_ticks: int):
        if diff_ticks > 5000:
            diff_ticks = 5000
        ideal_diff_ticks = diff_ticks * CommonTimeUtils.get_clock_speed_scale() + self._ticks_since_last_zone_update_error
        rounded_ticks = math.floor(ideal_diff_ticks + 0.5)
        ticks_error = ideal_diff_ticks - rounded_ticks
        self._ticks_since_last_zone_update_error += max(min(ticks_error, 1), -1)
        self.ticks_since_last_zone_update = rounded_ticks

    def _on_zone_update(self, zone: Zone, absolute_ticks: int):
        try:
            if not zone.is_zone_running:
                return False
            is_paused = CommonTimeUtils.game_is_paused()
            if not is_paused:
                diff_ticks = absolute_ticks - self._last_absolute_ticks
                if diff_ticks < 0:
                    return False
                self._update_ticks(diff_ticks)
            self._last_absolute_ticks = absolute_ticks
            return CommonEventRegistry.get().dispatch(S4CLZoneUpdateEvent(zone, is_paused, self.ticks_since_last_zone_update))
        except Exception as ex:
            self.log.error('Failed to run internal method \'{}\' at \'{}\'.'.format(CommonZoneUpdateEventDispatcherService._on_zone_update.__name__, Zone.update.__name__), exception=ex)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, Zone, Zone.update.__name__, handle_exceptions=False)
def _common_zone_update(original, self: Zone, *_, **__):
    result = original(self, *_, **__)
    CommonZoneUpdateEventDispatcherService.get()._on_zone_update(self, *_, **__)
    return result
