#!/usr/bin/env python3

import argparse

from .lib import encrypt_file, decrypt_file, discover_files, get_blacklist


def get_args():
    parser = argparse.ArgumentParser(
        prog="plus1",
        description="A symmetric substitution cipher that adds/subtracts one to each unicode character in a file/directory.",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40),
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="encrypt/decrypt directories recursively",
        default=False,
    )
    parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        help="after encrypting/decrypting, delete the original file",
        default=False,
    )
    parser.add_argument(
        "-i",
        "--ignore-blacklist",
        action="store_true",
        help="ignore the extension blacklist and consider files that would have been ignored otherwise",
        default=False,
    )
    parser.add_argument(
        "--hidden-files",
        action="store_true",
        help="don't ignore hidden files",
        default=False,
    )
    parser.add_argument(
        "--hidden-directories",
        action="store_true",
        help="don't ignore hidden directories",
        default=False,
    )
    parser.add_argument(
        "--force-delete",
        action="store_true",
        help="don't ask for confirmation when removing files",
        default=False,
    )
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "-f", "--file", required=True, help="file or directory to encrypt/decrypt"
    )
    required_m_group = required.add_mutually_exclusive_group(required=True)
    required_m_group.add_argument(
        "-a",
        "--add",
        action="store_true",
        help="encrypt; add 1 to each unicode character",
    )
    required_m_group.add_argument(
        "-s",
        "--subtract",
        action="store_true",
        help="decrypt; subtract 1 from each unicode character",
    )
    return parser.parse_args()


def main():
    args = get_args()
    files = discover_files(
        [args.file],
        args.recursive,
        get_blacklist(),
        args.ignore_blacklist,
        args.hidden_files,
        args.hidden_directories,
    )
    for f in files:
        if args.add:
            encrypt_file(f, args.delete, args.force_delete)
        else:
            decrypt_file(f, args.delete, args.force_delete)


if __name__ == "__main__":
    main()
