from update_manager_utils import HashDiff
import os
import sys
import json
import time
import hashlib
import shutil
import subprocess
import datetime
import update_manager_constants as const
import update_manager_core_logic as core
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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠀⠀⢠⠏⠀⠀⠀⣼⣿⠃⠀⠀⠀⡟⠀⠀⠀⢸⠇⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⢠⡄⢹⡇⠀⠀⠀⢹⣧⠾⣫⡾⠋⣴⡟⣿⠀⠀⢀⣿⢳    
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢹⠀⠀⢸⠀⠀⠀⢰⡟⣿⠀⠀⠀⣸⠃⠀⠀⠀⣾⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⣷⠈⣿⣤⡴⠖⣫⣵⡾⠏⢀⣴⣿⠃⣿⣇⣠⡞⠋⣿⠀⠀⠀⠀
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

This ASCII Art was taken from: https://emojicombos.com/umineko

-----
Umineko Project - Scripting Update Manager.
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


def get_usage() -> str:
    """Returns a string that shows how to use the script.

    Returns
    -------
    str
        A string showing the usage of the script.
    """
    return """\
Usage:
    - update_manager.py md5 <input_dir> <output_file>      
        - Generate MD5 hashes of all files in <input_dir> and write to <output_file> as JSON.

    - update_manager.py adler <input_dir> <output_file>
        - Generate Adler-32 checksums and output as INI-style format.

    - update_manager.py size <input_dir> <output_file>
        - Generate file sizes and output as INI-style format.

    - update_manager.py verify <old_hashes.json> <new_hashes.json> [<output_file> [json]]
        - Compare two sets of hashes and output modified files.
        - Optionally, if <output_file> is provided as the 4th argument, the result is saved as a INI file.
        - Optionally, if 'json' is passed as the 5th argument, the result will be saved as a JSON file.

    - update_manager.py dscript <output_script.txt> <scripting_dir> <locale> [<revision>]
        - Assemble the full translated script from components for the given locale.
        - Optionally include a version revision (e.g., 'r2').

    - update_manager.py script <input_script.txt> <output_script.bin> <locale>
        - Filter and encode a plain text script into binary format for the specified locale.

    - update_manager.py update <update.json> <source_dir> <target_dir> [<archive_name>]
        - Copy updated files as defined in <update.json> from <source_dir> to <target_dir>.
        - Optionally, if <archive_name> is given, create a 7z archive of the update and remove <target_dir>.

Commands:
md5, adler, size      - Generate file metadata (hash/checksum/size).
verify                - Compare two sets of metadata and identify differences.
dscript               - Build full localized script from parts.
script                - Filter and encode scripts into binary.
update                - Prepare patch/update files with optional archiving.
help                  - Show this usage information.
    """


def suggest_using_help_command() -> None:
    print("- If you need help, please execute the `help` command for more information.")


def handle_generate_metadata_command(
    arguments: list[str], number_of_arguments: int
) -> None:
    command: str = arguments[0]

    if number_of_arguments != 3:
        print(
            f"- The number of arguments after '{command}' must be 2, and you provided {number_of_arguments - 1}."
        )
        print(f"- Here is your argument list: {arguments}")
        suggest_using_help_command()
        return

    input_dir: str = arguments[1]
    output_file: str = arguments[2]
    output: str = ""

    hashes: dict[str, str] = {}
    core.hash_dir(input_dir, input_dir, hashes, command)

    if command == "md5":
        output = json.dumps(hashes, indent=2)
    else:
        output = core.filtered_ini_create(hashes, command)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Output written to {output_file}.")


