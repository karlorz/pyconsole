#!/usr/bin/env python3
"""
Bootstrap executable that bundles uv and creates .venv on first run
"""

import os
import sys
import subprocess
import tempfile
import shutil
import platform
from pathlib import Path

def get_resource_path(relative_path):
    """Get path to resource file, handling PyInstaller temp extraction"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return Path(sys._MEIPASS) / relative_path
    else:
        # Running in development environment
        return Path(__file__).parent / relative_path

def extract_uv():
    """Extract uv executable to temp directory"""
    uv_name = "uv.exe" if platform.system() == "Windows" else "uv"
    uv_source = get_resource_path(uv_name)

    if not uv_source.exists():
        print(f"Error: {uv_name} not found in bundled resources")
        return None

    # Create temp directory for extracted uv
    temp_dir = Path(tempfile.gettempdir()) / "uv_bootstrap"
    temp_dir.mkdir(exist_ok=True)

    uv_dest = temp_dir / uv_name

    # Copy uv executable if not already there
    if not uv_dest.exists() or uv_source.stat().st_size != uv_dest.stat().st_size:
        print(f"Extracting {uv_name}...")
        shutil.copy2(uv_source, uv_dest)
        # Make executable on Unix
        if platform.system() != "Windows":
            uv_dest.chmod(0o755)

    return uv_dest

def run_venv_setup(uv_path):
    """Setup venv and install dependencies"""
    print("Setting up virtual environment...")

    # Create .venv in current directory
    result = subprocess.run([
        str(uv_path), 'venv'
    ], capture_output=True, text=True, cwd=os.getcwd())

    if result.returncode != 0:
        print(f"Error creating venv: {result.stderr}")
        return False

    # Install dependencies
    print("Installing dependencies...")
    result = subprocess.run([
        str(uv_path), 'sync'
    ], capture_output=True, text=True, cwd=os.getcwd())

    if result.returncode != 0:
        print(f"Error installing dependencies: {result.stderr}")
        return False

    return True

def run_app():
    """Run the actual application"""
    print("Starting application...")

    # Run the app from .venv
    venv_python = Path(".venv")
    if platform.system() == "Windows":
        venv_python = venv_python / "Scripts" / "python.exe"
    else:
        venv_python = venv_python / "bin" / "python"

    if not venv_python.exists():
        print("Error: .venv/python not found")
        return False

    # Run app.py
    app_path = Path("app.py")
    if not app_path.exists():
        print("Error: app.py not found")
        return False

    # Pass all command line arguments to the app
    subprocess.run([str(venv_python), str(app_path)] + sys.argv[1:])
    return True

def main():
    """Main bootstrap logic"""
    print("=== Application Bootstrap ===")

    # Check if .venv exists
    venv_path = Path(".venv")

    if not venv_path.exists():
        print("First run detected - setting up environment...")

        # Extract bundled uv
        uv_path = extract_uv()
        if not uv_path:
            print("Failed to extract uv")
            sys.exit(1)

        # Setup venv and install dependencies
        if not run_venv_setup(uv_path):
            print("Failed to setup environment")
            sys.exit(1)

        print("Environment setup complete!")
    else:
        print("Environment already setup - starting application...")

    # Run the application
    if not run_app():
        print("Failed to start application")
        sys.exit(1)

if __name__ == "__main__":
    main()