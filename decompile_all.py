import os
from settings import decompile_src, game_folder, compiler_name, decompile_destination, include_ea_decompile, include_decompile_dir


def unpyc3(include_ea_decompileile=False, include_decompile_directory=False):
    from Utilities.compiler import extract_folder, decompile_dir

    ea_folder = 'EA'
    if not os.path.exists(ea_folder):
        os.mkdir(ea_folder)

    if include_decompile_directory:
        decompile_dir(decompile_src)
    if include_ea_decompileile:
        gameplay_folder_data = os.path.join(game_folder, 'Data', 'Simulation', 'Gameplay')
        gameplay_folder_game = os.path.join(game_folder, 'Game', 'Bin', 'Python')

        extract_folder(ea_folder, gameplay_folder_data)
        extract_folder(ea_folder, gameplay_folder_game)


def py37dec():
    from decompiler import main

    main(decompile_src, decompile_destination)


if compiler_name == 'unpyc3':
    unpyc3(include_ea_decompileile=include_ea_decompile, include_decompile_directory=include_decompile_dir)
elif compiler_name == 'py37dec':
    py37dec()
