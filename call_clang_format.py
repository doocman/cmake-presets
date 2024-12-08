#!/usr/bin/env python3

import argparse
import os
import subprocess
import re
from pathlib import Path

def get_clang_format_version(clang_format_path):
    clang_version_res = subprocess.run([clang_format_path, "--version"], check=True, stdout=subprocess.PIPE, text=True)
    pattern = re.compile("version ([0-9]+)\.")
    version_match = pattern.search(clang_version_res.stdout)
    if version_match:
        return int(version_match.group(1))
    else:
        raise RuntimeError(f"Could not parse the version from clang-format: {clang_version_res.stdout}")

def run_clang_format(clang_format_path, directories, cwd, clang_min_version):
    """Runs clang-format on all .hpp and .cpp files in the given directories recursively."""
    clang_version = get_clang_format_version(clang_format_path)
    if clang_version < clang_min_version:
        raise RuntimeError(f"Actual clang-format version {clang_version} is older than minimum clang-format version {clang_min_version}")
    file_list = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            has_printed_root = False
            for file in files:
                if file.endswith(('.hpp', '.cpp')):
                    file_path = Path(root) / file
                    file_list.append(file_path)
                    if not has_printed_root:
                        print(f"Formatting {root}/*")
                        has_printed_root = True

    try:
        subprocess.run(
            [clang_format_path, "-i", "--style=file"] + file_list,
            check=True, cwd=cwd,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error formatting {file_list}: {e}")
    except FileNotFoundError:
        print(f"clang-format not found at: {clang_format_path}")
        return
