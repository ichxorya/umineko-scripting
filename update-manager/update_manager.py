from re import Match
import sys
import os
import json
import hashlib
import zlib
import struct
import re
import shutil
import subprocess
import time
from functools import cmp_to_key
from . import update_manager_utils as utils
from typing import Optional

"""
⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠛⠓⠒⠥⣄⠀⢈⣉⣷⣶⣦⣽⣶⣤⠔⠚⠋⠉⠉⠛⢿⡿⢴⣿⣲⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠉⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠉⠁⠈⠳⣦⡀⠀⢀⣠⡴⠞⠻⠿⠦⢤⣄⡀⠀⠀⠈⠉⠓⠶⣤⣀⡀⠈⢳⡄⠀⠈⢷⣵⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣁⣀⡤⠤⠦⣤⣄⣨⣿⣞⣉⣀⣀⣀⣀⣀⠀⠀⠀⠉⠙⠶⣄⠀⢦⣄⠈⠹⣶⣄⣬⣿⣄⠀⠈⣷⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡯⠖⠛⠉⢀⣴⠞⠛⠁⠀⠞⠋⠉⢻⣶⠤⣄⣀⡉⠉⠛⠒⠤⠄⠀⠈⠻⣦⡈⢳⡀⠹⠙⢷⣄⠉⠛⠲⣾⣸⣧⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠱⣽⣿⣿⣿⣿⣿⣿⡿⠟⠉⠀⠀⠀⣰⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄⠈⠙⠻⣷⡦⣤⣀⠀⠀⠀⠀⠈⠙⢦⣻⡆⠀⠀⠙⣷⡦⠠⢼⡈⠙⣿⣆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣽⣻⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠘⠁⢀⡴⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⠀⠀⠀⠈⠳⣌⠙⠿⣶⣄⠀⠀⠀⢈⣿⣿⡀⠀⠀⢸⣧⠀⢸⡇⠀⢸⡟⡄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠰⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⣰⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡇⠀⠀⠀⠀⠈⢷⣄⠈⠻⣷⣦⡴⠟⠁⠘⣧⠀⠀⣾⣿⣦⣼⣿⠀⠀⣷⣧⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢻⣻⠿⡿⠀⠀⠀⡀⠀⠀⠀⢀⣾⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠀⠀⠀⠀⠀⠘⣿⣆⠀⠊⢻⣄⠀⠀⠀⢹⣆⣼⣳⣿⡿⣄⠙⢷⡀⡿⡟⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⣴⠃⠀⠀⢀⣾⡟⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠘⣿⠀⠀⠀⠹⣦⠀⠀⣠⡟⣵⡟⣹⣿⠸⡄⢸⣿⣿⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠀⠀⢠⠏⠀⠀⠀⣼⣿⠃⠀⠀⠀⡟⠀⠀⠀⢸⠇⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⢠⡄⢹⡇⠀⠀⠀⢹⣧⠾⣫⡾⠋⣴⡟⣿⠀⠀⢀⣿⢳⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢹⠀⠀⢸⠀⠀⠀⢰⡟⣿⠀⠀⠀⣸⠃⠀⠀⠀⣾⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⣷⠈⣿⣤⡴⠖⣫⣵⡾⠏⢀⣴⣿⠃⣿⣇⣠⡞⠋⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡄⠀⣿⠀⠀⠀⢸⣇⣿⠀⠀⠀⣿⠀⠀⠀⠀⣧⠀⢸⠀⠀⠀⣿⣧⠀⠀⠀⠀⠀⣿⡀⣿⣷⣶⡿⠿⡫⠀⣠⣾⣿⢻⣆⣯⠹⣏⠀⣰⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣇⣀⣿⡀⠀⠀⣸⣇⣿⠀⠀⠀⣿⡆⣄⠀⠀⣿⡄⢸⡄⠀⠀⢹⣟⣇⠀⠀⠀⠀⢹⡇⡟⢹⣦⠖⠋⣠⡾⣫⡿⡇⢸⣿⣿⠀⣿⣰⣿⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣴⣿⣿⡏⠟⠛⠛⠻⠿⢦⣤⣼⡿⢷⣿⡤⣤⣿⣧⣘⣧⡀⣀⣬⣿⣿⠦⠤⣤⡤⠻⣧⡇⠀⢻⣴⠞⣫⣴⠟⠀⡇⣾⣿⠀⢠⣿⡽⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡃⣿⣧⣐⣢⣤⣤⣄⡀⠙⢾⡀⠀⠈⢧⣄⠛⠮⠿⠟⠛⠉⠉⠀⠀⠀⠀⠀⠙⠳⣟⠀⠀⢸⣧⣾⣿⡏⠀⢀⣷⣿⣇⣀⣼⣻⠃⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠹⣿⡀⣻⡇⠈⣽⣿⢦⡀⠛⡆⠀⠀⠈⠁⠀⠀⢀⣴⣾⣿⣿⣿⢿⡶⢶⣦⣈⠙⠆⠀⢸⡿⢻⣿⠃⠀⢸⣿⠏⠉⢹⣿⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣧⠀⠉⠉⠉⠉⠻⣿⡆⢷⠀⠀⠀⠀⠀⠠⢿⣋⣠⡿⠿⠿⣿⣇⣰⡿⠷⠆⠀⠀⢸⢁⣼⠿⠶⠶⣿⡏⣀⡴⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠄⠀⠀⠀⣠⠟⠳⣄⠀⠀⠀⣠⠄⢀⡤⠀⠀⠀⠀⠙⠛⠂⠀⠀⠀⢠⡏⣼⡟⠀⠀⠀⢸⣟⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⢾⠋⠁⠀⠀⠈⢣⡀⠜⠁⡰⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣾⡟⠀⠀⠀⠀⣸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⡄⠀⠀⠀⠈⣧⠀⠀⠀⢠⠔⠁⠀⠀⠀⠀⠀⠀⠀⠙⠢⢤⣄⠀⠀⠀⣾⣿⡟⠀⠀⠀⠀⣰⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣇⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⢞⣹⠉⡇⠀⠀⣯⣿⡿⠀⢀⣠⣾⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣾⣆⠀⠀⠀⠀⠈⢿⡒⣶⢶⣶⣶⠶⠶⠾⠛⠳⢷⡴⣿⠏⠀⠀⠀⠀⠹⡜⢷⢾⡿⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣦⡀⠀⠀⠀⠈⠻⣽⣆⠀⠀⠀⠀⠀⢀⣀⡼⠟⠁⠀⠀⠀⠀⢀⡼⣷⡜⣿⣳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣯⢮⣷⣄⠀⠀⠀⠀⠈⢭⣓⠒⠒⠒⠚⣉⡡⠒⠀⠀⠀⠀⢀⡴⠋⠀⣿⣧⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣜⣏⣿⣕⣦⡀⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀⢀⣠⠖⠋⠀⠐⢶⡿⠋⣿⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣖⠲⢾⣾⢸⠀⠙⠾⣗⣦⡀⠀⠀⠀⠀⠀⢀⣠⠶⠚⠉⠀⠀⠀⣠⡞⠉⢀⣾⡏⢞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⣃⠼⠏⠀⠀⠀⠀⠙⠺⣗⣶⣶⡖⠋⠉⠀⠀⠀⢀⣠⢴⠞⠉⣠⣴⣿⣿⣿⡼⡄⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⣤⣤⣴⣚⣿⣷⠻⣧⣄⣠⡤⡶⠾⠛⣙⣤⣴⣿⣿⣿⣿⣿⣿⡿⣝⣦⡀⠀⠀⢀⣠⣶⠿⠟⠛⠉⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣴⡯⠓⠋⠉⠀⠀⠀⠉⣻⣄⡁⠁⢁⣡⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠈⠑⢿⣶⣴⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⡿⠋⠁⠀⠀⠀⠀⣀⣤⠴⢶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⣁⠀⠀⠀⠀⢀⡼⠋⠀⠀⢀⣠⠤⠒⢶⡉⠉⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⢴⣛⣹⣿⠟⠀⠀⠀⣀⡠⠖⠋⠁⠀⠀⠀⠻⢿⣿⣿⣿⣿⣿⣿⣿⡿⠿⡟⣉⡡⠶⠋⠁⠀⠀⠀⢀⠞⠀⢀⡴⡞⢿⡈⠣⠀⢀⣀⡀⢀⣀⣀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⣪⣾⣿⣿⣋⡿⠀⠀⣠⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⢉⣡⠤⠖⠚⠉⠁⠀⠀⠀⠀⠀⠀⢠⡞⣀⣶⡏⢠⡇⢠⣼⡀⠀⣾⣿⣿⣼⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⢠⡇⢀⡾⠁⠀⠀⠠⢄⡀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡤⠟⢛⣿⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠊⡴⡏⢸⠁⠀⢡⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿

Umineko Project - Script Update Manager.
Encoding: UTF-8

-----
Development notes:
- Consider using Ruff as the linter and formatter, and PyreFly as the type checker.
- The docstring convention used here is based on Numpy-style, with few modifications to work with VS Code.
See the original docstring convention at https://numpydoc.readthedocs.io/en/latest/format.html.
-----
Copyright (c) 2011-2025 Umineko Project. All rights reserved.

This program and the accompanying materials
are licensed and made available under the terms and conditions of the BSD License
which accompanies this distribution.

The full text of the license may be found at
http://opensource.org/licenses/bsd-license.php

THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
"""

