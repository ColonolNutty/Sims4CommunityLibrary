import os


def _remove_files_conflicting_with_decompile(decompile_ea_scripts: bool=False):
    ea_folder = os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'EA'))
    if not os.path.exists(ea_folder):
        os.mkdir(ea_folder)

    if decompile_ea_scripts:
        # print('Removing EA decompiled files before decompiling it again.')
        to_remove_before_compile = (
            'base',
            'base.zip',
            'core',
            'core.zip',
            'generated',
            'generated.zip',
            'simulation',
            'simulation.zip',
        )

        def _remove_directory_recursive(directory_path: str):
            for _file_in_dir in os.listdir(directory_path):
                _to_remove_path = os.path.join(directory_path, _file_in_dir)
                if os.path.isdir(_to_remove_path):
                    # noinspection PyBroadException
                    try:
                        os.rmdir(_to_remove_path)
                    except:
                        _remove_directory_recursive(_to_remove_path)
                        os.rmdir(_to_remove_path)
                else:
                    os.remove(_to_remove_path)

        for to_remove in to_remove_before_compile:
            to_remove_path = os.path.join(ea_folder, to_remove)
            if not os.path.exists(to_remove_path):
                # print(f'Did not exist \'{to_remove_path}\'')
                continue
            if os.path.isdir(to_remove_path):
                # noinspection PyBroadException
                try:
                    os.rmdir(to_remove_path)
                except:
                    _remove_directory_recursive(to_remove_path)
                    os.rmdir(to_remove_path)
            else:
                os.remove(to_remove_path)
    else:
        print('Renaming enum.py to enum.py_renamed')
        to_fix_before_decompile = (
            os.path.join('core', 'enum.py'),
            os.path.join('core', 'enum.pyc'),
        )

        for to_fix in to_fix_before_decompile:
            to_fix_path = os.path.join(ea_folder, to_fix)
            if not os.path.exists(to_fix_path):
                # print(f'Did not exist \'{to_fix_path}\'')
                continue
            if os.path.isdir(to_fix_path):
                os.rename(to_fix_path, to_fix_path + '_renamed')
            else:
                os.rename(to_fix_path, to_fix_path + '_renamed')


def _replace_renamed_files(decompile_ea_scripts: bool=False):
    if decompile_ea_scripts:
        return

    # print('Renaming enum.py_renamed to enum.py')

    ea_folder = os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'EA'))
    to_fix_after_decompile = (
        os.path.join('core', 'enum.py_renamed'),
        os.path.join('core', 'enum.pyc_renamed'),
    )

    for to_fix in to_fix_after_decompile:
        to_remove_path = os.path.join('.', ea_folder, to_fix)
        if not os.path.exists(to_remove_path):
            # print(f'Did not exist \'{to_remove_path}\'')
            continue
        if os.path.isdir(to_remove_path):
            os.rename(to_remove_path, to_remove_path.rstrip('_renamed'))
        else:
            os.rename(to_remove_path, to_remove_path.rstrip('_renamed'))