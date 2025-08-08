from _hashlib import HASH
from re import Match
from functools import cmp_to_key
import update_manager_constants as const
import update_manager_utils as utils
import os
import hashlib
import re
import zlib
import struct

"""
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠉⠉⠋⠙⠋⠻⠿⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠐⠀⠠⠀⢀⠀⠈⠀⠐⠀⢀⠀⠀⠘⠙⢻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠄⠀⠀⠀⠀⠂⠀⡀⠀⠀⠂⠀⠀⠀⠀⣻⠿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠉⠙⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠂⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣦⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⢾⣭⣝⡛⠿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠶⠄⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠄⢀⠀⠁⠝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠸⣧⢠⠐⠀⠈⣙⣿⣿⣿⣋⣭⠶⠒⠚⠛⠛⠛⠲⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣦⣊⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⢹⣜⢧⠀⠁⢸⣿⣿⣿⣟⠀⣴⡀⠀⠀⠂⡦⢰⡯⣗⠀⠀⣄⠀⠀⠀⠀⠀⠀⠐⢠⣻⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⢘⣿⠷⢶⣤⡿⠉⡻⢿⣿⣷⣝⡓⣀⣀⠠⣵⢯⡽⠆⠀⣦⡘⠧⠀⠃⣀⠀⠀⠀⣷⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠸⣷⣿⣿⣏⢎⡾⡽⣆⢻⣯⡼⢙⣩⣿⣙⢈⡷⡏⢀⣼⢳⡗⠀⣤⣾⣿⣧⡀⠀⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⣿⣿⣿⣿⣶⣜⠹⣡⣾⣿⣷⣿⣿⣿⣿⢸⣻⢠⡼⠊⠁⣠⣾⣿⣿⣿⣿⣷⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡈⢿⣿⣿⣷⣭⣭⣙⣛⣛⣛⣩⣿⣿⡏⡼⣏⡟⢠⡇⠐⣿⣿⣿⣿⣿⣿⣿⣬⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡙⢿⣿⣿⣿⣭⣽⣿⣿⣿⣿⠟⣰⠟⢈⡴⢯⠃⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢙⢿⣿⣿⣿⣿⡿⠟⠁⣚⡥⣞⠯⠉⠀⠀⢠⣆⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⡄⢹⣷⣭⡙⣭⡥⣴⢞⣻⠵⠛⠈⠀⠀⠀⢀⣾⣿⣆⠚⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣴⣿⠇⠀⢿⣿⣿⣦⡙⠷⠋⠀⠀⠀⠀⠀⠀⠀⡼⣿⢿⣿⣧⠢⣌⡙⠻⢿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⣋⢁⣤⣾⣿⠏⠀⡐⠈⠿⠛⠋⢁⠠⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣷⣝⢿⣷⣝⢿⣿⣶⣬⣤⣬⣍⣛⠻⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⣉⣩⣴⡶⣫⣷⣿⣿⣿⡿⠀⢂⠐⠀⠀⠀⠂⠄⢂⠡⠈⠄⡀⠀⠀⢠⣿⣿⣿⣿⣿⣷⣾⣭⣂⡹⣿⣿⣿⣿⣿⣿⣿⣶⣷⣦⠍⡙⢿⣿⣿⣿⣿⣿⣿
⣿⣿⠿⠿⢛⣋⣡⣴⣾⣿⣿⣟⢵⣿⣿⣿⣿⣿⣿⠃⢀⠂⠀⠀⠀⠀⠀⠀⠂⠄⡁⢂⠐⡀⢂⣿⣿⣿⣿⣿⣿⣿⠿⢛⣡⣦⣿⣿⣿⣿⣿⣿⣿⢟⣯⣾⣿⡇⢸⣿⣿⣿⣿⣿⣿
⣿⢀⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣆⡉⢿⣿⣿⣿⣿⠀⠆⠀⠀⠀⠀⠀⠀⠀⠀⠆⠰⠀⠆⠀⢸⣿⣿⣿⣿⣿⢿⣱⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⢱⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿
⣿⢀⢿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣛⣻⣥⣭⣿⡿⠃⠀⡀⠂⠀⠀⠀⠀⠀⡀⠄⠀⠂⠐⠦⠀⣿⣿⣿⣿⣿⣁⣛⣛⣛⡿⢿⣿⣿⣿⣿⣿⢫⢰⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿
⣿⢸⡜⣿⣿⣿⣿⢟⡫⠵⣾⣿⣿⣿⡿⣋⣭⢶⠀⡐⠠⠁⠀⠀⠀⠀⢂⠐⡈⠐⠠⢀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣶⡍⡿⣱⢇⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿
⡿⣾⣿⣞⢿⣿⣿⡸⣿⡹⣶⣾⣭⡟⣎⣫⡍⣼⠀⠐⠀⠀⠀⠀⠀⠐⡀⠂⠄⡁⠂⠄⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣥⣼⡿⣱⢣⣿⢾⣿⣿⣿⣿⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿
⢣⣿⣿⣿⣮⢿⣿⣧⢿⣏⢤⣬⣭⣝⠿⣟⡴⡇⠠⢁⠀⠀⠀⠀⠀⠠⢀⠡⢀⠀⠄⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⢻⣿⡿⣱⡇⣾⣿⢸⣿⣿⢿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿
⢰⣿⣿⣿⣿⣧⡓⣿⣎⢿⣷⡎⣥⡾⢻⡏⣟⡧⠁⡀⠀⠀⠀⠀⠀⠐⡀⠂⠄⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣾⢟⡜⣿⢰⣿⣿⡸⣿⣿⡨⡻⣿⣿⣿⡇⢻⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣧⢻⣿⡌⣿⣷⣶⣐⣛⡄⣯⢗⠀⠀⠀⠀⠀⠀⠀⠀⠄⠁⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⡀⣈⣿⢟⣵⢏⣾⡏⣾⣿⣿⣧⢻⣿⣷⡱⣮⡻⣿⣧⠸⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⢼⣿⣿⡞⢿⣿⣿⣿⣷⢻⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⠿⠿⢿⣿⣿⡿⣳⣿⢫⣾⣿⢡⣿⣿⣿⣿⣧⢻⣿⣿⣜⣿⣼⢻⡀⣿⣿⣿⣿⣿
⡿⣿⣿⣿⣿⣿⣿⡧⣿⣿⣿⣎⢿⣿⣿⣿⣧⠛⡆⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣧⣤⣼⡿⣫⣾⢟⣵⣿⣿⡟⢸⣿⣿⣿⣿⣿⣧⢻⣿⣿⣮⡻⣿⡇⢸⣿⣿⣿⣿
⣷⣿⡟⣿⣿⣿⣿⡇⣿⣿⣿⣿⣎⢿⣿⣿⠻⡧⢱⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣯⠒⣨⣿⣿⢟⣳⣾⢿⣱⣾⣿⣿⣿⠇⠈⣿⣿⣿⣿⣿⣿⣷⡹⣿⣿⣷⣝⢿⠀⣿⣿⣿⣿
⣿⢹⡇⣿⣿⣿⣿⡇⣿⣿⡻⠿⢿⣧⡻⣿⣖⣚⣧⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⡿⢟⣫⣶⣿⣯⣴⣿⣿⣿⣿⣿⡿⠀⣦⠸⣿⣿⣿⣿⣿⣿⣿⣎⢿⣿⣿⣷⡄⢸⣿⣿⣿
⣿⢸⣿⢹⣿⣿⣿⡇⢹⣿⣿⣮⡻⣶⣷⣝⢿⣿⡹⣆⠀⠀⠀⠀⢀⣾⣿⣿⣿⡿⣛⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⢸⣿⣇⠹⣿⣿⣿⣿⣿⣿⣿⣷⡹⣿⣿⣿⡈⣿⣿⣿
⣿⢸⣿⡞⣿⣿⣿⡧⠸⣿⣿⣿⣿⣮⣛⠿⣦⡻⣿⣦⡀⠀⠀⠀⣾⣿⡿⢛⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⡿⢀⣿⣿⣿⡄⢻⣿⣿⣿⣿⣿⣿⣿⣿⣎⢻⣿⣇⠸⣿⣿
⣿⢸⣿⣧⢿⣿⣿⣷⡇⢿⣿⣿⣿⣿⣿⣿⣶⣯⣬⡻⣿⡄⠀⣼⡿⣫⠾⠿⣟⣛⣛⣻⣽⣿⣿⣿⣿⡿⣫⣽⣿⣿⣿⠁⣼⣿⣿⣿⣿⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣝⢿⡄⢿⣿
⣿⡆⣿⣿⡘⣿⣿⢺⣧⢈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⣝⠐⢫⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣋⣵⣿⣿⠿⣿⣿⡏⢠⣿⣿⣿⣿⣿⣧⠸⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣮⡳⢸⣿
⣿⡇⣿⣿⡇⣿⣿⢸⣿⢸⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡶⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡹⣇⡈⢹⢿⣿⣿⣿⣿⡀⢿⡿⣉⣱⣶⣶⣀⣈⠿⣿⣿⣿⡆⢿
⣿⣿⣿⣿⣧⢸⣿⢸⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⠇⢃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣻⣽⣿⣿⣷⠄⢻⣿⣿⠟⣁⣴⣾⣿⣿⣿⣿⡿⣫⣵⣿⣿⣿⣿⣸
⣿⣿⣿⣿⣿⠀⢧⣿⣿⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⡈⠁⡀⠠⡍⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣛⣵⣾⣿⣿⠿⠿⣿⣏⣀⠛⢋⣠⣾⣿⣿⣿⣿⣿⢟⣥⣾⣿⣿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⢹⡌⣿⡿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡃⠟⢰⣦⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⣾⣿⣿⣿⡷⢖⣻⣿⣶⣶⣾⠻⢸⣿⢿⣿⣿⡿⢫⣵⣿⣿⣿⣿⣿⣿⣿⣿⡿⢁
⣿⡗⣿⣿⣿⡞⣿⡜⢣⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣱⣿⡿⠟⢉⣵⣾⣿⣿⣿⡿⠟⠉⢄⣛⠿⣮⡿⣫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢠⣿
⣿⣿⣿⣿⣿⡇⣿⡏⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡧⢸⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⣟⡥⣪⣾⣿⣿⣿⣿⡟⡥⢊⣼⣧⡲⡹⣿⠢⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢁⣴⣿⣿
⣿⣿⣿⣿⣿⡇⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⢸⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⢋⣾⣿⣿⣿⣿⣿⢯⡞⠄⣾⣿⣿⣿⡜⡜⣷⢹⣦⣻⣿⣿⣿⣿⡿⠋⣡⣶⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡧⠃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠸⣿⣿⣿⣿⣿⣿⣿⡿⢚⣵⣿⣿⣿⣿⣿⡿⣱⢏⠜⣼⣿⣿⣿⣿⣧⢱⢹⡇⢿⣿⣿⠿⠟⠋⢠⣾⣿⣿⣿⣿⣿⣿

This ASCII Art was made using: https://emojicombos.com/dot-art-generator

-----
Umineko Project - Scripting Update Manager - Core Logic.
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


def inplace_lines(
    data_dir: str, in_dir: str, by_dir: str, replace_grim: bool = False
) -> str:
    """Process script lines in place."""
    buffer: str = ""

    if (
        not os.path.exists(data_dir)
        or not os.path.exists(in_dir)
        or not os.path.exists(by_dir)
    ):
        utils.err("Invalid directory(ies)")

    # Get the scripts_in
    scripts_in: list[str] = [f for f in os.listdir(in_dir) if f.endswith(".txt")]
    scripts_in.sort()

    # Get the scripts_by
    scripts_by: list[str] = [f for f in os.listdir(by_dir) if f.endswith(".txt")]
    scripts_by.sort()

    # Get the data_in - Commented out as I feel this is redundant code.
    # data_in: list[str] = os.listdir(data_dir)
    # data_in = data_in[2:]  # Remove first two entries (usually '.' and '..')

    # # Keep only files that end with '.txt'
    # data_in = [file for file in data_in if file.endswith('txt')]

    # # Flip: filename => index
    # data_in: dict[str, int] = {file: idx for idx, file in enumerate(data_in)}

    if len(scripts_in) != len(scripts_by):
        utils.err("Invalid data in dirs")

    tmp_guid: str = utils.generate_guid()

    scripts: dict[str, str] = dict(zip(scripts_in, scripts_by))
    scripts = dict(
        sorted(scripts.items(), key=lambda x: cmp_to_key(utils.str_nat_sort)(x[0]))
    )

    for in_file, by_file in scripts.items():
        try:
            with open(os.path.join(in_dir, in_file), "r", encoding="utf-8") as f:
                data_in_content: str = f.read().strip()
        except Exception:
            continue

        try:
            with open(os.path.join(by_dir, by_file), "r", encoding="utf-8") as f:
                data_by_content: str = f.read().strip()
        except Exception:
            continue

        try:
            with open(os.path.join(data_dir, in_file), "r", encoding="utf-8") as f:
                text: str = f.read().strip()
        except Exception:
            continue

        if replace_grim:
            text = utils.remove_grim(text)

        if data_in_content and data_by_content and text:
            data_in_lines: list[str] = data_in_content.split(const.LF)
            data_by_lines: list[str] = data_by_content.split(const.LF)

            for i in range(len(data_in_lines)):
                if i >= len(data_in_lines):
                    print(
                        f"Missing data_in of {i} in {in_file} for {data_by_lines[i] if i < len(data_by_lines) else ''}"
                    )
                    continue

                if i >= len(data_by_lines):
                    print(f"Missing data_by of {i} in {by_file} for {data_in_lines[i]}")
                    continue

                # Fix first and last `s, also spaces, and double replacement
                data_in_lines[i] = data_in_lines[i].strip()
                data_by_lines[i] = data_by_lines[i].strip()

                line_grim: str | None = None
                if replace_grim:
                    match: Match[str] | None = re.search(
                        r"\[gstg \d+\]", data_by_lines[i]
                    )
                    if match:
                        line_grim = match.group(0)
                    data_by_lines[i] = re.sub(r"\[gstg \d+\]", "", data_by_lines[i])

                # Handle backticks
                if data_by_lines[i].startswith("`"):
                    data_by_lines[i] = "`" + tmp_guid + data_by_lines[i][1:]
                else:
                    data_by_lines[i] = "`" + tmp_guid + data_by_lines[i]

                if not data_by_lines[i].endswith("`"):
                    data_by_lines[i] += "`"

                if replace_grim and line_grim:
                    data_by_lines[i] += line_grim

                text = utils.str_replace_first(data_in_lines[i], data_by_lines[i], text)

        text = text.replace(tmp_guid, "")
        buffer += text + const.LF
    return buffer


def hash_dir(directory, base, hash_map, hash_type) -> None:
    """Recursively hash files in directory."""
    if not os.path.isdir(directory):
        utils.err(f"No such directory {directory}")

    for item in os.listdir(directory):
        item_path: str = os.path.join(directory, item)
        if os.path.isdir(item_path):
            hash_dir(item_path, base, hash_map, hash_type)
        else:
            relative_path: str = os.path.relpath(item_path, base).replace("\\", "/")
            hash_value: str = ""

            if hash_type == "md5":
                hash_value_md5: HASH = hashlib.md5()
                with open(item_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_value_md5.update(chunk)
                hash_value = hash_value_md5.hexdigest()
            elif hash_type == "adler":
                with open(item_path, "rb") as f:
                    content: bytes = f.read()
                hash_value = format(zlib.adler32(content) & 0xFFFFFFFF, "08x")
            elif hash_type == "size":
                hash_value = str(os.path.getsize(item_path))
            else:
                # This should not happen as `hash_type` is validated before it is called in this function.
                utils.err(f"Unknown hash type: {hash_type}")

            hash_map["/" + relative_path] = hash_value


def filtered_ini_create(hashes: dict[str, str], mode: str) -> str:
    """Create filtered INI output."""
    output: str = "[info]" + const.CRLF
    output += '"game"="UminekoPS3fication*"' + const.CRLF
    output += f'"hash"="{mode}"' + const.CRLF
    output += '"ver"="20190109-ru"' + const.CRLF
    output += '"apiver"="2.2.0"' + const.CRLF
    output += '"date"="ignore"' + const.CRLF
    output += "[data]" + const.CRLF

    for file_path, hash_value in hashes.items():
        if not utils.has_in(file_path, exclude) and "game.hash" not in file_path:
            if file_path.startswith("/"):
                file_path = file_path[1:]
            output += f'"{file_path}"="{hash_value}"' + const.CRLF

    return output


def compare_hashes(
    old_hashes: dict[str, str], new_hashes: dict[str, str]
) -> utils.HashDiff:
    """Compares old and new hashes and returns the differences."""
    out: utils.HashDiff = {"differences": {}, "deletions": [], "additions": {}}

    for old_file, old_hash in old_hashes.items():
        # Avoid any temporary files
        if utils.has_in(old_file, exclude) and old_file in new_hashes:
            del new_hashes[old_file]

        force_include: bool = utils.has_in(old_file, include)

        if old_file in new_hashes or force_include:
            # Has change
            if new_hashes.get(old_file) != old_hash or force_include:
                clean_file = re.sub(r"^[/\\]", "", old_file)
                out["differences"][clean_file] = new_hashes.get(old_file, old_hash)
            if old_file in new_hashes:
                del new_hashes[old_file]
        else:
            # Redundant file
            clean_file = re.sub(r"^[/\\]", "", old_file)
            out["deletions"].append(clean_file)

    # Process remaining new files
    for new_file, new_hash in list(new_hashes.items()):
        if not utils.has_in(new_file, exclude):
            clean_file = re.sub(r"^[/\\]", "", new_file)
            out["additions"][clean_file] = new_hash

    return out


def localise_script(script: str, locale_dir: str) -> str:
    """Localise script by importing locale files."""
    lstart = '#locale_import "'
    lend = '"'

    while True:
        script = script  # This line does nothing, but it helps resolve PyreFly false-positives!
        start: int = script.find(lstart)
        if start == -1:
            break

        end: int = script.find(lend, start + len(lstart))
        if end == -1:
            break

        file_name: str = script[start + len(lstart) : end]

        if not re.match(r"^[a-z0-9_]+\.txt$", file_name, re.IGNORECASE):
            break

        try:
            with open(os.path.join(locale_dir, file_name), "r", encoding="utf-8") as f:
                dst: str = f.read().replace(const.CRLF, const.LF)
            script = script[:start] + dst + script[end + len(lend) :]
        except Exception:
            break

    return script


def filter_script(script: str, ep: int) -> str:
    """Filter script based on episode number."""
    if ep < 1:
        utils.err("Invalid episode number")

    incomplete: str = utils.generate_incomplete(ep + 1)

    start_pattern: str = f"*umi{ep + 1}_op"
    start: int = script.find(start_pattern)

    if start != -1:
        end_pattern1 = "ura_8_end\ngoto *end_game"
        end_pattern2 = "ura_8_end\r\ngoto *end_game"

        end: int = script.find(end_pattern1, start)
        if end == -1:
            end = script.find(end_pattern2, start)
            end_len: int = len(end_pattern2)
        else:
            end_len = len(end_pattern1)

        if end != -1:
            script = script[:start] + incomplete + script[end + end_len :]

    script = script.replace(".txt", ".file")
    return script


def encode_script(data: str) -> bytes:
    """Encode script with header."""
    data_as_bytes: bytes = data.encode("utf-8")

    out_size: int = len(data_as_bytes)
    transformed_data: bytes = utils.transform_script(data_as_bytes)

    # Create header
    header: bytes = const.MAGIC.encode("ascii")
    header += struct.pack("<LLL", len(transformed_data), out_size, const.VERSION)

    return header + transformed_data
