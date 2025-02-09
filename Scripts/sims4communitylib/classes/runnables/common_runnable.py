"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

from typing import Union, Any, TypeVar, Generic

from sims4communitylib.classes.runnables.contexts.common_runnable_context import CommonRunnableContext
from sims4communitylib.enums.common_runnable_state_type import CommonRunnableStateType
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.time.common_alarm_handle import CommonAlarmHandle
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.enumtypes.common_int_flags import CommonIntFlags
from sims4communitylib.events.interval.common_interval_event_service import CommonIntervalEventRegistry, \
    CommonIntervalDispatcher
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from sims4communitylib.utils.time.common_alarm_utils import CommonAlarmUtils

CommonRunnableContextType = TypeVar('CommonRunnableContextType', bound=CommonRunnableContext)


class CommonRunnable(HasClassLog, Generic[CommonRunnableContextType]):
    """CommonRunnable()

    This class is used when you want to have something reoccurring again and again.

    :param context: A context containing information about the runnable as well as actions the runnable should perform.
    :type context: CommonRunnableContext
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    def __init__(self, context: CommonRunnableContextType) -> None:
        self._update_alarm: Union[CommonAlarmHandle, None] = None
        self._update_dispatcher: Union[CommonIntervalDispatcher, None] = None
        self._context = context
        self._has_initial_started = False
        self._change_state(CommonRunnableStateType.STOPPED)
        self.milliseconds_per_update = 1000
        # This is used when we are expecting a reset to happen, and we don't want to cancel the runnable.
        self._expect_reset = False
        self._is_ended = False
        self._await_stop = False
        self._await_stop_reason = self.unknown_stop_reason
        self._updating = False
        super().__init__()

    @property
    def context(self) -> CommonRunnableContextType:
        """A context containing information about the runnable as well as actions the runnable should perform."""
        return self._context

    @context.setter
    def context(self, value: CommonRunnableContextType):
        self._context = value

    @property
    def is_running(self) -> bool:
        """The runnable is running."""
        return self._current_state == CommonRunnableStateType.RUNNING

    @property
    def is_starting(self) -> bool:
        """The runnable is starting."""
        return self._current_state == CommonRunnableStateType.STARTING

    @property
    def is_waiting_for_start(self) -> bool:
        """The runnable is waiting to start."""
        return self._current_state == CommonRunnableStateType.WAITING_TO_START

    @property
    def is_stopping(self) -> bool:
        """The runnable is stopping."""
        return self._current_state == CommonRunnableStateType.STOPPING

    @property
    def is_stopped(self) -> bool:
        """The runnable is stopped."""
        return self._current_state == CommonRunnableStateType.STOPPED

    def _start_updater(self, milliseconds_per_update: int) -> None:
        self._stop_updater()
        self._updating = False

        def _start_update(_: Any) -> None:
            if self._updating:
                return
            self._updating = True

            def _run_update() -> None:
                try:
                    self.update(milliseconds_per_update)
                finally:
                    self._updating = False

            _run_update()

        if self.context.should_run_on_game_time:
            sim_minutes = int(CommonTimeUtils.convert_milliseconds_to_seconds(milliseconds_per_update))
            time_until_update = CommonTimeUtils.create_interval_from_sim_minutes(sim_minutes)
            self._update_alarm = CommonAlarmUtils.schedule_alarm(
                self,
                time_until_update,
                _start_update,
                should_repeat=True,
                time_until_repeat=time_until_update
            )
        else:
            self._update_dispatcher = CommonIntervalEventRegistry()._add_tracker(
                self.mod_identity,
                milliseconds_per_update,
                lambda *_, **__: _start_update(None)
            )

    def _stop_updater(self) -> None:
        if self._update_dispatcher is not None:
            if self._update_dispatcher in CommonIntervalEventRegistry()._registered_interval_trackers:
                self.log.format_with_message('Removing update dispatcher from interval trackers.')
                CommonIntervalEventRegistry()._registered_interval_trackers.remove(self._update_dispatcher)
            self._update_dispatcher = None

        if self._update_alarm is not None:
            CommonAlarmUtils.cancel_alarm(self._update_alarm)
            self._update_alarm = None

    @property
    def milliseconds_per_update(self) -> int:
        """The number of milliseconds between updates."""
        return self._milliseconds_per_update

    @milliseconds_per_update.setter
    def milliseconds_per_update(self, value: int):
        self._milliseconds_per_update = value
        self._start_updater(value)

    def _change_state(self, new_state: CommonRunnableStateType):
        self._current_state = new_state

    def start(self, *_, **__) -> CommonExecutionResult:
        """start(*_, **__)

        Start the runnable.

        :return: True, if the runnable has successfully been started. False, if not.
        :rtype: CommonExecutionResult
        """
        try:
            self._is_ended = False
            if self.is_starting:
                self.log.debug('Failed to start runnable, Already starting!')
                return CommonExecutionResult(True, reason=f'Runnable is already starting {self.__class__.__name__}', hide_tooltip=True)

            on_initialize_result = self._on_initialize(*_, **__)
            if not on_initialize_result:
                self.log.format_error_with_message('On Initialize Failed.', runnable=self, result=on_initialize_result)
                self.stop(self.invalid_stop_reason, force_stop=True)
                return on_initialize_result

            self.log.debug('Attempting to start runnable.')
            if self.is_running:
                self.log.debug('Success, runnable has already been started.')
                return CommonExecutionResult.TRUE

            is_waiting_to_start = self.is_waiting_for_start
            self._change_state(CommonRunnableStateType.STARTING)

            on_setup_result = self._on_setup(*_, is_waiting_to_start=is_waiting_to_start, **__)
            if not on_setup_result:
                self.log.format_error_with_message('On Setup Failed', runnable=self, context=self.context, result=on_setup_result)
                self.stop(self.invalid_stop_reason, force_stop=True)
                return on_setup_result

            if self.is_waiting_for_start:
                self.log.format_with_message('Runnable is waiting to start.')
                return CommonExecutionResult.TRUE

            self._start_updater(self.milliseconds_per_update)

            if not self._has_initial_started:
                on_initial_start_result = self._on_initial_start(*_, **__)
                if not on_initial_start_result:
                    self.log.format_error_with_message('On Initial Start Failed.', result=on_initial_start_result)
                    self.stop(self.invalid_stop_reason, force_stop=True)
                    return on_initial_start_result

            on_start_result = self._on_start()
            if not on_start_result:
                self.log.format_error_with_message('On Start Failed.', result=on_start_result)
                return on_start_result

            self.log.debug('Finished starting runnable.')
            self._change_state(CommonRunnableStateType.RUNNING)
            self._has_initial_started = True
            return CommonExecutionResult.TRUE
        except Exception as ex:
            self.log.error('Error occurred while starting runnable.', exception=ex)
            self._expect_reset = False
            self.stop(self.invalid_stop_reason, force_stop=True)
            return CommonExecutionResult(False, reason=f'An error occurred while starting {self.__class__.__name__} {ex}.', hide_tooltip=True)

    # noinspection PyUnusedLocal
    def should_update(self, milliseconds_since_last_update: int) -> CommonExecutionResult:
        """should_update(milliseconds_since_last_update)

        Determine if the runnable should update.

        :param milliseconds_since_last_update: The number of milliseconds since the last update.
        :type milliseconds_since_last_update: int
        :return: True, if the update should continue. False, if not.
        :rtype: CommonExecutionResult
        """
        return CommonExecutionResult.TRUE

    def update(self, milliseconds_since_last_update: int, *_, **__) -> CommonExecutionResult:
        """update(milliseconds_since_last_update, *_, **__)

        Update the runnable.

        .. note:: This function is invoked automatically by the runnable itself.

        :param milliseconds_since_last_update: The number of milliseconds since the last update.
        :type milliseconds_since_last_update: int
        :return: True, if the update is successful. False, if not.
        :rtype: CommonExecutionResult
        """
        try:
            if self._is_ended:
                self.verbose_log.debug('Failed to update runnable, it has already ended.')
                return CommonExecutionResult(False, reason=f'Runnable has already ended. {self.__class__.__name__}', hide_tooltip=True)

            if self._await_stop:
                self.verbose_log.debug('Failed to update runnable, it is awaiting a stop.')
                self.stop(self._await_stop_reason)
                return CommonExecutionResult(False, reason=f'Runnable is waiting to stop {self.__class__.__name__}.', hide_tooltip=True)

            if self.is_waiting_for_start:
                if self._has_finished_waiting_to_start(milliseconds_since_last_update, *_, **__):
                    self.log.format_with_message('Finished waiting to start. Attempting to start runnable now.')
                    self.restart(self.start_after_wait_reason)
                    return CommonExecutionResult(True, reason=f'Finished Waiting for runnable to begin. We still do not want to update. {self.__class__.__name__}', hide_tooltip=True)

                on_continue_waiting_result = self._on_continue_waiting_to_start()
                if not on_continue_waiting_result:
                    self.log.format_error_with_message('On Continue Waiting To Start Failed.', result=on_continue_waiting_result)
                    self.stop(self.invalid_stop_reason, force_stop=True)
                    return on_continue_waiting_result

                self.log.format_with_message('Waiting for runnable to start.')
                return CommonExecutionResult(True, reason=f'Waiting for runnable to start. {self.__class__.__name__}', hide_tooltip=True)

            if not self.is_running or self.is_stopping or self.is_stopped:
                self.verbose_log.format_with_message('Failed to update runnable, it is either not running, it is stopping, or it is stopped.', running=self.is_running, stopping=self.is_stopping)
                return CommonExecutionResult(False, reason=f'Runnable is not running. {self.__class__.__name__}', hide_tooltip=True)

            self.verbose_log.format_with_message(
                'Updating Runnable',
                class_name=self.__class__.__name__,
                milliseconds_since_last_update=milliseconds_since_last_update
            )
            should_update_result = self.should_update(milliseconds_since_last_update)
            if not should_update_result:
                self.verbose_log.format_with_message('Skipping update due to request to skip update.', result=should_update_result)
                return CommonExecutionResult.TRUE

            on_update_result = self._on_update(milliseconds_since_last_update)
            if not on_update_result:
                self.log.format_error_with_message('On Update Failed', result=on_update_result)
                self.stop(self.invalid_stop_reason, force_stop=True)

            return on_update_result
        except Exception as ex:
            self.log.error('Error occurred while updating runnable.', exception=ex)
            self._expect_reset = False
            self.stop(self.invalid_stop_reason, force_stop=True)
            return CommonExecutionResult(False, reason=f'An error occurred while updating runnable {self.__class__.__name__} {ex}.', hide_tooltip=True)

    def stop(self, stop_reason: Union[int, CommonInt, CommonIntFlags], *_, force_stop: bool = False, **__) -> CommonExecutionResult:
        """stop(stop_reason, force_stop=False)

        Stop the runnable.

        :param stop_reason: The reason the runnable is being stopped for.
        :type stop_reason: Union[int, CommonInt, CommonIntFlags]
        :param force_stop: If True, the is_stopping state will not be checked and the runner will be forced to stop. Default is False.
        :type force_stop: bool, optional
        :return: True, if the runnable has been stopped successfully. False, if not.
        :rtype: CommonExecutionResult
        """
        try:
            if not force_stop and self.is_stopping:
                self.log.format_with_message('Failed to stop, runnable is already stopping.', stop_reason=stop_reason)
                return CommonExecutionResult(True, reason=f'Runnable is already stopping. {self.__class__.__name__}', hide_tooltip=True)

            if self._expect_reset:
                self.log.format_with_message('Failed to stop, runnable is expected to be restarting.', stop_reason=stop_reason)
                return CommonExecutionResult.TRUE

            if stop_reason == self.invalid_stop_reason and not self._has_initial_started:
                stop_reason = self.cancel_stop_reason

            self._change_state(CommonRunnableStateType.STOPPING)
            self.log.format_with_message('Stopping runnable', stop_reason=stop_reason)

            on_stop_result = self._on_stop(stop_reason, *_, force_stop=force_stop, **__)
            if not on_stop_result:
                self.log.format_error_with_message('On Stop Failed.', result=on_stop_result)
                return on_stop_result

            if self._is_restart_stop_reason(stop_reason):
                self.log.format_with_message('Stopping due to a restart.', stop_reason=stop_reason)
                on_restart_result = self._on_restart(stop_reason)
                if not on_restart_result:
                    self.log.format_error_with_message('On Restart Failed.', result=on_restart_result)
                return CommonExecutionResult.TRUE

            self._stop_updater()

            self._is_ended = True

            on_end_result = self._on_end(stop_reason, *_, force_stop=force_stop, **__)
            if not on_end_result:
                self.log.format_with_message('On End Failed.', result=on_end_result)
                return on_end_result

            self.log.format_with_message('Done ending runnable.', stop_reason=stop_reason)
            return on_end_result
        except Exception as ex:
            self.log.error('Error occurred while stopping runnable.', exception=ex)
            self._expect_reset = False
            if stop_reason != self.invalid_stop_reason:
                self.stop(self.invalid_stop_reason, force_stop=True)
            return CommonExecutionResult(False, reason=f'An error occurred while stopping runnable {self.__class__.__name__} {ex}.', hide_tooltip=True)
        finally:
            self._change_state(CommonRunnableStateType.STOPPED)
            self._expect_reset = False

    def restart(self, restart_reason: Union[int, CommonInt, CommonIntFlags], *_, **__) -> CommonExecutionResult:
        """restart(restart_reason, *_, **__)

        Restart the runnable.

        :param restart_reason: The reason for the restart.
        :type restart_reason: Union[int, CommonInt, CommonIntFlags]
        :return: True, if the runnable has been restarted successfully. False, if not.
        :rtype: CommonExecutionResult
        """
        self.log.format_with_message('Restarting runnable', restart_reason=restart_reason)
        self.stop(restart_reason)
        return self.start()

    @property
    def invalid_stop_reason(self) -> Union[int, CommonInt, CommonIntFlags]:
        """A reason for the runnable to be stopped for invalid reasons."""
        raise NotImplementedError()

    @property
    def unknown_stop_reason(self) -> Union[int, CommonInt, CommonIntFlags]:
        """A reason for the runnable to be stopped for unknown reasons."""
        raise NotImplementedError()

    @property
    def cancel_stop_reason(self) -> Union[int, CommonInt, CommonIntFlags]:
        """A reason for the runnable to be stopped for a cancel reasons."""
        raise NotImplementedError()

    @property
    def start_after_wait_reason(self) -> Union[int, CommonInt, CommonIntFlags]:
        """A reason for the runnable to be stopped after waiting for it to start."""
        raise NotImplementedError()

    def _is_restart_stop_reason(self, stop_reason: Union[int, CommonInt, CommonIntFlags]) -> bool:
        raise NotImplementedError()

    def _is_end_stop_reason(self, stop_reason: Union[int, CommonInt, CommonIntFlags]) -> bool:
        raise NotImplementedError()

    def _on_start(self, *_, **__) -> CommonExecutionResult:
        return CommonExecutionResult.TRUE

    def _on_update(self, milliseconds_since_last_update: int, *_, **__) -> CommonExecutionResult:
        return self.context.update(milliseconds_since_last_update, *_, **__)

    # noinspection PyUnusedLocal
    def _on_restart(self, restart_reason: Union[int, CommonInt, CommonIntFlags], *_, **__) -> CommonExecutionResult:
        return self.context.restart(restart_reason, *_, **__)

    # noinspection PyUnusedLocal
    def _on_stop(self, stop_reason: Union[int, CommonInt, CommonIntFlags], *_, force_stop: bool = False, **__) -> CommonExecutionResult:
        return CommonExecutionResult.TRUE

    def _on_end(self, stop_reason: Union[int, CommonInt, CommonIntFlags], *_, force_stop: bool = False, **__) -> CommonExecutionResult:
        return self.context.teardown(stop_reason, *_, force_stop, **__)

    # noinspection PyUnusedLocal
    def _has_finished_waiting_to_start(self, milliseconds_since_last_update: int, *_, **__) -> bool:
        return True

    def _on_continue_waiting_to_start(self, *_, **__) -> CommonExecutionResult:
        return CommonExecutionResult.TRUE

    def _on_initialize(self, *_, **__) -> CommonExecutionResult:
        return self.context.initialize(*_, **__)

    def _on_initial_start(self, *_, **__) -> CommonExecutionResult:
        return CommonExecutionResult.TRUE

    def _on_setup(self, *_, is_waiting_to_start: bool = False, **__) -> CommonExecutionResult:
        return self.context.setup(*_, is_waiting_to_start=is_waiting_to_start, **__)

    def __eq__(self, other: 'CommonRunnable') -> bool:
        if not isinstance(other, CommonRunnable):
            return False
        return self.context.__eq__(other.context)

    def __repr__(self) -> str:
        return repr(self.context)

    def __str__(self) -> str:
        return str(self.context)
