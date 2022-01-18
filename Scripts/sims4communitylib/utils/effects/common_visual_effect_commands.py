"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import clock
from date_and_time import TimeSpan
from objects.game_object import GameObject
from server_commands.argument_helpers import OptionalTargetParam
from sims4.commands import Output
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_teardown import S4CLZoneTeardownEvent
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommandArgument, \
    CommonConsoleCommand
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.classes.effects.common_visual_effect import CommonVisualEffect


class _CommonVisualEffectCommandService(CommonService):
    def __init__(self) -> None:
        super().__init__()
        self._running_effects_list = list()

    # noinspection PyMissingOrEmptyDocstring
    def play_visual_effect(self, target: GameObject, effect_name: str, joint_bone_name: str= 'b__Head__', time_span: TimeSpan=None):
        effect = CommonVisualEffect(ModInfo.get_identity(), target, effect_name, joint_bone_name=joint_bone_name)

        def _on_end(_effect: CommonVisualEffect):
            if _effect in self._running_effects_list:
                self._running_effects_list.remove(_effect)

        effect.start(time_span=time_span, on_end=_on_end)
        self._running_effects_list.append(effect)

    # noinspection PyMissingOrEmptyDocstring
    def stop_all_visual_effects(self) -> None:
        for effect in tuple(self._running_effects_list):
            effect.stop()
            self._running_effects_list.remove(effect)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.play_visual_effect', 'Play a VFX on an Object or Sim. Run `s4clib.stop_all_visual_effects` to stop the visual effect.', command_arguments={
    CommonConsoleCommandArgument('effect_name', 'Text', 'The name of an effect to play.'),
    CommonConsoleCommandArgument('joint_bone_name', 'Text', 'The name of the bone or joint to attach the effect to on the target object.', is_optional=True, default_value='b__Head__'),
    CommonConsoleCommandArgument('sim_minutes_until_end', 'Number', 'The number of Sim Minutes to play the effect for before it auto stops.', is_optional=True, default_value='Effect default length'),
    CommonConsoleCommandArgument('opt_target', 'Instance Id of Object', 'The instance id of an Object or Sim to attach the VFX to.', is_optional=True, default_value='Active Sim'),
})
def _common_play_visual_effect(output: Output, effect_name: str, joint_bone_name: str= 'b__Head__', sim_minutes_until_end: int=None, opt_target: OptionalTargetParam=None):
    from server_commands.argument_helpers import get_optional_target
    target = get_optional_target(opt_target, output._context)
    if target is None:
        output(f'Target {opt_target} did not exist')
        return False
    output(f'Running VFX {effect_name} on Target {target}')

    time_span = None
    if sim_minutes_until_end is not None:
        time_span = clock.interval_in_sim_minutes(sim_minutes_until_end)
    _CommonVisualEffectCommandService().play_visual_effect(target, effect_name, joint_bone_name=joint_bone_name, time_span=time_span)
    output(f'Started effect {effect_name} on Target {target}')


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.stop_all_visual_effects', 'Stop all running effects that were started via `s4clib.play_visual_effect`.')
def _common_stop_all_debug_visual_effects(output: Output):
    output('Stopping all debug added VFX')
    _CommonVisualEffectCommandService().stop_all_visual_effects()


# noinspection PyUnusedLocal
@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _common_stop_all_debug_visual_effects_on_zone_teardown(event_data: S4CLZoneTeardownEvent):
    _CommonVisualEffectCommandService().stop_all_visual_effects()