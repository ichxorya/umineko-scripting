from _hashlib import HASH
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
import update_manager_utils as utils

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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠀⠀⢠⠏⠀⠀⠀⣼⣿⠃⠀⠀⠀⡟⠀⠀⠀⢸⠇⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⢠⡄⢹⡇⠀⠀⠀⢹⣧⠾⣫⡾⠋⣴⡟⣿⠀⠀⢀⣿⢳    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢹⠀⠀⢸⠀⠀⠀⢰⡟⣿⠀⠀⠀⣸⠃⠀⠀⠀⣾⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⣷⠈⣿⣤⡴⠖⣫⣵⡾⠏⢀⣴⣿⠃⣿⣇⣠⡞⠋⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡄⠀⣿⠀⠀⠀⢸⣇⣿⠀⠀⠀⣿⠀⠀⠀⠀⣧⠀⢸⠀⠀⠀⣿⣧⠀⠀⠀⠀⠀⣿⡀⣿⣷⣶⡿⠿⡫⠀⣠⣾⣿⢻⣆⣯⠹⣏⠀⣰⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣇⣀⣿⡀⠀⠀⣸⣇⣿⠀⠀⠀⣿⡆⣄⠀⠀⣿⡄⢸⡄⠀⠀⢹⣟⣇⠀⠀⠀⠀⢹⡇⡟⢹⣦⠖⠋⣠⡾⣫⡿⡇⢸⣿⣿⠀⣿⣰⣿⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣴⣿⣿⡏⠟⠛⠛⠻⠿⢦⣤⣼⡿⢷⣿⡤⣤⣿⣧⣘⣧⡀⣀⣬⣿⣿⠦⠤⣤⡤⠻⣧⡇⠀⢻⣴⠞⣫⣴⠟⠀⡇⣾⣿⠀⢠⣿⡽⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡃⣿⣧⣐⣢⣤⣤⣄⡀⠙⢾⡀⠀⠈⢧⣄⠛⠮⠿⠟⠛⠉⠉⠀⠀⠀⠀⠀⠙⠳⣟⠀⠀⢸⣧⣾⣿⡏⠀⢀⣷⣿⣇⣀⣼⣻⠃⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠹⣿⡀⣻⡇⠈⣽⣿⢦⡀⠛⡆⠀⠀⠈⠁⠀⠀⢀⣴⣾⣿⣿⣿⢿⡶⢶⣦⣈⠙⠆⠀⢸⡿⢻⣿⠃⠀⢸⣿⠏⠉⢹⣿⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣧⠀⠉⠉⠉⠉⠻⣿⡆⢷⠀⠀⠀⠀⠀⠠⢿⣋⣠⡿⠿⠿⣿⣇⣰⡿⠷⠆⠀⠀⢸⢁⣼⠿⠶⠶⣿⡏⣀⡴⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⣠⠟⠳⣄⠀⠀⠀⣠⠄⢀⡤⠀⠀⠀⠀⠙⠛⠂⠀⠀⠀⢠⡏⣼⡟⠀⠀⠀⢸⣟⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
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
    """Processes script lines in place by replacing content based on mapping files.

    Parameters
    ----------
    - data_dir : str
        - TODO: Figure out what this is for.
    - in_dir : str
        - TODO: Figure out what this is for.
    - by_dir : str
        - TODO: Figure out what this is for.
    - replace_grim : bool, optional
        - Whether to apply some specific replacements, by default it is set to `False`.

    Returns
    -------
    - str
        - The combined processed content from all script files.
    """
    buffer: str = ""
    tmp_guid: str = generate_guid()

    # Validate that the directories must exist.
    utils.validate_script_directories(data_dir, in_dir, by_dir)

    # Get and validate script file mappings.
    scripts: dict[str, str] = utils.get_and_validate_script_files(in_dir, by_dir)

    # Sort the keys by natural sort order.
    sorted_scripts: dict[str, str] = dict(
        sorted(scripts.items(), key=(lambda item: utils.str_nat_sort(item[0], item[1])))
    )

    # Process each script file.
    for in_file, by_file in sorted_scripts.items():
        processed_text: str = utils.process_single_script_file(
            in_file, by_file, data_dir, in_dir, by_dir, tmp_guid, replace_grim
        )
        buffer += processed_text + LF

    # Return the combined buffer content.
    return buffer


