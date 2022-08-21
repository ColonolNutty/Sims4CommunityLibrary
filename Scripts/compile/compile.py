"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from Utilities.unpyc3_compiler import Unpyc3PythonCompiler

release_dir = os.path.join('..', '..', 'Release', 'Sims4CommunityLib')

Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=release_dir,
    names_of_modules_include=('_s4cl_ctypes_module', 'sims4communitylib',),
    output_ts4script_name='sims4communitylib'
)

Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=f'{release_dir}Tests',
    names_of_modules_include=('s4cl_tests',),
    output_ts4script_name='sims4communitylib_tests'
)

Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=f'{release_dir}Development',
    names_of_modules_include=('sims4communitylib_development',),
    output_ts4script_name='sims4communitylib_development'
)
