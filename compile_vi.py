#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vietnamese Language Compilation Script for Umineko Project

This script compiles only the Vietnamese language files using the Python update_manager.
"""

import os
import sys
import subprocess
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

# Add the current directory to the path so we can import update_manager
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'update-manager'))

try:
    import update_manager
except ImportError:
    print("Error: Could not import update_manager.py")
    print("Make sure update_manager.py is in the update-manager directory")
    sys.exit(1)


def get_build_number():
    """Calculate build number using git rev-list count + 3500"""
    try:
        result = subprocess.run(
            ['git', 'rev-list', '--count', '--first-parent', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        git_count = int(result.stdout.strip())
        return git_count + 3500
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: Could not get git revision count, using default build number")
        return 3500


def load_last_episode(file_path, default_last):
    """Load last episode number from file, return default if file doesn't exist"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return content if content else str(default_last)
    except FileNotFoundError:
        return str(default_last)


def compile_vietnamese():
    """Compile Vietnamese language scripts"""
    print("Starting Vietnamese compilation...")
    
    # Setup
    build_number = get_build_number()
    today = datetime.now().strftime("%d.%m.%y")
    output_dir = 'ciout'
    
    print(f"Build number: {build_number}")
    print(f"Date: {today}")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Load last episode number for Vietnamese
    default_last = load_last_episode('current/last', '8')
    last_vi = load_last_episode('current/last_vi', default_last)
    
    print(f"Last Vietnamese episode: {last_vi}")
    
    # Step 1: Generate Vietnamese text script using dscript
    print("Generating Vietnamese text script...")
    output_txt = os.path.join(output_dir, "vi.txt")
    
    try:
        # Save original argv to restore later
        original_argv = sys.argv[:]
        
        # Simulate: php update-manager.php dscript "ciout/vi.txt" . vi BUILD
        sys.argv = ['update_manager.py', 'dscript', output_txt, '.', 'vi', str(build_number)]
        update_manager.main()
        
        # Restore original argv
        sys.argv = original_argv[:]
        
        print(f"✓ Generated {output_txt}")
    except SystemExit as e:
        sys.argv = original_argv[:]
        if e.code != 0:
            print(f"✗ Error generating {output_txt}")
            return False
    except Exception as e:
        sys.argv = original_argv[:]
        print(f"✗ Error generating {output_txt}: {e}")
        return False
    
    # Step 2: Copy required config files
    print("Copying configuration files...")
    config_files = [
        ('misc/chiru.file', os.path.join(output_dir, 'chiru.file')),
        ('misc/game.hash', os.path.join(output_dir, 'game.hash')),
        ('misc/default.cfg', os.path.join(output_dir, 'default.cfg'))
    ]
    
    for src, dst in config_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✓ Copied {src} to {dst}")
        else:
            print(f"⚠ Warning: {src} not found")
    
    # Step 3: Create development ZIP with .txt file
    print("Creating development ZIP file...")
    dev_zip_files = [
        os.path.join(output_dir, 'vi.txt'),
        os.path.join(output_dir, 'chiru.file'),
        os.path.join(output_dir, 'game.hash'),
        os.path.join(output_dir, 'default.cfg')
    ]
    
    dev_zip_path = os.path.join(output_dir, f'umineko-vi-scripts_r{build_number}_dev.zip')
    
    try:
        with zipfile.ZipFile(dev_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in dev_zip_files:
                if os.path.exists(file_path):
                    zipf.write(file_path, os.path.basename(file_path))
                    print(f"✓ Added {os.path.basename(file_path)} to dev ZIP")
        print(f"✓ Created {dev_zip_path}")
    except Exception as e:
        print(f"✗ Error creating development ZIP: {e}")
        return False
    
    # Step 4: Generate Vietnamese binary script using script command
    print("Generating Vietnamese binary script...")
    output_file = os.path.join(output_dir, "vi.file")
    
    try:
        # Save original argv
        original_argv = sys.argv[:]
        
        # Simulate: php update-manager.php script ciout/vi.txt "ciout/vi.file" "LAST_VI"
        sys.argv = ['update_manager.py', 'script', output_txt, output_file, last_vi]
        update_manager.main()
        
        # Restore original argv
        sys.argv = original_argv[:]
        
        print(f"✓ Generated {output_file}")
    except SystemExit as e:
        sys.argv = original_argv[:]
        if e.code != 0:
            print(f"✗ Error generating {output_file}")
            return False
    except Exception as e:
        sys.argv = original_argv[:]
        print(f"✗ Error generating {output_file}: {e}")
        return False
    
    # Step 5: Create release ZIP with .file
    print("Creating release ZIP file...")
    release_zip_files = [
        os.path.join(output_dir, 'vi.file'),
        os.path.join(output_dir, 'chiru.file'),
        os.path.join(output_dir, 'game.hash'),
        os.path.join(output_dir, 'default.cfg')
    ]
    
    release_zip_path = os.path.join(output_dir, f'umineko-vi-scripts_r{build_number}.zip')
    
    try:
        with zipfile.ZipFile(release_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in release_zip_files:
                if os.path.exists(file_path):
                    zipf.write(file_path, os.path.basename(file_path))
                    print(f"✓ Added {os.path.basename(file_path)} to release ZIP")
        print(f"✓ Created {release_zip_path}")
    except Exception as e:
        print(f"✗ Error creating release ZIP: {e}")
        return False
    
    print("\n🎉 Vietnamese compilation completed successfully!")
    print(f"\nOutput files:")
    print(f"  Text script: {output_txt}")
    print(f"  Binary script: {output_file}")
    print(f"  Development ZIP: {dev_zip_path}")
    print(f"  Release ZIP: {release_zip_path}")
    
    return True


if __name__ == '__main__':
    if not compile_vietnamese():
        sys.exit(1)
    sys.exit(0)
