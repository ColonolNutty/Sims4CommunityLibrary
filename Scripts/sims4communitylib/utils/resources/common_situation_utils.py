"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator, Tuple, List, Type

import services
from sims.sim_info import SimInfo
from sims4communitylib.enums.situations_enum import CommonSituationId
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from situations.situation import Situation
from situations.situation_job import SituationJob
from situations.situation_manager import SituationManager


class CommonSituationUtils:
    """Utilities for manipulating Situations.

    """

    @staticmethod
    def get_situation_id(situation_identifier: Union[int, Situation]) -> Union[int, None]:
        """get_situation_id(situation_identifier)

        Retrieve the decimal identifier of a Situation.

        :param situation_identifier: The identifier or instance of a Situation.
        :type situation_identifier: Union[int, Situation]
        :return: The decimal identifier of the Situation or None if the Situation does not have an id.
        :rtype: Union[int, None]
        """
        if isinstance(situation_identifier, int):
            return situation_identifier
        if not hasattr(situation_identifier, 'id'):
            return -1
        return situation_identifier.id or getattr(situation_identifier, 'id', -1)

    @staticmethod
    def get_situation_guid(situation_identifier: Union[int, Situation]) -> int:
        """get_situation_guid(situation_identifier)

        Retrieve the GUID of a Situation.

        :param situation_identifier: The identifier or instance of a Situation.
        :type situation_identifier: Union[int, Situation]
        :return: The GUID of the specified Situation or -1 if it does not have one.
        :rtype: int
        """
        if situation_identifier is None:
            return -1
        if isinstance(situation_identifier, int):
            return situation_identifier
        if not hasattr(situation_identifier, 'guid64'):
            return -1
        return getattr(situation_identifier, 'guid64', -1)

    @staticmethod
    def get_situation_job_guid(situation_job_identifier: Union[int, SituationJob]) -> int:
        """get_situation_job_guid(situation_job_identifier)

        Retrieve the GUID of a Situation Job.

        :param situation_job_identifier: The identifier or instance of a Situation Job.
        :type situation_job_identifier: Union[int, SituationJob]
        :return: The GUID of the specified Situation or -1 if it does not have one.
        :rtype: int
        """
        if situation_job_identifier is None:
            return -1
        if isinstance(situation_job_identifier, int):
            return situation_job_identifier
        if not hasattr(situation_job_identifier, 'guid64'):
            return -1
        return getattr(situation_job_identifier, 'guid64', -1)

    @staticmethod
    def get_situation_name(situation: Situation) -> Union[str, None]:
        """get_situation_name(situation)

        Retrieve the Name of a Situation.

        :param situation: An instance of a Situation.
        :type situation: Situation
        :return: The short name of a Situation or None if a problem occurs.
        :rtype: Union[str, None]
        """
        if situation is None:
            return None
        # noinspection PyBroadException
        try:
            return situation.__class__.__name__ or ''
        except:
            return ''

    @staticmethod
    def get_situation_names(situations: Iterator[Situation]) -> Tuple[str]:
        """get_situation_names(situations)

        Retrieve the Names of a collection of Situation.

        :param situations: A collection of Situation instances.
        :type situations: Iterator[Situation]
        :return: A collection of names for all specified Situations.
        :rtype: Tuple[str]
        """
        if situations is None or not situations:
            return tuple()
        names: List[str] = []
        for situation in situations:
            # noinspection PyBroadException
            try:
                name = CommonSituationUtils.get_situation_name(situation)
                if not name:
                    continue
            except:
                continue
            names.append(name)
        return tuple(names)

    @staticmethod
    def get_situation_manager_for_zone(zone_id: int=None) -> SituationManager:
        """get_situation_manager_for_zone(zone_id=None)

        Retrieve the situation manager for a zone.

        :param zone_id: The zone to retrieve the situation manager of. Default is None, which is the current zone.
        :type zone_id: int, optional
        :return: The situation manager for the specified zone.
        :rtype: SituationManager
        """
        return services.get_zone_situation_manager(zone_id=zone_id)

    @staticmethod
    def get_sim_info_for_all_sims_in_situation(situation: Situation) -> Tuple[SimInfo]:
        """get_sim_info_for_all_sims_in_situation(situation)

        Retrieve a SimInfo object for all Sims in a Situation.

        :param situation: A situation
        :type situation: Situation
        :return: A collection of SimInfo for all Sims in the situation.
        :rtype: Tuple[SimInfo]
        """
        if situation is None:
            return tuple()
        result: Tuple[SimInfo] = tuple([CommonSimUtils.get_sim_info(_sim) for _sim in situation.all_sims_in_situation_gen()])
        return result

    @staticmethod
    def get_sim_info_for_all_sims_in_running_situations_by_type(situation_type: Type[Situation]) -> Tuple[SimInfo]:
        """get_sim_info_for_all_sims_in_running_situations_by_type(situation_type)

        Retrieve a SimInfo object for all Sims in a Situation.

        :param situation_type: The type of situation to locate.
        :type situation_type: Type[Situation]
        :return: A collection of SimInfo for all Sims in the situations that match the specified type.
        :rtype: Tuple[SimInfo]
        """
        sim_info_list: List[SimInfo] = list()
        for situation in CommonSituationUtils.locate_running_situations_by_type(situation_type):
            for sim in tuple(situation.all_sims_in_situation_gen()):
                sim_info = CommonSimUtils.get_sim_info(sim)
                if sim_info is None:
                    continue
                sim_info_list.append(sim_info)
        return tuple(sim_info_list)

    @staticmethod
    def locate_running_situation_by_id(situation_id: Union[int, CommonSituationId, Situation], zone_id: int=None) -> Union[Situation, None]:
        """locate_situation_by_id(situation_id, zone_id=None)

        Locate a running Situation from a Zone by its id.

        :param situation_id: The decimal identifier of a Situation. (Not to be confused with the instance id)
        :type situation_id: Union[int, CommonSituationId, Situation]
        :param zone_id: The zone to retrieve the situation from. Default is None, which is the current zone.
        :type zone_id: int, optional
        :return: The situation from the specified zone that matches the specified id or None if not found.
        :rtype: Union[Situation, None]
        """
        if isinstance(situation_id, Situation):
            return situation_id
        situation_manager = CommonSituationUtils.get_situation_manager_for_zone(zone_id=zone_id)
        return situation_manager.get(situation_id)

    @staticmethod
    def locate_first_running_situation_by_type(situation_type: Type[Situation], zone_id: int=None) -> Union[Situation, None]:
        """locate_first_running_situation_by_type(situation_type, zone_id=None)

        Locate the first running Situation from a Zone by its Type.

        :param situation_type: The type of situation to search for.
        :type situation_type: Type[Situation]
        :param zone_id: The zone to locate the situations in. Default is None, which is the current zone.
        :type zone_id: int, optional
        :return: A collection of situations from the specified zone that have the specified tag.
        :rtype: Tuple[Situation]
        """
        situations = CommonSituationUtils.locate_running_situations_by_type(situation_type, zone_id=zone_id)
        if situations:
            return next(iter(situations))
        return None

    @staticmethod
    def locate_first_running_situation_by_tag(tag: CommonGameTag, zone_id: int=None) -> Union[Situation, None]:
        """locate_first_running_situation_by_tag(situation_type, zone_id=None)

        Locate the first running Situation from a Zone by a tag.

        :param tag: A tag to search for the situation with.
        :type tag: CommonGameTag
        :param zone_id: The zone to locate the situations in. Default is None, which is the current zone.
        :type zone_id: int, optional
        :return: A collection of situations from the specified zone that have the specified tag.
        :rtype: Tuple[Situation]
        """
        situations = CommonSituationUtils.locate_running_situations_by_tag(tag, zone_id=zone_id)
        if situations:
            return next(iter(situations))
        return None

    @staticmethod
    def locate_first_running_situation_by_tags(tags: Iterator[CommonGameTag], zone_id: int=None) -> Union[Situation, None]:
        """locate_first_running_situation_by_tag(situation_type, zone_id=None)

        Locate the first running Situation from a Zone by a collection of tags.

        :param tags: A list of tags to search for the situation with.
        :type tags: Iterator[CommonGameTag]
        :param zone_id: The zone to locate the situations in. Default is None, which is the current zone.
        :type zone_id: int, optional
        :return: A collection of situations from the specified zone that have the specified tag.
        :rtype: Tuple[Situation]
        """
        situations = CommonSituationUtils.locate_running_situations_by_tags(tags, zone_id=zone_id)
        if situations:
            return next(iter(situations))
        return None

    @staticmethod
    def locate_running_situations_by_type(situation_type: Type[Situation], zone_id: int=None) -> Tuple[Situation]:
        """locate_running_situations_by_type(situation_type, zone_id=None)

        Locate all running Situations in a Zone by Type.

        :param situation_type: The type of situation to search for.
        :type situation_type: Type[Situation]
        :param zone_id: The zone to locate the situations in. Default is None, which is the current zone.
        :type zone_id: int, optional
        :return: A collection of situations from the specified zone that have the specified tag.
        :rtype: Tuple[Situation]
        """
        if situation_type is None:
            return tuple()
        situation_manager = CommonSituationUtils.get_situation_manager_for_zone(zone_id=zone_id)
        return tuple(situation_manager.get_situations_by_type(situation_type))

    @staticmethod
    def locate_running_situations_by_tag(tag: CommonGameTag, zone_id: int=None) -> Tuple[Situation]:
        """locate_running_situations_by_tag(tag, zone_id=None)

        Locate all running Situations in a Zone by a tag.

        :param tag: A tag to search for situations with.
        :type tag: CommonGameTag
        :param zone_id: The zone to locate the situations in. Default is None, which is the current zone.
        :type zone_id: int, optional
        :return: A collection of situations from the specified zone that have the specified tag.
        :rtype: Tuple[Situation]
        """
        if tag is None:
            return tuple()
        return CommonSituationUtils.locate_running_situations_by_tags((tag,), zone_id=zone_id)

    @staticmethod
    def locate_running_situations_by_tags(tags: Iterator[CommonGameTag], zone_id: int=None) -> Tuple[Situation]:
        """locate_running_situations_by_tags(tags, zone_id=None)

        Locate all running Situations in a Zone by a collection of tags.

        :param tags: A list of tags to search for situations with.
        :type tags: Iterator[CommonGameTag]
        :param zone_id: The zone to locate the situations in. Default is None, which is the current zone.
        :type zone_id: int, optional
        :return: A collection of situations from the specified zone that have any of the specified tags.
        :rtype: Tuple[Situation]
        """
        tags = tuple(tags)
        if not tags:
            return tuple()
        situation_manager: SituationManager = CommonSituationUtils.get_situation_manager_for_zone(zone_id=zone_id)
        return tuple(situation_manager.get_situations_by_tags(set(tags)))

    @staticmethod
    def load_situation_by_id(situation_guid: Union[int, CommonSituationId, Situation]) -> Union[Situation, None]:
        """load_situation_by_id(situation_id)

        Load an instance of a Situation by its decimal identifier (GUID).

        :param situation_guid: The decimal identifier of a Situation. (Not to be confused with the instance id)
        :type situation_guid: Union[int, CommonSituationId, Situation]
        :return: An instance of a Situation matching the decimal identifier or None if not found.
        :rtype: Union[Situation, None]
        """
        if isinstance(situation_guid, Situation):
            return situation_guid
        # noinspection PyBroadException
        try:
            # noinspection PyCallingNonCallable
            situation_instance = situation_guid()
            if isinstance(situation_instance, Situation):
                return situation_guid
        except:
            pass
        # noinspection PyBroadException
        try:
            situation_guid: int = int(situation_guid)
        except:
            situation_guid: Situation = situation_guid
            return situation_guid

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.SITUATION, situation_guid)
