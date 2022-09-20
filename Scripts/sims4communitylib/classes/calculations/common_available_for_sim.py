"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Tuple, Iterator

from sims.sim_info import SimInfo
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.common_occult_type import CommonOccultType
from sims4communitylib.enums.common_species import CommonSpecies


class CommonAvailableForSim:
    """CommonAvailableForSim(\
        genders=(),\
        ages=(),\
        species=(),\
        occult_types=()\
    )

    Holds information for what types of Sims this is available for.

    .. note:: At least one argument must be supplied with values.

    :param genders: An iterator of CommonGender. Default is an empty collection.
    :type genders: Iterator[CommonGender], optional
    :param ages: An iterator of CommonAge. Default is an empty collection.
    :type ages: Iterator[CommonAge], optional
    :param species: An iterator of CommonSpecies. Default is an empty collection.
    :type species: Iterator[CommonSpecies], optional
    :param occult_types: An iterator of CommonOccultType. Default is an empty collection.
    :type occult_types: Iterator[CommonOccultType], optional
    """
    def __init__(
        self,
        genders: Iterator[CommonGender]=(),
        ages: Iterator[CommonAge]=(),
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
    def genders(self) -> Tuple[CommonGender]:
        """Genders this is available for."""
        return self._genders

    @property
    def ages(self) -> Tuple[CommonAge]:
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
        age = CommonAge.get_age(sim_info)
        if self.ages and age not in self.ages:
            return False
        gender = CommonGender.get_gender(sim_info)
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

    def clone(self) -> 'CommonAvailableForSim':
        """Clone the available for."""
        return CommonAvailableForSim(
            genders=tuple(self.genders),
            ages=tuple(self.ages),
            species=tuple(self.species),
            occult_types=tuple(self.occult_types)
        )

    @staticmethod
    def generate_for_sim(sim_info: SimInfo) -> 'CommonAvailableForSim':
        """generate_for_sim(sim_info)

        Generate an available for, for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: An available for matching the specified Sim.
        :rtype: CommonAvailableForSim
        """
        from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
        gender = CommonGender.get_gender(sim_info)
        if gender == CommonGender.INVALID:
            genders = tuple()
        else:
            genders = (gender,)
        age = CommonAge.get_age(sim_info)
        if age == CommonAge.INVALID:
            ages = tuple()
        elif CommonAgeUtils.is_teen_adult_or_elder_age(age):
            ages = (CommonAge.TEEN, CommonAge.YOUNGADULT, CommonAge.ADULT, CommonAge.ELDER)
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
        return CommonAvailableForSim(
            genders=genders,
            ages=ages,
            species=species,
            occult_types=occult_types
        )

    @staticmethod
    def everything() -> 'CommonAvailableForSim':
        """ Create an Available For instance that applies to everything. """
        return CommonAvailableForSim(
            genders=CommonGender.get_all(),
            ages=CommonAge.get_all(),
            species=CommonSpecies.get_all(),
            occult_types=CommonOccultType.get_all()
        )

    def __repr__(self) -> str:
        return '<genders:{}, ages:{}, species:{}, occult_types:{}>'\
            .format(pformat(self.genders), pformat(self.ages), pformat(self.species), pformat(self.occult_types))

    def __str__(self) -> str:
        return self.__repr__()
