#!/usr/bin/env python3
"""
Build truly self-contained executable with all dependencies bundled
"""

import platform
import subprocess
import sys
from pathlib import Path


def get_version():
    """Get version from pyproject.toml"""
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            return "unknown"

    try:
        with open("pyproject.toml", "rb") as f:
            config = tomllib.load(f)
            return config["project"]["version"]
    except (KeyError, FileNotFoundError, OSError):
        return "unknown"

def main():
    version = get_version()
    print(f"=== Self-Contained Executable Build (v{version}) ===")

    # Install dependencies and build tools
    print("\n1. Installing dependencies...")
    try:
        subprocess.run(["uv", "sync"], check=True)
        print("[OK] Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Failed to install dependencies: {e}")
        sys.exit(1)

    # Build self-contained executable with PyInstaller
    print("\n2. Building self-contained executable...")
    try:
        exe_name = f"pyconsole-portable-{version}.exe" if platform.system() == "Windows" else f"pyconsole-portable-{version}"

        cmd = [
            "uv", "run", "pyinstaller",
            "--onefile",
            "--console",
            "--add-data=pyproject.toml:.",  # Bundle pyproject.toml for auto-venv
            f"--name={exe_name}",
            "app.py"  # Build app.py directly
        ]
        subprocess.run(cmd, check=True)
        print(f"[OK] Executable built: {exe_name}")
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Build failed: {e}")
        sys.exit(1)

    # Show results
    exe_name = f"pyconsole-portable-{version}.exe" if platform.system() == "Windows" else f"pyconsole-portable-{version}"
    exe_path = Path("dist") / exe_name

    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print("\n+ SUCCESS! Self-contained executable built")
        print(f"  Location: {exe_path}")
        print(f"  Size: {size_mb:.1f} MB")
        print(f"  Version: {version}")
        print("\n[DEPLOY] Deployment Instructions:")
        print(f"  1. Copy ONLY {exe_name} to target system")
        print(f"  2. Run {exe_name} - no other files needed!")
        print("\n[GLOBAL] Works on fresh Windows/Linux without Python installed!")

        # Also create a version-less symlink/copy for convenience
        simple_name = "pyconsole-portable.exe" if platform.system() == "Windows" else "pyconsole-portable"
        simple_path = Path("dist") / simple_name

        try:
            if simple_path.exists():
                simple_path.unlink()

            if platform.system() == "Windows":
                # On Windows, copy the file
                import shutil
                shutil.copy2(exe_path, simple_path)
            else:
                # On Unix-like systems, create a symlink
                simple_path.symlink_to(exe_path.name)

            print(f"  Also created: {simple_path}")
        except OSError:
            print(f"  ! Could not create {simple_path}")
    else:
        print("[FAIL] Executable not found")
        sys.exit(1)

if __name__ == "__main__":
    main()