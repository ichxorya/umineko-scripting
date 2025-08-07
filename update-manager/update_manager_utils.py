import re
import os
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
    """Custom function to remove stuffs from the text.

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