"""
Constants.
"""
LF = "\n"
CRLF = "\r\n"
DS = "/"  # DIRECTORY_SEPARATOR
TAB = "\t"
MAGIC = "ONS2"
VERSION = 110
MAX_IN = 0x10000000
UPDATE_MANAGER = True
PASSWORD = "035646750436634546568555050"
REPLACE_GRIM_WITH_LOCALIZE: list[str] = ["cn", "cht"]

exclude: list[str] = [
    ".DS_Store",
    "thumbs.db",
    "Thumbs.db",
    "umi_scr",
    "dlls",
    "onscripter-ru",
    "/en.txt",
    "/ru.txt",
    "/pt.txt",
    "/cn.txt",
    "/cht.txt",
    "/test.txt",
    "gmon.out",
    "head.png",
    "ons.cfg",
    "_shine.png",
    "shine.png",
    "script.file",
    "language_pt",
    "language_cn",
    "language_cht",
    "/en.file",
    "/ru.file",
    "/pt.file",
    "/pt.cfg",
    "/cn.file",
    "/cn.cfg",
    "/cht.file",
    "/cht.cfg",
    "/chiru.file",
    "/game.hash",
    "/default.cfg",
]

include: list[str] = []


def err(message: str) -> None:
    """Prints an error message and exits the program.

    Parameters
    ----------
    - message : str
        - The error message to print.
    """
    print(message)
    sys.exit(0)


