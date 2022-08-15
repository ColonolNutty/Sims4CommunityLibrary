"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

from typing import Union, Iterator, List, Tuple, Any, Dict, Type, TypeVar, Generic

from sims.sim import Sim
from sims4communitylib.classes.runnables.contexts.common_runnable_context import CommonRunnableContext
from sims4communitylib.classes.runnables.contexts.common_runnable_sim_context import CommonRunnableSimContext
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.enumtypes.common_int_flags import CommonIntFlags
from sims4communitylib.mod_support.mod_identity import CommonModIdentity

CommonRunnableSimContextType = TypeVar('CommonRunnableSimContextType', bound=CommonRunnableSimContext)


class CommonRunnableContextWithSims(CommonRunnableContext, Generic[CommonRunnableSimContextType]):
    """CommonRunnableContextWithSims()

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

    def __init__(self, sim_contexts: Iterator[CommonRunnableSimContextType]) -> None:
        super().__init__()
        self._sim_contexts = list(sim_contexts)

    @property
    def sim_contexts(self) -> List[CommonRunnableSimContextType]:
        """A collection of Sim Contexts within the context."""
        return self._sim_contexts

    @classmethod
    def sim_context_type(cls) -> Type['CommonRunnableSimContextType']:
        """The context type for Sim info."""
        raise NotImplementedError()

    @property
    def sims_as_sim_id(self) -> Tuple[int]:
        """Retrieves a collection of decimal identifiers for the Sims."""
        result: Tuple[int, ...] = tuple([context.sim_id for context in self.sim_contexts])
        return result

    @property
    def sims_as_sim_info(self) -> Tuple[SimInfo]:
        """Retrieves a collection of Sim Info for the Sims."""
        result: Tuple[SimInfo, ...] = tuple([context.sim_info for context in self.sim_contexts])
        return result

    @property
    def sims_as_sim(self) -> Tuple[Sim]:
        """Retrieves a collection of Sim Instances for the Sims."""
        result: Tuple[Sim, ...] = tuple([context.sim for context in self.sim_contexts])
        return result

    def has_sim_context(self, sim_info: SimInfo) -> bool:
        """has_sim_context(sim_info)

        Determine if a Sim Context exists for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if a Sim Context exists for the Sim. False, if not.
        :rtype: bool
        """
        return self.get_sim_context(sim_info) is not None

    def get_sim_context(self, sim_info: SimInfo) -> Union[CommonRunnableSimContextType, None]:
        """get_sim_context(sim_info)

        Retrieve the Sim Context for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The Sim Context matching the Sim or None if no context matches.
        :rtype: Union[CommonRunnableSimContextType, None]
        """
        self.verbose_log.format_with_message('Retrieving Sim Context.', sim=sim_info)
        for sim_context in self.sim_contexts:
            if sim_context.sim_info is sim_info:
                self.verbose_log.format_with_message('Found Sim Context.', sim=sim_info)
                return sim_context
        self.verbose_log.format_with_message('Failed to locate Sim Context.', sim=sim_info)
        return None

    def add_sim_context(self, sim_context: CommonRunnableSimContextType, *_, **__) -> CommonExecutionResult:
        """add_sim_context(sim_context, *_, **__)

        Add a Sim Context to the context.

        :param sim_context: A Sim Context.
        :type sim_context: CommonRunnableSimContextType
        :return: True, if the context was added successfully. False, if not.
        :rtype: CommonExecutionResult
        """
        self.log.format_with_message('Adding Sim Context.', sim_context=sim_context)
        if self.has_sim_context(sim_context.sim_info):
            self.log.format_with_message('Failed, the Sim was already a part of the context.', sim_context=sim_context)
            return CommonExecutionResult.TRUE

        result = sim_context.initialize(self, *_, **__)
        if not result:
            self.log.format_error_with_message('Failed to initialize Sim Context', context=sim_context, result=result)
            return result

        if sim_context not in self._sim_contexts:
            self._sim_contexts.append(sim_context)
        self.log.format_with_message('Finished adding Sim Context.', sim=sim_context)
        return CommonExecutionResult.TRUE

    def remove_sim_context(self, sim_context: CommonRunnableSimContextType, remove_reason: Union[int, CommonInt, CommonIntFlags], *_, **__) -> CommonExecutionResult:
        """remove_sim_context(sim_context, remove_reason, *_, **__)

        Remove a Sim Context from the context.

        :param sim_context: A Sim Context.
        :type sim_context: CommonRunnableSimContextType
        :param remove_reason: The reason the context is being removed.
        :type remove_reason: Union[int, CommonInt, CommonIntFlags]
        :return: True, if the Sim Context was removed from the context successfully. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_context is None:
            self.log.format_with_message('Sim Context was None.', sim_context=sim_context)
            return CommonExecutionResult.FALSE
        self.log.format_with_message('Removing Sim Context.', sim_context=sim_context)
        result = sim_context.teardown(remove_reason, self, *_, **__)
        if not result:
            self.log.format_error_with_message('Failed to tear down Sim Context', context=sim_context, result=result)
            return result
        if sim_context in self._sim_contexts:
            self.log.format_with_message('Found Sim Context, removing it now.', sim_context=sim_context)
            self._sim_contexts.remove(sim_context)
        self.log.format_with_message('Removed Sim Context.', sim_context=sim_context)
        return CommonExecutionResult.TRUE

    def remove_sim(self, sim_info: SimInfo, remove_reason: Union[int, CommonInt, CommonIntFlags], *_, **__) -> CommonExecutionResult:
        """remove_sim(sim_info, remove_reason, *_, **__)

        Remove a Sim from the context.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param remove_reason: The reason the Sim is being removed.
        :type remove_reason: Union[int, CommonInt, CommonIntFlags]
        :return: True, if the sim was removed from the context successfully. False, if not.
        :rtype: CommonExecutionResult
        """
        sim_context = self.get_sim_context(sim_info)
        if sim_context is None:
            self.log.format_with_message('No Sim Context found for Sim.', sim=sim_info)
            return CommonExecutionResult.FALSE
        remove_result = self.remove_sim_context(sim_context, remove_reason, *_, **__)
        if not remove_result:
            self.log.format_with_message('Failed to remove Sim Context.', sim=sim_info, result=remove_result)
            return remove_result
        return CommonExecutionResult.TRUE

    def _initialize(self, *_, **__) -> CommonExecutionResult:
        self.log.format_with_message('Initializing Sim Contexts.')
        for sim_context in self.sim_contexts:
            result = sim_context.initialize(self, *_, **__)
            if not result:
                self.log.format_error_with_message('Failed to initialize Sim Context.', sim_context=sim_context, result=result)
                return result
        self.log.format_with_message('Finished initializing Sim Context.')
        return CommonExecutionResult.TRUE

    def _setup(self, *_, **__) -> CommonExecutionResult:
        self.log.format_with_message('Setting Up Sim Contexts.')
        for sim_context in self.sim_contexts:
            result = sim_context.setup(self, *_, **__)
            if not result:
                self.log.format_error_with_message('Failed to setup Sim Context', sim_context=sim_context, result=result)
                return result
        self.log.format_with_message('Finished setting up Sim Contexts.')
        return CommonExecutionResult.TRUE

    def _update(self, milliseconds_since_last_update: int, *_, **__) -> CommonExecutionResult:
        self.log.format_with_message('Updating Sim Contexts.')
        for sim_context in self.sim_contexts:
            result = sim_context.update(milliseconds_since_last_update, self, *_, **__)
            if not result:
                self.log.format_error_with_message('Failed to update Sim Context.', sim_context=sim_context, result=result)
                return result
        self.log.format_with_message('Finished updating Sim Contexts.')
        return CommonExecutionResult.TRUE

    def _restart(self, restart_reason: Union[int, CommonInt, CommonIntFlags], *_, **__) -> CommonExecutionResult:
        self.log.format_with_message('Restarting Sim Contexts.', restart_reason=restart_reason)
        for sim_context in self.sim_contexts:
            result = sim_context.restart(restart_reason, self, *_, **__)
            if not result:
                self.log.format_error_with_message('Failed to restart Sim Context.', sim_context=sim_context, result=result)
                return result
        self.log.format_with_message('Finished restarting Sim Contexts.', restart_reason=restart_reason)
        return CommonExecutionResult.TRUE

    def _teardown(self, teardown_reason: Union[int, CommonInt, CommonIntFlags], *_, **__) -> CommonExecutionResult:
        self.log.format_with_message('Tearing Down Sim Contexts.', teardown_reason=teardown_reason)
        for sim_context in self.sim_contexts:
            try:
                result = sim_context.teardown(teardown_reason, self, *_, **__)
                if not result:
                    self.log.format_error_with_message('Failed to tear down Sim Context.', sim_context=sim_context, result=result)
                    return result
            except Exception as ex:
                self.log.format_error_with_message('An error occurred while tearing down Sim Context.', sim_context=sim_context, exception=ex)
                continue
        self.log.format_with_message('Finished Tearing Down Sim Contexts.')
        return CommonExecutionResult.TRUE

    def _clone_args(self, *_, **__) -> Tuple[Any]:
        sim_context_clones = [sim_context.clone(*_, **__) for sim_context in self.sim_contexts]
        result: Tuple[Any, ...] = (
            sim_context_clones,
            *super()._clone_args(*_, **__)
        )
        return result

    def _serialize_data(self, data: Dict[str, Any]):
        super()._serialize_data(data)
        data['sim_contexts'] = [sim_context.serialize() for sim_context in self.sim_contexts]

    @classmethod
    def _deserialize_args(cls, data: Union[str, Dict[str, Any]]) -> Union[Tuple[Any], None]:
        sim_contexts_data = data.get('sim_contexts', None)
        if sim_contexts_data is None:
            return None

        sim_contexts: List[CommonRunnableSimContextType] = list()
        for sim_context_data in sim_contexts_data:
            sim_context = cls.sim_context_type().deserialize(sim_context_data)
            if sim_context is None:
                return None
            sim_contexts.append(sim_context)
        if not sim_contexts:
            return None

        deserialized_args = super()._deserialize_args(data)
        if deserialized_args is None:
            return None

        result: Tuple[Any, ...] = (
            sim_contexts,
            *deserialized_args
        )
        return result

    def __eq__(self, other: 'CommonRunnableContextWithSims') -> bool:
        if not isinstance(other, CommonRunnableContextWithSims):
            return False
        if len(self.sim_contexts) != len(other.sim_contexts):
            return False
        for (self_sim_context, other_sim_context) in zip(self.sim_contexts, other.sim_contexts):
            if not self_sim_context.__eq__(other_sim_context):
                return False
        return True

    def __repr__(self) -> str:
        return 'Runnable Context:\n'\
               'Sims: [{}]\n'.format(
                    self.sim_contexts,
                )
