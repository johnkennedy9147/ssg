import os
import shutil


def copy_static(src, dest):
    print(f"Copying files from {src} to {dest}.")
    if not os.path.exists(src):
        print(f"{src} directory not found, exiting.")
        return
    if os.path.exists(dest):
        print(f"{dest} directory already exists, deleting directory and all contents!")
        shutil.rmtree(dest)
    print(f"Creating {dest} directory")
    os.mkdir(dest)
    paths_to_copy = os.listdir(src)
    for path in paths_to_copy:
        fullpath = os.path.join(src, path)
        if os.path.isdir(fullpath):
            print(f"{fullpath} is a directory, recursing")
            copy_static(f"{src}/{path}", f"{dest}/{path}")
        else:
            destination_fullpath = os.path.join(dest, path)
            print(f"Copying file {fullpath} to {destination_fullpath}")
            shutil.copy(fullpath, destination_fullpath)
