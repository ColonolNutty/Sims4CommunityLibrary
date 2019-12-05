# TS4 Python decompiler front-end
#   by Scumbumbo @ Mod The Sims
#   and Andrew @ Sims 4 Studio
#
# May be freely modified for personal use
#
# May be redistributed AS-IS or in modified form, providing:
#   - All comments and code authorship attributions remain unmodified except as required for clarity
#   - This redistribution notice must remain intact
#   - The hosted site is free and community-friendly:
#     - Host site may be advertising supported to offset costs
#     - Host site may not restrict downloads in any way, particularly but not limited to
#       - Paid registration requirements (free registrations are okay)
#       - Forced download waits due to ad-block detection
#
from settings import compiler_name, game_folder
import os

# These defaults can be edited here and/or overriden on command line
#
# Location of the game's zipped binary scripts (base.zip, core.zip and simulation.zip)
if os.name == 'posix':
    # Mac default location
    GAME_ZIP_FOLDER = os.path.join(os.environ['HOME'], 'Applications/The Sims 4.app/Contents/Data/Simulation/Gameplay')
else:
    # Windows default location
    GAME_ZIP_FOLDER = game_folder

# Default destination folder to put decompiled scripts into.
# Will be created if not found.
DEFAULT_PY_DEST_FOLDER = './ts4_scripts'

# You may want to turn this down to 2 or 4 if you don't have a quad-core CPU
DEFAULT_MAX_THREADS = 1

# Set to either 'unpyc3' or 'py37dec'
DEFAULT_DECOMPILER = compiler_name

"""      Command line help:

decompiler.py - For decompiling The Sims 4 Python modules

Requires:
   - Python version 3.7.0
   - py37dec executable must be available on the system path or in current folder,
     or unpyc3 (with 3.7.0 decompile support) module must be available for import

usage: decompiler.py [-h] [-z ZIP_FOLDER] [-s SOURCE_FOLDER] [-d DEST_FOLDER]
                     [-S] [-p] [-t N] [-r [FILENAME]] [-L [N]]
                     [-c none|detail] [-U] [-P] [-T SEC]

optional arguments:
  -h, --help        show this help message and exit
  -z ZIP_FOLDER     location of installed game Zip files
  -s SOURCE_FOLDER  get compiled scripts from folder instead of Zip files
  -d DEST_FOLDER    destination folder for decompilaed files
  -S                create subfolders of DEST_FOLDER by result
  -p                prefix output filenames with [RESULT]
  -t N              number of simultaneous decompile threads to use
  -r [FILENAME]     create CSV file containing results for decompiled files
  -L [N]            code objects with >N bytes will not be analyzed
  -c none|detail    prefix decompiled files with test results comment (default brief)
  -U                use unpyc3 for decompilation
  -P                use py37dec for decompilation
  -T SEC            py37dec only: override timeout in seconds (0=no limit, default 5)
"""


#################################################################
# DO NOT EDIT BELOW THIS LINE WITHOUT KNOWING WHAT YOU'RE DOING #
#################################################################
import subprocess
import time
import traceback
import dis
import marshal
import types
import inspect
import difflib
import re
import multiprocessing
import sys
import argparse
import shutil
import zipfile

if DEFAULT_DECOMPILER != 'py37dec' and DEFAULT_DECOMPILER != 'unpyc3':
    print('Invalid setting for DEFAULT_DECOMPILER in source')
    exit()
if os.path.isfile('./py37dec.exe'):
    PY37DEC_LOCATION = './py37dec.exe'
elif os.path.isfile('./py37dec'):
    PY37DEC_LOCATION = './py37dec'
else:
    PY37DEC_LOCATION = shutil.which('py37dec')
PY37DEC_AVAILABLE = True if not PY37DEC_LOCATION is None else False
UNPYC3_AVAILABLE = False
DECOMPILER = None
try:
    import unpyc3
    UNPYC3_AVAILABLE = True
except:
    pass

