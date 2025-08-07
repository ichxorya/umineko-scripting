from re import Match
import re
import os
import sys
from typing import Optional

# Constants
LF = "\n"

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

Umineko Project - Script Update Manager - Utilities.
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


def natural_key(input: str) -> list[int | str]:
    """Splits the input string into natural keys.

    Parameters
    ----------
    - input : str
        - The input string to split.

    Returns
    -------
    - list[int | str]
        - A list of natural keys extracted from the input string. Can contain integers and strings.
    """
    # Initialize the parts list by splitting the input string using a regex that matches digits.
    parts: list[str] = re.split(r"(\d+)", input)
    # Initialize the key list to store the natural keys.
    key: list[int | str] = []

    # Iterate through each part in the parts list.
    for part in parts:
        # If the part is a digit, convert it to an integer and append it to the key list.
        if part.isdigit():
            key.append(int(part))
        # Else, if the part is not a digit, convert it to lowercase and append it to the key list.
        else:
            key.append(part.lower())
    # Return the list of natural keys.
    return key


def extract_guid(data: bytes) -> str:
    """Extracts a GUID from the given bytes.

    Parameters
    ----------
    - data : bytes
        - The input bytes from which to extract the GUID.

    Returns
    -------
    - padded_hex : str
        - A hexadecimal string representation of the GUID, padded to 32 characters with leading zeros.
    """
    # Convert the input bytes to a hexadecimal string and pad it to 32 characters with leading zeros.
    hex_str: str = data.hex()
    padded_hex: str = hex_str.rjust(32, "0")

    # Return the padded hexadecimal string.
    return padded_hex


def get_txt_files_from_a_directory(directory: str) -> list[str]:
    """Gets the list of all `.txt` files in the specified directory

    Parameters
    ----------
    - directory : str
        - The directory to search for `.txt` files.

    Returns
    -------
    - list[str]
        - A list of paths to the `.txt` files found in the directory.
    """
    # Get a list of all files in the directory.
    all_files: list[str] = os.listdir(directory)

    # Filter the list to include only `.txt` files.
    txt_files: list[str] = [f for f in all_files if f.endswith(".txt")]

    # Return the sorted list of `.txt` files.
    return txt_files


def remove_grim(text: str) -> str:
    """Remove some specific stuffs from the text. IDK what `grim` means, but it is in the original PHP code.

    Parameters
    ----------
    - text : str
        - The input text from which to remove the specified patterns.

    Returns
    -------
    - modified_text : str
        - The modified text with the specified patterns removed.
    """
    # Remove `[gstg <number>]`` from the text.
    modified_text: str = re.sub(r"\[gstg \d+\]", "", text)

    # Replace `{c:86EF9C:<some text>}` → some text
    modified_text: str = re.sub(r"\{c:86EF9C:(.*?)\}", r"\1", modified_text)

    # Return the modified text.
    return modified_text


