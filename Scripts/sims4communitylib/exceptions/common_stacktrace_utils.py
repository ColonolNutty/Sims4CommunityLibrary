"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sys
import traceback
from collections import namedtuple
from typing import Union, Any, List

# The following was tweaked slightly from the publicly made available, copyright free code here: https://stackoverflow.com/questions/13210436/get-full-traceback
from sims4communitylib.utils.common_collection_utils import CommonCollectionUtils

FullTraceback = namedtuple('FullTraceback', ('tb_frame', 'tb_lineno', 'tb_next'))


class CommonStacktraceUtil:
    """Utilities for accessing the full stack trace of your application.

    """
    @staticmethod
    def current_stack(skip: int=0) -> Any:
        """Retrieve the current stack

        :param skip: The number of lines to skip
        :return: A collection of the current stack.
        """
        cur_frame = None
        try:
            1/0
        except ZeroDivisionError:
            cur_frame = sys.exc_info()[2].tb_frame
        for i in range(skip + 2):
            cur_frame = cur_frame.f_back
        stack_trace = []
        while cur_frame is not None:
            stack_trace.append((cur_frame, cur_frame.f_lineno))
            cur_frame = cur_frame.f_back
        return stack_trace

    @staticmethod
    def _extend_traceback(tb, stack) -> FullTraceback:
        """Extend traceback with stack info.

        """
        head = tb
        for traceback_frame, traceback_line_number in stack:
            head = FullTraceback(traceback_frame, traceback_line_number, head)
        return head

    @staticmethod
    def full_exception_info() -> Union[type, Any, FullTraceback]:
        """Like sys.exc_info, but includes the full traceback.

        """
        exception_type, exception_value, exception_traceback = sys.exc_info()
        full_traceback = CommonStacktraceUtil._extend_traceback(exception_traceback, CommonStacktraceUtil.current_stack(1))
        return exception_type, exception_value, full_traceback

    @staticmethod
    def get_full_stack_trace() -> List[str]:
        """Retrieve the full stacktrace from the current stack.

        :return: A collection of stack trace strings.
        """
        exception_info = CommonStacktraceUtil.full_exception_info()
        if CommonCollectionUtils.is_collection(exception_info):
            exceptions = traceback.format_exception(*exception_info)
        else:
            exceptions = traceback.format_stack()
        return exceptions
