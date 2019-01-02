#!/usr/bin/env python3

import os
import sys
import argparse
from distutils.util import strtobool

EXTENSION_BLACKLIST = set([".pyc"])

def get_args():
    parser = argparse.ArgumentParser(prog="python3 {}".format(sys.argv[0]), description="A symmetric substitution cipher that adds/subtracts one to each unicode character in a file/directory.")
    parser.add_argument('-r', '--recursive', action="store_true", help="encypt/decrpyt files recursively. required for folders", default=False)
    parser.add_argument('-d', "--delete", action="store_true", help="after encrypting/decrypting, delete the original file", default=False)
    required = parser.add_argument_group('required arguments')
    required.add_argument("-f", "--file", required=True, help="file or directory to encode/decode")
    required_m_group = required.add_mutually_exclusive_group(required=True)
    required_m_group.add_argument("-a", "--add", action="store_true", help="encypt; add 1 to each unicode character")
    required_m_group.add_argument("-s", "--subtract", action="store_true", help="decrypt; subtract 1 from each unicode character")
    return parser.parse_args()

def discover_files(filepaths, recursive_opt):
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
                print(f"You passed in a directory ({f}), without specifying a recursive search. That doesn't make sense.", file=sys.stderr)
                sys.exit(1)
            else:
                # skip hidden directories
                if os.path.split(f)[-1].startswith('.'):
                    print(f"Skipping hidden directory: {f}")
                else:
                    dir_contents = [os.path.join(f, path) for path in os.listdir(f)]
                    filepaths.extend(dir_contents)
        else: # if path is a file
            name, extension = os.path.splitext(f)
            if extension in EXTENSION_BLACKLIST:
                print(f"Skipping file with blacklisted extension: {f}")
            elif os.path.split(f)[-1].startswith('.'):
                print(f"Skipping hidden file: {f}")
            else:
                discovered_files.add(f)
        i += 1
    return list(discovered_files)

def prompt(s):
    resp = input(s)
    try:
        return strtobool(resp)
    except:
        print(strtobool.__doc__)

def encrypt_file(filepath, delete_opt):
    print(f"Encryting {filepath}...")
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
                ordinal = ordinal - 1 # ignore
            f.write(chr(ordinal+1))
    if delete_opt:
        os.remove(filepath)

def decrypt_file(filepath, delete_opt):
    print(f"Decrypting {filepath}...")
    name, extension = os.path.splitext(filepath)
    if not name.endswith('[plus1]'):
        choice = prompt("File does not match encrypted file name pattern. Decrypt anyways?")
        if not choice:
            return
    with open(filepath, encoding='utf-8') as f:
        contents = f.read()
    output_filepath = "{}{}".format(name[:-7] if name.endswith('[plus1]') else name, extension)
    with open(output_filepath, 'w', encoding='utf-8') as f:
        for c in contents:
            ordinal = ord(c)
            if ordinal == sys.maxunicode:
                ordinal = ordinal + 1 # ignore
            f.write(chr(ordinal-1))
    if delete_opt:
        os.remove(filepath)


def main():
    args = get_args()
    files = discover_files([args.file], args.recursive)
    for f in files:
        if args.add:
            encrypt_file(f, args.delete)
        else:
            decrypt_file(f, args.delete)


if __name__ == "__main__":
    main()