"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import json
from typing import Dict, Any

from sims.household import Household
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.persistence_services.common_persistence_service import CommonPersistenceService
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils


class CommonHiddenHouseholdPersistenceService(CommonPersistenceService):
    """CommonHiddenHouseholdPersistenceService()

    A service that persists data into a hidden household. (This data is per save file, it won't carry to other Saves)
    """

    # noinspection PyMissingOrEmptyDocstring
    def load(self, mod_identity: CommonModIdentity, identifier: str=None) -> Dict[str, Any]:
        data_name = self._format_data_name(mod_identity, identifier=identifier)
        all_households = tuple(CommonHouseholdUtils.get_all_households_generator())
        if not all_households:
            raise Exception(f'Households have not been loaded yet, but data with name {data_name} is attempting to be loaded! Please try to use the data after the households have been loaded instead. (Households are available when the S4CLZoneLateLoadEvent event is dispatched)')

        self.log.format_with_message('Loading data.', data_name=data_name)
        loaded_data: Dict[str, Any] = None
        loaded_household: Household = None

        def _load_data_from_household(household: Household) -> Dict[str, Any]:
            # noinspection PyPropertyAccess
            _household_name = household.name
            # noinspection PyPropertyAccess
            self.log.format_with_message('Attempting to read data stored within household.', household_name=_household_name, household_id=household.id)
            # noinspection PyPropertyAccess
            raw_data = household.description
            if not raw_data:
                self.log.format_with_message('No raw data found, returning default data.', data=household)
                return dict()
            self.log.debug('Data found, attempting to parse data.')
            return json.loads(raw_data)

        self.log.format_with_message('Attempting to locate data by exact name', data_name=data_name)
        located_household = CommonHouseholdUtils.locate_household_by_name(data_name)
        if located_household is not None:
            self.log.format_with_message('Located data with exact name.', data_name=data_name)
            loaded_data = _load_data_from_household(located_household)
            if loaded_data is not None:
                loaded_household = located_household

        self.log.format_with_message('Attempting to locate data containing name.', data_name=data_name)
        for persisted_household in CommonHouseholdUtils.locate_households_by_name_generator(data_name, allow_partial_match=True):
            if persisted_household is None or (loaded_household is not None and persisted_household is loaded_household):
                self.log.debug('Household does not match.')
                continue
            # noinspection PyPropertyAccess
            household_name = persisted_household.name
            if loaded_data is not None:
                # noinspection PyPropertyAccess
                self.log.format_with_message('Duplicate household found, attempting to remove duplicate.', household_name=household_name, household_id=persisted_household.id)
                if CommonHouseholdUtils.delete_household(persisted_household):
                    self.log.format_with_message('Successfully deleted duplicate household.', household_name=household_name)
                else:
                    self.log.format_with_message('Failed to delete duplicate household.', household_name=household_name)
                continue
            loaded_data = _load_data_from_household(persisted_household)
            if loaded_data is not None:
                loaded_household = persisted_household
        if loaded_data is None:
            return dict()
        self.log.format_with_message('Done loading data.', data_name=data_name, loaded_data=loaded_data)
        return loaded_data

    # noinspection PyMissingOrEmptyDocstring
    def save(self, mod_identity: CommonModIdentity, data: Dict[str, Any], identifier: str=None) -> bool:
        data_name = self._format_data_name(mod_identity, identifier=identifier)
        self.log.format_with_message('Saving data.', data_name=data_name)
        self.log.format_with_message('Attempting to locate data.', data_name=data_name)
        persisted_data_storage = CommonHouseholdUtils.locate_household_by_name(data_name)
        if persisted_data_storage is None:
            self.log.debug('No persisted data found, creating new persisted data.')
            persisted_data_storage = CommonHouseholdUtils.create_empty_household(as_hidden_household=True)
            if persisted_data_storage is None:
                self.log.debug('Failed to persisted data.')
                return False
            self.log.debug('Persisted data created successfully. Setting properties.')
            persisted_data_storage.name = data_name
            persisted_data_storage.creator_id = 0
            persisted_data_storage.creator_name = data_name
            persisted_data_storage.creator_uuid = b''
        else:
            self.log.format_with_message('Found persisted data. Attempting to save data.', data=persisted_data_storage)
        self.log.format_with_message('Attempting to save data.', data=persisted_data_storage)
        try:
            self.log.format(data_being_saved=data)
            json_save_data = json.dumps(data)
            persisted_data_storage.description = json_save_data
        except Exception as ex:
            self.log.format_error_with_message('Failed to save data.', data_name=data_name, exception=ex)
            raise ex
        self.log.format_with_message('Done saving data.', data_name=data_name)
        return True

    # noinspection PyMissingOrEmptyDocstring
    def remove(self, mod_identity: CommonModIdentity, identifier: str=None) -> bool:
        data_name = self._format_data_name(mod_identity, identifier=identifier)
        self.log.format_with_message('Removing data.', data_name=data_name)
        self.log.format_with_message('Attempting to remove data.', data_name=data_name)
        result = CommonHouseholdUtils.delete_households_with_name(data_name, allow_partial_match=True)
        if not result:
            self.log.format_with_message('Failed to delete data.', data_name=data_name)
            return result
        self.log.format_with_message('Data deleted successfully.', data_name=data_name)
        return result
