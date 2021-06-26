import shutil
import os
import io
import fnmatch
import traceback
from zipfile import PyZipFile
from Utilities.unpyc3 import decompile


class Unpyc3PyDecompiler:
    """A handler that can both compile and decompile scripts using unpyc3."""
    _script_package_types = ['*.zip', '*.ts4script']

    @classmethod
    def decompile_file(cls, path_to_file_for_decompile: str, throw_on_error: bool=False) -> bool:
        """Decompile a python file using unpyc3."""
        _replace_characters = ()
        # print('Decompiling \'{}\''.format(path_to_file_for_decompile))
        decompiled_py = decompile(path_to_file_for_decompile)
        with io.open(path_to_file_for_decompile.replace('.pyc', '.py').replace('.pyo', '.py'), 'w', encoding="utf-8") as output_py:
            success = True
            for statement in decompiled_py.statements:
                try:
                    statement_str = str(statement)
                    for replace_char in _replace_characters:
                        statement_str = statement_str.replace(replace_char, '-----')
                    output_py.write(statement_str + '\r')
                except Exception as ex:
                    try:
                        statement_for_display = statement.gen_display() if hasattr(statement, 'gen_display') else statement
                        print(f'Failed to parse statement. {statement_for_display} {ex}')
                        traceback.print_exc()
                        if throw_on_error:
                            raise ex
                        success = False
                    except Exception as ex2:
                        print(f'Another error occurred! {ex} {ex2}')
                        if throw_on_error:
                            raise ex2
                        success = False
                        continue
        return success

    @classmethod
    def decompile_folder(cls, folder_path: str, throw_on_error: bool=False) -> None:
        """Decompile python files within a folder using unpyc3."""
        pattern = '*.pyc'
        successful_decompiles = 0
        failed_decompiles = 0
        for root, dirs, files in os.walk(folder_path):
            for file_name in fnmatch.filter(files, pattern):
                path_to_file_for_decompile = str(os.path.join(root, file_name))
                try:
                    if cls.decompile_file(path_to_file_for_decompile, throw_on_error=True):
                        print(f'SUCCESS: {path_to_file_for_decompile}')
                        successful_decompiles += 1
                    else:
                        print(f'FAILED: {path_to_file_for_decompile}')
                        failed_decompiles += 1
                except Exception as ex:
                    print("FAILED to decompile %s" % path_to_file_for_decompile)
                    failed_decompiles += 1
                    traceback.print_exc()
                    if throw_on_error:
                        raise ex

    @classmethod
    def _extract_sub_folder(cls, root: str, filename: str, ea_folder: str, decompile_files: bool=True):
        src = os.path.join(root, filename)
        dst = os.path.join(ea_folder, filename)
        if src != dst:
            shutil.copyfile(src, dst)
        py_zip = PyZipFile(dst)
        out_folder = os.path.join(ea_folder, os.path.splitext(filename)[0])
        py_zip.extractall(out_folder)
        if decompile_files:
            cls.decompile_folder(out_folder)
        pass

    @classmethod
    def extract_folder(cls, ea_folder: str, gameplay_folder: str, decompile_files: bool=True):
        """Extract a folder."""
        for root, dirs, files in os.walk(gameplay_folder):
            for ext_filter in Unpyc3PyDecompiler._script_package_types:
                for filename in fnmatch.filter(files, ext_filter):
                    cls._extract_sub_folder(root, filename, ea_folder, decompile_files=decompile_files)

