"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any


class CommonOption:
    """CommonOption(name)

    Useful for giving a type to arguments when str just won't cut it.

    :param name: The name of the option. It is also considered as the value of the option.
    :type name: str
    """
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        """The name and string value of the option.

        :return: The name of the option.
        :rtype: str
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
    """HasCommonOptions(options)

    An inheritable class that provides a dictionary of custom options.

    :param options: The options contained within the class.
    :type options: Dict[CommonOption, Any]
    """
    def __init__(self, options: Dict[CommonOption, Any]):
        self._options = dict()
        if options is not None:
            for key, val in options.items():
                self.set_option(key, val)

    @property
    def options(self) -> Dict[str, Any]:
        """Retrieve all options.

        :return: A dictionary of options.
        :rtype: Dict[str, Any]
        """
        if self._options is None:
            self._options = dict()
        return self._options

    @options.setter
    def options(self, options: Dict[str, Any]):
        self._options = options

    def set_option(self, option: CommonOption, value: Any):
        """set_option(option, value)

        Set an option to have the specified value.

        :param option: The option to set the value of.
        :type option: CommonOption
        :param value: The value to set an option to.
        :type value: Any
        """
        self._options[str(option)] = value

    def remove_option(self, option: CommonOption):
        """remove_option(option)

        Remove an option.

        :param option: The option to delete.
        :type option: CommonOption
        """
        del self._options[str(option)]

    def get_option(self, option: CommonOption, default_value: Any=None) -> Any:
        """get_option(option, default_value=None)

        Retrieve the value of an option.

        :param option: The option to retrieve.
        :type option: CommonOption
        :param default_value: A default value to return when an option does not exist. Default is None.
        :type default_value: Any
        :return: An option or the default value if not found.
        :rtype: Any
        """
        if str(option) not in self.options and default_value is not None:
            self.set_option(option, default_value)
        return self.options[str(option)]


class _DefaultCommonOption(CommonOption):
    def __init__(self, name: str):
        super().__init__(name or 'Default')
