from typing import TypedDict
from re import Match
import re
import os
import sys
import zlib
from typing import Optional
import update_manager_constants as const

"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣶⣿⣿⣿⣿⣿⠿⠿⢿⣿⣟⣿⣶⣤⡀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠛⠻⣶⣿⣿⡿⣿⣷⣾⣿⣥⣤⣶⣾⣛⣛⣛⠛⠛⣿⡿⠋⠉⠉⢿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⢛⣏⠀⣠⣾⣿⠽⠟⠛⠉⠁⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣷⡀⠀⢀⣼⡇⠉⠻⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⢞⣽⣾⠟⠉⠀⠀⣯⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠈⢿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢯⡿⠋⠀⠀⢠⡆⢸⣧⣶⣶⣶⣦⣤⣌⣀⡀⢀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⢻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⡿⠁⠀⠀⠀⣾⠁⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠈⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⠃⣾⣄⠀⢀⣟⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⢸⡏⣿⠀⢸⣿⠸⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⣹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡀⣿⣻⣆⢸⣿⣧⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣾⣿⣿⣷⣿⡿⠷⠿⠟⠟⠛⠋⠉⠁⢀⣀⣀⣠⣤⣤⡀⢸⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⠭⠥⠤⢤⣤⣶⡄⠀⠀⠘⢩⣭⡾⣿⣿⣿⣿⡟⢸⣼⣿⣿⣿⠈⣿⣿⣿⣿⡇⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣶⠛⠯⣙⣿⡿⠟⠀⠀⠀⠀⠈⠙⠛⠛⡋⠉⠀⢸⣿⣿⣿⣿⢰⣿⣿⣿⣿⠃⠀⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣇⠀⢢⡤⠂⠀⢀⡜⠙⢆⠀⢀⡶⠊⠁⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢠⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⡄⠁⠀⠀⠀⣌⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣸⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠐⠒⠒⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡟⠀⣿⣿⣿⣿⣿⣦⣄⡀⠀⠀⠀⠀⠀⠀⢀⣠⠖⠁⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⡿⠁⢠⣿⣿⣿⣿⣿⣿⣿⣿⠙⠒⢦⢤⡤⠖⢋⣠⠤⠚⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠘⢿⡳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⠁⠀⢸⣿⣿⣿⣿⣿⣿⣿⡏⠑⢦⣤⠴⠒⠊⠉⠀⠀⢀⣋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣍⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⠟⢀⣤⣴⣿⣿⠋⠉⠉⠉⠛⠻⠧⣀⡞⠈⣧⠀⣀⡤⠖⠋⠉⠀⠀⠀⠀⢸⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣷⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⡿⠀⠀⠀⠀⣀⣀⣤⣤⡏⠉⠉⣽⣥⡤⠄⠀⠀⠀⠀⠀⠀⣸⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠈⢙⣗⠒⢒⣏⡀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⣀⣤⠤⣶⣾⢻⡟⠉⠉⠹⡟⠻⣷⣒⠶⠤⣤⣄⡼⠁⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡶⠋⣉⣴⡾⠋⢡⡟⠀⠀⡄⠀⠹⡄⠀⠉⠻⢶⣦⣤⣉⣳⠟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠈⠛⠻⠛⠉⠀⢠⣿⣄⠀⡜⠀⠀⠀⣱⡀⠀⠀⠀⠈⠙⠳⢤⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⢀⣿⣿⣿⣦⠁⠀⣤⣾⣿⣧⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⣼⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⡆⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣾⣿⣿⣿⣿⣿⠃⠀⠀⠀
⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢻⣿⣿⣿⣿⣿⣿⣿⠿⠟⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠀
⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⣿⣿⣿⣿⣿⣿⣿⣷⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⡿⣿⣦
⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃
⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⢈⣿⣿⣿⣿⣿⣿⠋⠉⢻⣿⣿⡿⢻⣛⣿⡟⣿⣯⣀⣨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⡟⢛⣿⠇⠀
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣇⣸⣿⣿⣷⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣻⣿⣿⣿⣳⣾⣿⣿⣼⣿⠀⠀
⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣝⡻⢿⣿⣿⡿⣿⡏⠀⠀
⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣜⣻⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠙⠛⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣀⣿⠁⠀⠀
⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀
⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀
⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⣸⠛⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⢿⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀
⠈⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⡟⠀⠀⢠⠇⠀⠀⠀⠀⡜⠈⠉⠙⠻⠿⢿⡿⢿⣿⣿⣿⣿⣿⣿⡯⠉⠀⡇⠀⠀⠸⡄⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡿⠁⠀⢠⡏⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⠀⣿⠀⠀⠀⠉⠉⢩⣽⠁⠀⠀⠀⡇⠀⠀⠀⡇⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ 