# Quick 'n' dirty stopwatch timer
class Timer():
    def __init__(self):
        self.start_time = time.perf_counter()

    def elapsed_time(self):
        return time.perf_counter() - self.start_time

# Values returned from a "thread" to indicate results.  Since the Python VM doesn't really
# support true threads and shared data, the results are encapsulated in this and the Python
# "threading" library returns this information to the main thread via an OS dependent mechanism.
class DecompileResultData():
    def __init__(self, _pycFilename):
        self.pycFilename = _pycFilename
        self.pyFilename = ''
        self.decompile_time = -1
        self.analyze_time = -1
        self.result = -1

# Reads the code object from a compiled Python (.pyc) file
def get_codeobj_from_pyc(filename):
    with open(filename, 'rb') as fp:
        code_obj = marshal.loads(fp.read()[16:])
    return code_obj

# Code object comparison routines based on code written by Andrew from Sims 4 Studio
#
# Handle formatting dis() output of a code object in order to run through a diff process.
code_obj_regex = re.compile(r'(.*)\(\<code object (.*) at 0x.*, file "(.*)", line (.*)>\)', re.RegexFlag.IGNORECASE)

def format_dis_lines(co):

    def remove_line_number(s: str):
        ix = s.index(' ', 5)
        x = s[ix:].lstrip(' ')
        return x

    def clean_code_object_line(s: str):
        # strip out any line numbers, filenames, or offsets
        global code_obj_regex
        b = code_obj_regex.match(s)
        if b:
            return s.replace(b.group(0), '{}<{}>'.format(b.group(1), b.group(2)))
        return s

    return list(
               map(clean_code_object_line,
                   map(remove_line_number,
                       filter(None,
                              dis.Bytecode(co).dis().split('\n')))))

