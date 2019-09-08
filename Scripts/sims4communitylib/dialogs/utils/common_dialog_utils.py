"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""


class CommonDialogUtils:
    """ Utilities for use with dialogs. """
    @classmethod
    def get_chosen_item(cls, dialog):
        """ Retrieves the item chosen by the player from a dialog. """
        return dialog.get_result_tags()[-1] or dialog.get_result_tags()[0]
