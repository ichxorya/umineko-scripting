from os import PathLike
from subprocess import CompletedProcess
import subprocess
import os


import subprocess
import os
import shutil
import zipfile
import datetime

# === CONFIGURATION ===
SCRIPTING_ROOT_DIR: str = "."   
CONFIG_FILES: list[str] = ["chiru.file", "game.hash", "default.cfg"] 
OUTPUT_DIR: str = "build_output"
DEVELOPMENT_ZIP_DIR: str = "dev_zips"
RELEASE_ZIP_DIR: str = "release_zips"
REVISION: str = "r2"  # Optional, set to None to omit
LOCALES: list[str] = ["en", "vi"]
UPDATE_MANAGER_PATH: str = "update-manager/update_manager.py"

def run_update_manager_dscript(locale, output_txt) -> None:
    args: list[str] = [
        "python", UPDATE_MANAGER_PATH,
        "dscript",
        output_txt,
        SCRIPTING_ROOT_DIR,
        locale
    ]
    if REVISION:
        args.append(REVISION)

    result: CompletedProcess[str] = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"[dscript] Failed for {locale}: {result.stderr}")
    print(f"[dscript] Done for {locale}")


def run_update_manager_script(input_txt, output_bin, episode="1") -> None:
    args: list[str] = [
        "python", UPDATE_MANAGER_PATH,
        "script",
        input_txt,
        output_bin,
        episode
    ]
    result: CompletedProcess[str] = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"[script] Failed for {input_txt}: {result.stderr}")
    print(f"[script] Encoded binary for {input_txt}")


def zip_file(output_zip, files_to_zip) -> None:
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            arcname: PathLike[str] | str | None = os.path.basename(file)
            zipf.write(file, arcname)
    print(f"[zip] Created {output_zip}")


def build():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(DEVELOPMENT_ZIP_DIR, exist_ok=True)
    os.makedirs(RELEASE_ZIP_DIR, exist_ok=True)

    for locale in LOCALES:
        print(f"\n--- Building for locale: {locale} ---")
        timestamp: str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        base_name: str = f"umineko_{locale}_{timestamp}"
        txt_output: str = os.path.join(OUTPUT_DIR, f"{base_name}.txt")
        bin_output: str = os.path.join(OUTPUT_DIR, f"{base_name}.file")

        # Step 1: Generate full script .txt
        run_update_manager_dscript(locale, txt_output)

        # Step 2: Copy config files
        for config_file in CONFIG_FILES:
            config_src: str = os.path.join(SCRIPTING_ROOT_DIR, "misc/" + config_file)
            config_dst: str = os.path.join(OUTPUT_DIR, f"{locale}_{config_file}")
            if os.path.exists(config_src):
                shutil.copy(config_src, config_dst)
                print(f"[copy] Copied {config_file} for {locale}")

        # Step 3: Create development ZIP with .txt file + config
        dev_zip_path: str = os.path.join(DEVELOPMENT_ZIP_DIR, f"{base_name}_dev.zip")
        dev_files: list[str] = [txt_output] + [
            os.path.join(OUTPUT_DIR, f"{locale}_{cfg}") for cfg in CONFIG_FILES if os.path.exists(os.path.join(SCRIPTING_ROOT_DIR, cfg))
        ]
        zip_file(dev_zip_path, dev_files)

        # Step 4: Generate .file binary script
        run_update_manager_script(txt_output, bin_output)

        # Step 5: Create release ZIP with .file only
        release_zip_path: str = os.path.join(RELEASE_ZIP_DIR, f"{base_name}_release.zip")
        zip_file(release_zip_path, [bin_output])


if __name__ == "__main__":
    build()

