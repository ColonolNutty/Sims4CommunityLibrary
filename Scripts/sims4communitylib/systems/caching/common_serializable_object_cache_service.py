"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Union, Generic, TypeVar, Tuple, Dict, Any

from sims4communitylib.systems.caching.common_serializable_object_cache import CommonSerializableObjectCache
from sims4communitylib.classes.serialization.common_serializable import CommonSerializable
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_io_utils import CommonIOUtils
from sims4communitylib.utils.common_json_io_utils import CommonJSONIOUtils
from sims4communitylib.utils.common_log_utils import CommonLogUtils


CommonSerializableObjectCacheType = TypeVar('CommonSerializableObjectCacheType', bound=CommonSerializableObjectCache[CommonSerializable])


class CommonSerializableObjectCacheService(CommonService, HasLog, Generic[CommonSerializableObjectCacheType]):
    """A service that manages a cache of serializable objects."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_serializable_object_cache_service'

    @property
    def _cache_file_name(self) -> str:
        raise NotImplementedError()

    def __init__(self) -> None:
        super().__init__()
        self._cache = None

    def cache_needs_update(self, new_checksum_data: Any) -> bool:
        """Determine if the cache needs to be updated or not."""
        cache = self.load_from_cache()
        if cache is None or not cache.cached_checksums:
            return False
        (snippet_name, snippet_id, new_checksum) = new_checksum_data
        checksums = cache.cached_checksums
        key = f'{snippet_name}-{snippet_id}'
        if checksums.get(key, -1) != new_checksum:
            return True
        return False

    def save_to_cache(self, cache: CommonSerializableObjectCacheType) -> None:
        """Save a cache of data."""
        file_path = self._get_cache_file_path()
        folder_path = self._get_cache_folder_path()
        if os.path.exists(file_path):
            CommonIOUtils.delete_file(file_path)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)

        CommonJSONIOUtils.write_to_file(file_path, cache.serialize())
        self._cache = cache

    def load_from_cache(self) -> Union[CommonSerializableObjectCacheType, None]:
        """Load the cached data."""
        if self._cache is not None:
            return self._cache
        file_path = self._get_cache_file_path()
        if os.path.exists(file_path):
            self._cache = self._deserialize_cache(CommonJSONIOUtils.load_from_file(file_path))
        else:
            self._cache = None
        return self._cache

    def clear_cache(self) -> None:
        """Clear the cached data"""
        file_path = self._get_cache_file_path()
        if os.path.exists(file_path):
            CommonIOUtils.delete_file(file_path)
        self._cache = None

    def _get_cache_folder_path(self) -> str:
        return os.path.join(CommonLogUtils.get_mod_data_location_path(), self.mod_identity.base_namespace.lower(), 'caches')

    def _get_cache_file_path(self) -> str:
        return os.path.join(self._get_cache_folder_path(), f'{self._cache_file_name}_cache.json')

    def _deserialize_cache(self, data: Union[str, Dict[str, Any]]) -> CommonSerializableObjectCacheType:
        return CommonSerializableObjectCacheType[CommonSerializable].deserialize(data)

    def create_cache(self, objects: Tuple[CommonSerializable], checksums: Tuple[Any]) -> CommonSerializableObjectCacheType:
        """
        Create a new cache.
        """
        checksum_data = dict()
        for (snippet_name, snippet_id, checksum_value) in checksums:
            checksum_data[f'{snippet_name}-{snippet_id}'] = checksum_value
        return CommonSerializableObjectCache[CommonSerializable](objects, checksum_data)
