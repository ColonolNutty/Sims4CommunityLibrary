"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from event_testing.resolver import Resolver
from interactions import ParticipantType
from interactions.base.interaction import Interaction
from sims.sim_info import SimInfo
from sims4.sim_irq_service import yield_to_irq
from sims4communitylib.classes.test_based_scores.common_test_based_score import CommonTestBasedScore
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSingleSimTestBasedScore(CommonTestBasedScore):
    """ A test based score used when testing a resolver involving one Sim. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def get_score(cls, resolver: Resolver) -> int:
        """get_score(resolver)

        Calculate the score.
        """
        try:
            yield_to_irq()
            cls.get_verbose_log().format_with_message('Retrieving score.', class_name=cls.__name__)
            source_sim = resolver.get_participant(ParticipantType.Actor)
            if source_sim is None or not CommonTypeUtils.is_sim_or_sim_info(source_sim):
                cls.get_verbose_log().format_with_message('Failed, the Source was not a Sim.', source=source_sim)
                return cls.get_default_score()
            source_sim_info = CommonSimUtils.get_sim_info(source_sim)
            interaction_instance = resolver.interaction or getattr(resolver, 'affordance', None)
            score = cls.calculate_score(resolver, source_sim_info, interaction_instance)
            cls.get_verbose_log().format_with_message('Retrieved score for Sim.', source_sim=source_sim_info, score=score)
            return score
        except Exception as ex:
            cls.get_verbose_log().error('Error occurred while retrieving score.', exception=ex)
        return cls.get_default_score()

    @classmethod
    def calculate_score(cls, resolver: Resolver, source_sim_info: SimInfo, interaction: Interaction) -> int:
        """calculate_score(resolver, source_sim_info, interaction)

        Calculate a score involving one Sim.

        :param resolver: A resolver containing information about what is being tested.
        :type resolver: Resolver
        :param source_sim_info: The Source or Actor Sim of the test.
        :type source_sim_info: SimInfo
        :param interaction: The interaction or affordance, if available, that the Source Sim is attempting to perform. If no interaction or affordance is present, this value will be None.
        :type interaction: Interaction
        :return: The calculated Score.
        :rtype: int
        """
        raise NotImplementedError()