# Perform the actual code object comparisons
# Returns a string of errors found, or an empty string for a perfect comparison result
def compare_codeobjs(pyc_co, py_co, large_codeobjects_threshold):
    # Large code objects can take a significant time to process with diff(), so skipped by default
    if large_codeobjects_threshold and len(py_co.co_code) > large_codeobjects_threshold:
        return '{0}\nSKIPPING COMPARISON OF LARGE CODE OBJECT\n\t{1}\n{0}\n'.format('='*80, pyc_co.co_name)
    err_str = ''
    flags_err_str = ''
    names_err_str = ''
    consts_err_str = ''
    args_err_str = ''
    locals_err_str = ''
    if pyc_co.co_flags != py_co.co_flags:
        flags_err_str = 'Differings flags: {} != {}\n'.format(pyc_co.co_flags, py_co.co_flags)
        if (pyc_co.co_flags & 0x4) == 0x4 and (py_co.co_flags & 0x4) == 0:
            flags_err_str += '\tMissing expected *args\n'
        if (pyc_co.co_flags & 0x8) == 0x8 and (py_co.co_flags & 0x8) == 0:
            flags_err_str += '\tMissing expected **kwargs\n'
        if (pyc_co.co_flags & 0x20) != (py_co.co_flags & 0x20):
            if pyc_co.co_flags & 0x20 == 0x20:
                flags_err_str += '\tShould be generator function but is not\n'
            else:
                flags_err_str += '\tIs generator function but should not be\n'
    if pyc_co.co_kwonlyargcount != py_co.co_kwonlyargcount:
        args_err_str = 'Differing kwonlyargcount: {} != {}\n'.format(pyc_co.co_kwonlyargcount, py_co.co_kwonlyargcount)
    if pyc_co.co_argcount != py_co.co_argcount:
        args_err_str += 'Differing argcount: {} != {}\n'.format(pyc_co.co_argcount, py_co.co_argcount)
    if len(py_co.co_names) != len(pyc_co.co_names):
        names_err_str += 'Differing number of global names: {} != {}\n'.format(len(pyc_co.co_names), len(py_co.co_names))
        names_err_str +=  '\tExpected: {}\n\tActual:   {}\n'.format(pyc_co.co_names, py_co.co_names)
    else:
        idxc = 0
        # Compare all constant names to ensure equality
        for name in pyc_co.co_names:
            if len(py_co.co_names) < idxc + 1:
                names_err_str +=  'Unable to compare global name {}. Does not exist in the decompiled version\n'.format(name)
            elif name != py_co.co_names[idxc]:
                names_err_str +=  'Global name: {} != {}\n'.format(name, py_co.co_names[idxc])
            idxc += 1
    if len(py_co.co_consts) != len(pyc_co.co_consts):
        consts_err_str += 'Differing number of constants: {} != {}\n'.format(len(pyc_co.co_consts), len(py_co.co_consts))
        consts_err_str +=  '\tExpected: {}\n\tActual:   {}\n'.format(pyc_co.co_consts, py_co.co_consts)
    else:
        idxc = 0
        # Compare all constants to ensure equality
        for constant in pyc_co.co_consts:
            if len(py_co.co_consts) < idxc + 1:
                consts_err_str +=  'Unable to compare constant {}. Does not exist in the decompiled version\n'.format(constant)
            elif type(constant) is types.CodeType:
                if type(py_co.co_consts[idxc]) is types.CodeType:
                    err_str += compare_codeobjs(constant, py_co.co_consts[idxc], large_codeobjects_threshold)
                else:
                    consts_err_str += 'Constants mismatched: unable to compare code object {} to non-code object {}\n'.format(constant, py_co.co_consts[idxc])
            elif constant != py_co.co_consts[idxc]:
                consts_err_str +=  'Constant: {} != {}\n'.format(constant, py_co.co_consts[idxc])
            idxc += 1
    if py_co.co_nlocals != pyc_co.co_nlocals:
        locals_err_str += 'Differing number of locals: {} != {}\n'.format(pyc_co.co_nlocals, py_co.co_nlocals)
        locals_err_str +=  '\tExpected: {}\n\tActual:   {}\n'.format(pyc_co.co_varnames, py_co.co_varnames)
    else:
        idxc = 0
        # Compare all local names to ensure equality
        for name in pyc_co.co_varnames:
            if py_co.co_nlocals < idxc + 1:
                locals_err_str +=  'Unable to compare local var name {}. Does not exist in the decompiled version\n'.format(constant)
            elif name != py_co.co_varnames[idxc]:
                locals_err_str +=  'Local var name: {} != {}\n'.format(name, py_co.co_varnames[idxc])
            idxc += 1
    if len(py_co.co_cellvars) != len(pyc_co.co_cellvars):
        locals_err_str += 'Differing number of cellvars: {} != {}\n'.format(len(pyc_co.co_cellvars), len(py_co.co_cellvars))
        locals_err_str +=  '\tExpected: {}\n\tActual:   {}\n'.format(pyc_co.co_cellvars, py_co.co_cellvars)
    else:
        idxc = 0
        # Compare all cellvar names to ensure equality
        for name in pyc_co.co_cellvars:
            if len(py_co.co_cellvars) < idxc + 1:
                locals_err_str +=  'Unable to compare cellvar name {}. Does not exist in the decompiled version\n'.format(constant)
            elif name != py_co.co_cellvars[idxc]:
                locals_err_str +=  'Cellvar name: {} != {}\n'.format(name, py_co.co_cellvars[idxc])
            idxc += 1
    if flags_err_str or args_err_str or names_err_str or consts_err_str or locals_err_str:
        err_str += '{0}\n{1}\n{0}\n'.format('='*80, pyc_co.co_name)
        if flags_err_str:
            err_str += flags_err_str
        if args_err_str:
            err_str += args_err_str
        if names_err_str:
            err_str += names_err_str
        if consts_err_str:
            err_str += consts_err_str
        if locals_err_str:
            err_str += locals_err_str
    a = format_dis_lines(pyc_co)
    b = format_dis_lines(py_co)
    d = list(difflib.unified_diff(a, b))
    if any(d):
        err_str +=  '{0}\n{1}\n{0}\nEXPECTED:\n\t{2}\n{0}\nACTUAL:\n\t{3}\n{0}\nDIFF:\n\t{4}\n{0}\n'.format('='*80, pyc_co.co_name, str.join('\n\t', a), str.join('\n\t', b), str.join('\n\t', d))
    return err_str