This ASCII Art was made using: https://emojicombos.com/dot-art-generator

-----
Umineko Project - Scripting Update Manager - Utilities.
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
        - The error message to be printed.
    """
    print(message)
    print("The script will stop at this point, as this error occurred.")
    sys.exit(0)


def str_replace_first(
    search_for_this_string: str, replace_with_this_string: str, original_string: str
) -> str:
    """Replaces the first occurrence of `search_for_this_string` in `original_string` with `replace_with_this_string`.

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


def generate_guid() -> str:
    """Generates a GUID (Globally Unique Identifier) as a hexadecimal string.

    Returns
    -------
    - str
        - A hexadecimal string representation of the GUID, padded to 32 characters with leading zeros.
        - If the GUID generation fails, a default value is returned.

    Raises
    ------
    - Exception
        - If the GUID generation fails, an exception is raised.
    """
    # Try using the operating system's random number generator to create 16 random bytes, then extract the GUID from it.
    try:
        random_bytes: bytes = os.urandom(16)
        return extract_guid(random_bytes)
    # If that fails (which is kind of 0.000000000001% likely, shout out to Bernkastel if this happens), fall back to using the default value.
    except Exception:
        return "ea5078d1f71c405887bd54994bfeff24"


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


def has_in(haystack: str, needle: list[str]) -> bool:
    """Checks if the `haystack` string contains any of the `needle` strings.

    Parameters
    ----------
    - haystack : str
        - The string to search within.
    - needle : list[str]
        - The strings to search for in `haystack`.

    Returns
    -------
    - bool
        - `True` if `haystack` contains any of the `needle` strings, `False` otherwise.
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


def generate_incomplete(ep) -> str:
    """Generate incomplete episode script."""
    num: dict[int, int] = {1: 17, 2: 18, 3: 18, 4: 19, 5: 15, 6: 18, 7: 18, 8: 16}

    out = ""

    for i in range(ep, 9):
        out += f"*umi{i}_op{const.CRLF}jskip_s goto *incomplete ~{const.CRLF}"
        for j in range(1, num[i] + 1):
            out += f"*umi{i}_{j}{const.CRLF}jskip_s goto *incomplete ~{const.CRLF}"
        out += f"*umi{i}_end{const.CRLF}*teatime_{i}{const.CRLF}jskip_s goto *incomplete ~{const.CRLF}*teatime_{i}_end{const.CRLF}*ura_teatime_{i}{const.CRLF}jskip_s goto *incomplete ~{const.CRLF}*ura_{i}_end{const.CRLF}"

    return out


def transform_script(data: bytes) -> bytes:
    """Transform script data."""
    # First pass
    result: bytes = b""
    chunk_size = 131072
    for i in range(0, len(data), chunk_size):
        chunk: bytes = data[i : i + chunk_size]
        result += xor_data(chunk, 1)

    # Compress
    compressed = zlib.compress(result, 9)

    # Second pass
    result = b""
    for i in range(0, len(compressed), chunk_size):
        chunk = compressed[i : i + chunk_size]
        result += xor_data(chunk, 2)

    return result

def xor_data(data: bytes, pass_num: int) -> bytes:
    key_table: bytes = get_key_table()
    
    if not data:
        err('Nothing to xor')
    
    result: bytearray = bytearray()
    for byte in data:
        c: int = byte
        
        if pass_num != 2:
            c = key_table[c ^ 0x71] ^ 0x45
        else:
            c = key_table[c ^ 0x23] ^ 0x86
        
        result.append(c)
    
    return bytes(result)

class HashDiff(TypedDict):
    differences: dict[str, str]
    deletions: list[str]
    additions: dict[str, str]
