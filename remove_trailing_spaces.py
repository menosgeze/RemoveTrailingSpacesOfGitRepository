import argparse
import os

source_dirname = os.path.abspath(os.path.dirname(__file__)) + '/'

def main():
    parser = argparse.ArgumentParser(
         description='')
    parser.add_argument(
        '--git_repo_root', '--rr', type=str, default=None,
        help='absolute path of the repository root')
    parser.add_argument(
        '--extensions_list', '--el', type=list, default = ['py'],
        help='list of extensions of files to modify')
    args = parser.parse_args()

    print(f"LOG: repository root = {args.git_repo_root}")
    print(f"LOG: extensions = {args.extensions_list}")



if __name__ == '__main__':
    main()


