"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

from typing import Union, Dict, Any, Tuple

from sims4communitylib.classes.runnables.contexts.common_runnable_context import CommonRunnableContext
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.sim_type import CommonSimType
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonRunnableSimContext(CommonRunnableContext):
    """CommonRunnableSimContext(sim_info)

    A context used by a runnable that contains information about a Sim.

    :param sim_info: The Sim the context is for.
    :type sim_info: SimInfo
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    def __init__(self, sim_info: SimInfo):
        super().__init__()
        self._sim_info = sim_info
        self._sim_full_name = CommonSimNameUtils.get_full_name(self._sim_info)
        self._sim_type = CommonSimTypeUtils.determine_sim_type(self._sim_info)

    @property
    def sim_info(self) -> SimInfo:
        """The Sim this context is for."""
        return self._sim_info

    @property
    def sim_full_name(self) -> str:
        """The full name of the Sim this context is for."""
        return self._sim_full_name

    @property
    def sim_id(self) -> int:
        """The decimal identifier of the Sim this context is for."""
        return CommonSimUtils.get_sim_id(self._sim_info)

    @property
    def sim(self) -> Sim:
        """The instance of the Sim this context is for."""
        return CommonSimUtils.get_sim_instance(self._sim_info)

    @property
    def sim_type(self) -> CommonSimType:
        """The type of Sim."""
        return self._sim_type

    def _initialize(self, *_, **__) -> CommonExecutionResult:
        raise NotImplementedError()

    def _setup(self, *_, **__) -> CommonExecutionResult:
        raise NotImplementedError()

    def _update(self, milliseconds_since_last_update: int, *_, **__) -> CommonExecutionResult:
        raise NotImplementedError()

    def _teardown(self, teardown_reason: Union[int, CommonInt], *_, **__) -> CommonExecutionResult:
        raise NotImplementedError()

    def _clone_args(self, *_, **__) -> Tuple[Any]:
        result: Tuple[Any, ...] = (
            self.sim_info,
            *super()._clone_args(*_, **__)
        )
        return result

    def _serialize_data(self, data: Dict[str, Any]):
        super()._serialize_data(data)
        data['sim_id'] = self.sim_id

    @classmethod
    def _deserialize_args(cls, data: Union[str, Dict[str, Any]]) -> Union[Tuple[Any], None]:
        sim_id = data.get('sim_id', None)
        if sim_id is None:
            return None

        deserialized_args = super()._deserialize_args(data)
        if deserialized_args is None:
            return None

        sim_info = CommonSimUtils.get_sim_info(sim_id)
        if sim_info is None:
            return None

        result: Tuple[Any, ...] = (
            sim_info,
            *deserialized_args,
        )
        return result

    def __gt__(self, other: 'CommonRunnableSimContext') -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.sim_id > other.sim_id

    def __lt__(self, other: 'CommonRunnableSimContext') -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.sim_id < other.sim_id

    def __eq__(self, other: 'CommonRunnableSimContext') -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.sim_info is other.sim_info

    def __hash__(self) -> int:
        return self.sim_id

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        sim_type_name = self.sim_type.name
        str_extras = self._get_str()
        return f'<[CRSC] {self.sim_info} ST: {sim_type_name} {str_extras}>'
