"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Union

import alarms
from date_and_time import TimeSpan
from sims.sim import Sim
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from vfx import PlayEffect
from objects.game_object import GameObject


class CommonVisualEffect(HasLog):
    """CommonVisualEffect(\
        mod_identity,\
        target,\
        effect_name,\
        joint_bone_name='b__Root__',\
        target_actor_id=0,\
        target_joint_bone_name=None,\
        **kwargs\
    )

    A visual effect that will play while attached to an object or Sim.

    :param mod_identity: The identity of the mod that owns this visual effect.
    :type mod_identity: CommonModIdentity
    :param source: An instance of an object or Sim. They will be the source of the effect.
    :type source: Union[GameObject, Sim]
    :param effect_name: The name of the effect to play.
    :type effect_name: str
    :param joint_bone_name: The name of the joint to play the effect attached to. Default is the root bone 'b__Root__'.
    :type joint_bone_name: str, optional
    :param target_actor_id: The id of the target actor. Default will be the id of the target.
    :type target_actor_id: int, optional
    :param target_joint_bone_name: The name of the joint to play the effect attached to on the target. Default is the value of joint_bone_name.
    :type target_joint_bone_name: str, optional
    """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return self._mod_identity

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_game_object_effect'

    def __init__(
        self,
        mod_identity: CommonModIdentity,
        source: Union[GameObject, Sim],
        effect_name: str,
        joint_bone_name: str = 'b__Root__',
        target_actor_id: int = 0,
        target_joint_bone_name: str = None,
        **kwargs
    ):
        from sims4.hash_util import hash32
        super().__init__()
        self._source = source
        self._mod_identity = mod_identity
        self._effect_name = effect_name
        self._joint_bone_name = joint_bone_name
        self._target_actor_id = target_actor_id
        self._target_joint_bone_name = target_joint_bone_name
        if joint_bone_name is None:
            joint_bone_hash = 0
        else:
            joint_bone_hash = hash32(joint_bone_name)
        if target_joint_bone_name is None:
            target_joint_bone_hash = 0
        else:
            target_joint_bone_hash = hash32(target_joint_bone_name)
        self._effect_instance = PlayEffect(
            source,
            effect_name=effect_name,
            joint_name=joint_bone_hash,
            target_actor_id=target_actor_id,
            target_joint_name_hash=target_joint_bone_hash,
            **kwargs
        )
        self._alarm_handle = None

    def start(self, time_span: TimeSpan = None, on_end: Callable[['CommonVisualEffect'], None] = None) -> bool:
        """start(time_span=None, on_end=None)

        Start the effect.

        :param time_span: A span of time indicating how long to run the effect for. Default is however long the vfx itself runs.
        :type time_span: TimeSpan, optional
        :param on_end: A callback invoked when the effect ends. This is only used when sim_minutes_until_end is specified. Default is None.
        :type on_end: Callable[['CommonVisualEffect'], None], optional
        :return: True, if the effect was started successfully. False, if not.
        :rtype: bool
        """
        try:
            self.log.format_with_message('Running effect.', source=self._source, effect_name=self._effect_name, time_span=time_span)
            self._effect_instance.start()
            if time_span is not None:
                self._create_stop_alarm(time_span, on_end=on_end)
            return True
        except Exception as ex:
            self.log.format_error_with_message(
                'Error occurred while trying to start visual effect.',
                effect_instance=self._effect_instance,
                source=self._source,
                effect_name=self._effect_name,
                joint_bone_name=self._joint_bone_name,
                target_actor_id=self._target_actor_id,
                target_joint_bone_name=self._target_joint_bone_name,
                exception=ex
            )
            return False

    def start_run_once(self, time_span: TimeSpan = None, on_end: Callable[['CommonVisualEffect'], None] = None) -> bool:
        """start_run_once(time_span=None, on_end=None)

        Start the effect and have it run only once.

        :param time_span: A span of time indicating how long to run the effect for. Default is however long the vfx itself runs.
        :type time_span: TimeSpan, optional
        :param on_end: A callback invoked when the effect ends. This is only used when sim_minutes_until_end is specified. Default is None.
        :type on_end: Callable[['CommonVisualEffect'], None], optional
        :return: True, if the effect was started successfully. False, if not.
        :rtype: bool
        """
        try:
            self.log.format_with_message('Running effect once.', source=self._source, effect_name=self._effect_name, time_span=time_span)
            self._effect_instance.start_one_shot()
            if time_span is not None:
                self._create_stop_alarm(time_span, on_end=on_end)
            return True
        except Exception as ex:
            self.log.format_error_with_message(
                'Error occurred while trying to start visual effect via one shot.',
                effect_instance=self._effect_instance,
                source=self._source,
                effect_name=self._effect_name,
                joint_bone_name=self._joint_bone_name,
                target_actor_id=self._target_actor_id,
                target_joint_bone_name=self._target_joint_bone_name,
                exception=ex
            )
            return False

    def _create_stop_alarm(self, time_span: TimeSpan, on_end: Callable[['CommonVisualEffect'], None] = None) -> None:
        def _on_end(_) -> None:
            if on_end is not None:
                on_end(self)
            self.stop()

        self._alarm_handle = alarms.add_alarm(self, time_span, _on_end, repeating=False, use_sleep_time=False)

    def _destroy_stop_alarm(self) -> None:
        if self._alarm_handle is not None:
            alarms.cancel_alarm(self._alarm_handle)
            self._alarm_handle = None

    def stop(self) -> bool:
        """stop()

        Stop the effect.

        :return: True, if the effect was stopped successfully. False, if not.
        :rtype: bool
        """
        try:
            self.log.format_with_message('Stopping effect.', source=self._source, effect_name=self._effect_name)
            self._destroy_stop_alarm()
            self._effect_instance.stop()
            return True
        except Exception as ex:
            self.log.format_error_with_message(
                'Error occurred while trying to stop visual effect.',
                effect_instance=self._effect_instance,
                source=self._source,
                effect_name=self._effect_name,
                joint_bone_name=self._joint_bone_name,
                target_actor_id=self._target_actor_id,
                target_joint_bone_name=self._target_joint_bone_name,
                exception=ex
            )
            return False

    def stop_immediate(self) -> bool:
        """stop_immediate()

        Kill the effect.

        :return: True, if the effect was stopped successfully. False, if not.
        :rtype: bool
        """
        try:
            self.log.format_with_message('Stopping effect immediate.', source=self._source, effect_name=self._effect_name)
            self._destroy_stop_alarm()
            self._effect_instance.stop(immediate=True)
            return True
        except Exception as ex:
            self.log.format_error_with_message(
                'Error occurred while trying to stop visual effect immediately.',
                effect_instance=self._effect_instance,
                source=self._source,
                effect_name=self._effect_name,
                joint_bone_name=self._joint_bone_name,
                target_actor_id=self._target_actor_id,
                target_joint_bone_name=self._target_joint_bone_name,
                exception=ex
            )
            return False
