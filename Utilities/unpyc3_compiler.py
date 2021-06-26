from compile_utils import _remove_files_conflicting_with_decompile, _replace_renamed_files

_remove_files_conflicting_with_decompile(decompile_ea_scripts=False)

import traceback
from typing import Iterator
from zipfile import PyZipFile

from settings import *


class Unpyc3PythonCompiler:
    """Handles compilation of python files into ts4script files using unpyc3."""
    @classmethod
    def compile_mod(
        cls,
        names_of_modules_include: Iterator[str],
        folder_path_to_output_ts4script_to: str,
        output_ts4script_name: str,
        names_of_modules_to_exclude: str=None,
        mod_creator_name: str=None,
        folder_path_to_gather_script_modules_from: str='..'
    ):
        """compile_mod(\
            names_of_modules_include,\
            folder_path_to_output_ts4script_to,\
            output_ts4script_name,\
            names_of_modules_to_exclude=None,\
            mod_creator_name=None,\
            folder_path_to_gather_script_packages_from=None\
        )

        Compile a mod using unpyc3.

        """
        from compile_utils import _remove_files_conflicting_with_decompile, _replace_renamed_files
        _remove_files_conflicting_with_decompile(decompile_ea_scripts=False)
        names_of_modules_include = tuple(names_of_modules_include)
        if not mod_creator_name:
            mod_creator_name = creator_name
        if not output_ts4script_name:
            output_ts4script_name = os.path.join('..', '..', os.path.basename(os.path.normpath(os.path.dirname(os.path.realpath('__file__')))))
            print('No mod name found, setting the path name to \'{}\'.'.format(output_ts4script_name))
        print(f'The current working directory {os.getcwd()}.')

        if mod_creator_name:
            print('Mod creator name found, appending mod creator name to file name.')
            output_ts4script_name = '{}_{}'.format(mod_creator_name, output_ts4script_name)
        output_script_zip_name = '{}.ts4script'.format(output_ts4script_name)
        if not folder_path_to_output_ts4script_to:
            ts4script = output_script_zip_name
        else:
            ts4script = os.path.join(folder_path_to_output_ts4script_to, output_script_zip_name)

        # noinspection PyBroadException
        try:
            if os.path.exists(ts4script):
                print('Script archive found, removing found archive.')
                os.remove(ts4script)
                print('Script archive removed.')

            output_zip = PyZipFile(ts4script, mode='w', allowZip64=True, optimize=2)
            previous_working_directory = os.getcwd()

            if folder_path_to_gather_script_modules_from is not None:
                print(f'Changing the working directory to \'{folder_path_to_gather_script_modules_from}\'')
                os.chdir(folder_path_to_gather_script_modules_from)
            else:
                folder_path_to_gather_script_modules_from = '..'
                os.chdir(folder_path_to_gather_script_modules_from)
            print(f'Changed the current working directory \'{os.getcwd()}\'.')
            # print('Found child directories {}'.format(pformat(tuple(child_directories))))
            for folder_path in cls._child_directories_gen(os.getcwd()):
                # print(f'Attempting to compile {folder_path}')
                if names_of_modules_to_exclude is not None and os.path.basename(folder_path) in names_of_modules_to_exclude:
                    # print(f'Folder is set to be ignored {folder_path}. Continuing to the next folder.')
                    continue
                if names_of_modules_include is not None and os.path.basename(folder_path) not in names_of_modules_include:
                    # print(f'Folder is not set to be included {folder_path}. Continuing to the next folder.')
                    continue
                # noinspection PyBroadException
                try:
                    print(f'Compiling folder \'{folder_path}\'')
                    output_zip.writepy(folder_path)
                    print(f'\'{folder_path}\' compiled successfully.')
                except Exception as ex:
                    print(f'Failed to write {folder_path}. {ex}')
                    traceback.print_exc()
                    continue

            print('Done compiling modules.')
            output_zip.close()
            print('Changing working directory to previous working directory.')
            os.chdir(previous_working_directory)
            print(f'Changed the current working directory to \'{os.getcwd()}\'')
        except Exception as ex:
            print(f'Failed to create {ts4script}. {ex}')
            return
        finally:
            _replace_renamed_files(decompile_ea_scripts=False)

        # This code is meant to copy the file to the Mods folder, but in most cases, we probably do not want this to happen!
        # ts4script_mods = os.path.join(os.path.join(mods_folder), script_zip_name)
        # shutil.copyfile(ts4script, ts4script_mods)

    @classmethod
    def _child_directories_gen(cls, directory_path) -> Iterator[str]:
        for folder_path in os.listdir(directory_path):
            if not os.path.isdir(os.path.join(directory_path, folder_path)):
                continue
            yield folder_path


_replace_renamed_files(decompile_ea_scripts=False)