def handle_verify_command(arguments: list[str], number_of_arguments: int) -> None:
    command: str = arguments[0]

    if number_of_arguments < 3 or number_of_arguments > 5:
        print(
            f"- The number of arguments after '{command}' must be between 2 and 4, and you provided {number_of_arguments - 1}."
        )
        print(f"- Here is your argument list: {arguments}")
        suggest_using_help_command()
        return

    old_hashes_path: str = arguments[1]
    new_hashes_path: str = arguments[2]
    if number_of_arguments > 3:
        output_path: str = arguments[3]

    if not os.path.exists(old_hashes_path):
        print(f"Old hashes file does not exist: {old_hashes_path}")
        return

    if not os.path.exists(new_hashes_path):
        print(f"New hashes file does not exist: {new_hashes_path}")
        return

    old_hashes: dict[str, str] = json.load(open(old_hashes_path, "r", encoding="utf-8"))
    new_hashes: dict[str, str] = json.load(open(new_hashes_path, "r", encoding="utf-8"))

    hashes_differences: utils.HashDiff = core.compare_hashes(old_hashes, new_hashes)

    fixture = ""
    fixture += const.CRLF + "[different]" + const.CRLF
    for key, value in hashes_differences["differences"].items():
        if key.isdigit():
            fixture += f'"{value}"="DO"' + const.CRLF
        else:
            fixture += f'"{key}"="{value}"' + const.CRLF

    fixture += const.CRLF + "[deletions]" + const.CRLF
    for value in hashes_differences["deletions"]:
        fixture += f'"{value}"="DELETE"' + const.CRLF

    fixture += const.CRLF + "[additions]" + const.CRLF
    for key, value in hashes_differences["additions"].items():
        if key.isdigit():
            fixture += f'"{value}"="DO"' + const.CRLF
        else:
            fixture += f'"{key}"="{value}"' + const.CRLF

    fixture += (
        const.CRLF
        + "[update]"
        + const.CRLF
        + f'"hash"="{hashlib.md5(fixture.encode()).hexdigest()}"'
        + const.CRLF
        + const.CRLF
    )

    if number_of_arguments == 5 and arguments[4] == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(hashes_differences, f, indent=2)
        print(f"Output written to {output_path}.")
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(fixture)
        print(f"Output written to {output_path}.")


def handle_dscript_command(arguments: list[str], number_of_arguments: int) -> None:
    command: str = arguments[0]

    if number_of_arguments < 4 or number_of_arguments > 5:
        print(
            f"- The number of arguments after '{command}' must be between 3 and 4, and you provided {number_of_arguments - 1}."
        )
        print(f"- Here is your argument list: {arguments}")
        suggest_using_help_command()
        return

    output_path: str = arguments[1]
    scripting_dir: str = arguments[2]
    locale: str = arguments[3]
    game_id: str = f"UminekoPS3fication{locale.capitalize()}"
    version: str = "8.3b" + (f" r{arguments[4]}" if number_of_arguments == 5 else "")

    script: str = ""

    with open(
        os.path.join(scripting_dir, "script", "umi_hdr.txt"), "r", encoding="utf-8"
    ) as f:
        script = f.read() + const.LF

    script = script.replace(const.CRLF, const.LF)
    script = script.replace("builder_id", game_id)
    script = script.replace("builder_date", str(int(time.time())))
    script = script.replace("builder_localisation", locale)
    script = script.replace("builder_version", version)

    # Process episodes 1-8
    for i in range(1, 9):
        tldir: str = os.path.join(scripting_dir, "story", f"ep{i}", locale)
        if not os.path.isdir(tldir):
            tldir = os.path.join(scripting_dir, "story", f"ep{i}", "en")

        script += core.inplace_lines(
            os.path.join(scripting_dir, "game", "main"),
            os.path.join(scripting_dir, "story", f"ep{i}", "jp"),
            tldir,
            locale in const.REPLACE_GRIM_WITH_LOCALIZE,
        )

    # Process omake
    script += core.inplace_lines(
        os.path.join(scripting_dir, "game", "omake"),
        os.path.join(scripting_dir, "story", "omake", "jp"),
        os.path.join(scripting_dir, "story", "omake", locale),
    )

    # Read footer
    footer_path: str = os.path.join(scripting_dir, "script", "umi_ftr.txt")
    if locale == "cn":
        footer_path = os.path.join(scripting_dir, "script", "cn", "umi_ftr.txt")
    elif locale == "cht":
        footer_path = os.path.join(scripting_dir, "script", "cht", "umi_ftr.txt")
    elif locale == "tr":
        footer_path = os.path.join(scripting_dir, "script", "tr", "umi_ftr.txt")

    with open(footer_path, "r", encoding="utf-8") as f:
        footer = f.read()

    script += footer.replace(const.CRLF, const.LF)

    # Localise script
    script = core.localise_script(script, os.path.join(scripting_dir, "script", locale))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(script)
    print(f"Output written to {output_path}.")


