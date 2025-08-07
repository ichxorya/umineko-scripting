# Vietnamese Update Manager Scripts for Umineko Project

This directory contains Python scripts that invoke the update manager specifically for Vietnamese (vi) language processing, replicating the functionality found in the GitHub Actions workflow.

## Files

### 1. `invoke_vi_update_manager.py`
A basic Python script that performs the core Vietnamese update manager operations:
- Generates Vietnamese script files using the `dscript` command
- Creates filtered Vietnamese script files using the `script` command
- Reads the last episode number from `current/last_vi` file

#### Usage
```bash
python invoke_vi_update_manager.py [build_number]
```

#### Examples
```bash
# Use default build number (3500)
python invoke_vi_update_manager.py

# Use custom build number
python invoke_vi_update_manager.py 3600
```

### 2. `invoke_vi_update_manager_advanced.py`
An advanced Python script with comprehensive Vietnamese language processing capabilities:
- All functionality from the basic script
- Configuration file copying
- ZIP file creation for distribution
- File verification and validation
- Cleanup operations
- Command-line argument parsing

#### Usage
```bash
python invoke_vi_update_manager_advanced.py [options]
```

#### Options
- `--build-number NUMBER`: Specify build number (default: 3500)
- `--create-zip`: Create zip files for distribution
- `--cleanup`: Clean up intermediate files after processing
- `--output-dir DIR`: Specify output directory (default: ciout)
- `--help`: Show help message

#### Examples
```bash
# Basic run with default settings
python invoke_vi_update_manager_advanced.py

# Run with custom build number and create zip files
python invoke_vi_update_manager_advanced.py --build-number 3600 --create-zip

# Run with custom output directory and cleanup
python invoke_vi_update_manager_advanced.py --output-dir output --cleanup
```

### 3. `run_vi_update_manager.bat`
A Windows batch script that provides an interactive menu for running the Vietnamese update manager scripts.

#### Usage
Simply double-click the batch file or run from command prompt:
```cmd
run_vi_update_manager.bat
```

The script will present a menu with the following options:
1. Run basic Vietnamese update manager
2. Run advanced Vietnamese update manager (no zip)
3. Run advanced Vietnamese update manager (with zip files)
4. Run with custom build number
5. Exit

## Prerequisites

### Required Software
- **Python 3.6+**: For running the Python scripts
- **PHP**: Required for the update manager (update-manager.php)
- **zip** (optional): For creating distribution zip files

### Required Files
The scripts expect to be run from the Umineko project root directory and require:
- `update-manager/update-manager.php`
- `current/last_vi` (will default to "1" if missing)
- Various script and configuration files in the project structure

## Output Files

All scripts generate output files in the `ciout` directory (or custom directory if specified):

### Generated Files
- `vi.txt`: Vietnamese script in text format (intermediate file)
- `vi.file`: Vietnamese script in encoded format (final output)
- `vi.cfg`: Configuration file for Vietnamese language

### Optional Zip Files (with --create-zip)
- `umineko-vi-scripts_r{BUILD}_dev.zip`: Development version with .txt file
- `umineko-vi-scripts_r{BUILD}.zip`: Release version with .file

## How It Works

The scripts replicate the Vietnamese language processing from the GitHub Actions workflow:

1. **Script Generation** (`dscript` command):
   ```bash
   php update-manager/update-manager.php dscript "ciout/vi.txt" . vi {BUILD}
   ```

2. **Script Filtering** (`script` command):
   ```bash
   php update-manager/update-manager.php script ciout/vi.txt "ciout/vi.file" "{LAST_VI}"
   ```

3. **Configuration Copying**: Copy Vietnamese or default configuration files

4. **ZIP Creation** (optional): Package files for distribution

## Workflow Integration

These scripts are based on the Vietnamese language processing section from `.github/workflows/main.yml`:

```yaml
# From the original workflow
php update-manager/update-manager.php dscript "ciout/vi.txt" . vi ${BUILD}
php update-manager/update-manager.php script ciout/vi.txt "ciout/vi.file" "$LAST_VI"
zip -qry umineko-vi-scripts_r${BUILD}_dev.zip vi.txt vi.cfg
zip -qry umineko-vi-scripts_r${BUILD}.zip vi.file vi.cfg
```

## Troubleshooting

### Common Issues

1. **"update-manager.php not found"**
   - Ensure you're running the script from the project root directory
   - Check that `update-manager/` directory exists

2. **"PHP is not installed or not in PATH"**
   - Install PHP from https://www.php.net/
   - Add PHP to your system PATH

3. **"zip command not found"**
   - Install zip utility (Git Bash includes this on Windows)
   - Or skip zip creation by not using `--create-zip` flag

4. **Permission errors**
   - Ensure you have write permissions to the output directory
   - Run with appropriate privileges if needed

### Debugging

For more verbose output, you can modify the scripts or run with Python's verbose flag:
```bash
python -v invoke_vi_update_manager.py
```

## License

These scripts are part of the Umineko Project and follow the same BSD License as the main project.
