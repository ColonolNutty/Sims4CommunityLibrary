"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import TYPE_CHECKING

from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.has_class_mod_identity import HasClassModIdentity
from sims4communitylib.mod_support.mod_identity import CommonModIdentity

if TYPE_CHECKING:
    from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry


class HasClassLog(HasClassModIdentity, HasLog):
    """HasClassLog()

    An inheritable class that will add a log and mod identity to a class.

    .. note:: This class inherits from :class:`.HasLog` and may be used as an alternative to it.

    """
    def __init__(self) -> None:
        super().__init__()
        HasLog.__init__(self)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return self.__class__.get_mod_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return self.__class__.get_log_identifier()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def verbose_log_identifier(self) -> str:
        return self.__class__.get_verbose_log_identifier()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log(self) -> 'CommonLog':
        return self.__class__.get_log()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def verbose_log(self) -> 'CommonLog':
        return self.__class__.get_verbose_log()

    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        """get_mod_identity()

        Retrieve the identity of the mod that owns the class.

        .. warning:: Override this function with the :class:`.CommonModIdentity` of your mod.

        This is a *MUST* override to allow for proper Exception Handling and Logging!

        :return: An instance of CommonModIdentity
        :rtype: CommonModIdentity
        :exception NotImplementedError: Thrown when the function is not implemented.
        """
        raise NotImplementedError(f'Missing \'{cls.__name__}.get_mod_identity\'.')

    @classmethod
    def get_log(cls) -> 'CommonLog':
        """get_log()

        Retrieve a log for the class.

        .. note:: This function uses the :func:`~get_mod_identity` and :func:`~get_log_identifier` functions when logging.

        :return: An instance of CommonLog
        :rtype: CommonLog
        """
        from sims4communitylib.utils.common_log_registry import CommonLogRegistry
        if not hasattr(cls, '_log') or getattr(cls, '_log', None) is None:
            setattr(cls, '_log', CommonLogRegistry().register_log(cls.get_mod_identity(), cls.get_log_identifier()))
            if not hasattr(cls, '_verbose_log') or getattr(cls, '_verbose_log', None) is None:
                setattr(cls, '_verbose_log', CommonLogRegistry().register_log(cls.get_mod_identity(), cls.get_verbose_log_identifier()))
        return getattr(cls, '_log', None)

    @classmethod
    def get_verbose_log(cls) -> 'CommonLog':
        """get_verbose_log()

        Retrieve a verbose log for the class.

        .. note:: This function uses the :func:`~get_mod_identity` and :func:`~get_verbose_log_identifier` functions when logging.

        .. note:: This log can be used to log extra details that you don't want to appear when using the non verbose log.

        :return: An instance of CommonLog
        :rtype: CommonLog
        """
        from sims4communitylib.utils.common_log_registry import CommonLogRegistry
        if not hasattr(cls, '_verbose_log') or getattr(cls, '_verbose_log', None) is None:
            setattr(cls, '_verbose_log', CommonLogRegistry().register_log(cls.get_mod_identity(), cls.get_verbose_log_identifier()))
        return getattr(cls, '_verbose_log', None)

    @classmethod
    def get_log_identifier(cls) -> str:
        """get_log_identifier()

        A string identifier for the log of the class.

        .. note:: This is the text that will appear when logging messages.

        :return: The identifier for the log
        :rtype: str
        """
        return cls.__name__

    @classmethod
    def get_verbose_log_identifier(cls) -> str:
        """get_verbose_log_identifier()

        A string identifier for the log of the class.

        .. note:: This is the text that will appear when logging messages.

        :return: The identifier for the log
        :rtype: str
        """
        log_identifier = cls.get_log_identifier()
        return f'{log_identifier}_verbose'
