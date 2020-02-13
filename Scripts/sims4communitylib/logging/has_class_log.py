"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.has_class_mod_identity import HasClassModIdentity
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry


class HasClassLog(HasClassModIdentity, HasLog):
    """An inheritable class that will add a log and mod identity to a class.

    .. note:: This class inherits from :class:`.HasLog` and may be used as an alternative to it.

    """
    def __init__(self):
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
    def log(self) -> CommonLog:
        return self.__class__.get_log()

    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        """get_mod_identity()

        The identity of the mod that owns this class.

        .. warning:: Override this function with the :class:`.CommonModIdentity` of your mod.

        This is a *MUST* override to allow for proper Exception Handling and Logging!

        """
        raise NotImplementedError('Missing \'{}\'.'.format(cls.get_mod_identity.__name__))

    @classmethod
    def get_log(cls) -> CommonLog:
        """get_log()

        The Log for this class.

        .. note:: It uses the `mod_identity` and `log_identifier` when logging.
        """
        if not hasattr(cls, '_log') or getattr(cls, '_log', None) is None:
            mod_name = 'Missing Mod Name'
            if cls.get_mod_identity() is not None:
                mod_name = cls.get_mod_identity().name
            setattr(cls, '_log', CommonLogRegistry.get().register_log(mod_name, cls.get_log_identifier()))
        return getattr(cls, '_log', None)

    @classmethod
    def get_log_identifier(cls) -> str:
        """get_log_identifier()

        The string identifier for the Log of this class.

        .. note:: This is the string that will appear when logging messages using this logger

        :return: The identifier for the log
        :rtype: str
        """
        return cls.__name__
