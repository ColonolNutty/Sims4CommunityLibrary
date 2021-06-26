import os
from decompilation_method import S4PyDecompilationMethod

# This name will be appended to the front of compiled script files.
# Example:
# If I set the value to "ColonolNutty"
# compiling my scripts would output a file with the name "ColonolNutty_<script_name>.ts4script"
creator_name = ''

# Set to either S4PyDecompilationMethod.UNPYC3 or S4PyDecompilationMethod.PY37DEC
# S4PyDecompilationMethod.PY37DEC is the default, however if it fails to decompile some files, feel free to change this to S4PyDecompilationMethod.UNPYC3 and try to decompile using that decompiler instead
decompile_method_name = S4PyDecompilationMethod.PY37DEC

# If you want to decompile the EA Python Scripts:
# 1. Change should_decompile_ea_scripts to True
# 2. Create a folder in your project with the name EA. i.e. <Project>/EA
# 2. Run the decompile_scripts.py script
# 3. It will decompile the EA scripts and put them inside of the folder: <Project>/EA/...
# 4. Inside of the <Project>/EA folder, you should see four folders (base, core, generated, simulation)
# 5. Highlight all four of those folders and right click them. Then do Mark Directory as... Sources Root
# 6. Delete the <Project>/EA/core/enum.py file because it causes issues when attempting to compile the scripts of your own mod.
should_decompile_ea_scripts: bool = False

# If you want to decompile scripts from another authors mod
# 1. Create a folder in your project with the name decompiled. i.e. <Project>/custom_scripts_for_decompile
# 1. Put the script files (.pyc) of the mod you wish to decompile, inside of the 'decompiled' folder. (Every ts4script file is a zip file and can be opened like one!)
# 2. Change should_decompile_custom_scripts to True
# 3. Run the decompile_scripts.py script
# 4. It will decompile the custom scripts and put them inside of the folder: <Project>/custom_scripts_for_decompile/...
should_decompile_custom_scripts: bool = True
if should_decompile_ea_scripts:
    decompile_method_name = S4PyDecompilationMethod.UNPYC3
    should_decompile_custom_scripts = False

custom_scripts_for_decompile_source: str = './custom_scripts_for_decompile'
custom_scripts_for_decompile_destination: str = './custom_scripts_for_decompile'

# If this path is not correct, change it to your Mods folder location instead.
if os.name != 'nt':
    # Mac
    mods_folder = os.path.join(os.environ['HOME'], 'Documents', 'Electronic Arts', 'The Sims 4', 'Mods')
    print(f'Mods folder path: {mods_folder}')
else:
    # Windows
    mods_folder = os.path.join(os.environ['USERPROFILE'], 'Documents', 'Electronic Arts', 'The Sims 4', 'Mods')
    print(f'Mods folder path: {mods_folder}')

# Location of the game's zipped binary scripts (base.zip, core.zip and simulation.zip)
# If this path is not found properly when trying to decompile, change it to the location where you have installed The Sims 4 at, this would be the folder that contains the GameVersion.txt file
if os.name != 'nt':
    # Mac
    game_folder = os.path.join(os.environ['HOME'], 'Applications', 'The Sims 4.app', 'Contents', 'Data', 'Simulation', 'Gameplay')
    print(f'Game folder path: {game_folder}')
else:
    # noinspection PyBroadException
    try:
        # Windows
        import winreg as winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Maxis\\The Sims 4')
        (game_folder, _) = winreg.QueryValueEx(key, 'Install Dir')
        print(f'Game folder path: {game_folder}')
    except:
        raise Exception('The Sims 4 game folder was not found! Please specify one manually in settings.py.')
