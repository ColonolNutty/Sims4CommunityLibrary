"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any, Type, List

from sims4.tuning.instance_manager import InstanceManager
from sims4communitylib.logging._has_s4cl_log import _HasS4CLLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.services.resources.modification_handlers.common_instance_manager_modification_handler import \
    CommonInstanceManagerModificationHandler
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


class CommonInstanceManagerModificationRegistry(CommonService, _HasS4CLLog):
    """A registry containing handlers that manipulate and modify instance managers.

    """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_instance_manager_modification_registry'

    def __init__(self) -> None:
        super().__init__()
        self._handlers: List[CommonInstanceManagerModificationHandler] = list()

    def _try_modify(self, instance_manager: InstanceManager):
        for handler in self._handlers:
            try:
                if handler.should_apply_modifications(instance_manager):
                    handler.apply_modifications(instance_manager)
            except Exception as ex:
                self.log.format_error_with_message('An error occurred while applying modification.', handler=handler, exception=ex)

    def register_handler(self, handler: CommonInstanceManagerModificationHandler):
        """register_handler(handler)

        Manually register a handler.

        .. note:: It is recommended to decorate classes with :func:`~register_modification_handler`\
            instead of manually registering handlers.

        :param handler: The handler being registered.
        :type handler: CommonInstanceManagerModificationHandler
        """
        if handler in self._handlers:
            return
        self._handlers.append(handler)

    @staticmethod
    def register_modification_handler() -> Callable[..., Any]:
        """register_modification_handler()

        Decorate a class with this to register that class as a modification handler.
        """
        def _wrapper(_handler: Type[CommonInstanceManagerModificationHandler]) -> Type[CommonInstanceManagerModificationHandler]:
            if not issubclass(_handler, CommonInstanceManagerModificationHandler):
                raise AssertionError(
                    f'{_handler} is not an instance of {CommonInstanceManagerModificationHandler.__name__}')
            CommonInstanceManagerModificationRegistry().register_handler(_handler())
            return _handler
        return _wrapper


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), InstanceManager, InstanceManager.load_data_into_class_instances.__name__, handle_exceptions=False)
def _common_modify_instance_manager_on_load_data(original, self: InstanceManager, *_, **__) -> Any:
    result = original(self, *_, **__)
    CommonInstanceManagerModificationRegistry()._try_modify(self)
    return result