def get_usage() -> str:
    """Returns the string that shows how to use the update manager.

    Returns
    -------
    - str
        - The usage string for the update manager.
    """
    return (
        "Usage options:\n"
        "\tpython update_manager.py hash directory hashfile\n"
        "\tpython update_manager.py adler directory hashfile\n"
        "\tpython update_manager.py size directory hashfile\n"
        "\tpython update_manager.py verify old_hash_file new_hashfile [update.file json/ini]\n"
        "\tpython update_manager.py dscript script_file scripting_folder locale\n"
        "\tpython update_manager.py script script_file new_script last_episode\n"
        "\tpython update_manager.py update update_file source_folder new_folder [archive_prefix]\n"
    )


def str_replace_first(
    search_for_this_string: str, replace_with_this_string: str, original_string: str
) -> str:
    """Replaces the first occurrence of search string with replace string.

    Parameters
    ----------
    - search_for_this_string : str
        - The substring to search for.
    - replace_with_this_string : str
        - The substring to replace the first occurrence with.
    - original_string : str
        - The original string to modify.

    Returns
    -------
    - str
        - The modified string with the first occurrence replaced.

    Notes
    -----
    - If the `search_for_this_string` is not found in `original_string`, the function will return the `original_string` unchanged.
    """
    # Split `original_string` into parts, using `search_for_this_string` as the delimiter.
    # The split should only turn `original_string` into two parts.
    parts: list[str] = original_string.split(search_for_this_string, 1)

    # If the split resulted in two parts, join them with `replace_with_this_string`.
    if len(parts) == 2:
        return replace_with_this_string.join(parts)
    # Else, if the split did not result in two parts, return the original string unchanged.
    else:
        return original_string


def str_nat_sort(str1: str, str2: str) -> int:
    """Returns a number indicating the order of two strings in natural sort order.

    Parameters
    ----------
    - str1 : str
        - The first string to compare.
    - str2 : str
        - The second string to compare.

    Returns
    -------
    - int
        - A negative number if `str1 < str2`, a positive number if `str1 > str2`, and 0 if they are equal.
    """
    # The function first checks if the first four characters of both strings are equal.
    substr1: str = str1[:4]
    substr2: str = str2[:4]
    if substr1 == substr2:
        # If there is "op" in `substr1`, it is considered that `str1 < str2`.
        if "op" in substr1:
            return -1
        # Else, if there is "op" in `substr2`, it is considered that `str1 > str2`.
        elif "op" in substr2:
            return 1
        # Else, if both strings are equal, it is considered that `str1 == str2`.
        elif str1 == str2:
            return 0

    # Initialize the natural keys for both strings.
    key1: list[int | str] = utils.natural_key(str1)
    key2: list[int | str] = utils.natural_key(str2)

    # Compare the natural keys (performs a natural sort comparison).
    return (key1 > key2) - (key1 < key2)


