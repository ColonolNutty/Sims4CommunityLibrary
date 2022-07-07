"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, List

import clock
from date_and_time import TimeSpan
from objects.game_object import GameObject
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_teardown import S4CLZoneTeardownEvent
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommandArgument, \
    CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.classes.effects.common_visual_effect import CommonVisualEffect
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class _CommonVisualEffectCommandService(CommonService):
    def __init__(self) -> None:
        super().__init__()
        self._running_effects_list: Dict[int, List[CommonVisualEffect]] = dict()

    # noinspection PyMissingOrEmptyDocstring
    def play_visual_effect(
        self,
        target: GameObject,
        effect_name: str,
        joint_bone_name: str = 'b__Head__',
        time_span: TimeSpan = None,
        target_joint_bone_name: str = None,
        **kwargs
    ):
        effect = CommonVisualEffect(
            ModInfo.get_identity(),
            target,
            effect_name,
            joint_bone_name=joint_bone_name,
            target_joint_bone_name=target_joint_bone_name,
            **kwargs
        )

        if CommonTypeUtils.is_sim_or_sim_info(target):
            # noinspection PyTypeChecker
            object_id = CommonSimUtils.get_sim_id(target)
        else:
            object_id = CommonObjectUtils.get_object_id(target)

        def _on_end(_effect: CommonVisualEffect):
            if object_id in self._running_effects_list and _effect in self._running_effects_list[object_id]:
                self._running_effects_list[object_id].remove(_effect)

        effect.start(time_span=time_span, on_end=_on_end)
        if object_id not in self._running_effects_list:
            self._running_effects_list[object_id] = list()
        self._running_effects_list[object_id].append(effect)

    # noinspection PyMissingOrEmptyDocstring
    def stop_all_visual_effects(self, target: GameObject = None) -> None:
        if target is None:
            for (object_id, effects) in tuple(self._running_effects_list.items()):
                for effect in effects:
                    effect.stop()
                    self._running_effects_list[object_id].remove(effect)
        else:
            if CommonTypeUtils.is_sim_or_sim_info(target):
                # noinspection PyTypeChecker
                object_id = CommonSimUtils.get_sim_id(target)
            else:
                object_id = CommonObjectUtils.get_object_id(target)

            if object_id not in self._running_effects_list:
                return

            for effect in tuple(self._running_effects_list[object_id]):
                effect.stop()
                self._running_effects_list[object_id].remove(effect)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.play_visual_effect',
    'Play a VFX on a Sim. Run `s4clib.stop_all_visual_effects` to stop the visual effect.',
    command_arguments=(
        CommonConsoleCommandArgument('effect_name', 'Text', 'The name of an effect to play.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Id or Name of a Sim to attach the VFX to.', is_optional=True, default_value='Active Sim'),
        CommonConsoleCommandArgument('sim_minutes_until_end', 'Number', 'The number of Sim Minutes to play the effect for before it auto stops.', is_optional=True, default_value='Effect default length'),
        CommonConsoleCommandArgument('joint_bone_name', 'Text', 'The name of the bone or joint to attach the effect to on the source object.', is_optional=True, default_value='b__Head__'),
        CommonConsoleCommandArgument('target_joint_bone_name', 'Text', 'The name of the bone or joint to attach the effect to on the target object.', is_optional=True, default_value=None),
    )
)
def _common_play_visual_effect(
    output: CommonConsoleCommandOutput,
    effect_name: str,
    sim_info: SimInfo = None,
    sim_minutes_until_end: int = None,
    joint_bone_name: str = 'b__Head__',
    target_joint_bone_name: str = None
):
    sim = CommonSimUtils.get_sim_instance(sim_info)
    if sim is None:
        output(f'FAILED: Sim {sim_info} was not found nearby.')
        return False
    output(f'Running VFX {effect_name} on Sim {sim_info}')

    time_span = None
    if sim_minutes_until_end is not None:
        time_span = clock.interval_in_sim_minutes(sim_minutes_until_end)
    _CommonVisualEffectCommandService().play_visual_effect(sim, effect_name, joint_bone_name=joint_bone_name, target_joint_bone_name=target_joint_bone_name, time_span=time_span)
    output(f'Started effect {effect_name} on Sim {sim_info}')
    return True


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.play_visual_effect_object',
    'Play a VFX on an Object. Run `s4clib.stop_all_visual_effects` to stop the visual effect.',
    command_arguments=(
        CommonConsoleCommandArgument('effect_name', 'Text', 'The name of an effect to play.'),
        CommonConsoleCommandArgument('game_object', 'Instance Id of Object', 'The instance id of an Object to attach the VFX to.'),
        CommonConsoleCommandArgument('sim_minutes_until_end', 'Number', 'The number of Sim Minutes to play the effect for before it auto stops.', is_optional=True, default_value='Effect default length'),
        CommonConsoleCommandArgument('joint_bone_name', 'Text', 'The name of the bone or joint to attach the effect to on the source object.', is_optional=True, default_value='b__Head__'),
        CommonConsoleCommandArgument('target_joint_bone_name', 'Text', 'The name of the bone or joint to attach the effect to on the target object.', is_optional=True, default_value=None),
    )
)
def _common_play_visual_effect(
    output: CommonConsoleCommandOutput,
    effect_name: str,
    game_object: GameObject,
    sim_minutes_until_end: int = None,
    joint_bone_name: str = 'b__Root__',
    target_joint_bone_name: str = None
):
    output(f'Running VFX {effect_name} on Game Object {game_object}')

    time_span = None
    if sim_minutes_until_end is not None:
        time_span = clock.interval_in_sim_minutes(sim_minutes_until_end)
    _CommonVisualEffectCommandService().play_visual_effect(game_object, effect_name, joint_bone_name=joint_bone_name, target_joint_bone_name=target_joint_bone_name, time_span=time_span)
    output(f'Started effect {effect_name} on Game Object {game_object}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.stop_visual_effects_sim',
    'Stop all running effects that were started via `s4clib.play_visual_effect` on a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Id or Name of a Sim to attach the VFX to.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_stop_debug_visual_effects_on_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    output(f'Stopping all debug added VFX on {sim_info}.')
    _CommonVisualEffectCommandService().stop_all_visual_effects(target=sim_info)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.stop_visual_effects_object',
    'Stop all running effects that were started via `s4clib.play_visual_effect` on a Game Object.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Instance Id of Object', 'The instance id of an Object to attach the VFX to.'),
    )
)
def _common_stop_debug_visual_effects_on_object(output: CommonConsoleCommandOutput, game_object: GameObject):
    if not isinstance(game_object, GameObject):
        return False
    output(f'Stopping all debug added VFX on {game_object}.')
    _CommonVisualEffectCommandService().stop_all_visual_effects(target=game_object)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.stop_all_visual_effects',
    'Stop all running effects that were started via `s4clib.play_visual_effect`.'
)
def _common_stop_all_debug_visual_effects(output: CommonConsoleCommandOutput):
    output('Stopping all debug added VFX.')
    _CommonVisualEffectCommandService().stop_all_visual_effects()


# noinspection PyUnusedLocal
@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _common_stop_all_debug_visual_effects_on_zone_teardown(event_data: S4CLZoneTeardownEvent):
    _CommonVisualEffectCommandService().stop_all_visual_effects()