def read_file_content(file_path: str) -> str:
    """Reads the content of a file and returns it as a stripped string.

    Parameters
    ----------
    - file_path : str
        - The path to the file to read.

    Returns
    -------
    - str
        - The content of the file with leading and trailing whitespace removed.

    Raises
    ------
    - Exception
        - If the file cannot be read.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {e}") from e


def validate_directories_exist(*directories: str) -> bool:
    """Validates that all provided directories exist.

    Parameters
    ----------
    - *directories : str
        - Variable number of directory paths to validate.

    Returns
    -------
    - bool
        - True if all directories exist, False otherwise.
    """
    return all(os.path.exists(directory) for directory in directories)


def process_grim_line(
    data_by_line: str, replace_grim: bool
) -> tuple[str, Optional[str]]:
    """Processes a line for grim patterns if `replace_grim` is `True`.

    Parameters
    ----------
    - data_by_line : str
        - The line to process.
    - replace_grim : bool
        - Whether to process grim patterns.

    Returns
    -------
    - tuple[str, Optional[str]]
        - A tuple containing the processed line and the extracted grim pattern (if any).
    """
    line_grim: Optional[str] = None

    if replace_grim:
        # Search for a match in `data_by_line` that follows the pattern `[gstg <number>]`.
        match: Match[str] | None = re.search(r"\[gstg \d+\]", data_by_line)
        # If a match is found, store it in `line_grim`, otherwise set `line_grim` to None.
        line_grim = match.group(0) if match else None
        # Remove the `[gstg <number>]` pattern from `data_by_line`.
        data_by_line = re.sub(r"\[gstg \d+\]", "", data_by_line)

    return data_by_line, line_grim


def str_replace_first(
    search_for_this_string: str, replace_with_this_string: str, original_string: str
) -> str:
    """Replaces the first occurrence of a search string with a replacement string.

    Parameters
    ----------
    - search_for_this_string : str
        - The string to search for.
    - replace_with_this_string : str
        - The string to replace with.
    - original_string : str
        - The original string to perform the replacement on.

    Returns
    -------
    - str
        - The modified string with the first occurrence replaced.
    """
    # Split `original_string` into parts, using `search_for_this_string` as the delimiter.
    # The split should only turn `original_string` into two parts.
    parts: list[str] = original_string.split(search_for_this_string, 1)

    # If the split resulted in two parts, join them with `replace_with_this_string`.
    if len(parts) == 2:
        return replace_with_this_string.join(parts)
    else:
        return original_string


def wrap_line_with_guid(
    data_by_line: str, tmp_guid: str, line_grim: Optional[str], replace_grim: bool
) -> str:
    """Wraps a line with temporary GUID and backticks, and optionally appends grim pattern.

    Parameters
    ----------
    - data_by_line : str
        - The line to wrap.
    - tmp_guid : str
        - The temporary GUID to insert.
    - line_grim : Optional[str]
        - The grim pattern to append (if any).
    - replace_grim : bool
        - Whether grim replacement is enabled.

    Returns
    -------
    - str
        - The wrapped line.
    """
    # Add `temp_guid` to the `data_by_line` string, then wrap it in backticks if it hadn't been wrapped already.
    wrapped_line = "`" + tmp_guid + data_by_line.lstrip("`")

    if not wrapped_line.endswith("`"):
        wrapped_line += "`"

    # If `replace_grim` and `line_grim` are not empty, append `line_grim` to `wrapped_line`.
    if replace_grim and line_grim:
        wrapped_line += line_grim

    return wrapped_line


def err(message: str) -> None:
    """Prints an error message and exits the program.

    Parameters
    ----------
    - message : str
        - The error message to print.
    """
    print(message)
    sys.exit(0)


def validate_script_directories(data_dir: str, in_dir: str, by_dir: str) -> None:
    """Validates that all required directories exist for script processing.

    Parameters
    ----------
    - data_dir : str
        - The data directory path.
    - in_dir : str
        - The input directory path.
    - by_dir : str
        - The by/replacement directory path.
    """
    if not validate_directories_exist(data_dir, in_dir, by_dir):
        err("At least one of the directories does not exist.")


def get_and_validate_script_files(in_dir: str, by_dir: str) -> dict[str, str]:
    """Gets and validates script files from input and replacement directories.

    Parameters
    ----------
    - in_dir : str
        - The input directory path.
    - by_dir : str
        - The replacement directory path.

    Returns
    -------
    - dict[str, str]
        - A mapping of input files to replacement files.
    """
    # Get and sort script files from both directories.
    scripts_in: list[str] = get_txt_files_from_a_directory(in_dir)
    scripts_in.sort()

    scripts_by: list[str] = get_txt_files_from_a_directory(by_dir)
    scripts_by.sort()

    # Validate that we have the same number of files.
    if len(scripts_in) != len(scripts_by):
        err(
            "The number of input scripts does not match the number of scripts to replace."
        )

    # Create mapping of input files to replacement files.
    return {in_file: by_file for in_file, by_file in zip(scripts_in, scripts_by)}


def process_single_script_file(
    in_file: str,
    by_file: str,
    data_dir: str,
    in_dir: str,
    by_dir: str,
    tmp_guid: str,
    replace_grim: bool,
) -> str:
    """Processes a single script file by replacing lines according to the mapping.

    Parameters
    ----------
    - in_file : str
        - The input filename.
    - by_file : str
        - The replacement filename.
    - data_dir : str
        - The data directory path.
    - in_dir : str
        - The input directory path.
    - by_dir : str
        - The replacement directory path.
    - tmp_guid : str
        - Temporary GUID for line processing.
    - replace_grim : bool
        - Whether to apply grim replacements.

    Returns
    -------
    - str
        - The processed text content.
    """
    # Initialize paths for the "in", "by", and "text" files.
    data_in_path: str = os.path.join(in_dir, in_file)
    data_by_path: str = os.path.join(by_dir, by_file)
    text_path: str = os.path.join(data_dir, in_file)

    # Read file contents.
    text: str = read_file_content(text_path)
    data_in_content: str = read_file_content(data_in_path)
    data_by_content: str = read_file_content(data_by_path)

    # Apply grim removal if needed.
    if replace_grim:
        text = remove_grim(text)

    # Process lines if all content exists.
    if data_in_content and data_by_content and text:
        text = process_script_lines(
            text,
            data_in_content,
            data_by_content,
            in_file,
            by_file,
            tmp_guid,
            replace_grim,
        )

    # Remove temporary GUID and return
    return text.replace(tmp_guid, "")


def process_script_lines(
    text: str,
    data_in_content: str,
    data_by_content: str,
    in_file: str,
    by_file: str,
    tmp_guid: str,
    replace_grim: bool,
) -> str:
    """Processes individual lines within script files.

    Parameters
    ----------
    - text : str
        - The main text to modify.
    - data_in_content : str
        - Content from the input file.
    - data_by_content : str
        - Content from the replacement file.
    - in_file : str
        - Input filename (for error reporting).
    - by_file : str
        - Replacement filename (for error reporting).
    - tmp_guid : str
        - Temporary GUID for line processing.
    - replace_grim : bool
        - Whether to apply grim replacements.

    Returns
    -------
    - str
        - The processed text with line replacements applied.
    """
    # Split content into lines
    data_in_lines: list[str] = data_in_content.split(LF)
    data_by_lines: list[str] = data_by_content.split(LF)

    # Process each line pair
    for i in range(len(data_in_lines)):
        # Validate line indices and content
        if i >= len(data_in_lines) or not data_in_lines[i]:
            print(
                f"Missing data_in of {i} in {in_file} for {data_by_lines[i] if i < len(data_by_lines) else '?'}"
            )
            continue

        if i >= len(data_by_lines) or not data_by_lines[i]:
            print(f"Missing data_by of {i} in {by_file} for {data_in_lines[i]}")
            continue

        # Get cleaned lines
        data_in_line: str = data_in_lines[i].strip()
        data_by_line: str = data_by_lines[i].strip()

        # Process grim patterns if needed
        data_by_line, line_grim = process_grim_line(data_by_line, replace_grim)

        # Wrap line with GUID and backticks
        data_by_line = wrap_line_with_guid(
            data_by_line, tmp_guid, line_grim, replace_grim
        )

        # Replace first occurrence in text
        text = str_replace_first(data_in_line, data_by_line, text)

    return text
