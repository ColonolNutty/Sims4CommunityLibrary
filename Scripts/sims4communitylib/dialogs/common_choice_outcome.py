"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from enum import Int
except:
    # noinspection PyMissingOrEmptyDocstring
    class Int:
        pass


class CommonChoiceOutcome(Int):
    """The outcome of the player being given a choice.

    """
    CANCEL = 0
    CHOICE_MADE = 1
    ERROR = 2

    @staticmethod
    def is_error_or_cancel(result: 'CommonChoiceOutcome') -> bool:
        """is_error_or_cancel(result)

        Determine if an outcome is either :py:attr:`~ERROR` or :py:attr:`~CANCEL`.

        :param result: The result to check.
        :type result: CommonChoiceOutcome
        :return: True, if result is either an Error or Cancel. False, if not.
        :rtype: bool
        """
        return result == CommonChoiceOutcome.ERROR or result == CommonChoiceOutcome.CANCEL
