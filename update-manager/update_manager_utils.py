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


def err(message: str) -> None:
    """Prints an error message and exits the program.

    TODO: Replace this with proper use of exceptions, use logging, or something similar.

    Parameters
    ----------
    - message : str
        - The error message to print.
    """
    print(message)
    sys.exit(0)


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
    key1: list[int | str] = natural_key(str1)
    key2: list[int | str] = natural_key(str2)

    # Compare the natural keys (performs a natural sort comparison).
    return (key1 > key2) - (key1 < key2)


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
    """Remove some specific stuffs ("grim" pattern) from the text.
    IDK what `grim` means, but it is in the original PHP code.

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


def validate_directories_exist(directories: list[str]) -> bool:
    """Validates that all provided directories exist.

    Parameters
    ----------
    - directories : list[str]
        - A list of directory paths to validate.

    Returns
    -------
    - bool
        - True if all directories exist, False otherwise.
    """
    # Check if all directories in the list exist.
    for directory in directories:
        if not os.path.exists(directory):
            return False
    # If all directories exist, return True.
    return True


def process_grim_line(
    data_by_line: str, replace_grim: bool
) -> tuple[str, Optional[str]]:
    """Processes a line for "grim" patterns if `replace_grim` is `True`.

    Parameters
    ----------
    - data_by_line : str
        - The line to process.
    - replace_grim : bool
        - Whether to process "grim" patterns.

    Returns
    -------
    - tuple[str, Optional[str]]
        - A tuple containing the processed line and the extracted "grim" pattern (if any).
    """
    # Initialize `line_grim` to None, which will hold the "grim" pattern if found.
    line_grim: Optional[str] = None

    # If `replace_grim` is True...
    if replace_grim:
        # Search for a match in `data_by_line` that follows the pattern `[gstg <number>]`.
        match: Match[str] | None = re.search(r"\[gstg \d+\]", data_by_line)

        # If a match is found, store it in `line_grim`, otherwise set `line_grim` to None.
        line_grim = match.group(0) if match else None

        # Remove the `[gstg <number>]` pattern from `data_by_line`.
        data_by_line = re.sub(r"\[gstg \d+\]", "", data_by_line)

    # Return the processed line and the "grim" pattern (if any).
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
    # Else, if the split did not result in two parts, return the original string.
    else:
        return original_string


def wrap_line_with_guid(
    data_by_line: str, tmp_guid: str, line_grim: Optional[str], replace_grim: bool
) -> str:
    """Wraps a line with temporary GUID and backticks, and optionally appends "grim" pattern.

    Parameters
    ----------
    - data_by_line : str
        - The line to wrap.
    - tmp_guid : str
        - The temporary GUID to insert.
    - line_grim : Optional[str]
        - The "grim" pattern to append (if any).
    - replace_grim : bool
        - Whether "grim" replacement is enabled.

    Returns
    -------
    - str
        - The wrapped line.
    """
    # Add `temp_guid` to the `data_by_line` string, then wrap it in backticks if it hadn't been wrapped already.
    wrapped_line: str = "`" + tmp_guid + data_by_line.lstrip("`")

    if not wrapped_line.endswith("`"):
        wrapped_line += "`"

    # If `replace_grim` and `line_grim` are not empty, append `line_grim` to `wrapped_line`.
    if replace_grim and line_grim:
        wrapped_line += line_grim

    return wrapped_line


def validate_script_directories(data_dir: str, in_dir: str, by_dir: str) -> None:
    """Validates that all required directories exist for script processing.

    Parameters
    ----------
    - data_dir : str
        - TODO: Figure out what this is for.
    - in_dir : str
        - TODO: Figure out what this is for.
    - by_dir : str
        - TODO: Figure out what this is for.
    """
    if not validate_directories_exist([data_dir, in_dir, by_dir]):
        err("At least one of the directories does not exist.")


def get_and_validate_script_files(in_dir: str, by_dir: str) -> dict[str, str]:
    """Gets and validates script files from `in_dir` and `by_dir`.
    TODO: Figure out what `in_dir` and `by_dir` are for.

    Parameters
    ----------
    - in_dir : str
        - TODO: Figure out what this is for.
    - by_dir : str
        - TODO: Figure out what this is for.

    Returns
    -------
    - scripts : dict[str, str]
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

    # Create the required mapping.
    scripts: dict[str, str] = {
        in_file: by_file for in_file, by_file in zip(scripts_in, scripts_by)
    }

    # Return the mapping.
    return scripts


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
        - TODO: Figure out what this is for.
    - by_file : str
        - TODO: Figure out what this is for.
    - data_dir : str
        - TODO: Figure out what this is for.
    - in_dir : str
        - TODO: Figure out what this is for.
    - by_dir : str
        - TODO: Figure out what this is for.
    - tmp_guid : str
        - Temporary GUID for line processing.
    - replace_grim : bool
        - Whether to apply "grim" replacements.

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

    # Remove temporary GUID and return.
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
        - TODO: Figure out what this is for.
    - data_in_content : str
        - TODO: Figure out what this is for.
    - data_by_content : str
        - TODO: Figure out what this is for.
    - in_file : str
        - TODO: Figure out what this is for.
    - by_file : str
        - TODO: Figure out what this is for.
    - tmp_guid : str
        - Temporary GUID for line processing.
    - replace_grim : bool
        - Whether to apply "grim" replacements.

    Returns
    -------
    - str
        - The processed text with line replacements applied.
    """
    # Split content into lines.
    data_in_lines: list[str] = data_in_content.split(LF)
    data_by_lines: list[str] = data_by_content.split(LF)

    # Process each line pair.
    for i in range(len(data_in_lines)):
        # Validate line indices and content.
        if i >= len(data_in_lines) or not data_in_lines[i]:
            print(
                f"Missing data_in of {i} in {in_file} for {data_by_lines[i] if i < len(data_by_lines) else '?'}"
            )
            continue

        if i >= len(data_by_lines) or not data_by_lines[i]:
            print(f"Missing data_by of {i} in {by_file} for {data_in_lines[i]}")
            continue

        # Get cleaned lines.
        data_in_line: str = data_in_lines[i].strip()
        data_by_line: str = data_by_lines[i].strip()

        # Process "grim" patterns if needed.
        data_by_line, line_grim = process_grim_line(data_by_line, replace_grim)

        # Wrap line with GUID and backticks.
        data_by_line = wrap_line_with_guid(
            data_by_line, tmp_guid, line_grim, replace_grim
        )

        # Replace first occurrence in text.
        text = str_replace_first(data_in_line, data_by_line, text)

    # Return the processed text.
    return text


def has_in(haystack: str, needle: list[str]) -> bool:
    """Checks if the `haystack` string contains any of the `needle` strings.

    This function determines whether the haystack string contains any of the strings
    specified in the needle parameter. The needle can be either a single string or
    a list of strings to check against.

    Parameters
    ----------
    - haystack : str
        - The string to search within.
    - needle : list[str]
        - The strings to search for in the `haystack`.

    Returns
    -------
    - bool
        - True if haystack contains any of the needle strings, False otherwise.
    """

    # Check if any of the needle strings is present in the haystack
    for query in needle:
        if query in haystack:
            # Return immediately if a match is found
            return True

    # Return False if no matches are found
    return False


def get_key_table() -> bytes:
    """Returns the key table used for encryption/decryption.

    Returns
    -------
    - bytes
        - A bytes object containing the key table.
        - The table is a sequence of 256 bytes.
    """
    return (
        b"\xc0\xbc\x86\x66\x84\xf3\xbe\x90\xb0\x02\x98\x5e\x0f\x9c\x7b\xf4"
        b"\xd9\x91\xdb\xeb\x81\x74\x3a\xe3\x76\x94\x21\x93\x63\x68\x0d\xa1"
        b"\xba\xaa\x1b\xa0\x49\x2b\xe1\xe7\x38\xa6\x25\x53\x40\x4a\xec\x29"
        b"\x36\xbf\xf2\x9f\xac\x0c\xcb\x00\x1f\xf1\x7c\x80\x4f\x60\x82\x62"
        b"\x14\x6d\xd8\x32\x13\x2f\xe0\x99\xf7\x10\xd1\x30\x64\x4e\x8c\xde"
        b"\xc1\x6a\xad\xa7\xb5\x95\xcf\xc6\x0b\x2d\x69\x24\x5c\xc5\x03\xda"
        b"\xd6\x8e\xa3\x88\x31\x17\x3c\xb3\xa8\xb4\x01\x0e\xfc\x37\x65\x16"
        b"\x6c\xbb\x50\x55\x2a\xe5\x77\x97\x09\xb1\x04\x67\xc7\x79\x71\x7a"
        b"\x43\xd0\x22\x58\x0a\x57\xb7\xae\x4d\xc8\xe9\x46\xd3\x5b\x96\xcc"
        b"\x3f\xe6\x3e\x54\x5f\x1d\xfa\xf0\x3d\x7d\x83\xa5\xfd\xef\x15\x8b"
        b"\x70\x6b\xe2\xff\x07\xd7\x92\x41\x61\x75\x6f\x7f\xc4\xd5\xf9\x05"
        b"\x34\xfe\x5d\xdc\xb9\xe8\xab\xca\xc3\x35\x08\x3b\xa2\xbd\x8f\x7e"
        b"\x2e\x44\x5a\x12\xed\xe4\x11\x1e\xc2\x78\xf5\xaf\xf6\x72\x28\x9d"
        b"\x6e\x39\xd2\xea\x45\x73\x47\x9e\x26\x89\x85\x52\x33\xdf\xa4\x48"
        b"\x23\xce\x1c\x8d\x18\x27\x9a\xb6\xa9\xee\xb8\xc9\x2c\xfb\x59\x56"
        b"\x20\x42\xcd\x51\xb2\x06\x19\x4b\x9b\xd4\x8a\x4c\xf8\x87\x1a\xdd"
    )
