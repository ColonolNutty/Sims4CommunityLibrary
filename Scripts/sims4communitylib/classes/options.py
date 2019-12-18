"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any


class CommonOption:
    """ Useful for typing arguments when str just won't cut it. """
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        """
            The name of the option
        :return: A string name.
        """
        return self._name

    def __hash__(self) -> int:
        return hash((self.name,))

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __ne__(self, other) -> bool:
        return not(self == other)

    def __repr__(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self.__repr__()


class HasCommonOptions:
    """
        Provides a class the ability to store custom data.
    """
    def __init__(self, options: Dict[CommonOption, Any]):
        self._options = dict()
        if options is not None:
            for key, val in options.items():
                self.set_option(key, val)

    @property
    def options(self) -> Dict[str, Any]:
        """
            Retrieve options.
        :return: A dictionary of options.
        """
        if self._options is None:
            self._options = dict()
        return self._options

    @options.setter
    def options(self, options: Dict[str, Any]):
        self._options = options

    def set_option(self, option: CommonOption, value: Any) -> Any:
        """
            Set the value of an option
        :param option: An object of type CommonOption.
        :param value: The new value for the option.
        """
        self._options[str(option)] = value

    def remove_option(self, option: CommonOption):
        """
            Remove an option.
        :param option: An object of type CommonOption.
        """
        del self._options[str(option)]

    def get_option(self, option: CommonOption, default_value: Any=None) -> Any:
        """
            Retrieve the value of an option and give the specified default value if the option does not exist.
        :param option: An object of type CommonOption.
        :param default_value: The default value used when the option is not found.
        :return: The value of the option or the default_value if the option was not found.
        """
        if str(option) not in self.options and default_value is not None:
            self.set_option(option, default_value)
        return self.options[str(option)]


class _DefaultCommonOption(CommonOption):
    def __init__(self, name: str):
        super().__init__(name or 'Default')
