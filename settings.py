import os

creator_name = ''

mods_folder = os.path.expanduser(os.path.join('~', 'Documents', 'Electronic Arts', 'The Sims 4', 'Mods'))
game_folder = os.path.join('E:', os.sep, 'Program Files (x86)', 'Origin Games', 'The Sims 4')

# Set to either 'unpyc3' or 'py37dec'
compiler_name = 'py37dec'
include_ea_decompile = False
include_decompile_dir = True
if include_ea_decompile:
    compiler_name = 'unpyc3'
    include_decompile_dir = False

decompile_src = './decompiled'
decompile_destination = './decompiled'