def hash_dir(
    directory: str, base: str, hash_map: dict[str, str], hash_type: str
) -> None:
    """Recursively hashes files in a directory using the specified hashing algorithm.

    This function walks through all files in the given directory and its subdirectories,
    computing hashes using the specified algorithm. The computed hashes are stored in
    the provided `hash_map` dictionary with the relative file paths as keys.

    Parameters
    ----------
    - directory : str
        - The directory path to start the recursive hashing from.
    - base : str
        - The base directory path used to compute relative paths for the hash map keys.
    - hash_map : dict[str, str]
        - The dictionary to store the computed hashes with relative file paths as keys.
        - Note: Dictionary type as this parameter is pass-by-reference, so it will be modified in place.
    - hash_type : str
        - The type of hash to compute. Can be "adler", "size", or "md5".

    Raises
    ------
    - ValueError
        - If an unsupported hash type is provided.

    Notes
    -----
    - For "adler" hash type, uses zlib.adler32 and formats as 8-character hexadecimal.
    - For "size" hash type, uses the file size in bytes as the hash value.
    - For "md5" hash type, uses MD5 hashing with 4KB chunk reading.
    """
    # Check if the provided directory exists.
    if not os.path.isdir(directory):
        utils.err(f"No such directory {directory}.")

    # Iterate through all items in the current directory.
    for item in os.listdir(directory):
        # Construct the full path for the current item.
        item_path: str = os.path.join(directory, item)

        # If the item is a directory, recursively hash its contents.
        if os.path.isdir(item_path):
            hash_dir(item_path, base, hash_map, hash_type)
        else:
            # For files, compute the relative path from the base directory.
            relative_path: str = os.path.relpath(item_path, base).replace("\\", "/")

            # Compute hash based on the specified hash type.
            # If the Adler-32 checksum algorithm is used...
            if hash_type == "adler":
                with open(item_path, "rb") as f:
                    # Read entire file content.
                    content: bytes = f.read()
                # Compute Adler-32.
                hash_value: str = format(zlib.adler32(content) & 0xFFFFFFFF, "x")
            # Else, if the file size is used as the hash value...
            elif hash_type == "size":
                # Use file size as the hash value.
                hash_value: str = str(os.path.getsize(item_path))
            # Else, if the MD5 hash algorithm is used...
            elif hash_type == "md5":
                # Initialize MD5 hash object.
                hash_value_md5: HASH = hashlib.md5()
                # Read file in 4KB chunks for memory efficiency.
                with open(item_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        # Update hash with chunk data.
                        hash_value_md5.update(chunk)
                # Get the hexadecimal digest of the computed hash.
                hash_value: str = hash_value_md5.hexdigest()
            else:
                # Raise an error if an unsupported hash type is provided.
                raise ValueError(f"Unsupported hash type: {hash_type}")

            # Store the computed hash in the hash map with normalized path as key.
            hash_map["/" + relative_path] = hash_value


def filtered_ini_create(hashes: dict[str, str], mode: str) -> str:
    """Creates a filtered INI output string containing hash information.

    This function generates an INI-formatted string containing hash information for files,
    excluding certain files based on the global exclude list. The output follows a specific
    format used by the Umineko PS3fication project.

    Parameters
    ----------
    - hashes : dict[str, str]
        - A dictionary mapping file paths to their hash values.
    - mode : str
        - The hash mode/algorithm used (e.g., "adler", "size", "md5").

    Returns
    -------
    - str
        - A formatted INI string containing the hash information with proper headers and data sections.

    Notes
    -----
    - The output includes an [info] section with metadata about the game and hash type.
    - The [data] section contains the actual file path and hash value pairs.
    - Files matching patterns in the global exclude list are filtered out.
    - Files containing "game.hash" in their path are also excluded.
    """
    # Annotate that `exclude` is a global variable to be used in this function.
    global exclude

    # Initialize a clone of the hashes dictionary to avoid modifying the original.
    hashes_copy: dict[str, str] = hashes.copy()

    # Start building the INI output with the info section header.
    output: str = "[info]" + CRLF
    # Add game identifier information.
    output += '"game"="UminekoPS3fication*"' + CRLF
    # Add the hash mode/algorithm used.
    output += f'"hash"="{mode}"' + CRLF
    # Add version information.
    output += '"ver"="20190109-ru"' + CRLF
    # Add API version information.
    output += '"apiver"="2.2.0"' + CRLF
    # Add date field (set to ignore).
    output += '"date"="ignore"' + CRLF
    # Start the data section containing hash information
    output += "[data]" + CRLF

    # Process each file path and hash value pair
    for file_path, hash_value in hashes_copy.items():
        # Filter out files that match exclude patterns or contain "game.hash"
        if not utils.has_in(file_path, exclude) and "game.hash" not in file_path:
            # Remove leading forward slash from file path if present.
            if file_path.startswith("/"):
                file_path = file_path[1:]
            # Add the file path and hash value as a quoted key-value pair.
            output += f'"{file_path}"="{hash_value}"' + CRLF

    # Return the complete INI output string.
    return output


def compare_hashes(
    old_hashes: dict[str, str], new_hashes: dict[str, str]
) -> dict[str, dict[str, str]]:
    """Compares two hash dictionaries and returns the differences between them.

    This function analyzes two hash dictionaries (typically representing file states
    at different points in time) and categorizes the differences into three types:
    modified files, deleted files, and newly inserted files.

    TODO: Understand the purpose of this function and how it works. I don't dare to comment on it yet.
    THIS IS A BLIND TRANSLATION FROM THE PHP CODE.
    """
    # Annotate that `exclude` and `include` are global variables to be used in this function.
    global exclude
    global include

    # Initialize the output dictionary with three categories: different, deleted, and inserted.
    out: dict[str, dict[str, str]] = {"different": {}, "deleted": {}, "inserted": {}}

    old_hashes_clone: dict[str, str] = old_hashes.copy()
    new_hashes_clone: dict[str, str] = new_hashes.copy()

    for old_file_path, old_hash in old_hashes_clone.items():
        if utils.has_in(old_file_path, exclude) and new_hashes_clone.get(old_file_path):
            old_hashes_clone.pop(old_file_path)

        forced_include: bool = utils.has_in(old_file_path, include)

        if new_hashes_clone.get(old_file_path) or forced_include:
            if new_hashes_clone.get(old_file_path) != old_hash or forced_include:
                file_path_cleaned: str = old_file_path.lstrip("/")
                out["different"][file_path_cleaned] = new_hashes_clone[old_file_path]
                new_hashes_clone.pop(old_file_path)
        else:
            file_path_cleaned: str = old_file_path.lstrip("/")
            out["deleted"]["deleted"] = file_path_cleaned
        old_hashes_clone.pop(old_file_path)

    out["inserted"] = new_hashes_clone

    return out


def generate_incomplete(ep) -> str:
    """Generates script content for incomplete episodes in the Umineko visual novel.

    This function creates script directives that redirect incomplete episodes to an
    "incomplete" label, effectively skipping them. It's used to create partial builds
    that only include episodes up to a certain point.

    Parameters
    ----------
    - ep : int
        - The episode number from which to start generating incomplete directives.
        - Episodes from this number onwards will be marked as incomplete.

    Returns
    -------
    - str
        - A string containing script directives that redirect incomplete episodes
          to the "*incomplete" label using "jskip_s goto" commands.

    Notes
    -----
    - The function uses a predefined dictionary mapping episode numbers to their chapter counts.
    - Each episode includes opening, numbered chapters, ending, teatime, and ura (reverse) teatime sections.
    - All incomplete sections use the "jskip_s goto *incomplete ~" directive followed by CRLF.
    - The generated script covers episodes 1-8 with their respective chapter counts.
    """
    # Define the number of chapters for each episode (1-8)
    num: dict[int, int] = {1: 17, 2: 18, 3: 18, 4: 19, 5: 15, 6: 18, 7: 18, 8: 16}

    # Initialize output string
    out = ""

    # Generate incomplete directives for episodes starting from 'ep' to episode 8
    for i in range(ep, 9):
        # Add incomplete directive for episode opening
        out += f"*umi{i}_op{CRLF}jskip_s goto *incomplete ~{CRLF}"

        # Add incomplete directives for each chapter in the episode
        for j in range(1, num[i] + 1):
            out += f"*umi{i}_{j}{CRLF}jskip_s goto *incomplete ~{CRLF}"

        # Add incomplete directives for episode ending and teatime sections
        out += f"*umi{i}_end{CRLF}*teatime_{i}{CRLF}jskip_s goto *incomplete ~{CRLF}*teatime_{i}_end{CRLF}*ura_teatime_{i}{CRLF}jskip_s goto *incomplete ~{CRLF}*ura_{i}_end{CRLF}"

    return out


def filter_script(script: str, ep: str) -> str:
    """Filters a script to include only episodes up to a specified episode number.

    This function modifies a script to truncate content after a specified episode,
    replacing later episodes with incomplete directives and updating file extensions
    from .txt to .file.

    Parameters
    ----------
    - script : str
        - The input script content to be filtered.
    - ep : str
        - The episode number (as string) up to which content should be preserved.
        - Must be a valid positive integer.

    Returns
    -------
    - str
        - The filtered script with later episodes replaced by incomplete directives
          and file extensions updated.

    Raises
    ------
    - SystemExit
        - If the episode number is invalid (not a digit or less than 1).

    Notes
    -----
    - The function looks for the opening pattern of the episode after the specified one.
    - It searches for ending patterns to determine where to insert incomplete content.
    - File extensions are changed from ".txt" to ".file" in the final output.
    - Supports both LF and CRLF line endings in the ending patterns.
    """
    # Validate episode number input
    if not ep.isdigit() or int(ep) < 1:
        utils.err("Invalid episode number")

    # Convert episode string to integer
    ep_as_int: int = int(ep)
    # Generate incomplete episode content for episodes after the specified one
    incomplete: str = generate_incomplete(ep_as_int + 1)

    # Create the pattern to find the start of the next episode
    start_pattern: str = f"*umi{ep_as_int + 1}_op"
    # Find the position where the next episode begins
    start: int = script.find(start_pattern)

    # If the start pattern is found, replace content from that point
    if start != -1:
        # Define ending patterns to look for (supporting both LF and CRLF)
        end_pattern1: str = "ura_8_end\ngoto *end_game"  # LF line ending
        end_pattern2: str = "ura_8_end\r\ngoto *end_game"  # CRLF line ending

        # Search for the ending pattern starting from the found position
        end: int = script.find(end_pattern1, start)
        if end == -1:
            # If LF pattern not found, try CRLF pattern
            end = script.find(end_pattern2, start)
            end_len: int = len(end_pattern2)
        else:
            end_len: int = len(end_pattern1)

        # If an ending pattern is found, replace the content between start and end
        if end != -1:
            script: str = script[:start] + incomplete + script[end + end_len :]

    # Replace file extensions from .txt to .file throughout the script
    script: str = script.replace(".txt", ".file")
    return script


def localise_script(script: str, locale_dir: str) -> str:
    """Localizes a script by importing locale-specific files.

    This function processes a script to replace #locale_import directives with the
    actual content of locale files. It searches for import statements and replaces
    them with the corresponding file contents from the specified locale directory.

    Parameters
    ----------
    - script : str
        - The input script content containing #locale_import directives.
    - locale_dir : str
        - The directory path containing locale files to be imported.

    Returns
    -------
    - str
        - The localized script with import directives replaced by actual file contents.

    Notes
    -----
    - Import directives must follow the format: #locale_import "filename.txt"
    - Filename validation ensures only alphanumeric, underscore, and .txt files are allowed.
    - File contents are normalized to use LF line endings (CRLF converted to LF).
    - If a file cannot be read or doesn't exist, processing stops at that directive.
    - The function continues processing until all valid import directives are resolved.

    Security
    --------
    - Only .txt files with specific character patterns are allowed for import.
    """
    # Define the start and end markers for locale import directives
    lstart: str = '#locale_import "'  # Start of import directive
    lend: str = '"'  # End of import directive (closing quote)

    # Process import directives in a loop until none remain
    while True:
        # Find the next locale import directive
        start: int = script.find(lstart)
        if start == -1:
            break  # No more import directives found

        # Find the closing quote for the import directive
        end: int = script.find(lend, start + len(lstart))
        if end == -1:
            break  # Malformed directive, stop processing

        # Extract the filename from between the quotes
        file_name: str = script[start + len(lstart) : end]

        # Validate filename to prevent security issues and ensure valid format
        # Only allow alphanumeric characters, underscores, and .txt extension
        if not re.match(r"^[a-z0-9_]+\.txt$", file_name, re.IGNORECASE):
            break  # Invalid filename format, stop processing

        try:
            # Attempt to read the locale file
            with open(os.path.join(locale_dir, file_name), "r", encoding="utf-8") as f:
                dst: str = f.read().replace(CRLF, LF)  # Normalize line endings to LF
            # Replace the import directive with the file content
            script = script[:start] + dst + script[end + len(lend) :]
        except Exception:
            # If file reading fails (file not found, permission error, etc.), stop processing
            break

    return script


def xor_data(data: bytes, pass_num: int) -> bytes:
    """Performs XOR encryption/decryption on data using a predefined key table.

    This function applies XOR encryption to the input data using a 256-byte key table
    and different XOR patterns based on the pass number. This is used as part of the
    script transformation process in the Umineko visual novel engine.

    Parameters
    ----------
    - data : bytes
        - The binary data to be XOR processed.
    - pass_num : int
        - The pass number determining which XOR pattern to use:
          - pass_num != 2: Uses pattern (key_table[byte ^ 0x71] ^ 0x45)
          - pass_num == 2: Uses pattern (key_table[byte ^ 0x23] ^ 0x86)

    Returns
    -------
    - bytes
        - The XOR-processed data as a bytes object.

    Raises
    ------
    - SystemExit
        - If the input data is empty (via utils.err).

    Notes
    -----
    - The key table is a predefined 256-byte lookup table for XOR operations.
    - This function is typically used in a two-pass encryption process.
    - The XOR patterns and key table are specific to the ONScripter engine format.
    """
    # Predefined 256-byte key table for XOR operations
    key_table_as_bytes: bytes = utils.get_key_table()
    key_table: list[int] = list(key_table_as_bytes)

    # Validate input data
    if not data:
        utils.err("Nothing to xor")

    # Create a mutable byte array for the result
    result: bytearray = bytearray()

    # Process each byte in the input data
    for byte in data:
        c: int = byte  # Current byte value

        # Apply XOR transformation based on pass number
        if pass_num != 2:
            # First pass: XOR with 0x71, lookup in key table, then XOR with 0x45
            c = key_table[c ^ 0x71] ^ 0x45
        else:
            # Second pass: XOR with 0x23, lookup in key table, then XOR with 0x86
            c = key_table[c ^ 0x23] ^ 0x86

        # Add the transformed byte to the result
        result.append(c)

    # Convert result back to bytes and return
    return bytes(result)


def transform_script(data) -> bytes:
    """Transforms script data through a two-pass XOR encryption and compression process.

    This function applies a specific transformation algorithm used by the ONScripter
    engine for script files. The process involves XOR encryption, zlib compression,
    and a second XOR pass, all applied in chunks for memory efficiency.

    Parameters
    ----------
    - data : str or bytes
        - The input script data to be transformed. If a string is provided,
          it will be encoded to UTF-8 bytes.

    Returns
    -------
    - bytes
        - The transformed data as a bytes object, ready for storage or transmission.

    Notes
    -----
    - The transformation process consists of three main steps:
      1. First XOR pass (pass_num=1) applied in 128KB chunks
      2. Zlib compression with maximum compression level (9)
      3. Second XOR pass (pass_num=2) applied in 128KB chunks
    - Chunk processing (128KB = 131072 bytes) ensures memory efficiency for large files.
    - This is part of the ONScripter engine's script encoding format.
    """
    # Convert string input to bytes if necessary
    if isinstance(data, str):
        data = data.encode("utf-8")

    # First pass: Apply XOR encryption in chunks
    result = b""  # Initialize empty bytes result
    chunk_size = 131072  # 128KB chunks for memory efficiency

    # Process data in chunks for the first XOR pass
    for i in range(0, len(data), chunk_size):
        chunk = data[i : i + chunk_size]  # Extract current chunk
        result += xor_data(chunk, 1)  # Apply first XOR pass and append

    # Compress the XOR-encrypted data using maximum compression
    compressed = zlib.compress(result, 9)  # Level 9 = maximum compression

    # Second pass: Apply XOR encryption to compressed data in chunks
    result = b""  # Reset result for second pass

    # Process compressed data in chunks for the second XOR pass
    for i in range(0, len(compressed), chunk_size):
        chunk = compressed[i : i + chunk_size]  # Extract current chunk
        result += xor_data(chunk, 2)  # Apply second XOR pass and append

    return result


def encode_script(data: str | bytes) -> bytes:
    """Encodes script data with a proper header for the ONScripter engine format.

    This function creates a complete encoded script file by adding the appropriate
    header to transformed script data. The header contains metadata about the
    transformed data including magic signature, sizes, and version information.

    Parameters
    ----------
    - data : str or bytes
        - The input script data to be encoded. If a string is provided,
          it will be encoded to UTF-8 bytes before processing.

    Returns
    -------
    - bytes
        - The complete encoded script file with header and transformed data,
          ready to be written to disk.

    Notes
    -----
    - The header format follows the ONScripter engine specification:
      - Magic signature: "ONS2" (4 bytes ASCII)
      - Transformed data size: 4 bytes little-endian unsigned integer
      - Original data size: 4 bytes little-endian unsigned integer
      - Version number: 4 bytes little-endian unsigned integer (110)
    - The total header size is 16 bytes followed by the transformed data.
    - This creates files compatible with the ONScripter visual novel engine.
    """
    # Convert string input to bytes if necessary
    if isinstance(data, str):
        data_as_bytes: bytes = data.encode("utf-8")

    # Store the original size before transformation
    out_size: int = len(data_as_bytes)

    # Apply the script transformation (XOR + compression + XOR)
    transformed_data: bytes = transform_script(data_as_bytes)

    # Create the header according to ONScripter format specification
    header: bytes = MAGIC.encode("ascii")  # Magic signature "ONS2" as ASCII bytes

    # Pack header values as little-endian unsigned integers:
    # - Length of transformed data
    # - Original data size
    # - Version number (from global VERSION constant = 110)
    header += struct.pack("<LLL", len(transformed_data), out_size, VERSION)

    # Combine header and transformed data into final encoded script
    return header + transformed_data


def remove_grim(text: str) -> str:
    """Removes grim formatting tags from text content.

    This function strips specific formatting tags that are used in the "grim" format,
    which appears to be a markup system used in some versions of the Umineko scripts.
    It removes color formatting and stage tags while preserving the actual text content.

    Parameters
    ----------
    - text : str
        - The input text containing grim formatting tags to be removed.

    Returns
    -------
    - str
        - The cleaned text with grim formatting tags removed, preserving only the content.

    Notes
    -----
    - Removes color formatting tags in the format: {c:86EF9C:content} -> content
    - Removes stage tags in the format: [gstg NUMBER] -> (empty string)
    - The color code 86EF9C appears to be a specific hex color used in the grim format.
    - This function is used when converting between different script formatting systems.

    Examples
    --------
    >>> remove_grim("{c:86EF9C:Hello} World [gstg 1]")
    "Hello World "
    """
    # Remove color formatting tags, preserving the content inside
    # Pattern: {c:86EF9C:content} -> content
    text = re.sub(r"\{c:86EF9C:(.*?)\}", r"\1", text)

    # Remove gstg (stage) tags completely
    # Pattern: [gstg NUMBER] -> (empty string)
    text = re.sub(r"\[gstg \d+\]", "", text)

    return text


def main() -> None:
    """Main entry point for the Umineko Project Script Update Manager.

    This function processes command-line arguments and executes the appropriate
    operations for managing Umineko visual novel scripts. It supports multiple
    modes of operation including hashing, verification, script generation,
    and update package creation.

    Command-line Operations
    ----------------------
    - hash/adler/size: Generate hash files for directories
    - verify: Compare hash files and generate update information
    - dscript: Generate complete localized scripts from source files
    - script: Filter and encode scripts for specific episodes
    - update: Create update packages and optionally compress them

    Notes
    -----
    - All operations require specific command-line arguments as defined in get_usage()
    - File operations use UTF-8 encoding for text files and binary mode for script files
    - Error handling is performed via utils.err() which exits the program
    - The function processes sys.argv directly for command-line argument parsing

    Raises
    ------
    - SystemExit
        - If insufficient arguments are provided or invalid operations are specified
        - If required files or directories don't exist
        - If any file operations fail during processing
    """
    # Get command-line argument count and values
    argc = len(sys.argv)
    argv = sys.argv

    # Ensure at least one command argument is provided
    if argc < 2:
        utils.err(get_usage())

    # Extract the main command from arguments
    command = argv[1]

    # Hash generation commands: hash, adler, size
    if command in ["hash", "adler", "size"]:
        # Require: command, directory, output_file
        if argc < 4:
            utils.err(get_usage())

        # Initialize empty hash dictionary
        hashes = {}
        # Recursively hash files in the specified directory
        hash_dir(argv[2], argv[2], hashes, command)

        # Generate output based on hash type
        if command == "hash":
            # Generate JSON output for MD5 hashes
            output = json.dumps(hashes, indent=2)
        else:
            # Generate INI format for adler/size hashes
            output = filtered_ini_create(hashes, command)

        # Write output to specified file with UTF-8 encoding
        with open(argv[3], "w", encoding="utf-8") as f:
            f.write(output)

    # Hash verification and comparison command
    elif command == "verify":
        # Require: command, old_hash_file, new_hash_file
        if argc < 4:
            utils.err(get_usage())

        # Validate that both hash files exist
        if not os.path.exists(argv[2]):
            utils.err(f"No such file {argv[2]}")
        if not os.path.exists(argv[3]):
            utils.err(f"No such file {argv[3]}")

        # Load hash dictionaries from JSON files
        with open(argv[2], "r", encoding="utf-8") as f:
            old_hashes = json.load(f)
        with open(argv[3], "r", encoding="utf-8") as f:
            new_hashes = json.load(f)

        # Compare the hash dictionaries to find differences
        modifications: dict[str, dict[str, str]] = compare_hashes(
            old_hashes, new_hashes
        )

        # Build INI-format fixture string for the modifications
        fixture = ""
        for sect, content in modifications.items():
            fixture += CRLF + f"[{sect}]" + CRLF
            # Handle different content types (dict vs list)
            for key, value in content.items():
                if key.isdigit():
                    # Numeric keys indicate deletion operations
                    fixture += f'"{value}"="DO"' + CRLF
                else:
                    # String keys indicate file modifications or insertions
                    fixture += f'"{key}"="{value}"' + CRLF

        # Add MD5 hash of the fixture content for integrity verification
        fixture += (
            CRLF
            + "[update]"
            + CRLF
            + f'"hash"="{hashlib.md5(fixture.encode()).hexdigest()}"'
            + CRLF
            + CRLF
        )

        # Output to file if specified, otherwise print to console
        if argc > 5:
            # Determine output format (JSON or INI) based on optional argument
            output = (
                json.dumps(modifications)
                if len(argv) > 5 and argv[5] == "json"
                else fixture
            )
            with open(argv[4], "w", encoding="utf-8") as f:
                f.write(output)
        else:
            print(fixture)

    # Script generation command for localized builds
    elif command == "dscript":
        # Require: command, output_file, scripting_folder, locale
        if argc < 5:
            utils.err(get_usage())

        # Set version string with optional revision number
        ver = "8.3b" + (f" r{argv[5]}" if argc > 5 else "")
        locale = argv[4]  # Target locale (e.g., "en", "cn", "cht")
        # Generate game ID based on locale
        gameid = f"UminekoPS3fication{locale.capitalize()}"
        scripting = argv[3]  # Base scripting directory

        # Read and process header template
        with open(
            os.path.join(scripting, "script", "umi_hdr.txt"), "r", encoding="utf-8"
        ) as f:
            script = f.read() + LF

        # Normalize line endings and perform template substitutions
        script = script.replace(CRLF, LF)
        script = script.replace("builder_id", gameid)
        script = script.replace("builder_date", str(int(time.time())))
        script = script.replace("builder_localisation", locale)
        script = script.replace("builder_version", ver)

        # Process episodes 1-8 by merging Japanese and localized content
        for i in range(1, 9):
            # Determine translation directory, fallback to English if locale not found
            tldir = os.path.join(scripting, "story", f"ep{i}", locale)
            if not os.path.isdir(tldir):
                tldir = os.path.join(scripting, "story", f"ep{i}", "en")

            # Process episode content with localization
            script += inplace_lines(
                os.path.join(scripting, "game", "main"),
                os.path.join(scripting, "story", f"ep{i}", "jp"),
                tldir,
                locale
                in REPLACE_GRIM_WITH_LOCALIZE,  # Apply grim replacement for specific locales
            )

        # Process omake (bonus content) section
        script += inplace_lines(
            os.path.join(scripting, "game", "omake"),
            os.path.join(scripting, "story", "omake", "jp"),
            os.path.join(scripting, "story", "omake", locale),
        )

        # Read and append footer content with locale-specific handling
        footer_path = os.path.join(scripting, "script", "umi_ftr.txt")
        # Use locale-specific footer for certain languages
        if locale == "cn":
            footer_path = os.path.join(scripting, "script", "cn", "umi_ftr.txt")
        elif locale == "cht":
            footer_path = os.path.join(scripting, "script", "cht", "umi_ftr.txt")
        elif locale == "tr":
            footer_path = os.path.join(scripting, "script", "tr", "umi_ftr.txt")

        # Read footer content and normalize line endings
        with open(footer_path, "r", encoding="utf-8") as f:
            footer = f.read()

        script += footer.replace(CRLF, LF)

        # Apply locale-specific imports and substitutions
        script = localise_script(script, os.path.join(scripting, "script", locale))

        # Write final script to output file
        with open(argv[2], "w", encoding="utf-8") as f:
            f.write(script)

    # Script filtering and encoding command
    elif command == "script":
        # Require: command, input_script, output_file, episode_number
        if argc < 5:
            utils.err(get_usage())

        # Validate input file exists
        if not os.path.exists(argv[2]):
            utils.err(f"No such file {argv[2]}")

        # Read the input script file
        with open(argv[2], "r", encoding="utf-8") as f:
            script = f.read()

        # Filter script to include only episodes up to specified number
        script = filter_script(script, argv[4])
        # Encode script with proper header for ONScripter engine
        encoded: bytes = encode_script(script)

        # Write encoded script as binary file
        with open(argv[3], "wb") as f:
            f.write(encoded)

    # Update package creation command
    elif command == "update":
        # Require: command, update_file, source_folder, destination_folder
        if argc < 5:
            utils.err(get_usage())

        # Load update specification from JSON file
        with open(argv[2], "r", encoding="utf-8") as f:
            update = json.load(f)

        # Validate source directory exists
        if not os.path.isdir(argv[3]):
            utils.err(f"No source dir {argv[3]}")

        # Create destination directory if it doesn't exist
        if not os.path.isdir(argv[4]):
            os.makedirs(argv[4], 0o755, exist_ok=True)

        # Copy files specified in update package
        for sect, content in update.items():
            # Only process insert and different sections (ignore delete)
            if sect not in ["insert", "different"]:
                continue

            # Copy each file in the section
            for file_path, file_hash in content.items():
                # Create destination directory structure if needed
                dir_path = os.path.join(argv[4], os.path.dirname(file_path))
                if not os.path.isdir(dir_path):
                    os.makedirs(dir_path, 0o755, exist_ok=True)
                # Copy file with metadata preservation
                shutil.copy2(
                    os.path.join(argv[3], file_path), os.path.join(argv[4], file_path)
                )

        # Create compressed archive if archive prefix is specified
        if argc > 5:
            import datetime

            # Generate archive filename with current date
            archive = f"{argv[5]}_{datetime.datetime.now().strftime('%d.%m.%y')}.7z"
            folder = os.path.join(argv[4], "*")

            # Build 7z command with password protection and high compression
            cmd = [
                "7z",  # 7-Zip executable
                "a",  # Add to archive command
                archive,  # Output archive name
                "-t7z",  # Archive type: 7z
                "-m0=lzma2",  # Compression method: LZMA2
                "-mx=9",  # Compression level: Ultra (maximum)
                "-mfb=64",  # Number of fast bytes for LZMA2
                "-md=128m",  # Dictionary size: 128MB
                "-ms=on",  # Solid compression enabled
                "-mhe",  # Encrypt archive headers
                "-v1023m",  # Split into 1023MB volumes
                f"-p{PASSWORD}",  # Password protection
                folder,  # Source files pattern
            ]
            # Execute 7z command
            subprocess.run(cmd)
            # Clean up temporary update directory after archiving
            shutil.rmtree(argv[4])

    # Invalid command handling
    else:
        utils.err(get_usage())


if __name__ == "__main__":
    """Entry point when script is run directly.
    
    This conditional ensures that the main() function is only called when this script
    is executed directly (not when imported as a module). This is a Python best practice
    for creating executable scripts that can also be imported as modules.
    
    When executed directly, this will:
    - Parse command-line arguments via sys.argv
    - Execute the appropriate update manager operation
    - Handle any errors through utils.err() which will exit the program
    """
    main()  # Execute the main function to process command-line arguments
