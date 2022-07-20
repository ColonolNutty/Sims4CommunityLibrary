"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

from typing import Union, Tuple, Any, Dict

from sims4communitylib.classes.runnables.contexts.common_runnable_context import CommonRunnableContext
from objects.game_object import GameObject
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils


class CommonRunnableObjectContext(CommonRunnableContext):
    """CommonRunnableObjectContext(game_object)

    A context used by a runnable that contains information about an Object.

    :param game_object: The game object the context is for.
    :type game_object: Union[GameObject, None]
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    def __init__(
        self,
        game_object: Union[GameObject, None]
    ):
        super().__init__()

        if game_object is not None and CommonTypeUtils.is_game_object(game_object):
            self._game_object = game_object
        else:
            self._game_object = None

        self._game_object_id = -1
        if self._game_object is not None:
            self._game_object_id = CommonObjectUtils.get_object_id(self._game_object)

    @property
    def game_object(self) -> Union[GameObject, None]:
        """The Game Object this context is for."""
        return self._game_object

    @property
    def game_object_id(self) -> int:
        """The decimal identifier of the Game Object this context is for."""
        return self._game_object_id

    def _initialize(self, *_, **__) -> CommonExecutionResult:
        return CommonExecutionResult.TRUE

    def _setup(self, *_, **__) -> CommonExecutionResult:
        raise NotImplementedError()

    def _update(self, milliseconds_since_last_update: int, *_, **__) -> CommonExecutionResult:
        raise NotImplementedError()

    def _teardown(self, teardown_reason: Union[int, CommonInt], *_, **__) -> CommonExecutionResult:
        raise NotImplementedError()

    def _clone_args(self, *_, **__) -> Tuple[Any]:
        result: Tuple[Any, ...] = (
            self.game_object,
            *super()._clone_args(*_, **__)
        )
        return result

    def _serialize_data(self, data: Dict[str, Any]):
        super()._serialize_data(data)
        if self.game_object_id != -1:
            data['object_id'] = self.game_object_id

    @classmethod
    def _deserialize_args(cls, data: Union[str, Dict[str, Any]]) -> Union[Tuple[Any], None]:
        object_id = data.get('object_id', None)
        if object_id is None:
            return None

        game_object = CommonObjectUtils.get_game_object(object_id)
        if game_object is None:
            return None

        deserialized_args = super()._deserialize_args(data)
        if deserialized_args is None:
            return None

        result: Tuple[Any, ...] = (
            game_object,
            *deserialized_args
        )
        return result

    def __gt__(self, other: 'CommonRunnableObjectContext') -> bool:
        if self.game_object is None:
            return False
        return self.game_object_id > other.game_object_id

    def __lt__(self, other: 'CommonRunnableObjectContext') -> bool:
        if self.game_object is None:
            return False
        return self.game_object_id < other.game_object_id

    def __eq__(self, other: 'CommonRunnableObjectContext') -> bool:
        if self.game_object is None:
            return False
        return self.game_object is other.game_object

    def __hash__(self) -> int:
        if self.game_object is None:
            return 0
        return self.game_object_id

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        extra_str = self._get_str()
        return f'<[CROC] {self.game_object} ({self.game_object_id}) {extra_str}>'
