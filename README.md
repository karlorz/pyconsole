# PyInstaller + uv Auto-Venv Demo

A simple Python application that demonstrates how to create executables that automatically set up virtual environments using bundled uv.

## Features

- **Single executable** that bundles uv for environment setup
- **Auto-creates .venv** on first run in the same directory
- **Installs dependencies** automatically using bundled uv
- **Perfect for ML libraries** - avoids huge executable sizes

## Quick Start

### Build the executable:
```bash
python build_simple.py
```

### Distribute:
Copy these 3 files to any directory:
- `app-simple.exe` (the bootstrap executable)
- `app.py` (your application)
- `pyproject.toml` (dependencies)

### Run:
```bash
./app-simple.exe
```

**First run**: Creates .venv and installs dependencies (slower)
**Subsequent runs**: Runs directly from .venv (fast)

## Files

- `app.py` - Main application with urllib3 HTTP example
- `app_bootstrap.py` - Bootstrap logic that creates .venv
- `build_simple.py` - Single-command build script
- `pyproject.toml` - Project configuration and dependencies
- `requirements.txt` - Pinned dependencies
- `build.bat` / `build.sh` - Simple uv-based build scripts

## Build Options

### Option 1: Simple build (recommended)
```bash
python build_simple.py
```

### Option 2: Manual build
```bash
uv sync
uv run pyinstaller --onefile --console --add-data "uv.exe;." --add-data "app.py;." --add-data "pyproject.toml;." --name=app-simple app_bootstrap.py
```

### Option 3: Traditional build (no venv creation)
```bash
build.bat  # Windows
./build.sh  # Linux/macOS
```

## How It Works

1. **Build time**: uv is bundled into the executable with PyInstaller
2. **First run**: Extracts uv, creates .venv, installs dependencies
3. **Subsequent runs**: Runs app directly from existing .venv

## Perfect For

- Machine learning applications (avoid 200MB+ library bundles)
- Applications that need clean environment isolation
- Distribution to users without Python installed
- Teams that want consistent environments across machines