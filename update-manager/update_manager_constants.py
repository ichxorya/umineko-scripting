"""
⠄⢠⡤⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡗⢾⣷⣾⢲⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⢸⣿⣾⣿⣏⣧⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣾⢿⣿⣿⣿⣿⣝⣿⣿⣿⣿⣿⠀
⡇⢸⣿⣿⣾⣿⠿⢶⣶⣷⢶⣶⣶⣶⣶⡶⠶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣶⣶⣶⣶⣶⢾⣿⣿⡿⡻⣿⡷⠶⠿⢿⣿⣿⣿⡿⣿⣽⡿⣿⣽⠼
⡇⢸⣿⣿⠀⠈⠒⠒⠛⠛⠛⠛⠛⢿⣿⣻⣷⣿⣳⣀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣰⣿⣻⣿⣿⣿⣿⣿⣿⣿⢟⡟⡿⠟⠛⠒⠒⠚⠒⠃⠀⢀⣀⣀⣿⣿⢻⣿⠟⢛⡷⠛⠀⠀
⡇⢸⣿⢹⠀⠀⠀⠀⢠⣤⡤⢤⣤⣤⣿⣿⣿⣷⡍⣯⣧⡄⠀⢠⣤⣤⣼⣠⣿⣿⣿⣿⣿⡷⣛⣋⡿⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⢠⣤⡤⣿⡷⣿⣻⣟⣋⡿⠉⠉⠁⠀⠀⠀
⡇⢸⢹⢸⠀⠀⠀⡖⣻⡿⣻⣧⣽⣿⣿⣾⠛⣿⣿⣿⣗⣿⡖⢻⣿⡴⢺⡿⠗⠒⠾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣶⣶⣲⣶⡶⡿⣿⡿⢻⡿⠯⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⢸⢨⢸⣄⡀⠀⣧⣿⣿⣻⠛⠛⢿⣿⣿⠇⣿⣋⣼⡟⠋⡷⣟⣿⣿⠛⠀⠀⠀⢀⣤⣤⣤⣤⣤⣤⣮⢻⣿⣿⣽⣿⣯⣽⠽⢿⣿⣻⣿⣿⣿⣿⣥⣤⣄⣤⣤⣤⣤⣤⣤⡄⠀⠀
⡇⢸⠸⣴⣿⡇⠀⣷⣿⣮⡿⠀⢰⠾⡿⠙⣀⣶⢾⡥⠇⠀⣧⣿⡧⣟⠀⠀⠀⠀⠸⠴⠬⠽⠵⠧⠷⠶⠤⠾⠾⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠷⠾⣿⣿⣿⣿⣿⡿⣫⣯⣧⠀⠀
⡇⢸⠀⣿⣿⡇⠀⡿⣾⡏⢷⣀⠈⠓⠛⠛⠛⠓⠛⢀⣸⣏⣿⣿⡗⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣸⣟⢛⣽⣿⣿⢟⣿⡾⠛⠀⠀
⡇⢸⠁⣻⣸⠀⠀⢿⣿⢿⣦⣼⣤⢤⣤⣤⣤⣤⣤⣿⣺⡿⢿⣥⡇⠀⢠⢤⢤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣿⣿⣿⣿⣿⣯⣿⣾⣿⣥⡿⠉⠉⠀⠀⠀⠀
⡇⢸⣷⣿⣿⠀⠀⠀⠙⠒⠿⣿⣽⣽⣿⣿⣿⣿⣿⣾⡿⠶⠾⠃⠀⠀⠘⠾⠓⠻⣿⢿⣿⣽⣭⣯⣉⣹⣽⣿⣿⣻⣿⣶⣶⣾⡿⣷⣿⣿⣿⣿⣿⡿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⢸⢸⣿⣿⠃⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⢠⣤⣤⣤⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣩⣿⣧⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⢸⢸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⢤⡝⠾⣶⡶⣶⣶⣶⣖⢶⠀⠀⠀⠀⠀⠀⠀⣿⣿⠿⣿⢿⣿⣿⡿⢿⣿⣿⢿⡧⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⢸⠈⣿⣿⠀⠀⠀⠀⠀⡏⣹⣄⡀⠀⠀⠀⠀⠀⢀⣀⣀⣀⠀⠀⠓⠒⠚⠛⣿⣻⣿⣿⣻⣋⠻⣿⣟⣹⣿⣿⣽⣿⣷⣿⣿⣗⣯⣻⠛⠛⠛⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⢸⣶⣿⣿⠀⠀⠀⠀⠀⣧⡌⡷⣧⢤⠀⠀⠀⠀⠸⣭⣀⢺⣦⠤⡤⠀⠀⠀⠈⠁⠀⠙⠿⠽⠿⣿⣿⢿⣿⣷⣽⣿⢿⢿⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⢸⣻⣿⣿⡀⠀⢀⣰⢛⣳⣿⣿⣮⣿⣿⡛⣇⣀⠀⠈⠻⣗⠯⣷⣿⣿⣿⣿⣿⣿⣆⣀⣀⣀⣀⣈⣻⣿⣿⣿⢟⣻⣹⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⢸⣿⣿⣿⣧⠤⣯⣤⣾⣿⣼⠋⠛⣏⣿⣿⣿⣿⣤⣤⣤⣽⣿⢿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣯⣭⣽⣯⣭⣾⣏⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⢸⣿⣿⢿⣾⡾⢿⡾⠧⠟⠁⠀⠀⠀⠀⠙⠿⠿⣾⠿⢿⣿⣿⣶⣿⢿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⢸⣿⠙⣿⣋⣿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠋⠉⠉⠛⠋⠉⠙⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⢸⣿⣰⣿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⢸⣿⣻⠟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠃⠀⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

This ASCII Art was made using: https://emojicombos.com/dot-art-generator

-----
Umineko Project - Scripting Update Manager - Constant Values.
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
LF: str = "\n"
CRLF: str = "\r\n"
DS: str = "/"  # DIRECTORY_SEPARATOR.
TAB: str = "\t"
MAGIC: str = "ONS2"
VERSION: int = 110
MAX_INPUT_SIZE: int = 0x10000000
UPDATE_MANAGER: bool = True
PASSWORD: str = "035646750436634546568555050"
REPLACE_GRIM_WITH_LOCALIZE: list[str] = ["cn", "cht"]