def handle_script_command(arguments: list[str], number_of_arguments: int) -> None:
    command: str = arguments[0]

    if number_of_arguments != 4:
        print(
            f"- The number of arguments after '{command}' must be exactly 3, and you provided {number_of_arguments - 1}."
        )
        print(f"- Here is your argument list: {arguments}")
        suggest_using_help_command()
        return

    input_script_path: str = arguments[1]
    output_script_path: str = arguments[2]
    episode: str = arguments[3]

    if not episode.isdigit():
        utils.err(f"Invalid episode number: {episode}. It must be a digit.")
    episode_as_int: int = int(episode)

    if not os.path.exists(input_script_path):
        utils.err(f"No such file {input_script_path}")

    with open(input_script_path, "r", encoding="utf-8") as f:
        script: str = f.read()

    script = core.filter_script(script, episode_as_int)
    encoded: bytes = core.encode_script(script)

    with open(output_script_path, "wb") as f:
        f.write(encoded)
    print(f"Output written to {output_script_path}.")


def handle_update_command(arguments: list[str], number_of_arguments: int) -> None:
    command: str = arguments[0]

    if number_of_arguments < 4 or number_of_arguments > 5:
        print(
            f"- The number of arguments after '{command}' must be either 3 or 4, and you provided {number_of_arguments - 1}."
        )
        print(f"- Here is your argument list: {arguments}")
        suggest_using_help_command()
        return

    update_json_path: str = arguments[1]
    source_dir_path: str = arguments[2]
    target_dir_path: str = arguments[3]
    if number_of_arguments == 5:
        archive_name: str = arguments[4]

    with open(update_json_path, "r", encoding="utf-8") as f:
        update_json_content: HashDiff = json.load(f)

    if not os.path.exists(source_dir_path):
        utils.err(f"No such directory {source_dir_path}")

    if not os.path.isdir(target_dir_path):
        os.makedirs(target_dir_path, 0o755, exist_ok=True)

    differences: dict[str, str] = update_json_content.get("differences")
    additions: dict[str, str] = update_json_content.get("additions")

    for file_path, file_hash in differences.items():
        dir_path_1: str = os.path.join(target_dir_path, os.path.dirname(file_path))

        if not os.path.isdir(dir_path_1):
            os.makedirs(dir_path_1, 0o755, exist_ok=True)
        shutil.copy2(
            os.path.join(source_dir_path, file_path),
            os.path.join(target_dir_path, file_path),
        )

    for file_path, file_hash in additions.items():
        dir_path_2: str = os.path.join(target_dir_path, os.path.dirname(file_path))

        if not os.path.isdir(dir_path_2):
            os.makedirs(dir_path_2, 0o755, exist_ok=True)
        shutil.copy2(
            os.path.join(source_dir_path, file_path),
            os.path.join(target_dir_path, file_path),
        )

    if number_of_arguments == 5:
        archive = f"{archive_name}_{datetime.datetime.now().strftime('%d.%m.%y')}.7z"
        folder: str = os.path.join(target_dir_path, '*')
        
        cmd: list[str] = [
            '7z', 'a', archive, '-t7z', '-m0=lzma2', '-mx=9', '-mfb=64',
            '-md=128m', '-ms=on', '-mhe', '-v1023m', f'-p{const.PASSWORD}', folder
        ]
        subprocess.run(cmd)
        shutil.rmtree(target_dir_path)

def main() -> None:
    arguments: list[str] = sys.argv[1:]
    number_of_arguments: int = len(arguments)

    if number_of_arguments < 1:
        print(get_usage())
        return

    command: str = arguments[0]

    if command in ["md5", "adler", "size"]:
        handle_generate_metadata_command(arguments, number_of_arguments)
    elif command == "verify":
        handle_verify_command(arguments, number_of_arguments)
    elif command == "dscript":
        handle_dscript_command(arguments, number_of_arguments)
    elif command == "script":
        handle_script_command(arguments, number_of_arguments)
    elif command == "update":
        handle_update_command(arguments, number_of_arguments)
    elif command == "help":
        print(get_usage())
    else:
        print(f"- Unknown command: {command}")
        suggest_using_help_command()


if __name__ == "__main__":
    main()
