#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Umineko Project update manager
Encoding: UTF-8

Copyright (c) 2011-2019 Umineko Project

This document is considered confidential and proprietary,
and may not be reproduced or transmitted in any form 
in whole or in part, without the express written permission
of Umineko Project.
"""

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
import secrets
from functools import cmp_to_key
from pathlib import Path

# Constants
LF = '\n'
CRLF = '\r\n'
DS = '/'  # DIRECTORY_SEPARATOR
TAB = '\t'
MAGIC = 'ONS2'
VERSION = 110
MAX_IN = 0x10000000
UPDATE_MANAGER = True
PASSWORD = '035646750436634546568555050'
REPLACE_GRIM_WITH_LOCALIZE = ['cn', 'cht']

exclude = [
    '.DS_Store',
    'thumbs.db',
    'Thumbs.db',
    'umi_scr',
    'dlls',
    'onscripter-ru',
    '/en.txt',
    '/ru.txt',
    '/pt.txt',
    '/cn.txt',
    '/cht.txt',
    '/test.txt',
    'gmon.out',
    'head.png',
    'ons.cfg',
    '_shine.png',
    'shine.png',
    'script.file',
    'language_pt',
    'language_cn',
    'language_cht',
    '/en.file',
    '/ru.file',
    '/pt.file',
    '/pt.cfg',
    '/cn.file',
    '/cn.cfg',
    '/cht.file',
    '/cht.cfg',
    '/chiru.file',
    '/game.hash',
    '/default.cfg'
]

include = []


def err(message):
    """Print error message and exit."""
    print(message)
    sys.exit(0)


def get_usage():
    """Return usage string."""
    return (
        'Usage options:\n'
        '\tpython update_manager.py hash directory hashfile\n'
        '\tpython update_manager.py adler directory hashfile\n'
        '\tpython update_manager.py size directory hashfile\n'
        '\tpython update_manager.py verify old_hash_file new_hashfile [update.file json/ini]\n'
        '\tpython update_manager.py dscript script_file scripting_folder locale\n'
        '\tpython update_manager.py script script_file new_script last_episode\n'
        '\tpython update_manager.py update update_file source_folder new_folder [archive_prefix]\n'
    )


def str_replace_first(search, replace, subject):
    """Replace first occurrence of search string with replace string."""
    parts = subject.split(search, 1)
    if len(parts) == 2:
        return replace.join(parts)
    return subject


def str_nat_sort(str1, str2):
    """Natural sort comparison function."""
    if str1[:4] == str2[:4]:
        if 'op' in str1:
            return -1
        elif 'op' in str2:
            return 1
        elif str1 == str2:
            return 0
    
    # Simple natural comparison
    import re
    
    def natural_key(text):
        return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]
    
    key1, key2 = natural_key(str1), natural_key(str2)
    return (key1 > key2) - (key1 < key2)


def extract_guid(data):
    """Extract GUID from bytes."""
    if not data:
        return None
    
    hex_data = data.hex()
    return hex_data.ljust(32, '0')


def generate_guid():
    """Generate a random GUID."""
    try:
        return extract_guid(secrets.token_bytes(16))
    except:
        return 'ea5078d1f71c405887bd54994bfeff24'


def inplace_lines(data_dir, in_dir, by_dir, replace_grim=False):
    """Process script lines in place."""
    buffer = ''
    
    if not os.path.exists(data_dir) or not os.path.exists(in_dir) or not os.path.exists(by_dir):
        err('Invalid directory(ies)')
    
    # Get the scripts_in
    scripts_in = [f for f in os.listdir(in_dir) if f.endswith('.txt')]
    scripts_in.sort()
    
    # Get the scripts_by
    scripts_by = [f for f in os.listdir(by_dir) if f.endswith('.txt')]
    scripts_by.sort()
    
    # Get the data_in
    data_in_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
    data_in = {f: True for f in data_in_files}
    
    if len(scripts_in) != len(scripts_by):
        err('Invalid data in dirs')
    
    tmp_guid = generate_guid()
    
    scripts = dict(zip(scripts_in, scripts_by))
    scripts = dict(sorted(scripts.items(), key=lambda x: cmp_to_key(str_nat_sort)(x[0])))
    
    for in_file, by_file in scripts.items():
        try:
            with open(os.path.join(in_dir, in_file), 'r', encoding='utf-8') as f:
                data_in_content = f.read().strip()
        except:
            continue
            
        try:
            with open(os.path.join(by_dir, by_file), 'r', encoding='utf-8') as f:
                data_by_content = f.read().strip()
        except:
            continue
            
        try:
            with open(os.path.join(data_dir, in_file), 'r', encoding='utf-8') as f:
                text = f.read().strip()
        except:
            continue
        
        if replace_grim:
            text = remove_grim(text)
        
        if data_in_content and data_by_content and text:
            data_in_lines = data_in_content.split(LF)
            data_by_lines = data_by_content.split(LF)
            
            for i in range(len(data_in_lines)):
                if i >= len(data_in_lines):
                    print(f'Missing data_in of {i} in {in_file} for {data_by_lines[i] if i < len(data_by_lines) else ""}')
                    continue
                
                if i >= len(data_by_lines):
                    print(f'Missing data_by of {i} in {by_file} for {data_in_lines[i]}')
                    continue
                
                # Fix first and last `s, also spaces, and double replacement
                data_in_lines[i] = data_in_lines[i].strip()
                data_by_lines[i] = data_by_lines[i].strip()
                
                line_grim = None
                if replace_grim:
                    match = re.search(r'\[gstg \d+\]', data_by_lines[i])
                    if match:
                        line_grim = match.group(0)
                    data_by_lines[i] = re.sub(r'\[gstg \d+\]', '', data_by_lines[i])
                
                # Handle backticks
                if data_by_lines[i].startswith('`'):
                    data_by_lines[i] = '`' + tmp_guid + data_by_lines[i][1:]
                else:
                    data_by_lines[i] = '`' + tmp_guid + data_by_lines[i]
                
                if not data_by_lines[i].endswith('`'):
                    data_by_lines[i] += '`'
                
                if replace_grim and line_grim:
                    data_by_lines[i] += line_grim
                
                text = str_replace_first(data_in_lines[i], data_by_lines[i], text)
        
        text = text.replace(tmp_guid, '')
        buffer += text + LF
    
    return buffer


def hash_dir(directory, base, hash_map, hash_type):
    """Recursively hash files in directory."""
    if not os.path.isdir(directory):
        err(f'No such directory {directory}')
    
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            hash_dir(item_path, base, hash_map, hash_type)
        else:
            relative_path = os.path.relpath(item_path, base).replace('\\', '/')
            
            if hash_type == 'adler':
                with open(item_path, 'rb') as f:
                    content = f.read()
                hash_value = format(zlib.adler32(content) & 0xffffffff, '08x')
            elif hash_type == 'size':
                hash_value = os.path.getsize(item_path)
            else:  # md5
                hash_value = hashlib.md5()
                with open(item_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_value.update(chunk)
                hash_value = hash_value.hexdigest()
            
            hash_map['/' + relative_path] = hash_value


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
    output = '[info]' + CRLF
    output += '"game"="UminekoPS3fication*"' + CRLF
    output += f'"hash"="{mode}"' + CRLF
    output += '"ver"="20190109-ru"' + CRLF
    output += '"apiver"="2.2.0"' + CRLF
    output += '"date"="ignore"' + CRLF
    output += '[data]' + CRLF
    
    for file_path, hash_value in hashes.items():
        if not has_in(file_path, exclude) and 'game.hash' not in file_path:
            if file_path.startswith('/'):
                file_path = file_path[1:]
            output += f'"{file_path}"="{hash_value}"' + CRLF
    
    return output


def compare_hashes(old_hashes, new_hashes):
    """Compare two hash dictionaries and return differences."""
    out = {
        'different': {},
        'delete': [],
        'insert': {}
    }
    
    for old_file, old_hash in old_hashes.items():
        # Avoid any temporary files
        if has_in(old_file, exclude) and old_file in new_hashes:
            del new_hashes[old_file]
        
        force_include = has_in(old_file, include)
        
        if old_file in new_hashes or force_include:
            # Has change
            if new_hashes.get(old_file) != old_hash or force_include:
                clean_file = re.sub(r'^[/\\]', '', old_file)
                out['different'][clean_file] = new_hashes.get(old_file, old_hash)
            if old_file in new_hashes:
                del new_hashes[old_file]
        else:
            # Redundant file
            clean_file = re.sub(r'^[/\\]', '', old_file)
            out['delete'].append(clean_file)
    
    # Process remaining new files
    for new_file, new_hash in list(new_hashes.items()):
        if not has_in(new_file, exclude):
            clean_file = re.sub(r'^[/\\]', '', new_file)
            out['insert'][clean_file] = new_hash
    
    return out


def generate_incomplete(ep):
    """Generate incomplete episode script."""
    num = {
        1: 17, 2: 18, 3: 18, 4: 19,
        5: 15, 6: 18, 7: 18, 8: 16
    }
    
    out = ''
    
    for i in range(ep, 9):
        out += f'*umi{i}_op{CRLF}jskip_s goto *incomplete ~{CRLF}'
        for j in range(1, num[i] + 1):
            out += f'*umi{i}_{j}{CRLF}jskip_s goto *incomplete ~{CRLF}'
        out += f'*umi{i}_end{CRLF}*teatime_{i}{CRLF}jskip_s goto *incomplete ~{CRLF}*teatime_{i}_end{CRLF}*ura_teatime_{i}{CRLF}jskip_s goto *incomplete ~{CRLF}*ura_{i}_end{CRLF}'
    
    return out


def filter_script(script, ep):
    """Filter script based on episode number."""
    if not ep.isdigit() or int(ep) < 1:
        err('Invalid episode number')
    
    ep = int(ep)
    incomplete = generate_incomplete(ep + 1)
    
    start_pattern = f'*umi{ep + 1}_op'
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
            script = script[:start] + incomplete + script[end + end_len:]
    
    script = script.replace('.txt', '.file')
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
        
        file_name = script[start + len(lstart):end]
        
        if not re.match(r'^[a-z0-9_]+\.txt$', file_name, re.IGNORECASE):
            break
        
        try:
            with open(os.path.join(locale_dir, file_name), 'r', encoding='utf-8') as f:
                dst = f.read().replace(CRLF, LF)
            script = script[:start] + dst + script[end + len(lend):]
        except:
            break
    
    return script


def xor_data(data, pass_num):
    """XOR data with key table."""
    key_table = [
        0xc0, 0xbc, 0x86, 0x66, 0x84, 0xf3, 0xbe, 0x90, 0xb0, 0x02, 0x98, 0x5e, 0x0f, 0x9c, 0x7b, 0xf4,
        0xd9, 0x91, 0xdb, 0xeb, 0x81, 0x74, 0x3a, 0xe3, 0x76, 0x94, 0x21, 0x93, 0x63, 0x68, 0x0d, 0xa1,
        0xba, 0xaa, 0x1b, 0xa0, 0x49, 0x2b, 0xe1, 0xe7, 0x38, 0xa6, 0x25, 0x53, 0x40, 0x4a, 0xec, 0x29,
        0x36, 0xbf, 0xf2, 0x9f, 0xac, 0x0c, 0xcb, 0x00, 0x1f, 0xf1, 0x7c, 0x80, 0x4f, 0x60, 0x82, 0x62,
        0x14, 0x6d, 0xd8, 0x32, 0x13, 0x2f, 0xe0, 0x99, 0xf7, 0x10, 0xd1, 0x30, 0x64, 0x4e, 0x8c, 0xde,
        0xc1, 0x6a, 0xad, 0xa7, 0xb5, 0x95, 0xcf, 0xc6, 0x0b, 0x2d, 0x69, 0x24, 0x5c, 0xc5, 0x03, 0xda,
        0xd6, 0x8e, 0xa3, 0x88, 0x31, 0x17, 0x3c, 0xb3, 0xa8, 0xb4, 0x01, 0x0e, 0xfc, 0x37, 0x65, 0x16,
        0x6c, 0xbb, 0x50, 0x55, 0x2a, 0xe5, 0x77, 0x97, 0x09, 0xb1, 0x04, 0x67, 0xc7, 0x79, 0x71, 0x7a,
        0x43, 0xd0, 0x22, 0x58, 0x0a, 0x57, 0xb7, 0xae, 0x4d, 0xc8, 0xe9, 0x46, 0xd3, 0x5b, 0x96, 0xcc,
        0x3f, 0xe6, 0x3e, 0x54, 0x5f, 0x1d, 0xfa, 0xf0, 0x3d, 0x7d, 0x83, 0xa5, 0xfd, 0xef, 0x15, 0x8b,
        0x70, 0x6b, 0xe2, 0xff, 0x07, 0xd7, 0x92, 0x41, 0x61, 0x75, 0x6f, 0x7f, 0xc4, 0xd5, 0xf9, 0x05,
        0x34, 0xfe, 0x5d, 0xdc, 0xb9, 0xe8, 0xab, 0xca, 0xc3, 0x35, 0x08, 0x3b, 0xa2, 0xbd, 0x8f, 0x7e,
        0x2e, 0x44, 0x5a, 0x12, 0xed, 0xe4, 0x11, 0x1e, 0xc2, 0x78, 0xf5, 0xaf, 0xf6, 0x72, 0x28, 0x9d,
        0x6e, 0x39, 0xd2, 0xea, 0x45, 0x73, 0x47, 0x9e, 0x26, 0x89, 0x85, 0x52, 0x33, 0xdf, 0xa4, 0x48,
        0x23, 0xce, 0x1c, 0x8d, 0x18, 0x27, 0x9a, 0xb6, 0xa9, 0xee, 0xb8, 0xc9, 0x2c, 0xfb, 0x59, 0x56,
        0x20, 0x42, 0xcd, 0x51, 0xb2, 0x06, 0x19, 0x4b, 0x9b, 0xd4, 0x8a, 0x4c, 0xf8, 0x87, 0x1a, 0xdd
    ]
    
    if not data:
        err('Nothing to xor')
    
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
        data = data.encode('utf-8')
    
    # First pass
    result = b''
    chunk_size = 131072
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        result += xor_data(chunk, 1)
    
    # Compress
    compressed = zlib.compress(result, 9)
    
    # Second pass
    result = b''
    for i in range(0, len(compressed), chunk_size):
        chunk = compressed[i:i + chunk_size]
        result += xor_data(chunk, 2)
    
    return result


def encode_script(data):
    """Encode script with header."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    out_size = len(data)
    transformed_data = transform_script(data)
    
    # Create header
    header = MAGIC.encode('ascii')
    header += struct.pack('<LLL', len(transformed_data), out_size, VERSION)
    
    return header + transformed_data


