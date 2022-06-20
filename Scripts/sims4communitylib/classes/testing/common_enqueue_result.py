"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from event_testing.results import TestResult, EnqueueResult
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult


class CommonEnqueueResult(EnqueueResult):
    """CommonEnqueueResult(\
        test_result,\
        execute_result,\
    )

    The result of enqueuing an interaction.
    """
    TRUE = None
    FALSE = None
    NONE = None
    test_result: CommonTestResult
    execute_result: CommonExecutionResult

    def __new__(cls, test_result: CommonTestResult, execute_result: CommonExecutionResult):
        return super(CommonEnqueueResult, cls).__new__(cls, test_result, execute_result)

    def reverse_result(self) -> 'CommonExecutionResult':
        """reverse_result()

        Create a CommonExecutionResult that has a reversed result of this one, but with the same reason and tooltip information.

        .. note:: This function works best when the result value has an opposite, such as a boolean.

        :return: This CommonExecutionResult, but with a reversed result value.
        :rtype: CommonExecutionResult
        """
        return CommonEnqueueResult(
            self.test_result.reverse_result(),
            self.execute_result.reverse_result()
        )

    @property
    def is_success(self) -> bool:
        """True, if the result of enqueue is successful. False, if not."""
        return bool(self)

    @property
    def is_failure(self) -> bool:
        """False, if the result of enqueue is a failure. False, if not."""
        return not self.is_success

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {repr(self.test_result)} {repr(self.execute_result)}>'

    def __str__(self) -> str:
        return f'<{self.__class__.__name__}: {str(self.test_result)} {str(self.execute_result)}>'

    def __eq__(self, other) -> bool:
        if isinstance(other, bool):
            return self.is_success is other
        if isinstance(other, CommonEnqueueResult):
            return self.test_result == other.test_result and self.execute_result == other.execute_result
        if isinstance(other, CommonExecutionResult):
            return self.execute_result == other
        if isinstance(other, CommonTestResult):
            return self.test_result == other
        if isinstance(other, TestResult):
            return self.is_success == other.result
        if isinstance(other, EnqueueResult):
            return self.test_result == other.test_result and self.execute_result == other.execute_result
        return self.test_result == other and self.execute_result == other

    def __ne__(self, other) -> bool:
        return not self == other

    def __bool__(self) -> bool:
        return bool(self.test_result) and bool(self.execute_result)

    def __or__(self, other) -> 'CommonExecutionResult':
        if isinstance(other, CommonEnqueueResult):
            test_result = self.test_result or other.test_result
            execute_result = self.execute_result or other.execute_result
        elif isinstance(other, EnqueueResult):
            test_result = self.test_result or other.test_result
            execute_result = self.execute_result or other.execute_result
        elif isinstance(other, CommonExecutionResult):
            test_result = self.test_result or CommonTestResult(
                other.result,
                reason=other.reason,
                tooltip_text=other._tooltip_text,
                tooltip_tokens=other._tooltip_tokens,
                icon=other.icon,
                influenced_by_active_mood=other.influence_by_active_mood,
                hide_tooltip=other._hide_tooltip
            )
            execute_result = self.execute_result or other
        elif isinstance(other, CommonTestResult):
            test_result = self.test_result or other
            execute_result = self.execute_result or CommonExecutionResult(
                other.result,
                success_override=other._success_override,
                reason=other.reason,
                tooltip_text=other._tooltip_text,
                tooltip_tokens=other._tooltip_tokens,
                icon=other.icon,
                influenced_by_active_mood=other.influence_by_active_mood,
                hide_tooltip=other._hide_tooltip
            )
        elif isinstance(other, bool):
            test_result = self.test_result or CommonTestResult(
                other,
                reason=self.test_result.reason,
                tooltip_text=self.test_result._tooltip_text,
                tooltip_tokens=self.test_result._tooltip_tokens,
                icon=self.test_result.icon,
                influenced_by_active_mood=self.test_result.influence_by_active_mood,
                hide_tooltip=self.test_result._hide_tooltip
            )
            execute_result = self.execute_result or CommonExecutionResult(
                other,
                success_override=other,
                reason=self.execute_result.reason,
                tooltip_text=self.execute_result._tooltip_text,
                tooltip_tokens=self.execute_result._tooltip_tokens,
                icon=self.execute_result.icon,
                influenced_by_active_mood=self.execute_result.influence_by_active_mood,
                hide_tooltip=self.execute_result._hide_tooltip
            )
        else:
            return self

        return CommonEnqueueResult(
            test_result,
            execute_result
        )

    def __and__(self, other: 'CommonExecutionResult') -> 'CommonExecutionResult':
        if isinstance(other, CommonEnqueueResult):
            test_result = self.test_result and other.test_result
            execute_result = self.execute_result and other.execute_result
        elif isinstance(other, EnqueueResult):
            test_result = self.test_result and other.test_result
            execute_result = self.execute_result and other.execute_result
        elif isinstance(other, CommonExecutionResult):
            test_result = self.test_result and CommonTestResult(
                other.result,
                reason=other.reason,
                tooltip_text=other._tooltip_text,
                tooltip_tokens=other._tooltip_tokens,
                icon=other.icon,
                influenced_by_active_mood=other.influence_by_active_mood,
                hide_tooltip=other._hide_tooltip
            )
            execute_result = self.execute_result and other
        elif isinstance(other, CommonTestResult):
            test_result = self.test_result and other
            execute_result = self.execute_result and CommonExecutionResult(
                other.result,
                success_override=other._success_override,
                reason=other.reason,
                tooltip_text=other._tooltip_text,
                tooltip_tokens=other._tooltip_tokens,
                icon=other.icon,
                influenced_by_active_mood=other.influence_by_active_mood,
                hide_tooltip=other._hide_tooltip
            )
        elif isinstance(other, bool):
            test_result = self.test_result and CommonTestResult(
                other,
                reason=self.test_result.reason,
                tooltip_text=self.test_result._tooltip_text,
                tooltip_tokens=self.test_result._tooltip_tokens,
                icon=self.test_result.icon,
                influenced_by_active_mood=self.test_result.influence_by_active_mood,
                hide_tooltip=self.test_result._hide_tooltip
            )
            execute_result = self.execute_result and CommonExecutionResult(
                other,
                success_override=other,
                reason=self.execute_result.reason,
                tooltip_text=self.execute_result._tooltip_text,
                tooltip_tokens=self.execute_result._tooltip_tokens,
                icon=self.execute_result.icon,
                influenced_by_active_mood=self.execute_result.influence_by_active_mood,
                hide_tooltip=self.execute_result._hide_tooltip
            )
        else:
            return self

        return CommonEnqueueResult(
            test_result,
            execute_result
        )


CommonEnqueueResult.TRUE = CommonEnqueueResult(CommonTestResult.TRUE, CommonExecutionResult.TRUE)
CommonEnqueueResult.FALSE = CommonEnqueueResult(CommonTestResult.FALSE, CommonExecutionResult.FALSE)
CommonEnqueueResult.NONE = CommonEnqueueResult(CommonTestResult.NONE, CommonExecutionResult.NONE)
