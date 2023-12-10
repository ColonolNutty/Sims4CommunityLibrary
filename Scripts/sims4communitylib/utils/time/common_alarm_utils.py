"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Callable, Any, Union
from sims4communitylib.classes.time.common_alarm_handle import CommonAlarmHandle
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_time_utils import CommonTimeUtils

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

if ON_RTD:
    # noinspection PyMissingOrEmptyDocstring
    class Timeline:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class TimeSpan:
        pass

if not ON_RTD:
    from scheduling import Timeline
    from date_and_time import TimeSpan


class CommonAlarmUtils(HasClassLog):
    """Utilities for manipulating alarms."""

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_alarm_utils'

    @classmethod
    def schedule_alarm(
        cls,
        alarm_owner: Any,
        time_until_first_occurrence: TimeSpan,
        on_alarm_triggered_callback: Callable[['CommonAlarmHandle'], None],
        should_repeat: bool = False,
        time_until_repeat: TimeSpan = None,
        accurate_repeat: bool = True,
        persist_across_zone_loads: bool = False,
        timeline: Timeline = None
    ) -> Union['CommonAlarmHandle', None]:
        """schedule_alarm(\
            alarm_owner,\
            time_until_next_occurrence,\
            callback,\
            should_repeat=False,\
            time_until_repeat=None,\
            accurate_repeat=True,\
            persist_across_zone_loads=False,\
            timeline=None\
        )

        Schedule an alarm that will trigger a callback after a set amount of time.

        :param alarm_owner: The owner of the alarm.
        :type alarm_owner: Any
        :param time_until_first_occurrence: The time until the alarm triggers.
        :type time_until_first_occurrence: TimeSpan
        :param on_alarm_triggered_callback: When the alarm is triggered at the specified time, this callback will be invoked with the alarm handle.
        :type on_alarm_triggered_callback: Callable[['CommonAlarmHandle'], None]
        :param should_repeat: If True, the alarm will repeat on the specified interval. If False, the alarm will only trigger once. Default is False.
        :type should_repeat: bool, optional
        :param time_until_repeat: The amount of time that must pass before the alarm will trigger again. This only comes into play after being triggered once. Default is None.
        :type time_until_repeat: TimeSpan, optional
        :param accurate_repeat: Whether or not the initial time should be based on the now time or the future time. Default is the Now time.
        :type accurate_repeat: bool, optional
        :param persist_across_zone_loads: If True, the alarm will persist when loading a new zone. If False, the alarm will be canceled upon changing zones. Default is False.
        :type persist_across_zone_loads: bool, optional
        :param timeline: The timeline to use when determining the alarm trigger time as well as the initial time of the alarm. Default is Sim Timeline.
        :type timeline: Timeline, optional
        :return: The created alarm handle or None if the Time service is not currently available or a problem occurs.
        :rtype: Union[CommonAlarmHandle, None]
        """
        if timeline is None:
            time_service = CommonTimeUtils.get_time_service()
            if time_service.sim_timeline is None:
                return None
            timeline = time_service.sim_timeline

        if accurate_repeat:
            initial_time = timeline.now
        else:
            initial_time = timeline.future

        def _on_alarm_triggered(handle: CommonAlarmHandle):
            try:
                on_alarm_triggered_callback(handle)
            except Exception as ex:
                cls.get_log().format_error(f'An exception occurred when triggering alarm callback for {alarm_owner}.', alarm_owner=alarm_owner, exception=ex)

        return CommonAlarmHandle(
            alarm_owner,
            _on_alarm_triggered,
            timeline,
            initial_time + time_until_first_occurrence,
            should_repeat=should_repeat,
            time_until_repeat=time_until_repeat or time_until_first_occurrence,
            accurate_repeat=accurate_repeat,
            persist_across_zone_loads=persist_across_zone_loads
        )

    @classmethod
    def schedule_daily_alarm(
        cls,
        alarm_owner: Any,
        hour: int,
        minute: int,
        on_alarm_triggered: Callable[[CommonAlarmHandle], None],
        persist_across_zone_loads: bool = False
    ) -> CommonAlarmHandle:
        """schedule_daily_alarm(\
            alarm_owner,\
            hour,\
            minute,\
            on_alarm_triggered,\
            persist_across_zone_loads=False\
        )

        Schedule an alarm that will repeat once a day, every day.

        :param alarm_owner: The owner of the alarm.
        :type alarm_owner: Any
        :param hour: The hour of the day to trigger the alarm at.
        :type hour: int
        :param minute: The minute of the hour to trigger the alarm at.
        :type minute: int
        :param on_alarm_triggered: A callback invoked when the alarm is triggered.
        :type on_alarm_triggered: Callable[[CommonAlarmHandle], None]
        :param persist_across_zone_loads: If True, the alarm will persist when loading a new zone. If False, the alarm will be canceled upon changing zones. Default is False.
        :type persist_across_zone_loads: bool, optional
        :return: The scheduled alarm or None if a problem occurs.
        :rtype: CommonAlarmHandle
        """
        from date_and_time import create_date_and_time, sim_ticks_per_day
        now = CommonTimeUtils.get_current_date_and_time()
        alarm_time_of_day = create_date_and_time(hours=hour, minutes=minute)
        alarm_next_trigger_time = now.time_till_next_day_time(alarm_time_of_day)
        if alarm_next_trigger_time.in_ticks() == 0:
            alarm_next_trigger_time += TimeSpan(sim_ticks_per_day())

        repeat_interval = TimeSpan(sim_ticks_per_day())

        return cls.schedule_alarm(
            alarm_owner,
            alarm_next_trigger_time,
            on_alarm_triggered,
            time_until_repeat=repeat_interval,
            should_repeat=True,
            persist_across_zone_loads=persist_across_zone_loads
        )

    @classmethod
    def cancel_alarm(cls, alarm_handle: CommonAlarmHandle) -> bool:
        """cancel_alarm(alarm_handle)

        Cancel an alarm so that it will no longer occur.

        :param alarm_handle: The handle of the alarm to cancel.
        :type alarm_handle: CommonAlarmHandle
        :return: True, if the alarm was cancelled successfully. False, if not.
        :rtype: bool
        """
        if alarm_handle is None:
            return False
        alarm_handle.cancel()
        return True