def generate_guid() -> str:
    """Generates a GUID (Globally Unique Identifier) as a hexadecimal string.

    Returns
    -------
    - str
        - A hexadecimal string representation of the GUID, padded to 32 characters with leading zeros.
    """
    # Try using the operating system's random number generator to create 16 random bytes, then extract the GUID from it.
    try:
        random_bytes: bytes = os.urandom(16)
        return utils.extract_guid(random_bytes)
    # If that fails (which is kind of 0.000000000001% likely, shout out to Bernkastel if this happens), fall back to using the default value.
    except Exception:
        return "ea5078d1f71c405887bd54994bfeff24"


def inplace_lines(
    data_dir: str, in_dir: str, by_dir: str, replace_grim: bool = False
) -> str:
    # Initialize a buffer to store the processed lines.
    buffer = ""

    # Initialize the `tmp_guid` variable as a temporary GUID.
    tmp_guid: str = generate_guid()

    # Check if the provided directories exist.
    # If not, print an error message and exit.
    if (
        not os.path.exists(data_dir)
        or not os.path.exists(in_dir)
        or not os.path.exists(by_dir)
    ):
        err("At least one of the directories does not exist.")

    # Initialize the `scripts_in` list with all `.txt` files in the `in_dir`.
    # Then, sort it.
    scripts_in: list[str] = utils.get_txt_files_from_a_directory(in_dir)
    scripts_in.sort()

    # Initialize the `scripts_by` list with all `.txt` files in the `by_dir`.
    # Then, sort it.
    scripts_by: list[str] = utils.get_txt_files_from_a_directory(by_dir)
    scripts_by.sort()

    # Compare the lengths of `scripts_in` and `scripts_by`.
    # If they are not equal, print an error message and exit.
    if len(scripts_in) != len(scripts_by):
        err(
            "The number of input scripts does not match the number of scripts to replace."
        )

    # Initialize the `scripts` dictionary to map `scripts_in` values as the keys, to `scripts_by` values as the values.
    scripts: dict[str, str] = {
        in_file: by_file for in_file, by_file in zip(scripts_in, scripts_by)
    }

    # For each pair of key-value in the `scripts` dictionary, process as below.
    for in_file, by_file in scripts.items():
        # Initialize the variables to store the paths to the "in", "by", and "data" files.
        data_in_path: str = os.path.join(in_dir, in_file)
        data_by_path: str = os.path.join(by_dir, by_file)
        text_path: str = os.path.join(data_dir, in_file)

        # Try to open the "text" file in the `data_dir` and read its content.
        try:
            with open(text_path, "r", encoding="utf-8") as f:
                text: str = f.read().strip()
        except Exception:
            err(f"Failed to read the file: {text_path}")
        
        # If `replace_grim` is True, call the `remove_grim` function to process the text.
        if replace_grim:
            text = utils.remove_grim(text)

        # Try to open the "in" file and the "by" file, and read their content.
        try:
            with open(data_in_path, "r", encoding="utf-8") as f:
                data_in_content: str = f.read().strip()
        except Exception:
            err(f"Failed to read the file: {data_in_path}")
        try:
            with open(data_by_path, "r", encoding="utf-8") as f:
                data_by_content: str = f.read().strip()
        except Exception:
            err(f"Failed to read the file: {data_by_path}")

        # If both `data_in_content` and `data_by_content` are not empty, process the lines.
        if data_in_content and data_by_content and text:
            # Initialize the `data_in_lines` and `data_by_lines` lists by splitting the content of the "in" and "by" files by line breaks.
            data_in_lines: list[str] = data_in_content.split(LF)
            data_by_lines: list[str] = data_by_content.split(LF)

            # Iterate over the indices of `data_in_lines`.
            for i in range(len(data_in_lines)):
                # Check if the index `i` is out of bounds for either `data_in_lines` or `data_by_lines`.
                if i >= len(data_in_lines) or not data_in_lines[i]:
                    # If it is, print a warning message and continue to the next iteration.
                    print(f'Missing data_in of {i} in {in_file} for {data_by_lines[i] if i < len(data_by_lines) else "?"}')
                    continue
                # Check if the index `i` is out of bounds for `data_by_lines`.
                if i >= len(data_by_lines) or not data_by_lines[i]:
                    # If it is, print a warning message and continue to the next iteration.
                    print(f'Missing data_by of {i} in {by_file} for {data_in_lines[i] if i < len(data_in_lines) else "?"}')
                    continue
                
                # Initialize the `data_in_line` and `data_by_line` variables as the stripped lines from `data_in_lines` and `data_by_lines` at index `i`.
                # This removes any leading or trailing whitespace characters from the lines.
                data_in_line: str = data_in_lines[i].strip()
                data_by_line: str = data_by_lines[i].strip()

                # If `replace_grim` is True...
                if replace_grim:
                    # Search for a match in `data_by_line` that follows the pattern `[gstg <number>]`.
                    match: Match[str] | None = re.search(r'\[gstg \d+\]', data_by_line)
                    # If a match is found, store it in `line_grim`, otherwise set `line_grim` to None.
                    line_grim: str | None = match.group(0) if match else None
                    # Remove the `[gstg <number>]` pattern from `data_by_line`.
                    data_by_line = re.sub(r'\[gstg \d+\]', '', data_by_line)
                
                # Add `temp_guid` to the `data_by_line` string, then wrap it in backticks if it hadn't been wrapped already.
                data_by_line = '`' + tmp_guid + data_by_line.lstrip('`')

                if not data_by_line.endswith('`'):
                    data_by_line += '`'
                
                # If `replace_grim` and `line_grim` are not empty, append `line_grim` to `data_by_line`.
                if replace_grim and line_grim:
                    data_by_line += line_grim

                # Replace the first occurrence of `data_in_line` in `text` with `data_by_line`.
                text = str_replace_first(data_in_line, data_by_line, text)
    
        # After processing all lines, remove the `tmp_guid` from `text`.
        text = text.replace(tmp_guid, "")

        # Append the processed text to the `buffer` with a line break.
        buffer += text + LF
    
    # Return the final `buffer` containing all processed lines.
    return buffer

