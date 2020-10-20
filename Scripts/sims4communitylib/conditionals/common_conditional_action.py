"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class CommonConditionalAction(HasLog):
    """CommonConditionalAction()

    An inheritable class that Performs an action when a condition is met.

    .. note:: A common usage would be in a factory pattern with a collection of :class:`CommonConditionalAction` objects.

    """
    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> Union[CommonModIdentity, None]:
        return None

    def _should_apply(self, *_, **__) -> bool:
        """_should_apply(*_, **__)

        Determine if the action should apply based on the given arguments.

        .. warning:: The arguments must match the :func:`~try_apply` method.

        :return: True, if the action should be applied. False, if not.
        :rtype: bool
        """
        return True

    def try_apply(self, *_, **__) -> bool:
        """try_apply(*_, **__)

        Attempt to apply the action.

        .. note:: Override this method with any arguments you want to.

        :return: True, if the action was applied. False, if not.
        :rtype: bool
        """
        if self._should_apply(*_, **__):
            self.log.debug('Applying action \'{}\'.'.format(self.__class__.__name__))
            return self._apply(*_, **__)
        else:
            self.log.debug('Skipping action \'{}\'.'.format(self.__class__.__name__))
        return False

    def _apply(self, *_, **__) -> bool:
        """_apply(*_, **__)

        Apply the action.

        .. warning:: The arguments must match the :func:`~try_apply` arguments.

        :return: True, if the action was applied. False, if not.
        :rtype: bool
        """
        raise NotImplementedError('\'{}\' not implemented'.format(self.__class__._apply.__name__))
