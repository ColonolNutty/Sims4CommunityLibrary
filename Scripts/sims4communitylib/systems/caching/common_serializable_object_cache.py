"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Dict, Any, Type, Tuple, TypeVar, Generic, List

from sims4communitylib.classes.serialization.common_serializable import CommonSerializable

CommonSerializableObjectCacheType = TypeVar('CommonSerializableObjectCacheType', bound=CommonSerializable)


class CommonSerializableObjectCache(CommonSerializable, Generic[CommonSerializableObjectCacheType]):
    """A cache of serializable objects."""

    def __init__(self, cached_objects: Tuple[CommonSerializableObjectCacheType], checksums: Dict[str, int]):
        self._cached_objects = cached_objects
        self._checksums = checksums

    @property
    def cached_objects(self) -> Tuple[CommonSerializableObjectCacheType]:
        """Cached objects"""
        return self._cached_objects

    @property
    def cached_checksums(self) -> Dict[str, int]:
        """Cached checksums, these are used to check if the cache needs updating."""
        return self._checksums

    # noinspection PyMissingOrEmptyDocstring
    def serialize(self: 'CommonSerializableObjectCache') -> Union[str, Dict[str, Any]]:
        data = dict()
        data['cached_checksums'] = self._checksums
        data['cached_objects'] = [cached_object.serialize() for cached_object in self.cached_objects]
        return data

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def deserialize(
        cls: Type['CommonSerializableObjectCache'],
        data: Union[str, Dict[str, Any]]
    ) -> Union['CommonSerializableObjectCache', None]:
        checksums = data.get('cached_checksums', None)
        if checksums is None:
            return None
        cached_objects_data = data.get('cached_objects', tuple())

        if not cached_objects_data:
            return None

        cached_objects: List[CommonSerializableObjectCacheType] = list()
        for object_data in cached_objects_data:
            cached_object = cls._deserialize_object(object_data)
            if cached_object is None:
                continue
            cached_objects.append(cached_object)
        if not cached_objects:
            return None

        return cls(
            tuple(cached_objects),
            checksums
        )

    @classmethod
    def _deserialize_object(cls, data: Union[str, Dict[str, Any]]) -> Union[CommonSerializableObjectCacheType, None]:
        return CommonSerializableObjectCacheType.deserialize(data)