def hash_dir(directory, base, hash_map, hash_type):
    """Recursively hash files in directory."""
    if not os.path.isdir(directory):
        err(f"No such directory {directory}")

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            hash_dir(item_path, base, hash_map, hash_type)
        else:
            relative_path = os.path.relpath(item_path, base).replace("\\", "/")

            if hash_type == "adler":
                with open(item_path, "rb") as f:
                    content = f.read()
                hash_value = format(zlib.adler32(content) & 0xFFFFFFFF, "08x")
            elif hash_type == "size":
                hash_value = os.path.getsize(item_path)
            else:  # md5
                hash_value = hashlib.md5()
                with open(item_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_value.update(chunk)
                hash_value = hash_value.hexdigest()

            hash_map["/" + relative_path] = hash_value


def has_in(haystack, needle):
    """Check if haystack contains any of the needle strings."""
    if not isinstance(needle, list):
        needle = [needle]

    for query in needle:
        if query in haystack:
            return True
    return False


def filtered_ini_create(hashes, mode):
    """Create filtered INI output."""
    output = "[info]" + CRLF
    output += '"game"="UminekoPS3fication*"' + CRLF
    output += f'"hash"="{mode}"' + CRLF
    output += '"ver"="20190109-ru"' + CRLF
    output += '"apiver"="2.2.0"' + CRLF
    output += '"date"="ignore"' + CRLF
    output += "[data]" + CRLF

    for file_path, hash_value in hashes.items():
        if not has_in(file_path, exclude) and "game.hash" not in file_path:
            if file_path.startswith("/"):
                file_path = file_path[1:]
            output += f'"{file_path}"="{hash_value}"' + CRLF

    return output


def compare_hashes(old_hashes, new_hashes):
    """Compare two hash dictionaries and return differences."""
    out = {"different": {}, "delete": [], "insert": {}}

    for old_file, old_hash in old_hashes.items():
        # Avoid any temporary files
        if has_in(old_file, exclude) and old_file in new_hashes:
            del new_hashes[old_file]

        force_include: bool = has_in(old_file, include)

        if old_file in new_hashes or force_include:
            # Has change
            if new_hashes.get(old_file) != old_hash or force_include:
                clean_file = re.sub(r"^[/\\]", "", old_file)
                out["different"][clean_file] = new_hashes.get(old_file, old_hash)
            if old_file in new_hashes:
                del new_hashes[old_file]
        else:
            # Redundant file
            clean_file = re.sub(r"^[/\\]", "", old_file)
            out["delete"].append(clean_file)

    # Process remaining new files
    for new_file, new_hash in list(new_hashes.items()):
        if not has_in(new_file, exclude):
            clean_file = re.sub(r"^[/\\]", "", new_file)
            out["insert"][clean_file] = new_hash

    return out


def generate_incomplete(ep):
    """Generate incomplete episode script."""
    num = {1: 17, 2: 18, 3: 18, 4: 19, 5: 15, 6: 18, 7: 18, 8: 16}

    out = ""

    for i in range(ep, 9):
        out += f"*umi{i}_op{CRLF}jskip_s goto *incomplete ~{CRLF}"
        for j in range(1, num[i] + 1):
            out += f"*umi{i}_{j}{CRLF}jskip_s goto *incomplete ~{CRLF}"
        out += f"*umi{i}_end{CRLF}*teatime_{i}{CRLF}jskip_s goto *incomplete ~{CRLF}*teatime_{i}_end{CRLF}*ura_teatime_{i}{CRLF}jskip_s goto *incomplete ~{CRLF}*ura_{i}_end{CRLF}"

    return out


def filter_script(script, ep):
    """Filter script based on episode number."""
    if not ep.isdigit() or int(ep) < 1:
        err("Invalid episode number")

    ep = int(ep)
    incomplete = generate_incomplete(ep + 1)

    start_pattern = f"*umi{ep + 1}_op"
    start = script.find(start_pattern)

    if start != -1:
        end_pattern1 = "ura_8_end\ngoto *end_game"
        end_pattern2 = "ura_8_end\r\ngoto *end_game"

        end = script.find(end_pattern1, start)
        if end == -1:
            end = script.find(end_pattern2, start)
            end_len = len(end_pattern2)
        else:
            end_len = len(end_pattern1)

        if end != -1:
            script = script[:start] + incomplete + script[end + end_len :]

    script = script.replace(".txt", ".file")
    return script


def localise_script(script, locale_dir):
    """Localise script by importing locale files."""
    lstart = '#locale_import "'
    lend = '"'

    while True:
        start = script.find(lstart)
        if start == -1:
            break

        end = script.find(lend, start + len(lstart))
        if end == -1:
            break

        file_name = script[start + len(lstart) : end]

        if not re.match(r"^[a-z0-9_]+\.txt$", file_name, re.IGNORECASE):
            break

        try:
            with open(os.path.join(locale_dir, file_name), "r", encoding="utf-8") as f:
                dst = f.read().replace(CRLF, LF)
            script = script[:start] + dst + script[end + len(lend) :]
        except:
            break

    return script


def xor_data(data, pass_num):
    """XOR data with key table."""
    key_table = [
        0xC0,
        0xBC,
        0x86,
        0x66,
        0x84,
        0xF3,
        0xBE,
        0x90,
        0xB0,
        0x02,
        0x98,
        0x5E,
        0x0F,
        0x9C,
        0x7B,
        0xF4,
        0xD9,
        0x91,
        0xDB,
        0xEB,
        0x81,
        0x74,
        0x3A,
        0xE3,
        0x76,
        0x94,
        0x21,
        0x93,
        0x63,
        0x68,
        0x0D,
        0xA1,
        0xBA,
        0xAA,
        0x1B,
        0xA0,
        0x49,
        0x2B,
        0xE1,
        0xE7,
        0x38,
        0xA6,
        0x25,
        0x53,
        0x40,
        0x4A,
        0xEC,
        0x29,
        0x36,
        0xBF,
        0xF2,
        0x9F,
        0xAC,
        0x0C,
        0xCB,
        0x00,
        0x1F,
        0xF1,
        0x7C,
        0x80,
        0x4F,
        0x60,
        0x82,
        0x62,
        0x14,
        0x6D,
        0xD8,
        0x32,
        0x13,
        0x2F,
        0xE0,
        0x99,
        0xF7,
        0x10,
        0xD1,
        0x30,
        0x64,
        0x4E,
        0x8C,
        0xDE,
        0xC1,
        0x6A,
        0xAD,
        0xA7,
        0xB5,
        0x95,
        0xCF,
        0xC6,
        0x0B,
        0x2D,
        0x69,
        0x24,
        0x5C,
        0xC5,
        0x03,
        0xDA,
        0xD6,
        0x8E,
        0xA3,
        0x88,
        0x31,
        0x17,
        0x3C,
        0xB3,
        0xA8,
        0xB4,
        0x01,
        0x0E,
        0xFC,
        0x37,
        0x65,
        0x16,
        0x6C,
        0xBB,
        0x50,
        0x55,
        0x2A,
        0xE5,
        0x77,
        0x97,
        0x09,
        0xB1,
        0x04,
        0x67,
        0xC7,
        0x79,
        0x71,
        0x7A,
        0x43,
        0xD0,
        0x22,
        0x58,
        0x0A,
        0x57,
        0xB7,
        0xAE,
        0x4D,
        0xC8,
        0xE9,
        0x46,
        0xD3,
        0x5B,
        0x96,
        0xCC,
        0x3F,
        0xE6,
        0x3E,
        0x54,
        0x5F,
        0x1D,
        0xFA,
        0xF0,
        0x3D,
        0x7D,
        0x83,
        0xA5,
        0xFD,
        0xEF,
        0x15,
        0x8B,
        0x70,
        0x6B,
        0xE2,
        0xFF,
        0x07,
        0xD7,
        0x92,
        0x41,
        0x61,
        0x75,
        0x6F,
        0x7F,
        0xC4,
        0xD5,
        0xF9,
        0x05,
        0x34,
        0xFE,
        0x5D,
        0xDC,
        0xB9,
        0xE8,
        0xAB,
        0xCA,
        0xC3,
        0x35,
        0x08,
        0x3B,
        0xA2,
        0xBD,
        0x8F,
        0x7E,
        0x2E,
        0x44,
        0x5A,
        0x12,
        0xED,
        0xE4,
        0x11,
        0x1E,
        0xC2,
        0x78,
        0xF5,
        0xAF,
        0xF6,
        0x72,
        0x28,
        0x9D,
        0x6E,
        0x39,
        0xD2,
        0xEA,
        0x45,
        0x73,
        0x47,
        0x9E,
        0x26,
        0x89,
        0x85,
        0x52,
        0x33,
        0xDF,
        0xA4,
        0x48,
        0x23,
        0xCE,
        0x1C,
        0x8D,
        0x18,
        0x27,
        0x9A,
        0xB6,
        0xA9,
        0xEE,
        0xB8,
        0xC9,
        0x2C,
        0xFB,
        0x59,
        0x56,
        0x20,
        0x42,
        0xCD,
        0x51,
        0xB2,
        0x06,
        0x19,
        0x4B,
        0x9B,
        0xD4,
        0x8A,
        0x4C,
        0xF8,
        0x87,
        0x1A,
        0xDD,
    ]

    if not data:
        err("Nothing to xor")

    result = bytearray()
    for byte in data:
        c = byte

        if pass_num != 2:
            c = key_table[c ^ 0x71] ^ 0x45
        else:
            c = key_table[c ^ 0x23] ^ 0x86

        result.append(c)

    return bytes(result)


def transform_script(data):
    """Transform script data."""
    if isinstance(data, str):
        data = data.encode("utf-8")

    # First pass
    result = b""
    chunk_size = 131072
    for i in range(0, len(data), chunk_size):
        chunk = data[i : i + chunk_size]
        result += xor_data(chunk, 1)

    # Compress
    compressed = zlib.compress(result, 9)

    # Second pass
    result = b""
    for i in range(0, len(compressed), chunk_size):
        chunk = compressed[i : i + chunk_size]
        result += xor_data(chunk, 2)

    return result


def encode_script(data):
    """Encode script with header."""
    if isinstance(data, str):
        data = data.encode("utf-8")

    out_size = len(data)
    transformed_data = transform_script(data)

    # Create header
    header = MAGIC.encode("ascii")
    header += struct.pack("<LLL", len(transformed_data), out_size, VERSION)

    return header + transformed_data


def remove_grim(text):
    """Remove grim formatting from text."""
    # Remove color formatting
    text = re.sub(r"\{c:86EF9C:(.*?)\}", r"\1", text)
    # Remove gstg tags
    text = re.sub(r"\[gstg \d+\]", "", text)
    return text


def main():
    """Main function."""
    argc = len(sys.argv)
    argv = sys.argv

    if argc < 2:
        err(get_usage())

    command = argv[1]

    if command in ["hash", "adler", "size"]:
        if argc < 4:
            err(get_usage())

        hashes = {}
        hash_dir(argv[2], argv[2], hashes, command)

        if command == "hash":
            output = json.dumps(hashes, indent=2)
        else:
            output = filtered_ini_create(hashes, command)

        with open(argv[3], "w", encoding="utf-8") as f:
            f.write(output)

    elif command == "verify":
        if argc < 4:
            err(get_usage())

        if not os.path.exists(argv[2]):
            err(f"No such file {argv[2]}")
        if not os.path.exists(argv[3]):
            err(f"No such file {argv[3]}")

        with open(argv[2], "r", encoding="utf-8") as f:
            old_hashes = json.load(f)
        with open(argv[3], "r", encoding="utf-8") as f:
            new_hashes = json.load(f)

        modifications = compare_hashes(old_hashes, new_hashes)

        fixture = ""
        for sect, content in modifications.items():
            fixture += CRLF + f"[{sect}]" + CRLF
            for key, value in content.items():
                if isinstance(key, int) or key.isdigit():
                    fixture += f'"{value}"="DO"' + CRLF
                else:
                    fixture += f'"{key}"="{value}"' + CRLF

        fixture += (
            CRLF
            + "[update]"
            + CRLF
            + f'"hash"="{hashlib.md5(fixture.encode()).hexdigest()}"'
            + CRLF
            + CRLF
        )

        if argc > 5:
            output = (
                json.dumps(modifications)
                if len(argv) > 5 and argv[5] == "json"
                else fixture
            )
            with open(argv[4], "w", encoding="utf-8") as f:
                f.write(output)
        else:
            print(fixture)

    elif command == "dscript":
        if argc < 5:
            err(get_usage())

        ver = "8.3b" + (f" r{argv[5]}" if argc > 5 else "")
        locale = argv[4]
        gameid = f"UminekoPS3fication{locale.capitalize()}"
        scripting = argv[3]

        # Read header
        with open(
            os.path.join(scripting, "script", "umi_hdr.txt"), "r", encoding="utf-8"
        ) as f:
            script = f.read() + LF

        script = script.replace(CRLF, LF)
        script = script.replace("builder_id", gameid)
        script = script.replace("builder_date", str(int(time.time())))
        script = script.replace("builder_localisation", locale)
        script = script.replace("builder_version", ver)

        # Process episodes 1-8
        for i in range(1, 9):
            tldir = os.path.join(scripting, "story", f"ep{i}", locale)
            if not os.path.isdir(tldir):
                tldir = os.path.join(scripting, "story", f"ep{i}", "en")

            script += inplace_lines(
                os.path.join(scripting, "game", "main"),
                os.path.join(scripting, "story", f"ep{i}", "jp"),
                tldir,
                locale in REPLACE_GRIM_WITH_LOCALIZE,
            )

        # Process omake
        script += inplace_lines(
            os.path.join(scripting, "game", "omake"),
            os.path.join(scripting, "story", "omake", "jp"),
            os.path.join(scripting, "story", "omake", locale),
        )

        # Read footer
        footer_path = os.path.join(scripting, "script", "umi_ftr.txt")
        if locale == "cn":
            footer_path = os.path.join(scripting, "script", "cn", "umi_ftr.txt")
        elif locale == "cht":
            footer_path = os.path.join(scripting, "script", "cht", "umi_ftr.txt")
        elif locale == "tr":
            footer_path = os.path.join(scripting, "script", "tr", "umi_ftr.txt")

        with open(footer_path, "r", encoding="utf-8") as f:
            footer = f.read()

        script += footer.replace(CRLF, LF)

        # Localise script
        script = localise_script(script, os.path.join(scripting, "script", locale))

        with open(argv[2], "w", encoding="utf-8") as f:
            f.write(script)

    elif command == "script":
        if argc < 5:
            err(get_usage())

        if not os.path.exists(argv[2]):
            err(f"No such file {argv[2]}")

        with open(argv[2], "r", encoding="utf-8") as f:
            script = f.read()

        script = filter_script(script, argv[4])
        encoded = encode_script(script)

        with open(argv[3], "wb") as f:
            f.write(encoded)

    elif command == "update":
        if argc < 5:
            err(get_usage())

        with open(argv[2], "r", encoding="utf-8") as f:
            update = json.load(f)

        if not os.path.isdir(argv[3]):
            err(f"No source dir {argv[3]}")

        if not os.path.isdir(argv[4]):
            os.makedirs(argv[4], 0o755, exist_ok=True)

        for sect, content in update.items():
            if sect not in ["insert", "different"]:
                continue

            for file_path, file_hash in content.items():
                dir_path = os.path.join(argv[4], os.path.dirname(file_path))
                if not os.path.isdir(dir_path):
                    os.makedirs(dir_path, 0o755, exist_ok=True)
                shutil.copy2(
                    os.path.join(argv[3], file_path), os.path.join(argv[4], file_path)
                )

        if argc > 5:
            import datetime

            archive = f"{argv[5]}_{datetime.datetime.now().strftime('%d.%m.%y')}.7z"
            folder = os.path.join(argv[4], "*")

            cmd = [
                "7z",
                "a",
                archive,
                "-t7z",
                "-m0=lzma2",
                "-mx=9",
                "-mfb=64",
                "-md=128m",
                "-ms=on",
                "-mhe",
                "-v1023m",
                f"-p{PASSWORD}",
                folder,
            ]
            subprocess.run(cmd)
            shutil.rmtree(argv[4])

    else:
        err(get_usage())


if __name__ == "__main__":
    main()
