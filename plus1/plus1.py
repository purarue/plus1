#!/usr/bin/env python3

from plus1 import *


def get_args():
    parser = argparse.ArgumentParser(prog="plus1",
                                     description="A symmetric substitution cipher that adds/subtracts one to each unicode character in a file/directory.",
                                     formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40)
                                     )
    parser.add_argument('-r', '--recursive', action="store_true", help="encrypt/decrypt directories recursively", default=False)
    parser.add_argument('-d', "--delete", action="store_true", help="after encrypting/decrypting, delete the original file", default=False)
    parser.add_argument('-i', "--ignore-blacklist", action="store_true", help="ignore the extension blacklist and consider files that would have been ignored otherwise", default=False)
    parser.add_argument("--hidden-files", action="store_true", help="don't ignore hidden files", default=False)
    parser.add_argument("--hidden-directories", action="store_true", help="don't ignore hidden directories", default=False)
    parser.add_argument("--force-delete", action="store_true", help="don't ask for confirmation when removing files", default=False)
    required = parser.add_argument_group('required arguments')
    required.add_argument("-f", "--file", required=True, help="file or directory to encrypt/decrypt")
    required_m_group = required.add_mutually_exclusive_group(required=True)
    required_m_group.add_argument("-a", "--add", action="store_true", help="encrypt; add 1 to each unicode character")
    required_m_group.add_argument("-s", "--subtract", action="store_true", help="decrypt; subtract 1 from each unicode character")
    return parser.parse_args()


def get_blacklist():
    """Initializes the blacklist.

    If it doesn't exist, copies the default to the users home directory
    """
    blacklist_location = os.path.join(Path.home(), ".plus1_blacklist.txt")
    if not os.path.exists(blacklist_location):
        default_blacklist_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plus1_blacklist.txt.dist")
        print("Copying default blacklist to {}".format(blacklist_location))
        copyfile(default_blacklist_location, blacklist_location)
    with open(blacklist_location, 'r') as blacklist_f:
        return blacklist_f.read().splitlines()


def discover_files(filepaths, recursive_opt, blacklist, ignore_ext_opt, h_files_opt, h_dir_opt):
    """Make sure all files given exist, and discover any files in directories if we're discovering directories recursively."""
    discovered_files = set()
    i = 0
    while i < len(filepaths):
        f = os.path.abspath(filepaths[i])
        # exit if files given on command line don't exist
        if not os.path.exists(f):
            print(f"Unexpected error: No such file or directory {f}", file=sys.stderr)
            sys.exit(1)
        if os.path.isdir(f):
            if not recursive_opt:
                print(f"You passed in a directory ({f}), without specifying a recursive search (-r). That doesn't make sense.", file=sys.stderr)
                sys.exit(1)
            else:
                # skip hidden directories
                if not h_dir_opt and os.path.split(f)[-1].startswith('.'):
                    print(f"Skipping hidden directory: {f}")
                else:
                    dir_contents = [os.path.join(f, path) for path in os.listdir(f)]
                    filepaths.extend(dir_contents)
        else:  # if path is a file
            name, extension = os.path.splitext(f)
            if not ignore_ext_opt and extension in blacklist:
                print(f"Skipping file with blacklisted extension: {f}")
            elif not h_files_opt and os.path.split(f)[-1].startswith('.'):
                print(f"Skipping hidden file: {f}")
            else:
                discovered_files.add(os.path.abspath(f))
        i += 1
    return list(discovered_files)


def prompt(s):
    """Infinite loop user prompt"""
    while True:
        resp = input(s)
        try:
            return strtobool(resp)
        except:
            print(strtobool.__doc__)


def encrypt_file(filepath, delete_opt, force_opt):
    print(f"Encrypting {filepath}...")
    name, extension = os.path.splitext(filepath)
    if name.endswith('[plus1]'):
        print(f'{filepath} is already encrypted', file=sys.stderr)
        return
    with open(filepath, encoding='utf-8') as f:
        contents = f.read()
    output_filepath = "{}[plus1]{}".format(name, extension)
    with open(output_filepath, 'w', encoding='utf-8') as f:
        for c in contents:
            ordinal = ord(c)
            if ordinal == sys.maxunicode:
                ordinal = 0  # 'wrap around' to 0
            else:
                ordinal += 1
            f.write(chr(ordinal))
    if delete_opt:
        # if --force wasn't present and the user says no
        if not force_opt and not prompt("Remove '{}'? ".format(filepath)):
            return
        os.remove(filepath)


def decrypt_file(filepath, delete_opt, force_opt):
    name_mismatch_confirmed = False
    print(f"Decrypting {filepath}...")
    name, extension = os.path.splitext(filepath)
    if not name.endswith('[plus1]'):
        if not prompt("File does not match encrypted file name pattern. Decrypt anyways? "):
            return
        else:
            name_mismatch_confirmed = True
    with open(filepath, encoding='utf-8') as f:
        contents = f.read()
    output_filepath = "{}{}".format(name[:-7] if name.endswith('[plus1]') else name, extension)
    with open(output_filepath, 'w', encoding='utf-8') as f:
        for c in contents:
            ordinal = ord(c)
            if ordinal == 0:
                ordinal = sys.maxunicode  # 'wrap around' to sys.unicode
            else:
                ordinal -= 1
            f.write(chr(ordinal))
    if delete_opt:
        if not force_opt and not prompt("Remove '{}'? ".format(filepath)):
            return
        # if user confirmed that a file was being decrypted that didn't match
        # the file pattern, but still wanted to delete the file, we shouldn't
        # let them since the encrypted and decrypted filepath are the same
        if name_mismatch_confirmed:
            print("Encrypted and decrypted filepaths are the same, ignoring request to delete.")
        else:
            os.remove(filepath)


def main():
    args = get_args()
    files = discover_files([args.file], args.recursive, get_blacklist(),
                           args.ignore_blacklist, args.hidden_files,
                           args.hidden_directories)
    for f in files:
        if args.add:
            encrypt_file(f, args.delete, args.force_delete)
        else:
            decrypt_file(f, args.delete, args.force_delete)