# Decompile a .pyc file producing a .py file
# Returns a DecompileResultData encapsulation of the result information.
def decompile(srcFolder, destFolder, subFolder, pycFile, pyFile, prefix_filenames, large_codeobjects_threshold, comment_style, decompiler, py37dec_timeout, split_result_folders):
    decompile_results = DecompileResultData(os.path.realpath(os.path.join(srcFolder, subFolder, pycFile)))
    timer = Timer()
    remove_pyc = True if srcFolder == destFolder else False
    pycFullFilename = os.path.join(srcFolder, subFolder, pycFile)

    try:
        if decompiler == 'unpyc3':
            # For unpyc3, just call the decompile() method from that module
            src_code = ''
            lines = unpyc3.decompile(pycFullFilename)
            for line in lines:
                src_code += str(line) + '\n'
        else:
            # For py37dec, run the executable in a subprocess.  At least one file from TS4 still takes
            # too long (and too much virtual memory) to process, so a timeout is specified.
            subprocess_result = subprocess.run([PY37DEC_LOCATION, pycFullFilename.replace('\\','/')], capture_output=True, encoding='utf-8', timeout=py37dec_timeout)
            decompile_results.decompile_time = timer.elapsed_time()
            if subprocess_result.returncode != 0:
                # Non-zero return code from the py37dec executable indicates a crash failure
                # in the executable.  Summarize and build an empty .py file.
                if prefix_filenames:
                    pyFile = '[FAILED] ' + pyFile
                if split_result_folders:
                    pyFolder = os.path.join(destFolder, 'decompile_failure', subFolder)
                else:
                    pyFolder = os.path.join(destFolder, subFolder)
                os.makedirs(pyFolder, exist_ok=True)
                decompile_results.pyFilename = os.path.realpath(os.path.join(pyFolder, pyFile))
                with open(decompile_results.pyFilename, 'w', encoding='UTF-8') as fp:
                    if comment_style == 1:
                        fp.write('# {}: Decompile failed\n'.format(decompiler))
                    elif comment_style == 2:
                        fp.write('"""\npy37dec: Decompilation failure\n\n')
                        fp.write(subprocess_result.stderr)
                        fp.write('"""\n')
                decompile_results.result = 3
                if remove_pyc:
                    os.remove(pycFullFilename)
                return decompile_results
            # Rc = 0 from subprocess, so read the source code lines from the subproccess stdout
            src_code = subprocess_result.stdout
    except subprocess.TimeoutExpired:
        # This exception will only occur if a py37dec subprocess is killed off due to a timeout.
        decompile_results.decompile_time = timer.elapsed_time()
        if prefix_filenames:
            pyFile = '[TIMEOUT] ' + pyFile
        if split_result_folders:
            pyFolder = os.path.join(destFolder, 'timeout', subFolder)
        else:
            pyFolder = os.path.join(destFolder, subFolder)
        os.makedirs(pyFolder, exist_ok=True)
        decompile_results.pyFilename = os.path.realpath(os.path.join(pyFolder, pyFile))
        decompile_results.result = 4
        with open(decompile_results.pyFilename, 'w', encoding='UTF-8') as fp:
            if comment_style == 1:
                fp.write('# py37dec: Timeout\n')
            elif comment_style == 2:
                fp.write('"""\npy37dec: Timeout of {} seconds exceeded\n"""\n'.format(py37dec_timeout))
        if remove_pyc:
            os.remove(pycFullFilename)
        return decompile_results
    except:
        # A normal exception will occur if unpyc3 fails and throws an exception during the
        # decompilation process.
        if prefix_filenames:
            pyFile = '[FAILED] ' + pyFile
        if split_result_folders:
            pyFolder = os.path.join(destFolder, 'decompile_failure', subFolder)
        else:
            pyFolder = os.path.join(destFolder, subFolder)
        os.makedirs(pyFolder, exist_ok=True)
        decompile_results.pyFilename = os.path.realpath(os.path.join(pyFolder, pyFile))
        with open(decompile_results.pyFilename, 'w', encoding='UTF-8') as fp:
            if comment_style == 1:
                fp.write('# {}: Decompile failed\n'.format(decompiler))
            elif comment_style == 2:
                fp.write('"""\nunpyc3: Decompilation failure\n\n')
                fp.write(traceback.format_exc())
                fp.write('"""\n')
        decompile_results.result = 3
        if remove_pyc:
            os.remove(pycFullFilename)
        return decompile_results

    decompile_results.decompile_time = timer.elapsed_time()

    synErr = None
    try:
        # Try compiling the generated source, a syntax error in the source code
        # will throw an exception.
        py_codeobj = compile(src_code, pyFile, 'exec')

        # Get the code object from the .pyc file
        pyc_codeobj = get_codeobj_from_pyc(decompile_results.pycFilename)
        
        # Compare the code objects recursively
        issues = compare_codeobjs(pyc_codeobj, py_codeobj, large_codeobjects_threshold)
        decompile_results.analyze_time = timer.elapsed_time() - decompile_results.decompile_time

        if not issues:
            # There were no issues returned from the code object comparison, so this code
            # is identical to the original sources.
            if prefix_filenames:
                pyFile = '[PERFECT] ' + pyFile
            if split_result_folders:
                pyFolder = os.path.join(destFolder, 'perfect', subFolder)
            else:
                pyFolder = os.path.join(destFolder, subFolder)
            decompile_results.pyFilename = os.path.realpath(os.path.join(pyFolder, pyFile))
            decompile_results.result = 0
        else:
            # There were comparison issues with the code objects, this source code differs
            # from the original.  It may function identically or improperly (or not at all) but
            # only human inspection of the resulting code can determine how good the results are.
            if prefix_filenames:
                pyFile = '[GOOD] ' + pyFile
            if split_result_folders:
                pyFolder = os.path.join(destFolder, 'good', subFolder)
            else:
                pyFolder = os.path.join(destFolder, subFolder)
            decompile_results.pyFilename = os.path.realpath(os.path.join(pyFolder, pyFile))
            decompile_results.result = 1
    except:
        # An exception from the compile or comparison will end up here, this is generally
        # due to a syntax error in the decompilation results.
        if prefix_filenames:
            pyFile = '[SYNTAX] ' + pyFile
        if split_result_folders:
            pyFolder = os.path.join(destFolder, 'syntax', subFolder)
        else:
            pyFolder = os.path.join(destFolder, subFolder)
        decompile_results.pyFilename = os.path.realpath(os.path.join(pyFolder, pyFile))
        decompile_results.result = 2
        synErr = traceback.format_exc(1)
    # Create the destination folder for this .py file and write it, adding comments
    # if requested (1 = brief, 2 = detailed).
    os.makedirs(pyFolder, exist_ok=True)
    with open(decompile_results.pyFilename, 'w', encoding='UTF-8') as fp:
        if comment_style == 1:
            if synErr:
                fp.write('# {}: Syntax error in decompiled file\n'.format(decompiler))
            elif issues:
                fp.write('# {}: Decompiled file contains inaccuracies\n'.format(decompiler))
            else:
                fp.write('# {}: 100% Accurate decompile result\n'.format(decompiler))
        elif comment_style == 2:
            if synErr:
                fp.write('"""\n{}:\n{}"""\n'.format(decompiler, synErr))
            elif issues:
                fp.write('"""\n{}:\n{}"""\n'.format(decompiler, issues))
            else:
                fp.write('# {}: 100% Accurate decompile result\n'.format(decompiler))
        fp.write(src_code)

    if remove_pyc:
        os.remove(pycFullFilename)
    return decompile_results

