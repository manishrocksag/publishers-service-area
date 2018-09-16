"""
The module is used to create the folder structure for a debian package. This is
extensible for any repository.
"""

import os
import sys
import shutil

EXCLUDE = ['makepkg', 'pkg_creator.py', 'deb_package', '.git',
           '*.log', '*.log.*', '*.logs', '*.logs.*']

ROOT_FOLDER_NAME = 'debian_package'


def build_package(workspace_path, repo_name, debian_folder_name):
    dest = os.path.join(workspace_path, debian_folder_name, 'usr', 'share', repo_name)

    # Then, copying over the contents of the source. Exclude the files that are not required.
    src = os.path.join(workspace_path)
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns(*EXCLUDE))


def main(workspace, repo_name, debian_folder_name):
    build_package(workspace, repo_name, debian_folder_name)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
