#!/usr/bin/env python3
"""
Build truly self-contained executable with all dependencies bundled
"""

import subprocess
import sys
import platform
from pathlib import Path

def main():
    print("=== Self-Contained Executable Build ===")

    # Install dependencies and build tools
    print("\n1. Installing dependencies...")
    try:
        subprocess.run(["uv", "sync"], check=True)
        print("✓ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        sys.exit(1)

    # Build self-contained executable with PyInstaller
    print("\n2. Building self-contained executable...")
    try:
        cmd = [
            "uv", "run", "pyinstaller",
            "--onefile",
            "--console",
            "--add-data=pyproject.toml:.",  # Bundle pyproject.toml for auto-venv
            "--name=pyconsole-portable",
            "app.py"  # Build app.py directly
        ]
        subprocess.run(cmd, check=True)
        print("✓ Executable built")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        sys.exit(1)

    # Show results
    exe_name = "pyconsole-portable.exe" if platform.system() == "Windows" else "pyconsole-portable"
    exe_path = Path("dist") / exe_name

    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n✓ SUCCESS! Self-contained executable built")
        print(f"  Location: {exe_path}")
        print(f"  Size: {size_mb:.1f} MB")
        print(f"\n📦 Deployment Instructions:")
        print(f"  1. Copy ONLY {exe_name} to target system")
        print(f"  2. Run {exe_name} - no other files needed!")
        print(f"\n🌍 Works on fresh Windows/Linux without Python installed!")
    else:
        print("✗ Executable not found")
        sys.exit(1)

if __name__ == "__main__":
    main()