#
# The following all runs in the main "thread"
#
# Result buckets and counters for the DecompileResultData from each thread
perfect = []
good = []
syntax = []
failed = []
timeout = []
completed = 0
total = 0

# A completed thread will issue this callback in the main thread, place the
# DecompileResultData into a bucket depending on the returned result.
def completed_callback(result) -> bool:
    global completed, total
    completed += 1

    # Write percentage complete to stdout
    #sys.stdout.write('\b\b\b\b{:3}%'.format(int(completed/total*100)))
    #sys.stdout.flush()
    
    if result.result == 0:
        perfect.append(result)
        return True
    elif result.result == 1:
        good.append(result)
        return True
    elif result.result == 2:
        print('syntax')
        syntax.append(result)
        return False
    elif result.result == 3:
        print('failed')
        failed.append(result)
        return False
    else:
        print('timeout')
        timeout.append(result)
        return False


def is_success(result) -> bool:
    if result.result == 0:
        return True
    elif result.result == 1:
        return True
    elif result.result == 2:
        return False
    elif result.result == 3:
        return False
    else:
        return False

# Unzips the script files (.pyc) from the TS4 game executable folders into the destination folder.
def unzip_script_files(zip_folder, dest_folder):
    print('Extracting Zip files from game, please wait.')
    for file in ['base.zip', 'core.zip', 'simulation.zip']:
        zip = zipfile.ZipFile(os.path.join(zip_folder, file))
        zip.extractall(os.path.join(dest_folder, os.path.splitext(file)[0]))
    if os.name == 'posix':
        # Mac location for generated.zip
        generated_folder = os.path.realpath(os.path.join(zip_folder, '../../../Python'))
    else:
        # Windows location for generated.zip
        generated_folder = os.path.realpath(os.path.join(zip_folder, '../../../Game/Bin/Python'))
    zip = zipfile.ZipFile(os.path.join(generated_folder, 'generated.zip'))
    zip.extractall(os.path.join(dest_folder, 'generated'))


