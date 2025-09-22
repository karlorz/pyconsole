# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a PyInstaller demo project that demonstrates how to package Python console applications into standalone executables. The project contains a simple console application and multiple build configurations for different packaging scenarios.

## Development Commands

### PyInstaller Build Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Build windowed one-file executable (no console window)
python -m PyInstaller --onefile --windowed --name=pyconsole main.py

# Build console one-file executable (with console window)
python -m PyInstaller --onefile --console --name=pyconsole-console main.py

# Build one-directory executable
python -m PyInstaller --onedir --windowed --name=pyconsole-dir main.py

# Use existing build scripts
build.bat          # Windows windowed build
build_console.bat  # Windows console build
build_dir.bat      # Windows one-directory build
build.sh           # Linux/macOS build
```

### Advanced Build Script
```bash
# Interactive build with multiple options
python build_advanced.py
```

## Build Architecture

### Core Files
- `main.py` - Simple console application (prints "Hello from pyconsole!")
- `requirements.txt` - PyInstaller dependency specification
- `pyproject.toml` - Python project configuration (requires Python 3.13+)

### Build Configuration Files
- `pyconsole.spec` - PyInstaller spec file for windowed builds
- `pyconsole_console.spec` - PyInstaller spec file for console builds
- `build*.bat` - Windows batch build scripts
- `build.sh` - Unix shell build script
- `build_advanced.py` - Cross-platform interactive build script

### Build Output
- `dist/` - Contains compiled executables
- `build/` - Temporary build artifacts (can be deleted)

## PyInstaller Options

### Build Types
- **One-file**: Single executable with embedded dependencies
- **One-directory**: Executable with separate dependency files

### Window Modes (Windows-specific)
- **Windowed**: Hides console window (best for GUI apps)
- **Console**: Shows console window (best for CLI tools)

### File Sizes
- One-file executables: ~7MB (includes Python runtime)
- One-directory: Similar total size but distributed across multiple files

## Testing Built Applications
```bash
# Test the built executables
./dist/pyconsole.exe           # Windowed version
./dist/pyconsole-console.exe   # Console version
./dist/pyconsole-dir/pyconsole-dir.exe  # One-directory version
```

## Cross-Platform Notes
- PyInstaller automatically creates executables for the target platform
- Windows builds create `.exe` files
- Linux/macOS builds create executable binaries
- The build scripts handle platform differences automatically