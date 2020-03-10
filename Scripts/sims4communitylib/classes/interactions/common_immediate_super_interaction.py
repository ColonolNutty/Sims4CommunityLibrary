"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from sims4communitylib.classes.interactions.common_interaction import CommonInteraction

# ReadTheDocs
ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

# If on Read The Docs, create fake versions of extended objects to fix the error of inheriting from multiple MockObjects.
if not ON_RTD:
    from interactions.base.immediate_interaction import ImmediateSuperInteraction
else:
    # noinspection PyMissingOrEmptyDocstring
    class MockClass(object):
        # noinspection PyMissingTypeHints,PyUnusedLocal
        def __init__(self, *args, **kwargs):
            super(MockClass, self).__init__()

        # noinspection PyMissingTypeHints
        def __call__(self, *args, **kwargs):
            return None

    # noinspection PyMissingOrEmptyDocstring
    class ImmediateSuperInteraction(MockClass):
        pass


class CommonImmediateSuperInteraction(CommonInteraction, ImmediateSuperInteraction):
    """An inheritable class that provides a way to create Custom Immediate Super Interactions.

    .. note::

        The main use for this class is to create interactions that do something upon starting the interaction, without the Sim needing to queue the interaction.
        One example would be the `Replace` interaction to replace objects that were destroyed in a fire.

    .. warning:: Due to an issue with how Read The Docs functions, the base classes of this class will have different namespaces than they do in the source code!
    """
    pass
