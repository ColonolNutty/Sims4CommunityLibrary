from unpyc3 import decompile, dec_module
import io
import os
import sys
import zipfile
from shutil import copyfile

SLASH = "\\"
PATH_DIR = input("Enter the path of the sims 4 [C:\Program Files\The Sims 4\] : ")
PATH_DIR = PATH_DIR or 'C:\Program Files\The Sims 4' + SLASH
FILES_IN_ZIP = ("base","core","simulation")

if not os.path.exists(PATH_DIR):
    sys.exit("\nError! The Sims 4 Path Not Found")
else:
    print(">> OK. <<")

if(PATH_DIR[-1:] == "\\"):
    PATH_DIR = PATH_DIR + "Data\Simulation\Gameplay" + SLASH
else:
    PATH_DIR = PATH_DIR + "\Data\Simulation\Gameplay" + SLASH

NEW_DIR = input("Insert the destination of decompiled files [C:\Temp] : ")
NEW_DIR = NEW_DIR or 'C:\Temp' + SLASH

if(NEW_DIR[-1:] == SLASH):
    NEW_DIR = NEW_DIR + ""
else:
    NEW_DIR = NEW_DIR + SLASH

if not os.path.exists(NEW_DIR):
    sys.exit("\nError! Destination Path not Found")
else:
    print(">> OK. <<")

try:
    for file in FILES_IN_ZIP:
        FROM_COPY_DIR = PATH_DIR+file+".zip"
        TO_PATH_DIR = NEW_DIR+file+".zip"
        copyfile(FROM_COPY_DIR, TO_PATH_DIR)
        zip_ref = zipfile.ZipFile(TO_PATH_DIR, 'r')
        if not os.path.exists(NEW_DIR+file): os.makedirs(NEW_DIR+file)
        zip_ref.extractall(NEW_DIR+file)
        zip_ref.close()
        os.remove(TO_PATH_DIR)
except:
    sys.exit("Error in Unzipping files! Try With Another Destination Folder")

for root, dirs, files in os.walk(NEW_DIR):
    for file in files:
        print(root + SLASH + file + ' --> DECOMPILED!')
        if file.endswith(".pyo"):
            if not os.path.exists(root):
                os.makedirs(root)
            f1 = open(root+SLASH+file.replace(".pyo",".py"),"w+")
            try:
                print(decompile(root+SLASH+file), file=f1)
                os.remove(root+SLASH+file)
                f1.close()
            except:
                f1.close()
                os.remove(root+SLASH+file.replace(".pyo",".py"))
            continue
        else:
            continue
