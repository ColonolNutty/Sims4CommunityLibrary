"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from typing import Any, Callable


ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

if ON_RTD:
    # noinspection PyMissingOrEmptyDocstring
    class AlarmHandle:
        def cancel(self) -> Any:
            pass

    # noinspection PyMissingOrEmptyDocstring
    class DateAndTime:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class TimeSpan:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class Timeline:
        pass

if not ON_RTD:
    from scheduling import Timeline, ElementHandle
    from alarms import AlarmHandle
    from date_and_time import DateAndTime, TimeSpan


class CommonAlarmHandle(AlarmHandle):
    """A custom alarm handle that keeps track of when it is slated to trigger for the first time."""
    def __init__(
        self,
        owner: Any,
        on_alarm_triggered_callback: Callable[['CommonAlarmHandle'], None],
        timeline: Timeline,
        when: DateAndTime,
        should_repeat: bool=False,
        time_until_repeat: TimeSpan=None,
        accurate_repeat: bool=True,
        persist_across_zone_loads: bool=False
    ):
        self.started_at_date_and_time = when
        super().__init__(
            owner,
            on_alarm_triggered_callback,
            timeline,
            when,
            repeating=should_repeat,
            repeat_interval=time_until_repeat,
            accurate_repeat=accurate_repeat,
            cross_zone=persist_across_zone_loads
        )

    @property
    def is_active(self) -> bool:
        """True, if the Alarm Handle is currently active and scheduled. False, if not."""
        if self._element_handle is None:
            return False
        element_handle: ElementHandle = self._element_handle
        # noinspection PyPropertyAccess
        return element_handle.is_active and element_handle.is_scheduled


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.print_current_time', 'Prints the current time.')
def _s4clib_print_current_time(output: CommonConsoleCommandOutput):
    output('Current time')
    output('Hour {} Minute {}'.format(CommonTimeUtils.get_current_date_and_time().hour(), CommonTimeUtils.get_current_date_and_time().minute()))
    output('Abs Hour {} Abs Minute {}'.format(CommonTimeUtils.get_current_date_and_time().absolute_hours(), CommonTimeUtils.get_current_date_and_time().absolute_minutes()))
