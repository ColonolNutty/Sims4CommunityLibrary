"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from event_testing.resolver import Resolver
from event_testing.test_based_score import TestBasedScore
from sims4.math import Threshold
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class CommonTestBasedScore(TestBasedScore, HasClassLog):
    """ A test based score used when testing a resolver. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    def __init__(self, *_, **__) -> None:
        super().__init__(*_, **__)
        HasClassLog.__init__(self)

    @classmethod
    def get_default_score(cls) -> int:
        """The default score used when no other score is found or when an error occurs."""
        return 0

    @classmethod
    def passes_threshold(cls, resolver: Resolver, threshold: Threshold) -> bool:
        """ True if the threshold is passed. """
        if resolver is not None:
            cls.get_verbose_log().format(
                resolver_type=type(resolver),
                resolver_class=resolver.__class__,
                resolver_class_name=resolver.__class__.__name__
            )
        if threshold is not None:
            cls.get_verbose_log().format(
                threshold_type=type(threshold),
                threshold_class=threshold.__class__
            )
        return threshold.compare(cls.get_score(resolver))

    @classmethod
    def _verify_tuning_callback(cls) -> None:
        pass

    @classmethod
    def _tuning_loaded_callback(cls) -> None:
        pass

