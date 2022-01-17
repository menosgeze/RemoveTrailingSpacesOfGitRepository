"""
This script removes all trailing spaces of files with the given extensions
in a git repository, and then commits this change.

Copyright (c) 2022, Gerardo E Zelaya Eufemia
All rights reserved.
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

import argparse
import os

source_dirname = os.path.abspath(os.path.dirname(__file__)) + '/'


def listing_files(dirname: str, extensions_list: list):
    """
    Lists filenames in the git repository located at the dirname
    with extensions in the extensions_list.

    Arguments:
    - dirname (str): git repository local absolute path.
    - extensions_list (list): list of strings of all extensions to consider.

    Returns:
    - (list of str): absolute paths of files to consider.
    """
    if dirname[-1] != '/':
        dirname += '/'

    list_of_files = [
        dirname + filename.split()[-1].strip()
        for filename in list(os.popen(f'git ls-tree -r HEAD {dirname}'))]

    files_to_read = []
    for ext in extensions_list:
        print(f"Checking extension: {ext}")
        files_with_ext = [
            filename for filename in list_of_files
            if filename.endswith(ext)]
        print(files_with_ext)
        files_to_read += files_with_ext

    return files_to_read


def removing_spaces(list_of_files):
    """
    For each file in list_of_files, it removes the trailing spaces,
    then it stages with git, and then commits all changes.

    Arguments:
    - list_of_files (list of str): file names to update.
    """

    for filename in list_of_files:
        commands = []
        commands.append(f"sed 's/[ \t]*$//' {filename} > {filename}_tmp")
        commands.append(f"mv {filename}_tmp {filename}")
        commands.append(f"git add {filename}")
        for cmd in commands:
            os.system(cmd)
    os.system("git commit -m 'remove trailing spaces'")


def main():
    """
    Takes as input a git repository path and a list of extensions
    for the files to consider. Then finds all such files in the repository,
    and then removes the trailing spaces from all of them, and
    """

    # reading terminal arguments:
    # repository path and list of extensions to consider.
    parser = argparse.ArgumentParser(
         description='')
    parser.add_argument(
        '--git_repo_root', '-r', type=str, default=None,
        help='absolute path of the repository root')
    parser.add_argument(
        '--extensions_list', '-e', type=list, default=['py'],
        help='list of extensions of files to modify')
    args = parser.parse_args()

    # terminating if no repo path provided
    if isinstance(args.git_repo_root, str) and os.path.isdir(args.git_repo_root):
        os.chdir(args.git_repo_root)
        print(f"LOG: Now working on {args.git_repo_root}.")
    else:
        print("Please provide a valid repository path")
        exit()

    # printing arguments for logs.
    print(f"LOG: repository root = {args.git_repo_root}")
    print(f"LOG: extensions = {args.extensions_list}")

    # test if the path is that of a git repository
    exit_code = os.system('git status')
    if exit_code != 0:
        print(
            f"{args.git_repo_root} is not "
            "the path of a git repository")
        exit()

    # listing files
    files_to_read = listing_files(
        args.git_repo_root,
        extensions_list=args.extensions_list)

    # terminating if there are no files as required.
    if len(files_to_read) == 0:
        print(
            "There are no files with "
            "the given extensions in this repository")
        exit()

    print(f"LOG: there are {len(files_to_read)} in this repository")

    # removing trailing spaces
    removing_spaces(files_to_read)

    print("Now push these changes.")


if __name__ == '__main__':
    main()
