"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo


class CommonConditionalAction(HasLog):
    """Perform an action when a condition is met.

    """
    @property
    def mod_identity(self) -> CommonModIdentity:
        """The Identity of the mod that owns this class.

        """
        return ModInfo.get_identity()

    def _should_apply(self, *_, **__) -> bool:
        """Determine if this action should apply.

        """
        return True

    def try_apply(self, *_, **__) -> bool:
        """Attempt to apply the action.

        """
        if self._should_apply(*_, **__):
            self.log.debug('Applying action \'{}\'.'.format(self.__class__.__name__))
            return self._apply(*_, **__)
        else:
            self.log.debug('Skipping action \'{}\'.'.format(self.__class__.__name__))
        return False

    def _apply(self, *_, **__) -> bool:
        """Apply this action.

        """
        raise NotImplementedError('\'{}\' not implemented'.format(self.__class__._apply.__name__))
