"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo


class CommonConditionalAction(HasLog):
    """An inheritable class that Performs an action when a condition is met.

    A common usage would be in a factory pattern with a collection of :class:`CommonConditionalAction` objects.

    """
    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    def _should_apply(self, *_, **__) -> bool:
        """Determine if the action should apply based on the given arguments.

        .. warning:: The arguments must match the :func:`~try_apply` method.
        """
        return True

    def try_apply(self, *_, **__) -> bool:
        """Attempt to apply the action.

        .. note:: Override this method with any arguments you want to.
        """
        if self._should_apply(*_, **__):
            self.log.debug('Applying action \'{}\'.'.format(self.__class__.__name__))
            return self._apply(*_, **__)
        else:
            self.log.debug('Skipping action \'{}\'.'.format(self.__class__.__name__))
        return False

    def _apply(self, *_, **__) -> bool:
        """Apply the action.

        .. warning:: The arguments must match the :func:`~try_apply` arguments.
        """
        raise NotImplementedError('\'{}\' not implemented'.format(self.__class__._apply.__name__))
