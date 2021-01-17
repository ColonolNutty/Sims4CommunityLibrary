"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Tuple, Iterator

from sims.sim_info import SimInfo
from sims.sim_info_types import Age, Gender
from sims4communitylib.enums.common_occult_type import CommonOccultType
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils


class CommonAvailableFor:
    """CommonAvailableFor(\
        genders=(),\
        ages=(),\
        species=()\
    )

    Holds information for what types of Sims this is available for.

    .. note:: At least one argument must be supplied with values.

    :param genders: An iterable of Gender. Default is an empty collection.
    :type genders: Iterator[Gender], optional
    :param ages: An iterable of Age. Default is an empty collection.
    :type ages: Iterator[Age], optional
    :param species: An iterable of CommonSpecies. Default is an empty collection.
    :type species: Iterator[CommonSpecies], optional
    :param occult_types: An iterable of CommonOccultType. Default is an empty collection.
    :type occult_types: Iterator[CommonOccultType], optional
    """
    def __init__(
        self,
        genders: Iterator[Gender]=(),
        ages: Iterator[Age]=(),
        species: Iterator[CommonSpecies]=(),
        occult_types: Iterator[CommonOccultType]=()
    ):
        self._genders = tuple(genders)
        self._ages = tuple(ages)
        self._species = tuple(species)
        self._occult_types = tuple(occult_types)
        if not self._genders and not self._ages and not self._species and not self._occult_types:
            raise AssertionError('No Genders, Ages, Species, nor Occult Types were specified!')

    @property
    def genders(self) -> Tuple[Gender]:
        """Genders this is available for."""
        return self._genders

    @property
    def ages(self) -> Tuple[Age]:
        """Ages this is available for."""
        return self._ages

    @property
    def species(self) -> Tuple[CommonSpecies]:
        """Species this is available for."""
        return self._species

    @property
    def occult_types(self) -> Tuple[CommonOccultType]:
        """Occult Types this is available for."""
        return self._occult_types

    def is_available_for(self, sim_info: SimInfo) -> bool:
        """is_available_for(sim_info)

        Determine if available for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if is available for the specified Sim. False, if not.
        :rtype: bool
        """
        age = CommonAgeUtils.get_age(sim_info)
        if self.ages and age not in self.ages:
            return False
        gender = CommonGenderUtils.get_gender(sim_info)
        if self.genders and gender not in self.genders:
            return False
        common_species = CommonSpecies.get_species(sim_info)
        if self.species and common_species not in self.species:
            return False
        common_occult_type = CommonOccultType.determine_occult_type(sim_info)
        if self.occult_types and common_occult_type not in self.occult_types:
            return False
        return True

    def is_valid(self) -> Tuple[bool, str]:
        """is_valid()

        Determine if the Available For is valid.

        :return: If the Available For is valid, the return will be True and a Success message. If the Available For is not valid, the return will be False and an error message.
        :rtype: Tuple[bool, str]
        """
        if len(self.genders) == 0 and len(self.ages) == 0 and len(self.species) == 0 and len(self.occult_types) == 0:
            return False, 'No Genders, Ages, Species, nor Occult Types were specified!'
        return True, 'Success'

    def clone(self) -> 'CommonAvailableFor':
        """Clone the available for."""
        return CommonAvailableFor(
            genders=tuple(self.genders),
            ages=tuple(self.ages),
            species=tuple(self.species),
            occult_types=tuple(self.occult_types)
        )

    @staticmethod
    def generate_for_sim(sim_info: SimInfo) -> 'CommonAvailableFor':
        """generate_for_sim(sim_info)

        Generate an available for, for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: An available for matching the specified Sim.
        :rtype: CommonAvailableFor
        """
        gender = CommonGenderUtils.get_gender(sim_info)
        if gender is None:
            genders = tuple()
        else:
            genders = (gender,)
        age = CommonAgeUtils.get_age(sim_info)
        if age is None:
            ages = tuple()
        elif CommonAgeUtils.is_teen_adult_or_elder_age(age):
            ages = (Age.TEEN, Age.YOUNG_ADULT, Age.ADULT, Age.ELDER)
        else:
            ages = (age,)
        sim_species = CommonSpecies.get_species(sim_info)
        if sim_species == CommonSpecies.INVALID:
            species = tuple()
        else:
            species = (sim_species,)
        occult_type = CommonOccultType.determine_occult_type(sim_info)
        if occult_type == CommonOccultType.NON_OCCULT:
            occult_types = (occult_type,)
        else:
            occult_types = (CommonOccultType.NON_OCCULT, occult_type)
        return CommonAvailableFor(
            genders=genders,
            ages=ages,
            species=species,
            occult_types=occult_types
        )

    @staticmethod
    def everything() -> 'CommonAvailableFor':
        """ Create an Available For instance that applies to everything. """
        return CommonAvailableFor(
            genders=(Gender.MALE, Gender.FEMALE),
            ages=(Age.BABY, Age.TODDLER, Age.CHILD, Age.TEEN, Age.YOUNGADULT, Age.ADULT, Age.ELDER),
            species=(CommonSpecies.HUMAN, CommonSpecies.SMALL_DOG, CommonSpecies.LARGE_DOG, CommonSpecies.CAT),
            occult_types=(
                CommonOccultType.NON_OCCULT,
                CommonOccultType.ALIEN,
                CommonOccultType.GHOST,
                CommonOccultType.MERMAID,
                CommonOccultType.PLANT_SIM,
                CommonOccultType.ROBOT,
                CommonOccultType.SKELETON,
                CommonOccultType.VAMPIRE,
                CommonOccultType.WITCH
            )
        )

    def __repr__(self) -> str:
        return '<genders:{}, ages:{}, species:{}, occult_types:{}>'\
            .format(pformat(self.genders), pformat(self.ages), pformat(self.species), pformat(self.occult_types))

    def __str__(self) -> str:
        return self.__repr__()
