import shutil
import io
import fnmatch
from zipfile import PyZipFile
from Utilities.unpyc3 import decompile
from settings import *


def decompile_dir(rootPath):
    pattern = '*.pyc'
    for root, dirs, files in os.walk(rootPath):
        for filename in fnmatch.filter(files, pattern):
            p = str(os.path.join(root, filename))
            try:
                print('Decompiling \'{}\''.format(p))
                py = decompile(p)
                with io.open(p.replace('.pyc', '.py'), 'w') as output_py:
                    for statement in py.statements:
                        try:
                            output_py.write(str(statement) + '\r')
                        except Exception as ex:
                            print(statement.__class__)
                            raise ex
            except Exception as ex:
                print("FAILED to decompile %s" % p)
                print(ex)


def decompile_file(file_path, throw_on_error=True) -> bool:
    py = decompile(file_path)
    with io.open(file_path.replace('.pyc', '.py'), 'w') as output_py:
        success = True
        for statement in py.statements:
            try:
                output_py.write(str(statement) + '\r')
            except Exception as ex:
                print('Failed to parse statement.' + str(statement))
                print(statement.__class__)
                if throw_on_error:
                    raise ex
                success = False
    return success


script_package_types = ['*.zip', '*.ts4script']


def extract_subfolder(root, filename, ea_folder, decompile_files=True):
    src = os.path.join(root, filename)
    dst = os.path.join(ea_folder, filename)
    if src != dst:
        shutil.copyfile(src, dst)
    zip = PyZipFile(dst)
    out_folder = os.path.join(ea_folder, os.path.splitext(filename)[0])
    zip.extractall(out_folder)
    if decompile_files:
        decompile_dir(out_folder)
    pass


def extract_folder(ea_folder, gameplay_folder):
    for root, dirs, files in os.walk(gameplay_folder):
        for ext_filter in script_package_types:
            for filename in fnmatch.filter(files, ext_filter):
                extract_subfolder(root, filename, ea_folder)


def compile_module(mod_creator_name=None, root=None, mod_scripts_folder=None, mod_name=None, ignore_folders=None, include_folders=None):
    if not mod_creator_name:
        mod_creator_name = creator_name
    if not mod_name:
        mod_name = os.path.join('..', '..', os.path.basename(os.path.normpath(os.path.dirname(os.path.realpath('__file__')))))
        print('No mod name found, setting the path name to \'{}\'.'.format(mod_name))
    print('The current working directory {}.'.format(os.getcwd()))

    if mod_creator_name:
        print('Mod creator name found, appending mod creator name to file name.')
        mod_name = '{}_{}'.format(mod_creator_name, mod_name)
    script_zip_name = '{}.ts4script'.format(mod_name)
    if not root:
        ts4script = script_zip_name
    else:
        ts4script = os.path.join(root, script_zip_name)

    try:
        if os.path.exists(ts4script):
            print('Script archive found, removing found archive.')
            os.remove(ts4script)
            print('Script archive removed.')
        zf = PyZipFile(ts4script, mode='w', allowZip64=True, optimize=2)
        child_directories = get_child_directories(mod_scripts_folder)
        previous_working_directory = os.getcwd()
        print('Changing the working directory to \'{}\''.format(mod_scripts_folder))
        os.chdir(mod_scripts_folder)
        print('Changed the current working directory \'{}\'.'.format(os.getcwd()))
        # print('Found child directories {}'.format(pformat(tuple(child_directories))))
        for folder in child_directories:
            # print('Attempting to compile {}'.format(folder))
            if ignore_folders is not None and os.path.basename(folder) in ignore_folders:
                # print('Folder is set to be ignored. Continuing to the next folder.')
                continue
            if include_folders is not None and os.path.basename(folder) not in include_folders:
                # print('Folder is not set to be included. Continuing to the next folder.')
                continue
            try:
                print('Compiling folder \'{}\''.format(folder))
                zf.writepy(folder)
                print('\'{}\' compiled successfully.'.format(folder))
            except Exception as ex:
                print('Failed to write {}. {}'.format(folder, ex.args[1]))
                continue
        print('Done compiling files.')
        zf.close()
        print('Changing working directory to previous working directory.')
        os.chdir(previous_working_directory)
        print('Changed the current working directory to \'{}\''.format(os.getcwd()))
    except Exception as ex:
        print('Failed to create {}. {}'.format(ts4script, ex.args[1]))
        return

    # ts4script_mods = os.path.join(os.path.join(mods_folder), script_zip_name)
    # shutil.copyfile(ts4script, ts4script_mods)


def get_child_directories(d):
    return filter(os.path.isdir, [f for f in os.listdir(d)])