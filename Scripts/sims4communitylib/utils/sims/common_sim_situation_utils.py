"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from typing import Callable, Iterator, Union, List, Tuple, Type

from distributor.shared_messages import IconInfoData
from sims.sim_info import SimInfo
from sims4communitylib.enums.situations_enum import CommonSituationId
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.resources.common_situation_utils import CommonSituationUtils
from situations.dynamic_situation_goal_tracker import DynamicSituationGoalTracker
from situations.situation import Situation
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from situations.situation_goal import SituationGoal
from situations.situation_goal_targeted_sim import SituationGoalTargetedSim
from situations.situation_goal_tracker import SituationGoalTracker
from situations.situation_guest_list import SituationInvitationPurpose, SituationGuestList, SituationGuestInfo
from situations.situation_job import SituationJob
from whims.whim_set import WhimSetBaseMixin


class CommonSimSituationUtils(HasClassLog):
    """Utilities for manipulating the Situations of Sims.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_sim_situation_utils'

    @staticmethod
    def has_situation(sim_info: SimInfo, situation_guid: Union[int, CommonSituationId]) -> bool:
        """has_situation(sim_info, situation_guid)

        Determine if a Sim is involved in the specified Situation.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param situation_guid: The GUID of a Situation.
        :type situation_guid: Union[int, CommonSituationId]
        :return: True, if the Sim is involved in the specified Situation. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        return situation_guid in CommonSimSituationUtils.get_situation_guids(sim_info)

    # noinspection SpellCheckingInspection
    @staticmethod
    def has_situations(sim_info: SimInfo, situation_guids: Iterator[Union[int, CommonSituationId]]) -> bool:
        """has_situations(sim_info, situation_guids)

        Determine if a Sim is involved in any of the specified Situations.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param situation_guids: The GUID of Situations.
        :type situation_guids: Iterator[Union[int, CommonSituationId]]
        :return: True, if the Sim has any of the specified situations. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        for situation_guid in CommonSimSituationUtils.get_situation_guids(sim_info):
            if situation_guid in situation_guids:
                return True
        return False

    @staticmethod
    def has_situation_job(sim_info: SimInfo, situation_job_id: int) -> bool:
        """has_situation_job(sim_info, situation_job_id)

        Determine if a Sim has been assigned a situation job.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param situation_job_id: The situation job to check for.
        :type situation_job_id: int
        :return: True, if the Sim has the specified situation job. False, if not.
        :rtype: bool
        """
        return CommonSimSituationUtils.has_situation_jobs(sim_info, (situation_job_id,))

    @staticmethod
    def has_situation_jobs(sim_info: SimInfo, situation_job_ids: Tuple[int]) -> bool:
        """has_situation_jobs(sim_info, situation_job_ids)

        Determine if a Sim has been assigned any specified situation jobs.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param situation_job_ids: The situation jobs to check for.
        :type situation_job_ids: Tuple[int]
        :return: True, if the Sim has any of the specified situation jobs. False, if not.
        :rtype: bool
        """
        sim_situations = CommonSimSituationUtils.get_situations(sim_info)
        for situation in sim_situations:
            for situation_job in situation.all_jobs_gen():
                situation_job_id = CommonSituationUtils.get_situation_job_guid(situation_job)
                if situation_job_id < 0:
                    continue
                if situation_job_id in situation_job_ids:
                    return True
        return False

    @staticmethod
    def has_leave_situation(sim_info: SimInfo) -> bool:
        """has_situation_jobs(sim_info, situation_job_ids)

        Determine if a Sim is currently involved in a leaving situation.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently involved in a leaving situation. False, if not.
        :rtype: bool
        """
        leave_tags: Tuple[CommonGameTag] = (CommonGameTag.ROLE_LEAVE,)
        return CommonSimSituationUtils.has_situations(sim_info, (CommonSituationId.LEAVE, )) or CommonSimSituationUtils.is_in_situations_with_any_tags(sim_info, leave_tags)

    @staticmethod
    def is_assigned_situation_job(sim_info: SimInfo, situation_job_id: int) -> bool:
        """is_assigned_situation_job(sim_info, situation_job_id)

        Determine if a Sim is currently assigned a situation job.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param situation_job_id: The decimal identifier of a Situation Job.
        :type situation_job_id: int
        :return: True, if the Sim is assigned the specified situation job. False, if not.
        :rtype: bool
        """
        return CommonSimSituationUtils.is_assigned_situation_jobs(sim_info, (situation_job_id, ))

    @staticmethod
    def is_assigned_situation_jobs(sim_info: SimInfo, situation_job_ids: Tuple[int]) -> bool:
        """is_assigned_situation_jobs(sim_info, situation_job_ids)

        Determine if a Sim is currently assigned any of the specified situation jobs.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param situation_job_ids: A collection of decimal identifier for Situation Jobs.
        :type situation_job_ids: Tuple[int]
        :return: True, if the Sim is assigned any of the specified situation jobs. False, if not.
        :rtype: bool
        """
        sim_situations = CommonSimSituationUtils.get_situations(sim_info)
        for situation in sim_situations:
            for situation_job in situation.all_jobs_gen():
                situation_job_id = getattr(situation_job, 'guid64', None)
                if situation_job_id in situation_job_ids:
                    return True
        return False

    @staticmethod
    def is_in_situations_with_tag(sim_info: SimInfo, tag: CommonGameTag) -> bool:
        """is_in_situations_with_tag(sim_info, tag)

        Determine if a Sim is currently in a situation with a tag.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param tag: A tag to check for.
        :type tag: CommonGameTag
        :return: True, if the Sim is involved in any situations with any of the specified tags. False, if not.
        :rtype: bool
        """
        return CommonSimSituationUtils.is_in_situations_with_any_tags(sim_info, (tag,))

    @staticmethod
    def is_in_situations_with_any_tags(sim_info: SimInfo, tags: Tuple[CommonGameTag]) -> bool:
        """is_in_situations_with_any_tags(sim_info, tags)

        Determine if a Sim is currently in a situation with any of the specified tags.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param tags: A collection of game tags.
        :type tags: Tuple[CommonGameTag]
        :return: True, if the Sim is involved in any situations with any of the specified tags. False, if not.
        :rtype: bool
        """
        tags = set(tags)
        situations = CommonSimSituationUtils.get_situations(sim_info)
        for tag in tags:
            for situation in situations:
                if tag in getattr(situation, 'tags', tuple()):
                    return True
                for situation_job in situation.all_jobs_gen():
                    if tag in getattr(situation_job, 'tags', tuple()):
                        return True
        return False

    @staticmethod
    def is_in_situations_of_type(sim_info: SimInfo, situation_type: Type[Situation]) -> bool:
        """is_in_situations_of_type(sim_info, situation_type)

        Determine if a Sim is currently in a situation that is of the a specific type.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param situation_type: The type of situation to check.
        :type situation_type: Type[Situation]
        :return: True, if the Sim is involved in any situations with any of the specified tags. False, if not.
        :rtype: bool
        """
        return any(CommonSimSituationUtils.get_running_situations_sim_is_in_by_type(sim_info, situation_type))

    @staticmethod
    def make_sim_leave(sim_info: SimInfo):
        """make_sim_leave(sim_info)

        Make a Sim leave the current lot.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        """
        if sim_info is None:
            return
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return
        services.get_zone_situation_manager().make_sim_leave(sim)

    @staticmethod
    def remove_sim_from_situation(sim_info: SimInfo, situation_id: int) -> bool:
        """remove_sim_from_situation(sim_info, situation_id)

        Remove a Sim from a Situation.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param situation_id: The instance identifier of the Situation to remove the Sim from.
        :type situation_id: int
        :return: True, if the Sim was successfully removed from the situation. False, if not.
        :rtype: bool
        """
        situation_manager = services.get_zone_situation_manager()
        if sim_info is None or situation_id is None:
            return False
        situation_manager.remove_sim_from_situation(sim_info, situation_id)
        return True

    @staticmethod
    def create_visit_situation(sim_info: SimInfo, duration_override_in_sim_seconds: int = None, visit_situation_override: Situation = None):
        """create_visit_situation(sim_info, duration_override_in_sim_seconds=None, visit_situation_override=None)

        Create a visit situation for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param duration_override_in_sim_seconds: An override in Sim seconds for the visit to last. Default is None.
        :type duration_override_in_sim_seconds: int, optional
        :param visit_situation_override: An instance of a Situation to use for the Visit. If not specified, the default visit situation will be used. Default is None.
        :type visit_situation_override: Situation, optional
        """
        if sim_info is None:
            return
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return
        services.get_zone_situation_manager().create_visit_situation(sim, duration_override=duration_override_in_sim_seconds, visit_type_override=visit_situation_override)

    @staticmethod
    def create_situation_for_sim(
        sim_info: SimInfo,
        situation_type: Type[Situation],
        creation_source: str,
        invite_only: bool = True,
        user_facing: bool = False,
        situation_job: SituationJob = None,
        purpose: SituationInvitationPurpose = SituationInvitationPurpose.INVITED,
        **__
    ) -> int:
        """create_situation_for_sim(\
            sim_info,\
            situation_type,\
            creation_source,\
            invite_only=True,\
            user_facing=False,\
            situation_job=None,\
            purpose=SituationInvitationPurpose.INVITED,\
            **__\
        )

        Create a situation and put a Sim in it.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param situation_type: The type of situation to create.
        :type situation_type: Type[Situation]
        :param invite_only: If True, the situation will be invitation only. Default is True.
        :type invite_only: bool, optional
        :param user_facing: If True, the situation will be visible to the player (Like an Active Situation would be). If False, it will not be visible. Default is False.
        :type user_facing: bool, optional
        :param situation_job: The Situation Job to assign to the Sim upon situation creation. Default is whatever the situation specifies as the default job.
        :type situation_job: SituationJob, optional
        :param creation_source: The source of creation.
        :type creation_source: str
        :param purpose: The purpose of the situation. Default is SituationInvitationPurpose.INVITED.
        :type purpose: SituationInvitationPurpose, optional
        :return: The identifier of the situation that was created or 0 if an error occurs.
        :rtype: int
        """
        if sim_info is None:
            raise AssertionError('sim_info was None!')
        from sims4communitylib.utils.resources.common_situation_utils import CommonSituationUtils
        situation_manager = CommonSituationUtils.get_situation_manager_for_zone()
        guest_list = SituationGuestList(invite_only=invite_only)
        guest_info = SituationGuestInfo.construct_from_purpose(CommonSimUtils.get_sim_id(sim_info), situation_job or situation_type.default_job(), purpose)
        guest_list.add_guest_info(guest_info)
        situation_id = situation_manager.create_situation(situation_type, guest_list=guest_list, user_facing=user_facing, creation_source=creation_source, **__)
        if not situation_id:
            return 0
        return situation_id

    @staticmethod
    def complete_situation_goal(sim_info: SimInfo, situation_goal_id: int, target_sim_info: SimInfo = None, score_override: int = None, start_cooldown: bool = True):
        """complete_situation_goal(sim_info, situation_goal_id, target_sim_info=None, score_override=None, start_cooldown=True)

        Complete a situation goal for a Sim using the specified Target Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param situation_goal_id: The decimal identifier of a Situation Goal to mark as completed.
        :type situation_goal_id: int
        :param target_sim_info: A target used in the completion of the situation goal. Default is None.
        :type target_sim_info: SimInfo, optional
        :param score_override: An alternative score to award to the Sim instead of the score specified by the goal. Default is None.
        :type score_override: int, optional
        :param start_cooldown: Whether or not to start a cooldown for the situation. Default is True.
        :type start_cooldown: bool, optional
        """
        from sims4communitylib.utils.sims.common_whim_utils import CommonWhimUtils
        if target_sim_info is not None:
            if CommonSimUtils.get_sim_instance(target_sim_info) is None:
                return
        goal_instances: List[Union[SituationGoal, SituationGoalTargetedSim, WhimSetBaseMixin]] = []
        goal_instances.extend(CommonSimSituationUtils.get_situation_goals(sim_info))
        goal_instances.extend(CommonWhimUtils.get_current_whims(sim_info))
        for goal_instance in goal_instances:
            if goal_instance.guid64 != situation_goal_id:
                continue
            goal_instance.force_complete(target_sim=CommonSimUtils.get_sim_instance(target_sim_info), score_override=score_override, start_cooldown=start_cooldown)

    # noinspection SpellCheckingInspection
    @staticmethod
    def get_guids_of_all_running_situations_for_sim(sim_info: SimInfo) -> Tuple[int]:
        """get_guids_of_all_running_situations_for_sim(sim_info)

        Retrieve GUIDs for all Situations a Sim is involved in.

        :param sim_info: The sim to check.
        :type sim_info: SimInfo
        :return: A collection of Situation GUIDs the specified Sim is involved in.
        :rtype: Tuple[int]
        """
        situation_guids = []
        for situation in CommonSimSituationUtils.get_situations(sim_info):
            situation_guid = CommonSituationUtils.get_situation_guid(situation)
            if situation_guid is None and situation_guid != -1:
                continue
            situation_guids.append(situation_guid)
        return tuple(situation_guids)

    @staticmethod
    def get_situations(sim_info: SimInfo, include_situation_callback: Callable[[Situation], bool] = None) -> Iterator[Situation]:
        """get_situations(sim_info, include_situation_callback=None)

        Retrieve all Situations that a Sim is currently involved in.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param include_situation_callback: If the result of this callback is True, the Situation will be included in the results. If set to None, All situations will be included. Default is None.
        :type include_situation_callback: Callable[[Situation], bool], optional
        :return: An iterator of Situations that pass the include callback filter.
        :rtype: Iterator[Situation]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return
        situations = tuple(services.get_zone_situation_manager().get_situations_sim_is_in(sim))
        if sim is None or not situations:
            return tuple()
        for situation in situations:
            if include_situation_callback is not None and not include_situation_callback(situation):
                continue
            yield situation

    @staticmethod
    def get_first_running_situation_sim_is_in_by_type(sim_info: SimInfo, situation_type: Type[Situation]) -> Union[Situation, None]:
        """get_first_running_situation_sim_is_in_by_type(sim_info, situation_type)

        Retrieve the first Situation that a Sim is currently involved in that is a specific type.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param situation_type: A situation type to locate a situation with.
        :type situation_type: Type[Situation]
        :return: A situation the Sim is involved in that is of the specified type or None if not found.
        :rtype: Union[Situation, None]
        """
        for situation in CommonSimSituationUtils.get_running_situations_sim_is_in_by_type(sim_info, situation_type):
            return situation
        return None

    @staticmethod
    def get_first_running_situation_sim_is_in_by_tag(sim_info: SimInfo, tag: CommonGameTag) -> Union[Situation, None]:
        """get_first_running_situation_sim_is_in_by_tag(sim_info, tag)

        Retrieve the first Situation that a Sim is currently involved in that has a tag.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param tag: The tag to locate a situation with.
        :type tag: CommonGameTag
        :return: A situation the Sim is involved in that has the specified tag or None if not found.
        :rtype: Union[Situation, None]
        """
        for situation in CommonSimSituationUtils.get_running_situations_sim_is_in_by_tag(sim_info, tag):
            return situation
        return None

    @staticmethod
    def get_running_situations_sim_is_in_by_tag(sim_info: SimInfo, tag: CommonGameTag) -> Tuple[Situation]:
        """get_running_situations_sim_is_in_by_tag(sim_info, tag)

        Retrieve all Situations that a Sim is currently involved in that have the specified tag.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param tag: The tag to locate situations with.
        :type tag: CommonGameTag
        :return: An iterator of Situations the Sim is running that have the specified tag.
        :rtype: Iterator[Situation]
        """
        def _situation_has_tag(_situation: Situation) -> bool:
            if hasattr(_situation, 'tags'):
                return tag in _situation.tags
            return False

        return tuple(CommonSimSituationUtils.get_situations(sim_info, include_situation_callback=_situation_has_tag))

    @staticmethod
    def get_running_situations_sim_is_in_by_tags(sim_info: SimInfo, tags: Tuple[CommonGameTag]) -> Tuple[Situation]:
        """get_running_situations_sim_is_in_by_tag(sim_info, tags)

        Retrieve all Situations that a Sim is currently involved in that have the specified tag.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param tags: A collection of tags to locate situations with. Matching situations will have at least one of these tags.
        :type tags: Iterator[CommonGameTag]
        :return: An iterator of Situations the Sim is running that have any of the specified tags.
        :rtype: Iterator[Situation]
        """
        matching_situations: List[Situation] = list()
        for tag in tags:
            for situation in CommonSimSituationUtils.get_running_situations_sim_is_in_by_tag(sim_info, tag):
                if situation not in matching_situations:
                    matching_situations.append(situation)
        return tuple(matching_situations)

    @staticmethod
    def get_running_situations_sim_is_in_by_type(sim_info: SimInfo, situation_type: Type[Situation]) -> Tuple[Situation]:
        """get_running_situations_sim_is_in_by_type(sim_info, situation_type)

        Retrieve all Situations that a Sim is currently involved in that match the specified type.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param situation_type: A situation type to locate situations with.
        :type situation_type: Type[Situation]
        :return: An iterator of Situations the Sim is running that are of the specified type.
        :rtype: Iterator[Situation]
        """
        def _situation_is_of_type(_situation: Situation) -> bool:
            return isinstance(_situation, situation_type)

        return tuple(CommonSimSituationUtils.get_situations(sim_info, include_situation_callback=_situation_is_of_type))

    @staticmethod
    def get_situation_ids(sim_info: SimInfo) -> List[int]:
        """get_situation_ids(sim_info)

        Retrieve decimal identifiers for all Situations a Sim is involved in.

        :param sim_info: The sim to check.
        :type sim_info: SimInfo
        :return: A collection of Situation decimal identifiers the specified Sim is involved in.
        :rtype: List[int]
        """
        situation_ids = []
        for situation in CommonSimSituationUtils.get_situations(sim_info):
            situation_id = CommonSituationUtils.get_situation_id(situation)
            if situation_id is None and situation_id != -1:
                continue
            situation_ids.append(situation_id)
        return situation_ids

    # noinspection SpellCheckingInspection
    @staticmethod
    def get_situation_guids(sim_info: SimInfo) -> List[int]:
        """get_situation_guids(sim_info)

        Retrieve GUIDs for all Situations a Sim is involved in.

        :param sim_info: The sim to check.
        :type sim_info: SimInfo
        :return: A collection of Situation GUIDs the specified Sim is involved in.
        :rtype: List[int]
        """
        situation_guids = []
        for situation in CommonSimSituationUtils.get_situations(sim_info):
            situation_guid = CommonSituationUtils.get_situation_guid(situation)
            if situation_guid is None and situation_guid != -1:
                continue
            situation_guids.append(situation_guid)
        return situation_guids

    @staticmethod
    def get_situation_goals(sim_info: SimInfo) -> Tuple[Union[SituationGoal, SituationGoalTargetedSim]]:
        """get_situation_goals(sim_info)

        Retrieve the goals of all situations a Sim is currently in.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The situation goals of all Situations the Sim is currently involved in.
        :rtype: Tuple[Union[SituationGoal, SituationGoalTargetedSim]]
        """
        goal_instances: List[Union[SituationGoal, SituationGoalTargetedSim]] = []
        for situation in CommonSimSituationUtils.get_situations(sim_info):
            goal_tracker = situation._get_goal_tracker()
            if goal_tracker is None:
                continue
            if isinstance(goal_tracker, SituationGoalTracker):
                if goal_tracker._realized_minor_goals is not None:
                    goal_instances.extend(goal_tracker._realized_minor_goals.keys())
                if goal_tracker._realized_main_goal is not None:
                    goal_instances.insert(0, goal_tracker._realized_main_goal)
            elif isinstance(goal_tracker, DynamicSituationGoalTracker):
                goal_instances.extend(goal_tracker.goals)
        return tuple(goal_instances)


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_situations',
    'Print a list of all situations a Sim is in.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib_testing.printsituations',
    )
)
def _common_show_running_situations(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        return
    log = CommonSimSituationUtils.get_log()
    try:
        log.enable()
        output(f'Attempting to print all running situations of Sim {sim_info}')
        situation_strings: List[str] = list()
        for situation in CommonSimSituationUtils.get_situations(sim_info):
            situation_name = CommonSituationUtils.get_situation_name(situation)
            situation_id = CommonSituationUtils.get_situation_id(situation)
            situation_strings.append(f'{situation_name} ({situation_id})')

        situation_strings = sorted(situation_strings, key=lambda x: x)
        sim_situations = ', '.join(situation_strings)
        text = ''
        text += f'Situations:\n{sim_situations}\n\n'
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        log.debug(f'{sim_info} Situations ({sim_id})')
        log.debug(text)
        CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string(f'{sim_info} Situations ({sim_id})'),
            CommonLocalizationUtils.create_localized_string(text)
        ).show(
            icon=IconInfoData(obj_instance=CommonSimUtils.get_sim_instance(sim_info))
        )
    finally:
        log.disable()
