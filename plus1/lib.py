import os
import sys
from pathlib import Path
from shutil import copyfile

from typing import List
from distutils.util import strtobool


def prompt(s) -> bool:
    """Infinite loop user prompt"""
    while True:
        resp = input(s)
        try:
            return strtobool(resp)
        except ValueError:
            print(strtobool.__doc__)


def encrypt_file(filepath: str, delete_opt: bool, force_opt: bool) -> None:
    print(f"Encrypting {filepath}...")
    name, extension = os.path.splitext(filepath)
    if name.endswith("[plus1]"):
        print(f"{filepath} is already encrypted", file=sys.stderr)
        return
    with open(filepath, encoding="utf-8") as f:
        contents = f.read()
    output_filepath = "{}[plus1]{}".format(name, extension)
    with open(output_filepath, "w", encoding="utf-8") as f:
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


def decrypt_file(filepath: str, delete_opt: bool, force_opt: bool) -> None:
    name_mismatch_confirmed = False
    print(f"Decrypting {filepath}...")
    name, extension = os.path.splitext(filepath)
    if not name.endswith("[plus1]"):
        if not prompt(
            "File does not match encrypted file name pattern. Decrypt anyways? "
        ):
            return
        else:
            name_mismatch_confirmed = True
    with open(filepath, encoding="utf-8") as f:
        contents = f.read()
    output_filepath = "{}{}".format(
        name[:-7] if name.endswith("[plus1]") else name, extension
    )
    with open(output_filepath, "w", encoding="utf-8") as f:
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
            print(
                "Encrypted and decrypted filepaths are the same, ignoring request to delete."
            )
        else:
            os.remove(filepath)


def get_blacklist() -> List[str]:
    """Initializes the blacklist.

    If it doesn't exist, copies the default to the users config directory
    """
    user_config_dir: str = os.environ.get(
        "XDG_CONFIG_HOME", os.path.join(Path.home(), ".config")
    )
    blacklist_location: str = os.path.join(user_config_dir, "plus1_blacklist.txt")
    if not os.path.exists(blacklist_location):
        default_blacklist_location: str = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "plus1_blacklist.txt.dist"
        )
        print("Copying default blacklist to {}".format(blacklist_location))
        copyfile(default_blacklist_location, blacklist_location)
    with open(blacklist_location, "r") as blacklist_f:
        return blacklist_f.read().splitlines()


def discover_files(
    filepaths: List[str],
    recursive_opt: bool,
    blacklist: List[str],
    ignore_ext_opt: bool,
    h_files_opt: bool,
    h_dir_opt: bool,
):
    """Make sure all files given exist, and discover any files in directories if we're discovering directories recursively."""
    discovered_files = set()
    i = 0
    while i < len(filepaths):
        f: str = os.path.abspath(filepaths[i])
        # exit if files given on command line don't exist
        if not os.path.exists(f):
            print(f"Unexpected error: No such file or directory {f}", file=sys.stderr)
            sys.exit(1)
        if os.path.isdir(f):
            if not recursive_opt:
                print(
                    f"You passed in a directory ({f}), without specifying a recursive search (-r). That doesn't make sense.",
                    file=sys.stderr,
                )
                sys.exit(1)
            else:
                # skip hidden directories
                if not h_dir_opt and os.path.split(f)[-1].startswith("."):
                    print(f"Skipping hidden directory: {f}")
                else:
                    dir_contents: List[str] = [
                        os.path.join(f, path) for path in os.listdir(f)
                    ]
                    filepaths.extend(dir_contents)
        else:  # if path is a file
            name, extension = os.path.splitext(f)
            if not ignore_ext_opt and extension in blacklist:
                print(f"Skipping file with blacklisted extension: {f}")
            elif not h_files_opt and os.path.split(f)[-1].startswith("."):
                print(f"Skipping hidden file: {f}")
            else:
                discovered_files.add(os.path.abspath(f))
        i += 1
    return list(discovered_files)
