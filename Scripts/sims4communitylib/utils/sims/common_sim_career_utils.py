"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Union, Callable, Iterator, Tuple

import services
from careers.career_enums import CareerShiftType, CareerCategory
from careers.career_event import CareerEvent
from careers.career_history import CareerHistory
from careers.career_tracker import CareerTracker
from careers.career_tuning import Career, CareerLevel, TunableCareerTrack
from event_testing.resolver import SingleSimResolver
from rewards.reward_enums import RewardType
from server_commands.argument_helpers import TunableInstanceParam
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from sims4communitylib.utils.sims.common_career_track_utils import CommonCareerTrackUtils
from sims4communitylib.utils.sims.common_career_utils import CommonCareerUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from singletons import DEFAULT


class CommonSimCareerUtils(_HasS4CLClassLog):
    """ Utilities for manipulating the Careers of Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_sim_career_utils'

    @classmethod
    def get_career_by_category(cls, sim_info: SimInfo, career_category: CareerCategory) -> Union[Career, None]:
        """get_career_by_category(sim_info, career_category)

        Retrieve the career of a Sim by its career category.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param career_category: The category to retrieve the career of.
        :type career_category: CareerCategory
        :return: A career matching the career category specified or None if not found.
        :rtype: Union[Career, None]
        """
        career_tracker = cls.get_career_tracker(sim_info)
        if career_tracker is None:
            return None
        return next(career_tracker.get_careers_by_category_gen(career_category))

    @classmethod
    def get_all_careers_for_sim_gen(cls, sim_info: SimInfo, include_career_callback: Callable[[Career], bool]=None) -> Iterator[Career]:
        """get_all_careers_for_sim_gen(sim_info, include_career_callback=None)

        Retrieve all Careers of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param include_career_callback: If the result of this callback is True, the Career of the Sim will be included in the results. If set to None, All Careers of the Sim will be included. Default is None.
        :type include_career_callback: Callable[[Career], bool], optional
        :return: An iterator of all Careers matching the `include_career_callback` filter.
        :rtype: Iterator[Career]
        """
        if sim_info is None:
            return tuple()
        career_tracker = cls.get_career_tracker(sim_info)
        if career_tracker is None:
            return tuple()
        for career in career_tracker.careers.values():
            if include_career_callback is not None and not include_career_callback(career):
                continue
            yield career

    @classmethod
    def get_first_career(cls, sim_info: SimInfo, include_career_callback: Callable[[Career], bool] = None) -> Union[Career, None]:
        """get_first_career(sim_info, include_career_callback=None)

        Retrieve the first Career a Sim has.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param include_career_callback: If the result of this callback is True, the Career of the Sim will be considered in the result. If set to None, All Careers of the Sim will be considered. Default is None.
        :type include_career_callback: Callable[[Career], bool], optional
        :return: The first career the Sim has, or None if they do not have a career.
        :rtype: Union[Career, None]
        """
        if sim_info is None:
            return None
        for career in cls.get_all_careers_for_sim_gen(sim_info, include_career_callback=include_career_callback):
            return career
        return None

    @classmethod
    def has_career(cls, sim_info: SimInfo, career_identifier: Union[int, Career]) -> bool:
        """has_career_by_guid(sim_info, career)

        Determine if a Sim has a Career.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param career_identifier: The Guid64 identifier of a Career, the decimal identifier of a Career, or a Career instance.
        :type career_identifier: Union[int, Career]
        :return: True, if the Sim has the specified Career. False, if not.
        :rtype: bool
        """
        return cls.get_career(sim_info, career_identifier) is not None

    @classmethod
    def get_career(cls, sim_info: SimInfo, career_identifier: Union[int, Career]) -> Union[Career, None]:
        """get_career(sim_info, career_identifier)

        Retrieve the Career of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param career_identifier: The Guid64 identifier of a Career, the decimal identifier of a Career, or a Career instance.
        :type career_identifier: Union[int, Career]
        :return: The career of the Sim that matches the identifier or None if not found.
        :rtype: Union[Career, None]
        """
        if sim_info is None or career_identifier is None:
            return None
        if not isinstance(career_identifier, Career):
            cls.get_log().format_with_message('Identifier was not a Career instance. Attempting to load it now.', career_identifier=career_identifier)
            career_identifier = CommonCareerUtils.load_career_by_guid(career_identifier)
        career_guid = CommonCareerUtils.get_career_guid(career_identifier)
        career_id = CommonCareerUtils.get_career_id(career_identifier)
        if career_guid is None and career_id is None:
            return None
        cls.get_log().format_with_message('Checking for career info.', career_identifier=career_identifier, career_guid=career_guid, career_id=career_id)
        career_tracker = cls.get_career_tracker(sim_info)
        if career_tracker is None:
            return None
        for career in cls.get_all_careers_for_sim_gen(sim_info):
            if (career_guid is not None and career_guid != -1  and CommonCareerUtils.get_career_guid(career) == career_guid)\
                    or (career_id is not None and career_id != -1 and CommonCareerUtils.get_career_id(career) == career_id)\
                    or career is career_identifier:
                cls.get_log().format_with_message('Successfully found career.', career=career, career_identifier=career_identifier, career_guid=career_guid, career_id=career_id, checked_career_guid=CommonCareerUtils.get_career_guid(career), checked_career_id=CommonCareerUtils.get_career_id(career))
                return career
        cls.get_log().format_with_message('Failed to locate career.', career_identifier=career_identifier, career_guid=career_guid, career_id=career_id)
        return None

    @classmethod
    def has_career_at_current_zone(cls, sim_info: SimInfo) -> bool:
        """has_career_at_current_zone(sim_info)

        Determine if a Sim has a Career at the current zone.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a Career at the current zone. False, if not.
        :rtype: bool
        """
        return cls.get_career_at_current_zone(sim_info)

    @classmethod
    def get_career_at_current_zone(cls, sim_info: SimInfo) -> Union[Career, None]:
        """get_career_at_current_zone(sim_info)

        Retrieve the Career of a Sim that has its location set to the current zone.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim works at the current zone. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return None
        current_zone_id = CommonLocationUtils.get_current_zone_id()
        for career in cls.get_all_careers_for_sim_gen(sim_info):
            career_zone_id = CommonCareerUtils.get_career_location_zone_id(career)
            if career_zone_id == 0:
                continue
            if career_zone_id == current_zone_id:
                return career
        return None

    @classmethod
    def is_at_work(cls, sim_info: SimInfo) -> bool:
        """is_at_work(sim_info)

        Determine if a Sim is currently at work.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently at work for any of their careers. False, if not.
        :rtype: bool
        """
        for career in cls.get_all_careers_for_sim_gen(sim_info):
            if career.currently_at_work:
                return True
        return False

    @classmethod
    def has_career_tracker(cls, sim_info: SimInfo) -> bool:
        """has_career_tracker(sim_info)

        Determine if a Sim has a career tracker or not.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a career tracker. False, if not.
        :rtype: bool
        """
        return cls.get_career_tracker(sim_info) is not None

    @classmethod
    def get_career_tracker(cls, sim_info: SimInfo) -> Union[CareerTracker, None]:
        """get_career_tracker(sim_info)

        Retrieve a career tracker for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The career tracker of the Sim or None if not found.
        :rtype: Union[CareerTracker, None]
        """
        if sim_info is None:
            return None
        # noinspection PyTypeChecker
        return sim_info.career_tracker

    @classmethod
    def is_taking_part_in_active_career_event(cls, sim_info: SimInfo) -> bool:
        """is_taking_part_in_active_career_event(sim_info)

        Determine if a Sim is taking part in an active career event.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is taking part in an active career event. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        return any(career.is_at_active_event for career in sim_info.careers.values())

    @classmethod
    def is_sim_household_part_of_active_career_event(cls, sim_info: SimInfo) -> bool:
        """is_household_part_of_active_career_event(sim_info)

        Determine if any members of a Sims Household are part of an active career event.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if any members of the Sims Household are taking part in an active career event. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        household = CommonHouseholdUtils.get_household(sim_info)
        for sim_info in CommonHouseholdUtils.get_sim_info_of_all_sims_in_household_generator(household):
            if cls.is_taking_part_in_active_career_event(sim_info):
                return True
        return False

    @classmethod
    def attend_career(cls, career: Career, allow_career_events: bool=True) -> CommonExecutionResult:
        """attend_career(career, allow_career_events=True)

        Start a career without running any career events (If they are an active career).

        :param career: The career to mark.
        :type career: Career
        :param allow_career_events: If True, a career event will be started for active careers. If False, a career event will not be started for active careers. No effect on non active careers. Default is True.
        :rtype: allow_career_events: bool, optional
        :return: Tbe result of the action.
        :rtype: CommonExecutionResult
        """
        if allow_career_events and career.is_active:
            return cls.start_active_career_on_current_lot(career)

        if services.get_persistence_service().is_save_locked():
            return CommonExecutionResult(False, reason='Currently save locked.', tooltip_text=CommonStringId.S4CL_CURRENTLY_SAVE_LOCKED)
        if not services.get_career_service().enabled:
            return CommonExecutionResult(False, reason='Career service is not enabled.', hide_tooltip=True)
        from date_and_time import create_time_span
        start_time = CommonTimeUtils.get_current_date_and_time()
        end_time = start_time + create_time_span(hours=10)

        if start_time > end_time:
            return CommonExecutionResult(False, reason='Start time is greater than end time.', hide_tooltip=True)

        career._at_work = False
        career._career_session_extended = False
        gig = career.get_current_gig()
        if gig is not None:
            gig.prep_time_end()

        career._current_work_start = start_time
        career._current_work_end = end_time
        career._current_work_duration = career._current_work_end - career._current_work_start
        career._create_work_session_alarms()
        career.resend_at_work_info()
        if gig is None or gig.odd_job_tuning is None:
            tracker = career._sim_info.get_tracker(career.WORK_SESSION_PERFORMANCE_CHANGE)
            if tracker is not None:
                career._sim_info.add_statistic(career.WORK_SESSION_PERFORMANCE_CHANGE, career.WORK_SESSION_PERFORMANCE_CHANGE.initial_value)

        if career.is_school_career and not career._sim_info.is_npc:
            career.reset_homework_help()

        career.active_days_worked_statistic.add_value(1)
        career.resend_at_work_info()
        career.attend_work(start_tones=False)
        from careers.career_base import TELEMETRY_WORKDAY_TYPE_ACTIVE
        career._send_workday_info_telemetry(TELEMETRY_WORKDAY_TYPE_ACTIVE)
        return CommonExecutionResult.TRUE

    @classmethod
    def start_active_career_on_current_lot(cls, career: Career, career_event: CareerEvent=None) -> CommonExecutionResult:
        """start_active_career_on_current_lot(career, career_event=None)

        Start a career event on the current lot for an Active career.

        .. note:: This function only works if the Career is flagged as an Active Career (is_active in the Tuning).

        :param career: The career to begin.
        :type career: Career
        :param career_event: The career event to trigger. If set to None, a random career event will be chosen from the career. Default is None.
        :type career_event: CareerEvent, optional
        :return: Tbe result of the action.
        :rtype: CommonExecutionResult
        """
        if career is None:
            raise AssertionError('career was None.')
        if not career.is_active:
            return CommonExecutionResult(False, reason='Career is not an active career.', tooltip_text=CommonStringId.S4CL_CAREER_IS_NOT_AN_ACTIVE_CAREER)
        if services.get_persistence_service().is_save_locked():
            return CommonExecutionResult(False, reason='Currently save locked.', tooltip_text=CommonStringId.S4CL_CURRENTLY_SAVE_LOCKED)
        if not services.get_career_service().enabled:
            return CommonExecutionResult(False, reason='Career service is not enabled.', hide_tooltip=True)
        from date_and_time import create_time_span
        start_time = CommonTimeUtils.get_current_date_and_time()
        end_time = start_time + create_time_span(hours=10)

        if start_time > end_time:
            return CommonExecutionResult(False, reason='Start time is greater than end time.', hide_tooltip=True)

        career._at_work = False
        career._career_session_extended = False
        gig = career.get_current_gig()
        if gig is not None:
            gig.prep_time_end()

        career._current_work_start = start_time
        career._current_work_end = end_time
        career._current_work_duration = career._current_work_end - career._current_work_start
        career._create_work_session_alarms()
        career.resend_at_work_info()
        if gig is None or gig.odd_job_tuning is None:
            tracker = career._sim_info.get_tracker(career.WORK_SESSION_PERFORMANCE_CHANGE)
            if tracker is not None:
                career._sim_info.add_statistic(career.WORK_SESSION_PERFORMANCE_CHANGE, career.WORK_SESSION_PERFORMANCE_CHANGE.initial_value)
        if career.is_school_career and not career._sim_info.is_npc:
            career.reset_homework_help()

        if career._sim_info.is_npc:
            return CommonExecutionResult(False, reason='Sim is an NPC, NPCs are not allowed to start active careers.', tooltip_text=CommonStringId.S4CL_SIM_IS_AN_NPC_AND_CANNOT_START_ACTIVE_CAREERS, tooltip_tokens=(career._sim_info,))

        import careers.career_base
        current_gig = career.get_current_gig()
        if career_event is None:
            if career._sim_info in careers.career_base._career_event_overrides:
                career_event = careers.career_base._career_event_overrides.pop(career._sim_info)
            elif current_gig is not None and current_gig.career_events:
                career_event = current_gig.get_random_gig_event()
            else:
                career._prune_stale_career_event_cooldowns()
                resolver = SingleSimResolver(career._sim_info)
                available_events = tuple(event for event in career.career_events if career.is_career_event_on_cooldown(event) or event.tests.run_tests(resolver))
                if not available_events:
                    return CommonExecutionResult(False, reason='No events were available.', tooltip_text=CommonStringId.S4CL_NO_EVENTS_WERE_AVAILABLE)
                household = career._sim_info.household
                for sim_info in household.sim_info_gen():
                    if cls.is_taking_part_in_active_career_event(sim_info):
                        return CommonExecutionResult(False, reason=f'{sim_info} is already at the active event.', tooltip_text=CommonStringId.S4CL_SIM_IS_ALREADY_AT_ACTIVE_EVENT, tooltip_tokens=(sim_info,))
                career_event = random.choice(available_events)

        career.on_career_event_accepted(career_event)
        return CommonExecutionResult.TRUE

    @classmethod
    def randomize_career(
        cls,
        sim_info: SimInfo,
        randomize_career_level: bool = True,
        remove_all_existing_careers: bool = True,
        randomize_agency: bool = True,
        use_career_history: bool = True,
        force_out_of_retirement: bool = True,
        force_quit_previous_jobs: bool = True,
        check_availability: bool = True
    ) -> CommonExecutionResult:
        """set_random_career(\
            sim_info,\
            choose_random_career_level=True,\
            remove_all_existing_careers=True,\
            randomize_agent=True,\
            use_career_history=True,\
            force_out_of_retirement=False,\
            force_quit_previous_jobs=False,\
            check_availability=True\
        )

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param randomize_career_level: If True, a random Career Level will be chosen in addition to the Career. If False, the Career Level will be dictated by the Sim that is joining. Default is True.
        :type randomize_career_level: bool, optional
        :param remove_all_existing_careers: If True, all careers the Sim is currently a part of will be removed. If False, the existing careers of the Sim will not be removed. Default is False.
        :type remove_all_existing_careers: bool, optional
        :param randomize_agency: If True, a random agency from available agencies will be randomly chosen for a Career that has agencies upon being added. If False, the "Select An Agency" dialog will appear. Default is True.
        :type randomize_agency: bool, optional
        :param force_out_of_retirement: If True, the Sim will be forced out of retirement without prompting the player. If False, a dialog will prompt the player to choose whether or not to come out of retirement. Default is False.
        :type force_out_of_retirement: bool, optional
        :param force_quit_previous_jobs: If True, the Sim will be forced to quit all of their previous jobs. If False, a confirmation will display that will prompt the player whether this should happen or not. Default is False.
        :type force_quit_previous_jobs: bool, optional
        :param use_career_history: If True, then the career history of the Sim will be used when adding the Career. If False, then the career history of the Sim will not be used when adding the Career. Default is True.
        :type use_career_history: bool, optional
        :param check_availability: If True, every career will be checked for availability before becoming available. If False, every career regardless of availability will be selectable. Default is True. WARNING: A Career that is not allowed for a Sim may be chosen if this is set to False!
        :type check_availability: bool, optional
        :return: The result of setting their career.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if remove_all_existing_careers:
            cls.remove_careers(sim_info)

        def _career_is_available(_career: Career) -> bool:
            if not check_availability:
                return True
            return bool(cls.is_career_available_for_sim(sim_info, _career, from_join=True))

        all_careers = tuple(CommonCareerUtils.get_all_careers_generator(include_career_callback=_career_is_available))
        if not all_careers:
            return CommonExecutionResult(False, reason=f'No careers found to be available for {sim_info}.', tooltip_text=CommonStringId.S4CL_NO_CAREERS_FOUND_AVAILABLE_FOR_SIM, tooltip_tokens=(sim_info,))
        cls.get_log().format_with_message('Found all available careers.', careers=sorted([f'{career.__name__} ({CommonCareerUtils.get_career_guid(career)})' for career in all_careers], key=lambda x: x))
        chosen_career = random.choice(all_careers)
        career_level = None
        if randomize_career_level:
            career_levels = CommonCareerUtils.get_career_levels(chosen_career)
            if career_levels:
                career_level = random.choice(career_levels)
        result = cls.add_career(sim_info, chosen_career, randomize_agency=randomize_agency, career_level=career_level, use_career_history=use_career_history, force_out_of_retirement=force_out_of_retirement, force_quit_previous_jobs=force_quit_previous_jobs)
        if not result:
            return result
        return CommonExecutionResult(True, reason=f'Added Career {chosen_career.__name__} to {sim_info}.', tooltip_text=CommonStringId.S4CL_ADDED_CAREER_TO_SIM, tooltip_tokens=(chosen_career.__name__, sim_info))

    @classmethod
    def is_career_available_for_sim(cls, sim_info: SimInfo, career: Career, from_join: bool = False) -> CommonTestResult:
        """is_career_available_for_sim(sim_info, career, from_join=False)

        Determine if a Career is available for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param career: A career.
        :type career: Career
        :param from_join: Use to flag whether the career is planned to be tested as though the Sim is joining it. Default is False.
        :type from_join: bool, optional
        :return: The result of testing for availability. True, if the Career is available for the specified Sim. False, if not.
        :rtype: CommonTestResult
        """
        # noinspection PyTypeChecker
        non_playable_career_ids: Tuple[int] = (
            223698,  # University_BaseCareer
            231099,  # career_Batuu
            207004,  # career_OddJob
            209979,  # university_CourseSlot_A
            209984,  # university_CourseSlot_B
            209988,  # university_CourseSlot_C
            209989,  # university_CourseSlot_D
            260893,  # careers_VillagerHelp
            206791,  # careers_Adult_Freelancer_No_Agency
        )
        # noinspection PyTypeChecker
        allowed_non_displayed_career_ids: Tuple[int] = (
            205686,  # career_Adult_Freelancer_Artist
            207568,  # careers_Adult_Freelancer_Agency_Programmer
            207579,  # careers_Adult_Freelancer_Agency_Writer
            214782,  # careers_Adult_Freelancer_Agency_Fashion_Photographer
            232809,  # careers_Adult_Freelancer_Agency_Maker
            252593,  # careers_Adult_Freelancer_Agency_ParanormalInvestigator
        )
        if not CommonSimTypeUtils.is_non_player_sim(sim_info):
            if 'npc' in career.__name__.lower():
                return CommonTestResult(False, reason=f'{career.__name__} is an NPC career and {sim_info} is not an NPC.', tooltip_text=CommonStringId.S4CL_CAREER_IS_NPC_ONLY_CAREER_AND_SIM_IS_NOT_NPC, tooltip_tokens=(career.__name__, sim_info))
        career_guid = CommonCareerUtils.get_career_guid(career)
        if career_guid in non_playable_career_ids:
            return CommonTestResult(False, reason=f'Career {career.__name__} is non playable.', tooltip_text=CommonStringId.S4CL_CAREER_IS_MARKED_AS_NON_PLAYABLE, tooltip_tokens=(career.__name__,))
        valid_result = career.is_valid_career(sim_info=sim_info, from_join=from_join)
        if not valid_result:
            return valid_result
        if career_guid not in allowed_non_displayed_career_ids:
            if from_join and not career.show_career_in_join_career_picker:
                return CommonTestResult(False, reason=f'Career {career.__name__} is not joinable through normal means.', tooltip_text=CommonStringId.S4CL_CAREER_IS_NOT_JOINABLE_THROUGH_NORMAL_MEANS, tooltip_tokens=(career.__name__,))
        return CommonTestResult.TRUE

    @classmethod
    def add_career(
        cls,
        sim_info: SimInfo,
        career_identifier: Union[int, Career],
        remove_all_existing_careers: bool = False,
        randomize_agency: bool = True,
        use_career_history: bool = True,
        force_out_of_retirement: bool = False,
        force_quit_previous_jobs: bool = False,
        show_confirmation_dialog: bool = False,
        user_level: int = None,
        career_level: CareerLevel = None,
        give_skipped_rewards: bool = True,
        defer_rewards: bool = False,
        show_post_quit_message: bool = True,
        schedule_shift_override: CareerShiftType = CareerShiftType.ALL_DAY,
        show_join_message: bool = True,
        disallowed_reward_types: Tuple[RewardType] = (),
        force_rewards_to_sim_info_inventory: bool = False,
        defer_first_assignment: bool = False,
        schedule_init_only: bool = False,
        allow_outfit_generation: bool = True
    ) -> CommonExecutionResult:
        """add_career(\
            sim_info,\
            career_identifier,\
            remove_all_existing_careers=False,\
            randomize_agency=True,\
            use_career_history=True,\
            force_out_of_retirement=False,\
            force_quit_previous_jobs=False,\
            show_confirmation_dialog=False,\
            user_level=None,\
            career_level=None,\
            give_skipped_rewards=True,\
            defer_rewards=False,\
            show_post_quit_message=True,\
            schedule_shift_override=CareerShiftType.ALL_DAY,\
            show_join_message=True,\
            disallowed_reward_types=(),\
            force_rewards_to_sim_info_inventory=False,\
            defer_first_assignment=False,\
            schedule_init_only=False,\
            allow_outfit_generation=True\
        )

        Add a Career to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param career_identifier: The Guid64 identifier of a Career, the decimal identifier of a Career, or a Career instance.
        :type career_identifier: Union[int, Career]
        :param remove_all_existing_careers: If True, all careers the Sim is currently a part of will be removed. If False, the existing careers of the Sim will not be removed. Default is False.
        :type remove_all_existing_careers: bool, optional
        :param randomize_agency: If True, a random agency from available agencies will be randomly chosen for a Career that has agencies upon being added. If False, the "Select An Agency" dialog will appear. Default is True.
        :type randomize_agency: bool, optional
        :param use_career_history: If True, then the career history of the Sim will be used when adding the Career. If False, then the career history of the Sim will not be used when adding the Career. Default is True.
        :type use_career_history: bool, optional
        :param force_out_of_retirement: If True, the Sim will be forced out of retirement without prompting the player. If False, a dialog will prompt the player to choose whether or not to come out of retirement. Default is False.
        :type force_out_of_retirement: bool, optional
        :param force_quit_previous_jobs: If True, the Sim will be forced to quit all of their previous jobs. If False, a confirmation will display that will prompt the player whether this should happen or not. Default is False.
        :type force_quit_previous_jobs: bool, optional
        :param show_confirmation_dialog: Show Confirmation Dialog. Default is False.
        :type show_confirmation_dialog: bool, optional
        :param user_level: The level of the career track to assign to the Sim upon joining the career. Default is None.
        :type user_level: int, optional
        :param career_level: The Career Level to set the Sim to upon joining the career. Default is None.
        :type career_level: CareerLevel, optional
        :param give_skipped_rewards: If True, any rewards skipped due to the career level skips will be given to the Sim upon joining the career. If False, no rewards will be given for career levels before the one they join into. Default is True.
        :type give_skipped_rewards: bool, optional
        :param defer_rewards: If True, rewards will be deferred until later. If False, rewards will be given immediately. Default is False.
        :type defer_rewards: bool, optional
        :param show_post_quit_message: If True, the quit message for their existing career before switching will be displayed. If False, the quit message will not be displayed. Default is True.
        :type show_post_quit_message: bool, optional
        :param schedule_shift_override: An override for the Sims shift schedule. Default is CareerShiftType.ALL_DAY.
        :type schedule_shift_override:  CareerShiftType, optional
        :param show_join_message: If True, the joined career message will be displayed after joining the career. If False, the join message will not be displayed. Default is True.
        :type show_join_message: bool, optional
        :param disallowed_reward_types: A collection of rewards types not allowed to be collected by the Sim that is joining. If empty, all rewards will be allowed to be rewarded. Default is empty.
        :type disallowed_reward_types: Tuple[RewardType], optional
        :param force_rewards_to_sim_info_inventory: If True, rewards will be forced in the inventory of the joining Sim. If False, rewards will be sent to their intended locations as specified by the career. Default is False.
        :type force_rewards_to_sim_info_inventory: bool, optional
        :param defer_first_assignment: If True, the first assignment upon joining the career will be delayed until later. If False, the first assignment will not be delayed. Default is False.
        :type defer_first_assignment: bool, optional
        :param schedule_init_only: If True, Shift schedule will only be initialized. If False, Shift schedule will be setup fully. Default is False.
        :type schedule_init_only: bool, optional
        :param allow_outfit_generation: If True, an outfit for the career will be generated upon join. If False, an outfit will not be generated. Default is True.
        :type allow_outfit_generation: bool, optional
        :return: The result of adding the Career or the reason why it was not properly added.
        :rtype: CommonExecutionResult
        """
        if sim_info is None or career_identifier is None:
            return CommonExecutionResult(False, reason=f'Sim or Career Identifier was None Sim: {sim_info} ID: {career_identifier}.', hide_tooltip=True)
        if remove_all_existing_careers:
            cls.remove_careers(sim_info)
        career = CommonCareerUtils.load_career_by_guid(career_identifier)
        career_tracker = cls.get_career_tracker(sim_info)
        if career_tracker is None:
            return CommonExecutionResult(False, reason=f'The Sim did not have a career tracker. {sim_info}', hide_tooltip=True)
        if career_tracker.has_career_by_uid(CommonCareerUtils.get_career_guid(career)):
            cls.get_log().format_with_message('Sim already had the specified career.', sim=sim_info, career=career)
            return CommonExecutionResult.TRUE

        picked_track: Union[TunableCareerTrack, None] = None
        if career_level is None and user_level is not None:
            (career_level_index, _, picked_track) = CommonCareerUtils.determine_entry_level_into_career_from_user_level(career, user_level)
            picked_track: TunableCareerTrack = picked_track
            career_level = CommonCareerTrackUtils.get_career_level_by_index(picked_track, career_level_index)
        elif career_level is None:
            entry_level_values = tuple(cls.determine_entry_level_into_career_for_sim(sim_info, career, use_career_history=use_career_history))
            cls.get_log().format_with_message('Got entry level values', entry_level_values=entry_level_values)
            if len(entry_level_values) == 1:
                entry_level_values = entry_level_values[0]
            (career_level_index, _, picked_track) = entry_level_values
            picked_track: TunableCareerTrack = picked_track
            career_level = CommonCareerTrackUtils.get_career_level_by_index(picked_track, career_level_index)
            cls.get_log().format_with_message('Got career level.', career_level=career_level_index, returned_user_level=_, picked_track=picked_track)

        if career_level is None:
            cls.get_log().format_with_message('No career level found.', sim=sim_info, career_history=career_tracker.career_history, career=career)
            return CommonExecutionResult(False, reason=f'Failed to locate career level for Sim {sim_info}, Career {career}, and Career History {career_tracker.career_history}.', hide_tooltip=True)

        cls.get_log().format_with_message('Adding new career.', picked_track=picked_track, career_level=career_level, sim=sim_info, career=career)
        new_career = career_level.career(sim_info)
        return cls._add_career(
            career_tracker,
            new_career,
            randomize_agency=randomize_agency,
            use_career_history=use_career_history,
            force_out_of_retirement=force_out_of_retirement,
            force_quit_previous_jobs=force_quit_previous_jobs,
            show_confirmation_dialog=show_confirmation_dialog,
            user_level_override=user_level,
            career_level_override=career_level,
            give_skipped_rewards=give_skipped_rewards,
            defer_rewards=defer_rewards,
            post_quit_msg=show_post_quit_message,
            schedule_shift_override=schedule_shift_override,
            show_join_msg=show_join_message,
            disallowed_reward_types=disallowed_reward_types,
            force_rewards_to_sim_info_inventory=force_rewards_to_sim_info_inventory,
            defer_first_assignment=defer_first_assignment,
            schedule_init_only=schedule_init_only,
            allow_outfit_generation=allow_outfit_generation
        )

    @classmethod
    def _add_career(
        cls,
        career_tracker: CareerTracker,
        new_career: Career,
        randomize_agency: bool = True,
        use_career_history: bool = True,
        force_out_of_retirement: bool = False,
        force_quit_previous_jobs: bool = False,
        show_confirmation_dialog = False,
        user_level_override: int = None,
        career_level_override: CareerLevel = None,
        give_skipped_rewards: bool = True,
        defer_rewards: bool = False,
        post_quit_msg: bool = True,
        schedule_shift_override = CareerShiftType.ALL_DAY,
        show_join_msg: bool = True,
        disallowed_reward_types: Tuple[RewardType] = (),
        force_rewards_to_sim_info_inventory: bool = False,
        defer_first_assignment: bool = False,
        schedule_init_only: bool = False,
        allow_outfit_generation: bool = True
    ) -> CommonExecutionResult:
        if show_confirmation_dialog:
            (level, _, track) = new_career.get_career_entry_data(career_history=career_tracker._career_history, user_level_override=user_level_override, career_level_override=career_level_override)
            career_level_tuning = CommonCareerTrackUtils.get_career_level_by_index(track, level)
            if career_tracker._retirement is not None:
                def _on_unretire_confirmation_dialog_response(dialog, _disallowed_reward_types: Tuple[RewardType]=disallowed_reward_types) -> None:
                    if not dialog.accepted:
                        return
                    cls._add_career(
                        career_tracker,
                        new_career,
                        randomize_agency=randomize_agency,
                        use_career_history=use_career_history,
                        force_out_of_retirement=True,
                        force_quit_previous_jobs=force_quit_previous_jobs,
                        show_confirmation_dialog=show_confirmation_dialog,
                        user_level_override=user_level_override,
                        career_level_override=career_level_override,
                        give_skipped_rewards=give_skipped_rewards,
                        defer_rewards=defer_rewards,
                        post_quit_msg=post_quit_msg,
                        schedule_shift_override=schedule_shift_override,
                        show_join_msg=show_join_msg,
                        disallowed_reward_types=_disallowed_reward_types,
                        force_rewards_to_sim_info_inventory=force_rewards_to_sim_info_inventory,
                        defer_first_assignment=defer_first_assignment,
                        schedule_init_only=schedule_init_only,
                        allow_outfit_generation=allow_outfit_generation
                    )

                if not force_out_of_retirement:
                    career_tracker._retirement.send_dialog(Career.UNRETIRE_DIALOG, career_level_tuning.get_title(career_tracker._sim_info), icon_override=DEFAULT, on_response=lambda dialog: _on_unretire_confirmation_dialog_response(dialog))
                    cls.get_log().format_with_message('Sim is retired.')
                    return CommonExecutionResult(False, reason=f'{career_tracker._sim_info} is retired.', tooltip_text=CommonStringId.S4CL_SIM_IS_RETIRED, tooltip_tokens=(career_tracker._sim_info,))

            if new_career.can_quit:
                def _on_quit_confirmation_dialog_response(dialog, _disallowed_reward_types: Tuple[RewardType]=disallowed_reward_types) -> None:
                    if not dialog.accepted:
                        return
                    cls._add_career(
                        career_tracker,
                        new_career,
                        randomize_agency=randomize_agency,
                        use_career_history=use_career_history,
                        force_out_of_retirement=force_out_of_retirement,
                        force_quit_previous_jobs=True,
                        show_confirmation_dialog=show_confirmation_dialog,
                        user_level_override=user_level_override,
                        career_level_override=career_level_override,
                        give_skipped_rewards=give_skipped_rewards,
                        defer_rewards=defer_rewards,
                        post_quit_msg=post_quit_msg,
                        schedule_shift_override=schedule_shift_override,
                        show_join_msg=show_join_msg,
                        disallowed_reward_types=_disallowed_reward_types,
                        force_rewards_to_sim_info_inventory=force_rewards_to_sim_info_inventory,
                        defer_first_assignment=defer_first_assignment,
                        schedule_init_only=schedule_init_only,
                        allow_outfit_generation=allow_outfit_generation
                    )

                quittable_careers = career_tracker.get_quittable_careers(schedule_shift_type=schedule_shift_override)
                if quittable_careers and not force_quit_previous_jobs:
                    career = next(iter(quittable_careers.values()))
                    switch_jobs_dialog = Career.SWITCH_JOBS_DIALOG
                    if len(quittable_careers) > 1:
                        switch_jobs_dialog = Career.SWITCH_MANY_JOBS_DIALOG
                    career.send_career_message(switch_jobs_dialog, career_level_tuning.get_title(career_tracker._sim_info), icon_override=DEFAULT, on_response=lambda dialog: _on_quit_confirmation_dialog_response(dialog, _disallowed_reward_types=(RewardType.MONEY,)))
                    cls.get_log().format_with_message('Sim has quittable careers. Too many jobs!')
                    return CommonExecutionResult(False, reason=f'{career_tracker._sim_info} has existing jobs, they need to be quit before a new one may be added.', tooltip_text=CommonStringId.S4CL_SIM_HAS_EXISTING_JOBS_NEED_TO_QUIT_THEM_BEFORE_ADDING_NEW_ONES, tooltip_tokens=(career_tracker._sim_info,))

        cls.get_log().format_with_message('Doing end retirement.')
        career_tracker.end_retirement()
        career_tracker.remove_custom_career_data(send_update=False)
        if new_career.guid64 in career_tracker._careers:
            cls.get_log().format_with_message('Attempting to add career that Sim is already in.', career=new_career, sim=career_tracker._sim_info)
            return CommonExecutionResult(False, reason=f'{career_tracker._sim_info} already has career {new_career}.', tooltip_text=CommonStringId.S4CL_SIM_ALREADY_HAS_CAREER, tooltip_tokens=(career_tracker._sim_info, str(new_career)))
        if new_career.can_quit:
            career_tracker.quit_quittable_careers(post_quit_msg=post_quit_msg, schedule_shift_type=schedule_shift_override)
        career_tracker._careers[new_career.guid64] = new_career
        result = cls._join_career(
            new_career,
            randomize_agency=randomize_agency,
            career_history=career_tracker._career_history if use_career_history else None,
            user_level_override=user_level_override,
            career_level_override=career_level_override,
            give_skipped_rewards=give_skipped_rewards,
            defer_rewards=defer_rewards,
            schedule_shift_override=schedule_shift_override,
            show_join_msg=show_join_msg,
            disallowed_reward_types=disallowed_reward_types,
            force_rewards_to_sim_info_inventory=force_rewards_to_sim_info_inventory,
            defer_first_assignment=defer_first_assignment,
            schedule_init_only=schedule_init_only,
            allow_outfit_generation=allow_outfit_generation
        )
        if not result:
            return result
        career_tracker.resend_career_data()
        career_tracker.update_affordance_caches()
        if career_tracker._on_promoted not in new_career.on_promoted:
            new_career.on_promoted.append(career_tracker._on_promoted)
        if career_tracker._on_demoted not in new_career.on_demoted:
            new_career.on_demoted.append(career_tracker._on_demoted)
        return CommonExecutionResult.TRUE

    @classmethod
    def remove_careers(
        cls,
        sim_info: SimInfo,
        show_post_quit_message: bool = False,
        update_ui_after_remove: bool = True,
        include_career_callback: Callable[[Career], bool] = None
    ) -> None:
        """remove_careers(\
            sim_info,\
            show_post_quit_message=False,\
            update_ui_after_remove=True,\
            include_career_callback=None\
        )

        Remove Careers of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param show_post_quit_message: If True, the post quit message will show for each removed Career. If False, no post quit message will show for each removed Career. Default is False.
        :type show_post_quit_message: bool, optional
        :param update_ui_after_remove: If True, the UI will be updated after the Career is removed. If False, the UI will not be updated. Default is True.
        :type update_ui_after_remove: bool, optional
        :param include_career_callback: If the result of this callback is True, the Career of the Sim will be removed. If set to None, All Careers of the Sim will be removed. Default is None.
        :type include_career_callback: Callable[[Career], bool], optional
        """
        career_tracker = cls.get_career_tracker(sim_info)
        if career_tracker is None:
            return
        to_remove_career_uids = list()
        for (career_uid, career) in career_tracker.careers.items():
            if include_career_callback is not None and not include_career_callback(career):
                continue
            to_remove_career_uids.append(career_uid)

        for career_uid in to_remove_career_uids:
            career_tracker.remove_career(career_uid, post_quit_msg=show_post_quit_message, update_ui=update_ui_after_remove)

    @classmethod
    def _join_career(
        cls,
        career: Career,
        randomize_agency: bool = True,
        career_history: CareerHistory = None,
        user_level_override: int = None,
        career_level_override: int = None,
        give_skipped_rewards: bool = True,
        defer_rewards: bool = False,
        schedule_shift_override: CareerShiftType = CareerShiftType.ALL_DAY,
        show_join_msg: bool = True,
        disallowed_reward_types: Tuple[RewardType] = (),
        force_rewards_to_sim_info_inventory: bool = False,
        defer_first_assignment: bool = False,
        schedule_init_only: bool = False,
        allow_outfit_generation: bool = True
    ) -> CommonExecutionResult:
        (new_level, new_user_level, current_track) = career.get_career_entry_data(career_history=career_history, user_level_override=user_level_override, career_level_override=career_level_override)
        if defer_rewards:
            career.defer_player_rewards()
        career._current_track = current_track
        career._join_time = services.time_service().sim_now
        career._level = new_level
        career._user_level = new_user_level
        career._current_shift_type = schedule_shift_override
        if career_history is not None:
            career._load_days_worked_commodities(career_history, current_track)
        career._reset_career_objectives(career._current_track, new_level)
        starting_level = career._sim_info.career_tracker.get_highest_level_reached(career.guid64)
        career._sim_info.career_tracker.update_history(career)
        career.career_start(schedule_init_only=schedule_init_only, allow_outfit_generation=allow_outfit_generation)
        career._setup_assignments_for_career_joined(defer_assignment=defer_first_assignment)
        resolver = SingleSimResolver(career._sim_info)
        for loot in career.current_level_tuning.loot_on_join:
            if randomize_agency:
                loot_guid = getattr(loot, 'guid64', None)
                if loot_guid is None:
                    continue
                # loot_Buff_ActorCareer_NewJob
                if loot_guid == 192996:
                    agents_available = tuple(career.current_level_tuning.agents_available)
                    if agents_available:
                        chosen_agent = random.choice(agents_available)
                        if CommonTraitUtils.add_trait(career.sim_info, CommonTraitUtils.get_trait_id(chosen_agent)):
                            continue
            loot.apply_to_resolver(resolver)
        if give_skipped_rewards:
            career._give_rewards_for_skipped_levels(starting_level=starting_level, disallowed_reward_types=disallowed_reward_types, force_rewards_to_sim_info_inventory=force_rewards_to_sim_info_inventory)
        from careers.career_base import TELEMETRY_HOOK_CAREER_START
        career._send_telemetry(TELEMETRY_HOOK_CAREER_START)
        join_career_notification = career.career_messages.join_career_notification
        if show_join_msg and career.display_career_info and join_career_notification is not None:
            (_, first_work_time, _) = career.get_next_work_time()
            career.send_career_message(join_career_notification, first_work_time)
        career.add_coworker_relationship_bit()
        career._add_career_knowledge()
        return CommonExecutionResult.TRUE

    @classmethod
    def determine_entry_level_into_career_for_sim(
        cls,
        sim_info: SimInfo,
        career: Career,
        use_career_history: bool = True
    ) -> Tuple[Union[int, None], Union[int, None], Union[TunableCareerTrack, None]]:
        """determine_entry_level_into_career_for_sim(sim_info, career, use_career_history=True)

        Determine the entry level into a Career for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param career: The career to retrieve an entry level of.
        :type career: Career
        :param use_career_history: If True, then the career history of the Sim will be used when adding the Career. If False, then the career history of the Sim will not be used when adding the Career. Default is True.
        :type use_career_history: bool, optional
        :return: The career level for the career track (or branch career track) used, the level of the user in that career track, and the career track itself.
        :rtype: Tuple[int, int, TunableCareerTrack]
        """
        if sim_info is None:
            return None, None, None
        if use_career_history:
            career_tracker = cls.get_career_tracker(sim_info)
            if career_tracker is None:
                return None, None, None
            career_history = career_tracker.career_history
        else:
            career_history = None
        return career.get_career_entry_level(career_history=career_history, resolver=SingleSimResolver(sim_info))


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.has_career',
    'Check if a Sim has a career.',
    command_arguments=(
        CommonConsoleCommandArgument('career', 'Name or Decimal Id', 'The name or id of a career to check.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of a Sim.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_has_career(output: CommonConsoleCommandOutput, career: TunableInstanceParam(Types.CAREER), sim_info: SimInfo=None):
    if sim_info is None:
        return
    output(f'Checking {sim_info} to see if they have career {career}')
    if career is None:
        output(f'Failed, Career does not exist.')
        return False
    if CommonSimCareerUtils.has_career(sim_info, career):
        output(f'SUCCESS: Sim has the career.')
    else:
        output(f'FAILED: Sim does not have the career.')
    return True


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.add_career',
    'Add a career to a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('career', 'Name or Decimal Id', 'The name or id of a career to add.'),
        CommonConsoleCommandArgument('user_level', 'Number', 'The Career Level to put the Sim into for the Career.', is_optional=True, default_value='Starting Level'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of a Sim.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_add_career(output: CommonConsoleCommandOutput, career: TunableInstanceParam(Types.CAREER), user_level: int=None, sim_info: SimInfo=None):
    if sim_info is None:
        return
    output(f'Attempting to add career {career}')
    if career is None:
        output(f'Failed, Career does not exist.')
        return False
    output('Adding career')
    result = CommonSimCareerUtils.add_career(sim_info, career, user_level=user_level, randomize_agency=True, use_career_history=False, show_confirmation_dialog=False)
    if result:
        output(f'SUCCESS: Career added.')
    else:
        output(f'FAILED: Failed to add career. {result.reason}')
    return True


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.randomize_career',
    'Give a random career to a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of a Sim.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_randomize_career(output: CommonConsoleCommandOutput, sim_info: SimInfo=None):
    if sim_info is None:
        return
    output(f'Attempting to randomize career for Sim {sim_info}')
    result = CommonSimCareerUtils.randomize_career(sim_info, remove_all_existing_careers=True, randomize_agency=True, use_career_history=False)
    if result:
        output(f'SUCCESS: Career randomized to {result.reason}')
    else:
        output(f'FAILED: Failed to randomize career. {result.reason}')
    return True
