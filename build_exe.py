#!/usr/bin/env python3
"""
Build self-contained executable with bundled uv for cross-platform deployment
"""

import subprocess
import sys
import shutil
import platform
from pathlib import Path

def find_uv_executable():
    """Find uv executable in system"""
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True, check=True)
        print(f"Found uv: {result.stdout.strip()}")
        
        # Get uv path
        if platform.system() == "Windows":
            result = subprocess.run(["where", "uv"], capture_output=True, text=True, check=True)
        else:
            result = subprocess.run(["which", "uv"], capture_output=True, text=True, check=True)
        
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        print("✗ uv not found in PATH")
        return None

def main():
    print("=== Self-Contained Executable Build ===")
    
    # Find uv executable
    uv_path = find_uv_executable()
    if not uv_path:
        print("Please install uv first: https://docs.astral.sh/uv/getting-started/installation/")
        sys.exit(1)
    
    print(f"Using uv from: {uv_path}")
    
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
            "--add-data", f"{uv_path};.",  # Bundle uv executable
            "--add-data", "app.py;.",      # Bundle main app
            "--add-data", "pyproject.toml;.",  # Bundle project config
            "--name=pyconsole-portable",
            "app_bootstrap.py"  # Use bootstrap as entry point
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
        print(f"  1. Copy {exe_name} + app.py + pyproject.toml to target system")
        print(f"  2. Run {exe_name} - it will:")
        print(f"     • Extract bundled uv")
        print(f"     • Create .venv in current directory")
        print(f"     • Install dependencies automatically")
        print(f"     • Run your application")
        print(f"\n🌍 Works on fresh Windows/Linux without Python or uv installed!")
    else:
        print("✗ Executable not found")
        sys.exit(1)

if __name__ == "__main__":
    main()