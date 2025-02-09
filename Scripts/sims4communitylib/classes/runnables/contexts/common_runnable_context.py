"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

from typing import Union, Dict, Any, Tuple, TypeVar, Type

from sims4communitylib.classes.serialization.common_serializable import CommonSerializable
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.enumtypes.common_int_flags import CommonIntFlags
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity

CommonRunnableContextType = TypeVar('CommonRunnableContextType', bound="CommonRunnableContext")


class CommonRunnableContext(CommonSerializable, HasClassLog):
    """CommonRunnableContext()

    A context used by a runnable.
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    def __init__(self: CommonRunnableContextType) -> None:
        super().__init__()
        self._initialized = False
        self._total_milliseconds = 0

    @property
    def should_run_on_game_time(self) -> bool:
        """Determine if the context should be run using game time or if it should be run using real time."""
        return True

    @property
    def should_track_total_time(self) -> bool:
        """Determine if the total time in milliseconds should be tracked. Default is False."""
        return False

    @property
    def total_milliseconds(self) -> int:
        """A counter for the total number of milliseconds the context has been running for."""
        return self._total_milliseconds

    def clear_total_milliseconds(self) -> None:
        """clear_time_since_setup()

        Clear the total time passed since the context was set up.
        """
        self._total_milliseconds = 0

    def initialize(self, *_, **__) -> CommonExecutionResult:
        """initialize(*_, **__)

        Initialize the context.

        :return: True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        self.log.format_with_message('Attempting to initialize runnable context.')
        if self._initialized:
            self.log.format_with_message('Failed to initialize context. It was already initialized.')
            return CommonExecutionResult.TRUE
        initialize_result = self._initialize(*_, **__)
        if not initialize_result:
            self.log.format_with_message('Failed to initialize context.')
            return initialize_result
        self._initialized = True
        self.log.debug('Finished initializing context.')
        return CommonExecutionResult.TRUE

    def setup(self, *_, **__) -> CommonExecutionResult:
        """setup(*_, **__)

        Setup the context.

        :return: True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        self.log.format_with_message('Setting up context.')
        self.clear_total_milliseconds()
        return self._setup(*_, **__)

    # noinspection PyUnusedLocal
    def should_update(self, milliseconds_since_last_update: int, *_, **__) -> CommonExecutionResult:
        """should_update(milliseconds_since_last_update, *_, **__)

        Determine if the context should update.

        :param milliseconds_since_last_update: The number of milliseconds since the last update.
        :type milliseconds_since_last_update: int
        :return: True, if the context should update. False, if not.
        :rtype: CommonExecutionResult
        """
        return CommonExecutionResult.TRUE

    def update(self, milliseconds_since_last_update: int, *_, **__) -> CommonExecutionResult:
        """update(milliseconds_since_last_update, *_, **__)

        Update the context.

        :param milliseconds_since_last_update: The number of milliseconds since the last update.
        :type milliseconds_since_last_update: int
        :return: True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        should_update_result = self.should_update(milliseconds_since_last_update, *_, **__)
        if not should_update_result:
            return should_update_result.reverse_result()
        pre_update_result = self._pre_update(milliseconds_since_last_update, *_, **__)
        if not pre_update_result:
            return pre_update_result
        if self.should_track_total_time:
            self._total_milliseconds += milliseconds_since_last_update
        update_result = self._update(milliseconds_since_last_update, *_, **__)
        if not update_result:
            return update_result
        return self._post_update(milliseconds_since_last_update, *_, **__)

    def restart(self, restart_reason: Union[int, CommonInt, CommonIntFlags], *_, **__) -> CommonExecutionResult:
        """restart(restart_reason, *_, **__)

        Restart the context.

        :param restart_reason: The reason the context to be restarted.
        :type restart_reason: Union[int, CommonInt, CommonIntFlags]
        :return: True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        self.log.format_with_message(f'Restarting context. {self.__class__.__name__}', reason=restart_reason)
        return self._restart(restart_reason, *_, **__)

    def teardown(self, teardown_reason: Union[int, CommonInt, CommonIntFlags], *_, **__) -> CommonExecutionResult:
        """teardown(teardown_reason, *_, **__)

        Teardown the context.

        :param teardown_reason: The reason the context to be torn down.
        :type teardown_reason: Union[int, CommonInt, CommonIntFlags]
        :return: True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        self.log.format_with_message(f'Tearing down context. {self.__class__.__name__}', reason=teardown_reason)
        return self._teardown(teardown_reason, *_, **__)

    # -------------------------Hooks Start-------------------------

    def _initialize(self, *_, **__) -> CommonExecutionResult:
        raise NotImplementedError()

    def _setup(self, *_, **__) -> CommonExecutionResult:
        raise NotImplementedError()

    # noinspection PyUnusedLocal
    def _pre_update(self, milliseconds_since_last_update: int, *_, **__) -> CommonExecutionResult:
        return CommonExecutionResult.TRUE

    def _update(self, milliseconds_since_last_update: int, *_, **__) -> CommonExecutionResult:
        raise NotImplementedError()

    # noinspection PyUnusedLocal
    def _post_update(self, milliseconds_since_last_update: int, *_, **__) -> CommonExecutionResult:
        return CommonExecutionResult.TRUE

    def _restart(self, restart_reason: Union[int, CommonInt, CommonIntFlags], *_, **__) -> CommonExecutionResult:
        return CommonExecutionResult.TRUE

    def _teardown(self, teardown_reason: Union[int, CommonInt, CommonIntFlags], *_, **__) -> CommonExecutionResult:
        raise NotImplementedError()

    # -------------------------Hooks End-------------------------

    def clone(self: CommonRunnableContextType, *_, **__) -> CommonRunnableContextType:
        """clone(*_, **__)

        Create a clone of the context.

        :return: A cloned version of this context.
        :rtype: CommonRunnableContext
        """
        clone_args = self._clone_args(*_, **__)
        clone_kwargs = self._clone_kwargs(*_, **__)

        # noinspection PyArgumentList
        return self.__class__(
            *clone_args,
            **clone_kwargs
        )

    def _clone_args(self, *_, **__) -> Tuple[Any]:
        return tuple()

    def _clone_kwargs(self, *_, **__) -> Dict[str, Any]:
        return dict()

    # noinspection PyMissingOrEmptyDocstring
    def serialize(self) -> Union[str, Dict[str, Any]]:
        data = dict()
        self._serialize_data(data)
        return data

    def _serialize_data(self, data: Dict[str, Any]):
        pass

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def deserialize(cls: Type[CommonRunnableContextType], data: Union[str, Dict[str, Any]]) -> Union[CommonRunnableContextType, None]:
        deserialized_args = cls._deserialize_args(data)
        if deserialized_args is None:
            return None
        deserialized_kwargs = cls._deserialize_kwargs(data)
        if deserialized_kwargs is None:
            return None

        # noinspection PyArgumentList
        return cls(
            *deserialized_args,
            **deserialized_kwargs
        )

    @classmethod
    def _deserialize_args(cls, data: Union[str, Dict[str, Any]]) -> Union[Tuple[Any], None]:
        return tuple()

    # noinspection PyUnusedLocal
    @classmethod
    def _deserialize_kwargs(cls, data: Union[str, Dict[str, Any]]) -> Union[Dict[str, Any], None]:
        return dict()

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        str_extras = self._get_str()
        return f'<[CRC] {str_extras}>'

    def _get_str(self) -> str:
        return ''
