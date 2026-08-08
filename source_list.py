#!/usr/bin/env python3

import os
import sys


def list_files(root_dir, extension=None):
    for current_dir, dirs, files in os.walk(root_dir):
        for file_name in files:
            if extension and not file_name.lower().endswith(extension.lower()):
                continue

            full_path = os.path.join(current_dir, file_name)
            print(os.path.relpath(full_path, root_dir))


def list_folders(root_dir, extension=None):
    folders = set()

    for current_dir, dirs, files in os.walk(root_dir):
        for file_name in files:
            if extension and not file_name.lower().endswith(extension.lower()):
                continue

            relative_dir = os.path.relpath(current_dir, root_dir)
            folders.add(relative_dir)

    for folder in sorted(folders):
        print(folder)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            f"Використання:\n"
            f"  {sys.argv[0]} <директорія> [розширення]\n"
            f"  {sys.argv[0]} <директорія> [розширення] -folder"
        )
        sys.exit(1)

    root_directory = sys.argv[1]

    if not os.path.isdir(root_directory):
        print(f"Помилка: '{root_directory}' не є директорією.")
        sys.exit(1)

    extension = None
    folder_mode = False

    for arg in sys.argv[2:]:
        if arg == "-folder":
            folder_mode = True
        else:
            extension = arg

    if folder_mode:
        list_folders(root_directory, extension)
    else:
        list_files(root_directory, extension)