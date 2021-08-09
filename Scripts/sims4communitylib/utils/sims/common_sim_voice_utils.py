"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from server_commands.argument_helpers import OptionalTargetParam
from sims.sim_info import SimInfo
from sims4.commands import Command, CommandType, CheatOutput
from sims4communitylib.enums.common_voice_actor_type import CommonVoiceActorType
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimVoiceUtils:
    """Utilities for manipulating the Voice of Sims.

    """

    @staticmethod
    def get_voice_pitch(sim_info: SimInfo) -> float:
        """get_voice_pitch(sim_info)
        
        Retrieve the Pitch of the Voice of a Sim.
        
        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A value that represents the pitch of the voice of a Sim. The value can range from -1.0 to 1.0
        :rtype: float
        """
        # noinspection PyPropertyAccess
        return sim_info.voice_pitch

    @staticmethod
    def set_voice_pitch(sim_info: SimInfo, voice_pitch: float) -> None:
        """set_voice_pitch(sim_info, voice_pitch)
        
        Set the Pitch of the Voice of a Sim.
        
        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param voice_pitch: The value to set the voice pitch to, from -1.0 to 1.0.
        :type voice_pitch: float
        """
        sim_info.voice_pitch = voice_pitch

    @staticmethod
    def get_voice_actor(sim_info: SimInfo) -> Union[int, CommonVoiceActorType]:
        """get_voice_actor(sim_info)
        
        Retrieve the Actor of the Voice of a Sim.
        
        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A value that represents the voice actor of a Sim.
        :rtype: int
        """
        # noinspection PyPropertyAccess
        voice_actor = sim_info.voice_actor
        if voice_actor not in CommonVoiceActorType.value_to_name:
            return voice_actor

        return CommonResourceUtils.get_enum_by_name(CommonVoiceActorType.value_to_name[voice_actor].upper(), CommonVoiceActorType, default_value=voice_actor)

    @staticmethod
    def set_voice_actor(sim_info: SimInfo, voice_actor: Union[int, CommonVoiceActorType]) -> None:
        """set_voice_actor(sim_info, voice_actor)

        Set the Voice Actor of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param voice_actor: The voice actor to set the Sim to have.
        :type voice_actor: Union[int, CommonVoiceActorType]
        """
        sim_info.voice_actor = int(voice_actor)


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'voice_actor_log')
log.enable()


@Command('s4clib.get_voice_pitch', command_type=CommandType.Live)
def _common_get_voice_pitch(opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    voice_pitch = CommonSimVoiceUtils.get_voice_pitch(sim_info)
    log.format_with_message('Got voice pitch', sim=sim_info, voice_pitch=voice_pitch)
    output('Got voice pitch {}'.format(voice_pitch))


@Command('s4clib.set_voice_pitch', command_type=CommandType.Live)
def _common_set_voice_pitch(voice_pitch_str: str=None, opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    if voice_pitch_str is None:
        output('Failed, no voice_pitch was specified! Please specify a voice pitch.')
        return
    # noinspection PyBroadException
    try:
        voice_pitch = float(voice_pitch_str)
    except:
        output('Failed, voice pitch {} was not a float.'.format(voice_pitch_str))
        return
    try:
        sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
        if sim_info is None:
            output('Failed, no Sim was specified or the specified Sim was not found!')
            return
        CommonSimVoiceUtils.set_voice_pitch(sim_info, voice_pitch)
        log.format_with_message('Set voice pitch', sim=sim_info, voice_pitch=voice_pitch)
        output('Set voice pitch')
    except Exception as ex:
        log.error('An error occurred while setting voice pitch.', exception=ex)
        output('An error occurred while setting voice pitch.')


@Command('s4clib.get_voice_actor', command_type=CommandType.Live)
def _common_get_voice_actor(opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    voice_actor = CommonSimVoiceUtils.get_voice_actor(sim_info)
    log.format_with_message('Got voice pitch', sim=sim_info, voice_actor=voice_actor)
    output('Got voice actor {}'.format(voice_actor))


@Command('s4clib.set_voice_actor', command_type=CommandType.Live)
def _common_set_voice_actor(voice_actor_str: str='MUTE', opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    if voice_actor_str is None:
        output('Please specify a voice actor. Valid Voice Actors: ({})'.format(', '.join(CommonVoiceActorType.get_all_names())))
        return
    voice_actor: CommonVoiceActorType = CommonResourceUtils.get_enum_by_name(voice_actor_str.upper(), CommonVoiceActorType, default_value=None)
    if voice_actor is None:
        output('{} is not a valid voice actor. Valid Voice Actors: ({})'.format(voice_actor_str, ', '.join(CommonVoiceActorType.get_all_names())))
        return
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    CommonSimVoiceUtils.set_voice_actor(sim_info, voice_actor)
    log.format_with_message('Set voice actor', sim=sim_info, voice_actor=voice_actor)
    output('Set voice actor to {}'.format(voice_actor.name))


@Command('s4clib.set_voice_actor_custom', command_type=CommandType.Live)
def _common_set_voice_actor_custom(voice_actor_id: int=None, opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    if voice_actor_id is None:
        output('Please specify a voice actor.')
        return
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    CommonSimVoiceUtils.set_voice_actor(sim_info, voice_actor_id)
    log.format_with_message('Set voice actor', sim=sim_info, voice_actor_id=voice_actor_id)
    output('Set custom voice actor to {}'.format(voice_actor_id))
