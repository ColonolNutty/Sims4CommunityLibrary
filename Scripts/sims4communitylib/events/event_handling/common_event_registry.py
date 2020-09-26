"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from queue import Queue
from threading import Thread
from typing import List, Callable, Any, Union
from sims4communitylib.events.event_handling.common_event import CommonEvent
from sims4communitylib.events.event_handling.common_event_handler import CommonEventHandler
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from zone import Zone


class CommonEventRegistry(CommonService):
    """Register event listeners and dispatch events to any that are registered.

    """

    def __init__(self) -> None:
        self._event_handlers: List[CommonEventHandler] = []
        self._event_queue = Queue()
        self._running = True
        self._number_of_worker_threads = 5
        for i in range(self._number_of_worker_threads):
            worker = Thread(target=self._work_the_queue, args=(self._event_queue,))
            worker.daemon = True
            worker.start()

    @staticmethod
    def handle_events(mod_identifier: Union[str, CommonModIdentity]) -> Callable[[Callable[[CommonEvent], bool]], Callable[[CommonEvent], bool]]:
        """handle_events(mod_identifier)

        Decorate functions with this static method to register that function to handle an event.

        :warning:: Event functions MUST be decorated with staticmethod and must only have a single argument with the name 'event_data' (Errors will be thrown upon loading the game otherwise)

        :param mod_identifier: The name or identity of the mod the class is being registered for.
        :type mod_identifier: Union[str, CommonModIdentity]
        :return: A callable function wrapped to handle events.
        :rtype: Callable[[Callable[[CommonEvent], bool]], Callable[[CommonEvent], bool]]
        """
        def _wrapper(event_function: Callable[[CommonEvent], bool]) -> Callable[..., Any]:
            CommonEventRegistry.get()._register_event_handler(mod_identifier, event_function)
            return event_function
        return _wrapper

    def _register_event_handler(self, mod_identifier: Union[str, CommonModIdentity], event_function: Callable[[CommonEvent], bool]):
        event_handler = CommonEventHandler(mod_identifier, event_function)
        self._event_handlers.append(event_handler)

    def stop(self) -> None:
        """stop()

        Stop dispatching events.
        """
        self._running = False

    def _should_continue_running(self) -> bool:
        return self._running

    def _work_the_queue(self, event_queue: Queue):
        while self._should_continue_running():
            (event, on_complete) = event_queue.get()
            result = self._dispatch(event)
            if on_complete is not None:
                on_complete(result)
            event_queue.task_done()

    def dispatch(self, event: CommonEvent) -> bool:
        """dispatch(event)

        Dispatch an event to any event handlers listening for it.

        .. note:: If any listeners return False or None when they handle the event, the total result of dispatch will be False as well.

        :param event: An instance of an Event to dispatch to listeners.
        :type event: CommonEvent
        :return: True, if the Event was dispatched to all listeners successfully. False, if any listeners failed to handle the event.
        :rtype: bool
        """
        return self._dispatch(event)

    def dispatch_async(self, event: CommonEvent, on_complete: Callable[[bool], Any]=None) -> bool:
        """dispatch_async(event, on_complete=None)

        Dispatch an event asynchronously and perform a callback upon it's completion.

        :param event: An instance of an Event to dispatch to listeners.
        :type event: CommonEvent
        :param on_complete: If provided, when the event has finished being dispatched, this callback will be invoked with the result. Default is None.
        :type on_complete: Callable[[bool], Any], optional
        :return: True will always be returned.
        :rtype: bool
        """
        self._event_queue.put((event, on_complete))
        return True

    def _dispatch(self, event: CommonEvent) -> bool:
        event_handlers = list(self._event_handlers)
        result = True
        try:
            for event_handler in event_handlers:
                if not event_handler.can_handle_event(event):
                    continue
                try:
                    handle_result = event_handler.handle_event(event)
                    if not handle_result:
                        result = False
                except Exception as ex:
                    CommonExceptionHandler.log_exception(event_handler.mod_name, 'Error occurred when attempting to handle event type \'{}\' via event handler \'{}\''.format(type(event), str(event_handler)), exception=ex)
                    continue
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to dispatch event \'{}\''.format(event), exception=ex)
            return False
        return result

    @staticmethod
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, Zone, Zone.on_teardown.__name__)
    def _common_stop_dispatching_events_on_zone_teardown(original, self: Zone, client):
        CommonEventRegistry().stop()
        result = original(self, client)
        return result
