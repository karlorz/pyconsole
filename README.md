# PyConsole

Self-contained Python application that creates portable executables with bundled dependencies and runtime environment setup.

## What This Does

Creates a **truly portable executable** that:

- Runs on fresh Windows/Linux systems (no Python required)
- Bundles `uv` package manager inside the executable
- Auto-creates `.venv` and installs dependencies on first run
- Perfect for distributing Python apps to non-technical users

## Quick Start

### Prerequisites

- Python 3.8+
- uv package manager ([install guide](https://docs.astral.sh/uv/getting-started/installation/))

### Build Portable Executable

```bash
# Install dependencies
uv sync

# Build self-contained executable
python build_exe.py
```

### Deploy Anywhere

Copy these 3 files to any system:

- `pyconsole-portable.exe` (the executable)
- `app.py` (your application code)
- `pyproject.toml` (dependency specification)

Run the executable - it handles everything automatically!

## Project Structure

```
pyconsole/
├── app.py              # Main application (HTTP demo)
├── app_bootstrap.py    # Runtime environment setup
├── build_exe.py        # Build script
├── test_deployment.py  # Deployment testing
├── pyproject.toml      # Project config
└── README.md
```

## How It Works

1. **Build**: PyInstaller bundles `uv` + bootstrap code into single executable
2. **Deploy**: Copy 3 files to target system
3. **Run**: Executable extracts `uv`, creates `.venv`, installs deps, runs app

## Development

```bash
# Run in development
uv run python app.py

# Test deployment
python test_deployment.py
```

## Use Cases

- Distributing Python apps to end users
- Deployment to systems without Python
- Corporate environments with restricted installations
- Demos and prototypes that "just work"
