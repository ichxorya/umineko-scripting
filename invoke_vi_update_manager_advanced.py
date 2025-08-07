#!/usr/bin/env python3
"""
Advanced Vietnamese (VI) Update Manager Invoker for Umineko Project

This script provides comprehensive Vietnamese language processing capabilities,
including script generation, zip file creation, and optional cleanup operations.
It replicates the full functionality found in the GitHub Actions workflow.

Usage:
    python invoke_vi_update_manager_advanced.py [options]

Options:
    --build-number NUMBER    Specify build number (default: 3500)
    --create-zip            Create zip files for distribution
    --cleanup               Clean up intermediate files after processing
    --output-dir DIR        Specify output directory (default: ciout)
    --help                  Show this help message
"""

import os
import sys
import subprocess
import argparse
import shutil
from pathlib import Path
from typing import Optional

class VietnameseUpdateManager:
    """Vietnamese Update Manager for Umineko Project."""
    
    def __init__(self, build_number: int, output_dir: str = "ciout"):
        """
        Initialize the Vietnamese Update Manager.
        
        Parameters
        ----------
        build_number : int
            The build number for script generation.
        output_dir : str
            The output directory for generated files.
        """
        self.build_number = build_number
        self.output_dir = Path(output_dir)
        self.last_vi = self._get_last_episode_vi()
        
    def _get_last_episode_vi(self) -> str:
        """
        Read the last episode number for Vietnamese from current/last_vi file.
        
        Returns
        -------
        str
            The last episode number, or "1" if file doesn't exist or is empty.
        """
        try:
            with open("current/last_vi", "r", encoding="utf-8") as f:
                content = f.read().strip()
                return content if content else "1"
        except FileNotFoundError:
            return "1"
    
    def _ensure_output_directory(self) -> None:
        """Create output directory if it doesn't exist."""
        self.output_dir.mkdir(exist_ok=True)
        print(f"Output directory: {self.output_dir.absolute()}")
    
    def _run_command(self, cmd: list[str], description: str) -> subprocess.CompletedProcess:
        """
        Run a command and handle errors.
        
        Parameters
        ----------
        cmd : list[str]
            The command to run as a list of arguments.
        description : str
            Description of what the command does for error reporting.
            
        Returns
        -------
        subprocess.CompletedProcess
            The completed process result.
        """
        print(f"Running: {description}")
        print(f"Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✓ {description} completed successfully")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return result
        except subprocess.CalledProcessError as e:
            print(f"✗ {description} failed with exit code {e.returncode}")
            if e.stdout:
                print(f"stdout: {e.stdout}")
            if e.stderr:
                print(f"stderr: {e.stderr}")
            sys.exit(1)
        except FileNotFoundError:
            print("✗ Command not found. Make sure Python is installed and in PATH.")
            print(f"Failed command: {' '.join(cmd)}")
            sys.exit(1)
    
    def _check_prerequisites(self) -> None:
        """Check if all required files and tools are available."""
        # Check if we're in the right directory
        if not os.path.exists("update-manager/update_manager.py"):
            print("Error: update_manager.py not found in update-manager directory. Please run from the project root.")
            sys.exit(1)
        
        # Check if Python is available
        try:
            subprocess.run(["python", "--version"], 
                         check=True, capture_output=True, text=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: Python is not installed or not in PATH.")
            sys.exit(1)
        
        # Check if required config files exist
        required_files = [
            "misc/default.cfg",
            "misc/vi.cfg" if Path("misc/vi.cfg").exists() else "misc/default.cfg"
        ]
        
        for file_path in required_files:
            if not os.path.exists(file_path):
                print(f"Warning: {file_path} not found")
    
    def generate_vietnamese_script(self) -> None:
        """Generate Vietnamese script using dscript command."""
        dscript_cmd = [
            "python",
            "update-manager/update_manager.py",
            "dscript",
            str(self.output_dir / "vi.txt"),
            ".",
            "vi",
            str(self.build_number)
        ]
        
        self._run_command(dscript_cmd, "Generate Vietnamese script (dscript)")
    
    def create_filtered_script(self) -> None:
        """Create filtered Vietnamese script file using Python script command."""
        script_cmd = [
            "python",
            "update-manager/update_manager.py",
            "script",
            str(self.output_dir / "vi.txt"),
            str(self.output_dir / "vi.file"),
            self.last_vi
        ]
        
        self._run_command(script_cmd, "Create filtered Vietnamese script file")
    
    def copy_config_files(self) -> None:
        """Copy required configuration files to output directory."""
        config_files = []
        
        # Copy vi.cfg if it exists, otherwise use default.cfg
        if os.path.exists("misc/vi.cfg"):
            config_files.append(("misc/vi.cfg", "vi.cfg"))
        else:
            config_files.append(("misc/default.cfg", "vi.cfg"))
        
        for src, dst in config_files:
            if os.path.exists(src):
                shutil.copy2(src, self.output_dir / dst)
                print(f"✓ Copied {src} to {self.output_dir / dst}")
            else:
                print(f"⚠ Warning: {src} not found, skipping")
    
    def create_zip_files(self) -> tuple[Optional[Path], Optional[Path]]:
        """
        Create zip files for Vietnamese scripts.
        
        Returns
        -------
        tuple[Optional[Path], Optional[Path]]
            Paths to the created dev and release zip files, or None if creation failed.
        """
        # Check if zip command is available
        try:
            subprocess.run(["zip", "--version"], 
                         check=True, capture_output=True, text=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: zip command not found. Skipping zip file creation.")
            return None, None
        
        dev_zip = self.output_dir / f"umineko-vi-scripts_r{self.build_number}_dev.zip"
        release_zip = self.output_dir / f"umineko-vi-scripts_r{self.build_number}.zip"
        
        # Create dev zip (with .txt file)
        dev_files = ["vi.txt"]
        if (self.output_dir / "vi.cfg").exists():
            dev_files.append("vi.cfg")
        
        if all((self.output_dir / f).exists() for f in dev_files):
            dev_cmd = ["zip", "-qry", str(dev_zip)] + dev_files
            
            # Change to output directory for zip creation
            original_cwd = os.getcwd()
            try:
                os.chdir(self.output_dir)
                self._run_command(dev_cmd, f"Create dev zip: {dev_zip.name}")
            finally:
                os.chdir(original_cwd)
        else:
            print("⚠ Warning: Some files missing for dev zip creation")
            dev_zip = None
        
        # Create release zip (with .file)
        release_files = ["vi.file"]
        if (self.output_dir / "vi.cfg").exists():
            release_files.append("vi.cfg")
        
        if all((self.output_dir / f).exists() for f in release_files):
            release_cmd = ["zip", "-qry", str(release_zip)] + release_files
            
            # Change to output directory for zip creation
            original_cwd = os.getcwd()
            try:
                os.chdir(self.output_dir)
                self._run_command(release_cmd, f"Create release zip: {release_zip.name}")
            finally:
                os.chdir(original_cwd)
        else:
            print("⚠ Warning: Some files missing for release zip creation")
            release_zip = None
        
        return dev_zip, release_zip
    
    def verify_output_files(self) -> dict[str, bool]:
        """
        Verify that output files were created successfully.
        
        Returns
        -------
        dict[str, bool]
            Dictionary mapping file names to whether they exist.
        """
        files_to_check = {
            "vi.txt": self.output_dir / "vi.txt",
            "vi.file": self.output_dir / "vi.file",
            "vi.cfg": self.output_dir / "vi.cfg"
        }
        
        results = {}
        for name, path in files_to_check.items():
            exists = path.exists()
            results[name] = exists
            
            if exists:
                size = path.stat().st_size
                print(f"✓ {name} created ({size:,} bytes)")
            else:
                print(f"✗ {name} was not created")
        
        return results
    
    def cleanup_intermediate_files(self) -> None:
        """Clean up intermediate files if requested."""
        intermediate_files = [
            self.output_dir / "vi.txt"  # Keep only the .file and config
        ]
        
        for file_path in intermediate_files:
            if file_path.exists():
                file_path.unlink()
                print(f"✓ Cleaned up {file_path.name}")
    
    def run_full_process(self, create_zip: bool = False, cleanup: bool = False) -> None:
        """
        Run the complete Vietnamese update manager process.
        
        Parameters
        ----------
        create_zip : bool
            Whether to create zip files for distribution.
        cleanup : bool
            Whether to clean up intermediate files after processing.
        """
        print("Umineko Vietnamese (VI) Update Manager - Advanced")
        print("=" * 55)
        print(f"Build number: {self.build_number}")
        print(f"Last VI episode: {self.last_vi}")
        print()
        
        # Check prerequisites
        print("Checking prerequisites...")
        self._check_prerequisites()
        print("✓ Prerequisites check passed")
        print()
        
        # Ensure output directory exists
        self._ensure_output_directory()
        print()
        
        # Step 1: Generate Vietnamese script
        print("Step 1: Generating Vietnamese script...")
        self.generate_vietnamese_script()
        print()
        
        # Step 2: Create filtered script file
        print("Step 2: Creating filtered script file...")
        self.create_filtered_script()
        print()
        
        # Step 3: Copy configuration files
        print("Step 3: Copying configuration files...")
        self.copy_config_files()
        print()
        
        # Step 4: Verify output files
        print("Step 4: Verifying output files...")
        verification_results = self.verify_output_files()
        print()
        
        # Step 5: Create zip files if requested
        if create_zip:
            print("Step 5: Creating zip files...")
            dev_zip, release_zip = self.create_zip_files()
            if dev_zip and release_zip:
                print(f"✓ Created {dev_zip.name}")
                print(f"✓ Created {release_zip.name}")
            print()
        
        # Step 6: Cleanup if requested
        if cleanup:
            print("Step 6: Cleaning up intermediate files...")
            self.cleanup_intermediate_files()
            print()
        
        # Final summary
        print("Vietnamese update manager processing completed!")
        print(f"Output files are available in: {self.output_dir.absolute()}")
        
        if all(verification_results.values()):
            print("✓ All expected files were created successfully")
        else:
            print("⚠ Some files may be missing - check the output above")

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Advanced Vietnamese Update Manager for Umineko Project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python invoke_vi_update_manager_advanced.py
  python invoke_vi_update_manager_advanced.py --build-number 3600 --create-zip
  python invoke_vi_update_manager_advanced.py --output-dir output --cleanup
        """
    )
    
    parser.add_argument(
        "--build-number",
        type=int,
        default=3500,
        help="Specify build number (default: 3500)"
    )
    
    parser.add_argument(
        "--create-zip",
        action="store_true",
        help="Create zip files for distribution"
    )
    
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Clean up intermediate files after processing"
    )
    
    parser.add_argument(
        "--output-dir",
        default="ciout",
        help="Specify output directory (default: ciout)"
    )
    
    return parser.parse_args()

def main():
    """Main function that orchestrates the advanced Vietnamese update manager."""
    args = parse_arguments()
    
    # Create and run the Vietnamese Update Manager
    manager = VietnameseUpdateManager(
        build_number=args.build_number,
        output_dir=args.output_dir
    )
    
    manager.run_full_process(
        create_zip=args.create_zip,
        cleanup=args.cleanup
    )

if __name__ == "__main__":
    main()
