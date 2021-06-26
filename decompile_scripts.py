import os

from compile_utils import _remove_files_conflicting_with_decompile, _replace_renamed_files
from decompilation_method import S4PyDecompilationMethod
from settings import custom_scripts_for_decompile_source, game_folder, decompile_method_name, custom_scripts_for_decompile_destination, should_decompile_ea_scripts, should_decompile_custom_scripts


def _decompile_using_unpyc3(decompile_ea_scripts: bool=False, decompile_custom_scripts: bool=False):
    output_folder = 'EA'
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    _remove_files_conflicting_with_decompile(decompile_ea_scripts=decompile_ea_scripts)

    from Utilities.unpyc3_decompiler import Unpyc3PyDecompiler

    if decompile_custom_scripts:
        Unpyc3PyDecompiler.decompile_folder(custom_scripts_for_decompile_source)

    if decompile_ea_scripts:
        gameplay_folder_data = os.path.join(game_folder, 'Data', 'Simulation', 'Gameplay')
        if os.name != 'nt':
            gameplay_folder_game = os.path.join(game_folder, 'Python')
        else:
            gameplay_folder_game = os.path.join(game_folder, 'Game', 'Bin', 'Python')

        Unpyc3PyDecompiler.extract_folder(output_folder, gameplay_folder_data)
        Unpyc3PyDecompiler.extract_folder(output_folder, gameplay_folder_game)

    _replace_renamed_files(decompile_ea_scripts=should_decompile_ea_scripts)


def _decompile_using_py37dec() -> None:
    _remove_files_conflicting_with_decompile(decompile_ea_scripts=should_decompile_ea_scripts)

    from py37_decompiler import Py37PythonDecompiler
    Py37PythonDecompiler().decompile(
        custom_scripts_for_decompile_source,
        custom_scripts_for_decompile_destination
    )
    _replace_renamed_files(decompile_ea_scripts=should_decompile_ea_scripts)


if decompile_method_name == S4PyDecompilationMethod.UNPYC3:
    _decompile_using_unpyc3(decompile_ea_scripts=should_decompile_ea_scripts, decompile_custom_scripts=should_decompile_custom_scripts)
elif decompile_method_name == S4PyDecompilationMethod.PY37DEC:
    _decompile_using_py37dec()
