"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

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
    """An outcome of the player being given a choice.

    """
    CANCEL = 0
    CHOICE_MADE = 1
    ERROR = 2

    @staticmethod
    def is_error_or_cancel(result: 'CommonChoiceOutcome'):
        """ Determine if an outcome is either Error or Cancel. """
        return result == CommonChoiceOutcome.ERROR or result == CommonChoiceOutcome.CANCEL
