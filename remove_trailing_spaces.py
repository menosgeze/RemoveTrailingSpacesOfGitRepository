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

    # reading terminal arguments: repository path and list of extensions to consider.
    parser = argparse.ArgumentParser(
         description='')
    parser.add_argument(
        '--git_repo_root', '--rr', type=str, default=None,
        help='absolute path of the repository root')
    parser.add_argument(
        '--extensions_list', '--el', type=list, default = ['py'],
        help='list of extensions of files to modify')
    args = parser.parse_args()

    if args.git_repo_root is None:
        print("Please provide a valid repository path")

    # printing arguments for logs.
    print(f"LOG: repository root = {args.git_repo_root}")
    print(f"LOG: extensions = {args.extensions_list}")

    # listing files
    files_to_read = listing_files(
        args.git_repo_root,
        extensions_list=args.extensions_list)

    print(f"LOG: there are {len(files_to_read)} in this repository")
    print(f"     e.g. ?{files_to_read[0]}?")

    if len(files_to_read) == 0:
        print(
            f"There are no files with "
            "the given extensions in this repository")
        exit()

    # removing trailing spaces
    removing_spaces(files_to_read)

    print("Now push these changes.")

if __name__ == '__main__':
    main()
