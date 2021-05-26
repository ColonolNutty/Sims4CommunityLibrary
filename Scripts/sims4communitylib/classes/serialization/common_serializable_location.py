"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any, Union

from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.classes.math.common_quaternion import CommonQuaternion
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.classes.math.common_transform import CommonTransform
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.classes.serialization.common_serializable import CommonSerializable


class CommonSerializableLocation(CommonSerializable):
    """A wrapper to serialize/deserialize a CommonLocation."""
    def __init__(self, location: CommonLocation):
        self.location = location
        if isinstance(location, CommonSerializableLocation):
            self.location = location.location

    # noinspection PyMissingOrEmptyDocstring
    def serialize(self) -> Union[str, Dict[str, Any]]:
        if self.location is None:
            return dict()
        transform = self.location.transform
        translation = transform.translation
        x = translation.x
        y = translation.y
        z = translation.z
        orientation = transform.orientation
        or_x = orientation.x
        or_y = orientation.y
        or_z = orientation.z
        or_w = orientation.w
        routing_surface = self.location.routing_surface
        primary_id = routing_surface.primary_id
        secondary_id = routing_surface.secondary_id
        joint_name_or_hash = self.location.joint_name_or_hash
        slot_hash = self.location.slot_hash
        parent_ref = self.location.parent_ref

        return {
            'transform': {
                'translation': {
                    'x': x,
                    'y': y,
                    'z': z
                },
                'orientation': {
                    'x': or_x,
                    'y': or_y,
                    'z': or_z,
                    'w': or_w
                }
            },
            'routing_surface': {
                'primary_id': primary_id,
                'secondary_id': secondary_id
            },
            'joint_name_or_hash': joint_name_or_hash,
            'slot_hash': slot_hash,
            'parent_ref': parent_ref
        }

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def deserialize(cls, data: Union[str, Dict[str, Any]]) -> Union['CommonSerializableLocation', None]:
        if not data:
            return None
        if isinstance(data, CommonSerializableLocation):
            return data
        data: Dict[str, Any] = data
        transform_data = data['transform']
        translation_data = transform_data['translation']
        x = translation_data['x']
        y = translation_data['y']
        z = translation_data['z']
        orientation_data = transform_data['orientation']
        or_x = orientation_data['x']
        or_y = orientation_data['y']
        or_z = orientation_data['z']
        or_w = orientation_data['w']
        routing_surface = data['routing_surface']
        primary_id = routing_surface['primary_id']
        secondary_id = routing_surface['secondary_id']
        joint_name_or_hash = data['joint_name_or_hash']
        slot_hash = data['slot_hash']
        parent_ref = data['parent_ref']

        translation = CommonVector3(x, y, z)
        orientation = CommonQuaternion(or_x, or_y, or_z, or_w)
        transform = CommonTransform(translation, orientation)
        routing_surface = CommonSurfaceIdentifier(primary_id, secondary_id=secondary_id)
        return cls(CommonLocation(transform, routing_surface, parent_ref=parent_ref, joint_name_or_hash=joint_name_or_hash, slot_hash=slot_hash))