# Launch "threads" and summarize results
def main(src_folder, dest_folder, prefix_filenames=False, max_threads=DEFAULT_MAX_THREADS, results_file=None, test_large_codeobjects=False, large_codeobjects_threshold=10000, comment_style=0, py37dec_timeout=5, split_result_folders=False):
    global total, DEFAULT_DECOMPILER
    from shutil import copyfile
    from Utilities.compiler import decompile_file as unpyc3_decompile

    timer = Timer()
    if py37dec_timeout == 0:
        py37dec_timeout = None

    # Create our "thread" pool
    results = []
    #pool = multiprocessing.Pool(processes=max_threads)

    print('Decompiling all files in {} using {}, please wait'.format(src_folder, DEFAULT_DECOMPILER))

    # Search the source folder for all .pyc files and add a call to decompile()
    # to the "thread" pool.
    srcFolder = os.path.realpath(src_folder)
    destFolder = os.path.realpath(dest_folder)
    for root, subFolders, files in os.walk(src_folder):
        files = [f for f in files if os.path.splitext(f)[1].lower() == '.pyc']
        for pycFile in files:
            total += 1
            subFolder = os.path.relpath(root, srcFolder)
            file_name = os.path.splitext(pycFile)[0]
            pyFile = file_name + '.py'
            pyFullFilename = os.path.join(srcFolder, subFolder, pyFile)
            copiedFilePath = os.path.join(srcFolder, subFolder, pycFile + '_copied')
            pycFullFilename = os.path.join(srcFolder, subFolder, pycFile)
            copyfile(pycFullFilename, copiedFilePath)
            sys.stdout.write(os.path.join(src_folder, subFolder, pycFile) + '\n')
            result = decompile(srcFolder, destFolder, subFolder, pycFile, pyFile, prefix_filenames, large_codeobjects_threshold, comment_style, DECOMPILER, py37dec_timeout, split_result_folders)
            if not is_success(result):
                print('Failed to decompile file, attempting to use alternative decompiler.')
                os.remove(pyFullFilename)
                copyfile(copiedFilePath, pycFullFilename)
                os.remove(copiedFilePath)
                if not unpyc3_decompile(pycFullFilename, throw_on_error=False):
                    print('Failed to decompile, even with alternative decompiler')
                else:
                    print('Success! File decompiled successfully via alternative method.')
                    os.remove(pycFullFilename)
                    result = DecompileResultData(os.path.realpath(pycFullFilename))
                    result.result = 1
            else:
                os.remove(copiedFilePath)
            completed_callback(result)
            results.append(result)

    # Print results summary and CSV results file if requested
    sys.stdout.write('\b\b\b\b\b\b')
    if total == 0:
        print('      \nError, no compiled Python files found in source folder')
        return
    print('Completed')

    print('\nperfect\t= {} ({:0.1f}%)'.format(len(perfect), len(perfect)/total*100))
    print('good\t= {} ({:0.1f}%)'.format(len(good), len(good)/total*100))
    print('syntax\t= {} ({:0.1f}%)'.format(len(syntax), len(syntax)/total*100))
    print('failure\t= {} ({:0.1f}%)'.format(len(failed), len(failed)/total*100))
    if len(timeout) > 0:
        print('timeout\t= {} ({:0.1f}%)'.format(len(timeout), len(timeout)/total*100))
    print('{:0.2f} seconds'.format(timer.elapsed_time()))

    if results_file:
        with open(results_file, 'w', encoding='UTF-8') as fp:
            fp.write(' ,Compiled,Decompiled,Decompile,Compare\nResult,Path,Path,Time,Time\n')
            for decompile_result in perfect:
                fp.write('PERFECT,{},{},{},{}\n'.format(os.path.relpath(decompile_result.pycFilename, src_folder), os.path.relpath(decompile_result.pyFilename, dest_folder), decompile_result.decompile_time, decompile_result.analyze_time))
            for decompile_result in good:
                fp.write('GOOD,{},{},{},{}\n'.format(os.path.relpath(decompile_result.pycFilename, src_folder), os.path.relpath(decompile_result.pyFilename, dest_folder), decompile_result.decompile_time, decompile_result.analyze_time))
            for decompile_result in failed:
                fp.write('FAILED,{},{},{},{}\n'.format(os.path.relpath(decompile_result.pycFilename, src_folder), os.path.relpath(decompile_result.pyFilename, dest_folder), decompile_result.decompile_time, decompile_result.analyze_time))
            for decompile_result in syntax:
                fp.write('SYNTAX,{},{},{},{}\n'.format(os.path.relpath(decompile_result.pycFilename, src_folder), os.path.relpath(decompile_result.pyFilename, dest_folder), decompile_result.decompile_time, decompile_result.analyze_time))
            for decompile_result in timeout:
                fp.write('TIMEOUT,{},{},{},{}\n'.format(os.path.relpath(decompile_result.pycFilename, src_folder), os.path.relpath(decompile_result.pyFilename, dest_folder), decompile_result.decompile_time, decompile_result.analyze_time))

