"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Type, Tuple, List, Union

from sims4.resources import Types
from sims4.tuning.dynamic_enum import DynamicEnumLocked
from sims4communitylib.enums.enumtypes.common_int import Int
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class _S4CLEnumValueUpdateUtils(HasLog):
    """Utilities used when I ColonolNutty go to update various different Enums by adding new values to them. This should not be used under normal circumstances when making mods."""

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_enum_value_update_utils'

    def __init__(self) -> None:
        super().__init__()
        self.log.enable()

    def _read_values_from_enum(self, vanilla_enum_type: Union[Int, DynamicEnumLocked], name_to_cleaned_name_mappings: Dict[str, str], enum_type: Type, skip_not_found: bool=False) -> Tuple[str]:
        """_read_values_from_enum(vanilla_enum_type, name_to_cleaned_name_mappings, enum_type, skip_not_found=False)

        Read the values and return the ones not found.

        :param vanilla_enum_type: The enum to sift through.
        :type vanilla_enum_type: Union[Int, DynamicEnumLocked]
        :param name_to_cleaned_name_mappings: A mapping of names to cleaned names, these cleaned names will be used for the Enum names in the output, instead of the default names.
        :type name_to_cleaned_name_mappings: Dict[str, str]
        :param enum_type: The type of the enum being created. This is used when putting type hints on the output values.
        :type enum_type: Type
        :param skip_not_found: If True, any values not found in the conversion mapping will not be output. If False, any values not found in the conversion mapping will be output.
        :return: A collection of value names that were not found within the provided value name conversions.
        :rtype: Tuple[str]
        """
        enum_name = enum_type.__name__
        self.log.format_with_message(f'Logging {enum_name} values.')
        self.log.format_with_message('---------------------------------------------------------------------------------')
        conversion_table: Dict[str, str] = dict()
        values: List[Tuple[str, int]] = list()
        not_found_values: List[str] = list()
        for (value_name, value_value) in vanilla_enum_type.name_to_value.items():
            original_name = value_name.strip().upper()
            val_name = original_name
            if val_name in name_to_cleaned_name_mappings:
                val_name = name_to_cleaned_name_mappings[val_name]
            else:
                existing_value = CommonResourceUtils.get_enum_by_int_value(int(value_value), enum_type, default_value=None)
                if existing_value is not None:
                    val_name = existing_value.name
                else:
                    not_found_values.append(value_name)
                    if skip_not_found:
                        continue
            conversion_table[original_name] = val_name
            values.append((val_name, int(value_value)))
        sorted_values = sorted(values, key=lambda x: x[0])
        for (value_name, value_value) in sorted_values:
            self.log.debug(f'{value_name}: \'{enum_name}\' = {int(value_value)}')
        self.log.format_with_message('---------------------------------------------------------------------------------')
        self.log.debug('{')
        sorted_conversion_table = sorted(tuple(conversion_table.items()), key=lambda x: x[0])
        for (vanilla_value_name, cleaned_value_name) in sorted_conversion_table:
            self.log.debug(f'    \'{vanilla_value_name}\': \'{cleaned_value_name}\',')
        self.log.debug('}')
        self.log.format_with_message('---------------------------------------------------------------------------------')
        self.log.format_with_message(f'Finished Logging {enum_name}. These {enum_name} were not found in the conversion mapping.', not_found_values=not_found_values)
        return tuple(not_found_values)

    def _read_values_from_instances(self, instance_type: Types, name_to_cleaned_name_mappings: Dict[str, str], enum_type: Type, skip_not_found: bool=False) -> Tuple[str]:
        """_read_values_from_instances(instance_type, name_to_cleaned_name_mappings, enum_type, skip_not_found=False)

        Read the values and return the ones not found.

        :param instance_type: The type of instances being read from.
        :type instance_type: Types
        :param name_to_cleaned_name_mappings: A mapping of names to cleaned names, these cleaned names will be used for the Enum names in the output, instead of the default names.
        :type name_to_cleaned_name_mappings: Dict[str, str]
        :param enum_type: The type of the enum being created. This is used when putting type hints on the output values.
        :type enum_type: Type
        :param skip_not_found: If True, any values not found in the conversion mapping will not be output. If False, any values not found in the conversion mapping will be output. Default is False.
        :type skip_not_found: bool, optional
        :return: A collection of value names that were not found within the provided value name conversions.
        :rtype: Tuple[str]
        """
        enum_name = enum_type.__name__
        self.log.format_with_message(f'Printing {enum_name} values.')
        self.log.format_with_message('---------------------------------------------------------------------------------')
        conversion_table: Dict[str, str] = dict()
        values: List[Tuple[str, int]] = list()
        not_found_values: List[str] = list()
        for (value_guid, value_instance) in CommonResourceUtils.load_all_instances_as_guid_to_instance(instance_type).items():
            original_name = value_instance.__name__.strip().upper()
            val_name = original_name
            if val_name in name_to_cleaned_name_mappings:
                val_name = name_to_cleaned_name_mappings[val_name]
            else:
                existing_value = CommonResourceUtils.get_enum_by_int_value(int(value_guid), enum_type, default_value=None)
                if existing_value is not None:
                    val_name = existing_value.name
                else:
                    not_found_values.append(val_name)
                    if skip_not_found:
                        continue
            conversion_table[original_name] = val_name
            values.append((val_name, int(value_guid)))
        sorted_values = sorted(values, key=lambda x: x[0])
        for (value_name, value_value) in sorted_values:
            self.log.debug(f'{value_name}: \'{enum_name}\' = {int(value_value)}')
        self.log.format_with_message('---------------------------------------------------------------------------------')
        self.log.debug('{')
        sorted_conversion_table = sorted(tuple(conversion_table.items()), key=lambda x: x[0])
        for (vanilla_value_name, cleaned_value_name) in sorted_conversion_table:
            self.log.debug(f'    \'{vanilla_value_name}\': \'{cleaned_value_name}\',')
        self.log.debug('}')
        self.log.format_with_message('---------------------------------------------------------------------------------')
        self.log.format_with_message(f'Finished logging {enum_name}. These {enum_name} were not found in the conversion mapping.', not_found_values=not_found_values)
        return tuple(not_found_values)
