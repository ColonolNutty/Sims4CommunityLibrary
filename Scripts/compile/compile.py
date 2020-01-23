"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from Utilities.compiler import compile_module

compile_module(root='..\\Release\\Sims4CommunityLib', mod_scripts_folder='.', include_folders=('sims4communitylib',), mod_name='sims4communitylib')
compile_module(root='..\\Release\\Sims4CommunityLibTests', mod_scripts_folder='.', include_folders=('tests',), mod_name='sims4communitylib_tests')