# Setup and parse command line options, calling main() with all desired options
if __name__ == '__main__':
    if sys.version_info[0] != 3 or sys.version_info[1] != 7 or sys.version_info[2] != 0:
        print('Decompiler requires Python version 3.7.0 for proper results')
        exit()

    # If the default decompiler is not available, override that and print a warning
    if DEFAULT_DECOMPILER == 'py37dec':
        if not PY37DEC_AVAILABLE:
            if UNPYC3_AVAILABLE:
                print('py37dec unavailable, will use unpyc3 as default')
                DECOMPILER = 'unpyc3'
        else:
            DECOMPILER = 'py37dec'
    else:
        if not UNPYC3_AVAILABLE:
            if PY37DEC_AVAILABLE:
                print('unpyc3 unavailable, will use py37dec as default')
                DECOMPILER = 'py37dec'
        else:
            DECOMPILER = 'unpyc3'
    if not DECOMPILER:
        print('No decompiler is available, please install unpyc3 or py37dec')
        exit()

    parser = argparse.ArgumentParser()
    parser.add_argument('-z', nargs=1, metavar='ZIP_FOLDER', default=[GAME_ZIP_FOLDER], dest='zip_folder', help='location of installed game Zip files')
    parser.add_argument('-s', nargs=1, metavar='SOURCE_FOLDER', default=[None], dest='src_folder', help='get compiled scripts from folder instead of Zip files')
    parser.add_argument('-d', nargs=1, metavar='DEST_FOLDER', default=[DEFAULT_PY_DEST_FOLDER], dest='dest_folder', help='destination folder for decompilaed files')
    parser.add_argument('-S', action='store_true', dest='split_result_folders', help='create subfolders of DEST_FOLDER by result')
    parser.add_argument('-p', action='store_true', dest='prefix_filenames', help='prefix output filenames with [RESULT]')
    parser.add_argument('-t', nargs=1, type=int, metavar='N', default=[DEFAULT_MAX_THREADS], dest='max_threads', help='number of simultaneous decompile threads to use')
    parser.add_argument('-r', nargs='?', metavar='FILENAME', default=argparse.SUPPRESS, dest='results_file', help='create CSV file containing results for decompiled files')
    parser.add_argument('-L', nargs='?', type=int, metavar='N', default=argparse.SUPPRESS, dest='large_codeobjects_threshold', help='code objects with >N bytes will not be analyzed')
    parser.add_argument('-c', nargs=1, metavar='none|detail', choices=['none', 'detail'], default=argparse.SUPPRESS, dest='comment_style', help='prefix decompiled files with test results comment (default brief)')
    if UNPYC3_AVAILABLE:
        parser.add_argument('-U', action='store_true', dest='use_unpyc3', help='use unpyc3 for decompilation')
    if PY37DEC_AVAILABLE:
        parser.add_argument('-P', action='store_true', dest='use_py37dec', help='use py37dec for decompilation')
        parser.add_argument('-T', nargs=1, type=int, metavar='SEC', default=[5], dest='py37dec_timeout', help='py37dec only: override timeout in seconds (0=no limit, default 5)')

    args = parser.parse_args()
    if hasattr(args, 'use_unpyc3') and hasattr(args, 'use_py37dec') and args.use_unpyc3 and args.use_py37dec:
        parser.print_help()
        print('\n-U and -P options conflict, please use only one')
        exit()
    if hasattr(args, 'use_unpyc3') and args.use_unpyc3:
        DECOMPILER = 'unpyc3'
    if hasattr(args, 'use_py37dec') and args.use_py37dec:
        DECOMPILER = 'py37dec'
    if hasattr(args, 'results_file'):
        if args.results_file is None:
            args.results_file = 'results.csv'
    else:
        args.results_file = None
    if hasattr(args, 'large_codeobjects_threshold'):
        if args.large_codeobjects_threshold is None:
            args.large_codeobjects_threshold = 10000
    else:
        args.large_codeobjects_threshold = None
    comment_style = 1
    if hasattr(args, 'comment_style'):
        if args.comment_style[0] == 'none':
            comment_style = 0
        else:
            comment_style = 2
    if not hasattr(args, 'py37dec_timeout'):
        args.py37dec_timeout = [0]
    if args.src_folder[0] is None:
        unzip_script_files(args.zip_folder[0], args.dest_folder[0])
        args.src_folder[0] = args.dest_folder[0]
    main(args.src_folder[0], args.dest_folder[0], prefix_filenames=args.prefix_filenames, max_threads=args.max_threads[0], results_file=args.results_file, large_codeobjects_threshold=args.large_codeobjects_threshold, comment_style=comment_style, py37dec_timeout=args.py37dec_timeout[0], split_result_folders=args.split_result_folders)
