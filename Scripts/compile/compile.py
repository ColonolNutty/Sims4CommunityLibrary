"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from Utilities.compiler import compile_module

release_dir = os.path.join('../', 'Release', 'Sims4CommunityLib')

compile_module(root=release_dir, mod_scripts_folder='.', include_folders=('_s4cl_ctypes_module', 'sims4communitylib',), mod_name='sims4communitylib')
compile_module(root=f'{release_dir}Tests', mod_scripts_folder='.', include_folders=('s4cl_tests',), mod_name='sims4communitylib_tests')
