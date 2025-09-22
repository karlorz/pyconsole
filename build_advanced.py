#!/usr/bin/env python3
"""
Advanced PyInstaller build script with cross-platform support
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, description=""):
    """Run a command and handle errors"""
    print(f"\n{description}")
    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False

def install_dependencies():
    """Install required dependencies"""
    return run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                      "Installing dependencies...")

def build_console_app(build_type="onefile", console=False, name="pyconsole"):
    """Build console application with specified options"""
    cmd = [sys.executable, "-m", "PyInstaller"]

    if build_type == "onefile":
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")

    if console:
        cmd.append("--console")
    else:
        cmd.append("--windowed")

    cmd.extend(["--name", name, "main.py"])

    return run_command(cmd, f"Building {build_type} {'console' if console else 'windowed'} app...")

def clean_build():
    """Clean build artifacts"""
    import shutil

    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}...")
            shutil.rmtree(dir_name)

    # Remove .spec files
    for spec_file in os.listdir("."):
        if spec_file.endswith(".spec"):
            print(f"Removing {spec_file}...")
            os.remove(spec_file)

def main():
    """Main build function"""
    print("PyInstaller Console App Demo - Advanced Build Script")
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version}")

    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("Error: main.py not found!")
        return

    # Ask user for build options
    print("\nBuild Options:")
    print("1. One-file windowed app")
    print("2. One-file console app")
    print("3. One-directory windowed app")
    print("4. One-directory console app")
    print("5. All variants")
    print("6. Clean build artifacts")

    choice = input("\nSelect option (1-6): ").strip()

    if choice == "6":
        clean_build()
        return

    # Install dependencies
    if not install_dependencies():
        return

    # Build based on choice
    success = True

    if choice == "1":
        success = build_console_app("onefile", False, "pyconsole")
    elif choice == "2":
        success = build_console_app("onefile", True, "pyconsole-console")
    elif choice == "3":
        success = build_console_app("onedir", False, "pyconsole-dir")
    elif choice == "4":
        success = build_console_app("onedir", True, "pyconsole-dir-console")
    elif choice == "5":
        builds = [
            ("onefile", False, "pyconsole"),
            ("onefile", True, "pyconsole-console"),
            ("onedir", False, "pyconsole-dir"),
            ("onedir", True, "pyconsole-dir-console")
        ]
        for build_type, console, name in builds:
            if not build_console_app(build_type, console, name):
                success = False
                break
    else:
        print("Invalid choice!")
        return

    if success:
        print("\nBuild completed successfully!")
        print("Check the 'dist' directory for executables")
    else:
        print("\nBuild failed!")

if __name__ == "__main__":
    main()