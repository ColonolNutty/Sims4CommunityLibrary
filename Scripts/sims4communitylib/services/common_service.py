"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""


class CommonService:
    """
        A service used to create a common structure for singleton services.
    """
    def __init__(self):
        pass

    @classmethod
    def get(cls) -> 'CommonService':
        """
        Get an instance of the service
        :return: An instance of the service
        """
        raise NotImplementedError()
