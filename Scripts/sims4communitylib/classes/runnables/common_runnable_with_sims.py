"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

from typing import Union, List, Tuple, TypeVar, Generic

from sims.sim import Sim
from sims4communitylib.classes.runnables.common_runnable import CommonRunnable
from sims4communitylib.classes.runnables.contexts.common_runnable_context_with_sims import CommonRunnableContextWithSims
from sims4communitylib.classes.runnables.contexts.common_runnable_sim_context import CommonRunnableSimContext
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.enumtypes.common_int_flags import CommonIntFlags
from sims4communitylib.mod_support.mod_identity import CommonModIdentity

CommonRunnableContextWithSimsType = TypeVar('CommonRunnableContextWithSimsType', bound=CommonRunnableContextWithSims)
CommonRunnableSimContextType = TypeVar('CommonRunnableSimContextType', bound=CommonRunnableSimContext)


class CommonRunnableWithSims(CommonRunnable[CommonRunnableContextWithSimsType], Generic[CommonRunnableContextWithSimsType, CommonRunnableSimContextType]):
    """CommonRunnableWithSims()

    This class is used when you want to have something reoccurring again and again. Specifically when it involves something reoccurring for Sims again and again.

    :param context: A context containing information about the runnable as well as actions the runnable should perform, including which Sims to perform the actions with.
    :type context: CommonRunnableContextWithSims
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def invalid_stop_reason(self) -> Union[int, CommonInt, CommonIntFlags]:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def unknown_stop_reason(self) -> Union[int, CommonInt, CommonIntFlags]:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def cancel_stop_reason(self) -> Union[int, CommonInt, CommonIntFlags]:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def start_after_wait_reason(self) -> Union[int, CommonInt, CommonIntFlags]:
        raise NotImplementedError()

    def _is_restart_stop_reason(self, stop_reason: Union[int, CommonInt, CommonIntFlags]) -> bool:
        raise NotImplementedError()

    def _is_end_stop_reason(self, stop_reason: Union[int, CommonInt, CommonIntFlags]) -> bool:
        raise NotImplementedError()

    def __init__(self, context: CommonRunnableContextWithSimsType) -> None:
        super().__init__(context)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def context(self) -> CommonRunnableContextWithSimsType:
        return self._context

    @context.setter
    def context(self, value: CommonRunnableContextWithSimsType):
        self._context = value

    @property
    def sim_contexts(self) -> List[CommonRunnableSimContextType]:
        """A collection of Sim Contexts within the context."""
        return self.context.sim_contexts

    @property
    def sims_as_sim_id(self) -> Tuple[int]:
        """Retrieves a collection of decimal identifiers for the Sims."""
        return self.context.sims_as_sim_id

    @property
    def sims_as_sim_info(self) -> Tuple[SimInfo]:
        """Retrieves a collection of Sim Info for the Sims."""
        return self.context.sims_as_sim_info

    @property
    def sims_as_sim(self) -> Tuple[Sim]:
        """Retrieves a collection of Sim Instances for the Sims."""
        return self.context.sims_as_sim

    def has_sim_context(self, sim_info: SimInfo) -> bool:
        """has_sim_context(sim_info)

        Determine if a Sim Context exists for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if a Sim Context exists for the Sim. False, if not.
        :rtype: bool
        """
        return self.context.has_sim_context(sim_info)

    def get_sim_context(self, sim_info: SimInfo) -> Union[CommonRunnableSimContextType, None]:
        """get_sim_context(sim_info)

        Retrieve the Sim Context for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The Sim Context matching the Sim or None if no context matches.
        :rtype: Union[CommonRunnableSimContext, None]
        """
        return self.context.get_sim_context(sim_info)

    def add_sim_context(self, sim_context: CommonRunnableSimContextType, add_reason: Union[int, CommonInt, CommonIntFlags], restart_after_add: bool = True) -> CommonExecutionResult:
        """add_sim_context(sim_context, add_reason, restart_after_add=True)

        Add a Sim Context to the context.

        :param sim_context: A Sim Context.
        :type sim_context: CommonRunnableSimContextType
        :param add_reason: The reason the Sim Context is being added.
        :type add_reason: Union[int, CommonInt, CommonIntFlags]
        :param restart_after_add: If True, the Runnable will be restarted after the Sim is added. If False, the Runnable will not be restarted after add. Default is True.
        :type restart_after_add: bool, optional
        :return: True, if the context was added successfully. False, if not.
        :rtype: CommonExecutionResult
        """
        if self.has_sim_context(sim_context.sim_info):
            return CommonExecutionResult(False, reason=f'Sim {sim_context.sim_info} is already a part of the runnable. {self.__class__.__name__}', hide_tooltip=True)
        add_result = self.context.add_sim_context(sim_context)
        if not add_result:
            return add_result
        if restart_after_add:
            return self.restart(add_reason)
        return CommonExecutionResult.TRUE

    def remove_sim_context(self, sim_context: CommonRunnableSimContextType, remove_reason: Union[int, CommonInt, CommonIntFlags], *_, restart_after_remove: bool = True, **__) -> CommonExecutionResult:
        """remove_sim_context(sim_context, remove_reason, restart_after_remove=True)

        Remove a Sim Context from the context.

        :param sim_context: A Sim Context.
        :type sim_context: CommonRunnableSimContextType
        :param remove_reason: The reason the context is being removed.
        :type remove_reason: Union[int, CommonInt, CommonIntFlags]
        :param restart_after_remove: If True, the Runnable will be restarted after the Sim is removed. If False, the Runnable will not be restarted after remove. Default is True.
        :type restart_after_remove: bool, optional
        :return: True, if the Sim Context was removed from the context successfully. False, if not.
        :rtype: CommonExecutionResult
        """
        remove_result = self.context.remove_sim_context(sim_context, remove_reason, *_, restart_after_remove=restart_after_remove, **__)
        if not remove_result:
            return remove_result
        if restart_after_remove:
            return self.restart(remove_reason)
        return CommonExecutionResult.TRUE

    def remove_sim(self, sim_info: SimInfo, remove_reason: Union[int, CommonInt, CommonIntFlags], *_, restart_after_remove: bool = False, **__) -> CommonExecutionResult:
        """remove_sim(sim_info, remove_reason)

        Remove a Sim from the context.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param remove_reason: The reason the Sim is being removed.
        :type remove_reason: Union[int, CommonInt, CommonIntFlags]
        :param restart_after_remove: If True, the Runnable will be restarted after the Sim is removed. If False, the Runnable will not be restarted after remove. Default is True.
        :type restart_after_remove: bool, optional
        :return: True, if the sim was removed from the context successfully. False, if not.
        :rtype: CommonExecutionResult
        """
        sim_context = self.get_sim_context(sim_info)
        if sim_context is None:
            return CommonExecutionResult(False, reason=f'Sim {sim_info} did not have a Sim context! {self.__class__.__name__}', hide_tooltip=True)
        return self.remove_sim_context(sim_context, remove_reason, *_, restart_after_remove=restart_after_remove, **__)
