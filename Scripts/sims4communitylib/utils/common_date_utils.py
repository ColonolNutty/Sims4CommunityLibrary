"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from datetime import datetime


class CommonRealDateUtils:
    """A utility for managing real life date and time.

    """
    @staticmethod
    def get_current_date_string() -> str:
        """Retrieve the current date as a pre-formatted string.

        :return: The string representation of the current date.
        """
        return str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
