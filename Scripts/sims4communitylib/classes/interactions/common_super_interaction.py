"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from interactions import ParticipantType
from interactions.base.super_interaction import SuperInteraction
from sims4.utils import flexmethod
from sims4communitylib.classes.interactions.common_interaction import CommonInteraction
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo


class CommonSuperInteraction(CommonInteraction, SuperInteraction):
    """ A base for accessing super interaction hooks. """

    def _run_interaction_gen(self, timeline):
        super()._run_interaction_gen(timeline)
        return self.on_run(self.sim, self.target, timeline)

    # noinspection PyUnusedLocal
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=True)
    def on_run(self, interaction_sim, interaction_target, timeline) -> bool:
        """
            Occurs upon the interaction being run.
        :param interaction_sim: The sim performing the interaction.
        :param interaction_target: The target of the interaction.
        :param timeline: The timeline the interaction is running on.
        :return: True if the interaction hook was executed successfully.
        """
        return True


class CommonConstrainedSuperInteraction(SuperInteraction):
    """ A base for accessing super interaction hooks with constraints. """

    # noinspection PyMethodParameters
    @flexmethod
    def _constraint_gen(cls, inst, sim, target, participant_type=ParticipantType.Actor):
        interaction_instance = inst if inst is not None else cls
        yield cls.on_constraint_gen(interaction_instance, sim or interaction_instance.sim, target or interaction_instance.target)

    @classmethod
    def on_constraint_gen(cls, inst, sim, target):
        """
            Occurs upon retrieving an interactions constraints.
        :param inst: An object of type Interaction.
        :param sim: The sim performing the interaction.
        :param target: The target of the interaction.
        """
        raise NotImplementedError()
