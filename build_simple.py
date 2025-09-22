#!/usr/bin/env python3
"""
Simple build script - one command to build exe with bundled uv
"""

import subprocess
import sys
import shutil
from pathlib import Path

def find_uv_executable():
    """Find uv executable in common locations"""
    possible_paths = [
        "C:/Users/user/.local/bin/uv.exe",
        "C:/Users/user/AppData/Local/uv/bin/uv.exe",
        "C:/Program Files/uv/bin/uv.exe",
    ]

    for path in possible_paths:
        if Path(path).exists():
            return Path(path)

    # Try to find uv in PATH
    try:
        result = subprocess.run(["where", "uv"], capture_output=True, text=True, check=True)
        return Path(result.stdout.strip())
    except:
        pass

    return None

def main():
    print("=== Simple Build - One Command ===")

    # Find uv executable
    uv_path = find_uv_executable()
    if not uv_path:
        print("Error: uv.exe not found. Please install uv first:")
        print("  pip install uv")
        sys.exit(1)

    print(f"Using uv from: {uv_path}")

    # Step 1: Install dependencies
    print("\n1. Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "uv", "sync"], check=True)
        print("OK: Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install dependencies: {e}")
        sys.exit(1)

    # Step 2: Build executable
    print("\n2. Building executable...")
    try:
        cmd = [
            sys.executable, "-m", "uv", "run", "pyinstaller",
            "--onefile", "--console",
            "--add-data", f"{uv_path};.",
            "--add-data", "app.py;.",
            "--add-data", "pyproject.toml;.",
            "--name=app-simple",
            "app_bootstrap.py"
        ]
        subprocess.run(cmd, check=True)
        print("OK: Executable built successfully")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to build executable: {e}")
        sys.exit(1)

    # Step 3: Show results
    exe_path = Path("dist/app-simple.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\nSUCCESS: Build complete!")
        print(f"  Location: {exe_path}")
        print(f"  Size: {size_mb:.1f} MB")
        print(f"\nUsage:")
        print(f"  1. Copy app-simple.exe + app.py + pyproject.toml to any directory")
        print(f"  2. Run app-simple.exe - it will create .venv and install dependencies automatically")
    else:
        print("ERROR: Build failed - executable not found")
        sys.exit(1)

if __name__ == "__main__":
    main()