def remove_grim(text):
    """Remove grim formatting from text."""
    # Remove color formatting
    text = re.sub(r'\{c:86EF9C:(.*?)\}', r'\1', text)
    # Remove gstg tags
    text = re.sub(r'\[gstg \d+\]', '', text)
    return text


def main():
    """Main function."""
    argc = len(sys.argv)
    argv = sys.argv
    
    if argc < 2:
        err(get_usage())
    
    command = argv[1]
    
    if command in ['hash', 'adler', 'size']:
        if argc < 4:
            err(get_usage())
        
        hashes = {}
        hash_dir(argv[2], argv[2], hashes, command)
        
        if command == 'hash':
            output = json.dumps(hashes, indent=2)
        else:
            output = filtered_ini_create(hashes, command)
        
        with open(argv[3], 'w', encoding='utf-8') as f:
            f.write(output)
    
    elif command == 'verify':
        if argc < 4:
            err(get_usage())
        
        if not os.path.exists(argv[2]):
            err(f'No such file {argv[2]}')
        if not os.path.exists(argv[3]):
            err(f'No such file {argv[3]}')
        
        with open(argv[2], 'r', encoding='utf-8') as f:
            old_hashes = json.load(f)
        with open(argv[3], 'r', encoding='utf-8') as f:
            new_hashes = json.load(f)
        
        modifications = compare_hashes(old_hashes, new_hashes)
        
        fixture = ''
        for sect, content in modifications.items():
            fixture += CRLF + f'[{sect}]' + CRLF
            for key, value in content.items():
                if isinstance(key, int) or key.isdigit():
                    fixture += f'"{value}"="DO"' + CRLF
                else:
                    fixture += f'"{key}"="{value}"' + CRLF
        
        fixture += CRLF + '[update]' + CRLF + f'"hash"="{hashlib.md5(fixture.encode()).hexdigest()}"' + CRLF + CRLF
        
        if argc > 5:
            output = json.dumps(modifications) if len(argv) > 5 and argv[5] == 'json' else fixture
            with open(argv[4], 'w', encoding='utf-8') as f:
                f.write(output)
        else:
            print(fixture)
    
    elif command == 'dscript':
        if argc < 5:
            err(get_usage())
        
        ver = '8.3b' + (f' r{argv[5]}' if argc > 5 else '')
        locale = argv[4]
        gameid = f'UminekoPS3fication{locale.capitalize()}'
        scripting = argv[3]
        
        # Read header
        with open(os.path.join(scripting, 'script', 'umi_hdr.txt'), 'r', encoding='utf-8') as f:
            script = f.read() + LF
        
        script = script.replace(CRLF, LF)
        script = script.replace('builder_id', gameid)
        script = script.replace('builder_date', str(int(time.time())))
        script = script.replace('builder_localisation', locale)
        script = script.replace('builder_version', ver)
        
        # Process episodes 1-8
        for i in range(1, 9):
            tldir = os.path.join(scripting, 'story', f'ep{i}', locale)
            if not os.path.isdir(tldir):
                tldir = os.path.join(scripting, 'story', f'ep{i}', 'en')
            
            script += inplace_lines(
                os.path.join(scripting, 'game', 'main'),
                os.path.join(scripting, 'story', f'ep{i}', 'jp'),
                tldir,
                locale in REPLACE_GRIM_WITH_LOCALIZE
            )
        
        # Process omake
        script += inplace_lines(
            os.path.join(scripting, 'game', 'omake'),
            os.path.join(scripting, 'story', 'omake', 'jp'),
            os.path.join(scripting, 'story', 'omake', locale)
        )
        
        # Read footer
        footer_path = os.path.join(scripting, 'script', 'umi_ftr.txt')
        if locale == 'cn':
            footer_path = os.path.join(scripting, 'script', 'cn', 'umi_ftr.txt')
        elif locale == 'cht':
            footer_path = os.path.join(scripting, 'script', 'cht', 'umi_ftr.txt')
        elif locale == 'tr':
            footer_path = os.path.join(scripting, 'script', 'tr', 'umi_ftr.txt')
        
        with open(footer_path, 'r', encoding='utf-8') as f:
            footer = f.read()
        
        script += footer.replace(CRLF, LF)
        
        # Localise script
        script = localise_script(script, os.path.join(scripting, 'script', locale))
        
        with open(argv[2], 'w', encoding='utf-8') as f:
            f.write(script)
    
    elif command == 'script':
        if argc < 5:
            err(get_usage())
        
        if not os.path.exists(argv[2]):
            err(f'No such file {argv[2]}')
        
        with open(argv[2], 'r', encoding='utf-8') as f:
            script = f.read()
        
        script = filter_script(script, argv[4])
        encoded = encode_script(script)
        
        with open(argv[3], 'wb') as f:
            f.write(encoded)
    
    elif command == 'update':
        if argc < 5:
            err(get_usage())
        
        with open(argv[2], 'r', encoding='utf-8') as f:
            update = json.load(f)
        
        if not os.path.isdir(argv[3]):
            err(f'No source dir {argv[3]}')
        
        if not os.path.isdir(argv[4]):
            os.makedirs(argv[4], 0o755, exist_ok=True)
        
        for sect, content in update.items():
            if sect not in ['insert', 'different']:
                continue
            
            for file_path, file_hash in content.items():
                dir_path = os.path.join(argv[4], os.path.dirname(file_path))
                if not os.path.isdir(dir_path):
                    os.makedirs(dir_path, 0o755, exist_ok=True)
                shutil.copy2(os.path.join(argv[3], file_path), os.path.join(argv[4], file_path))
        
        if argc > 5:
            import datetime
            archive = f"{argv[5]}_{datetime.datetime.now().strftime('%d.%m.%y')}.7z"
            folder = os.path.join(argv[4], '*')
            
            cmd = [
                '7z', 'a', archive, '-t7z', '-m0=lzma2', '-mx=9', '-mfb=64',
                '-md=128m', '-ms=on', '-mhe', '-v1023m', f'-p{PASSWORD}', folder
            ]
            subprocess.run(cmd)
            shutil.rmtree(argv[4])
    
    else:
        err(get_usage())


if __name__ == '__main__':
    main()
