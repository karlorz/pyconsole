# PyConsole Portable

Smart Python application runner that automatically sets up virtual environments and manages dependencies for seamless deployment.

## ✅ CI/CD Status

All tests passing! Automated publishing workflow ready.

## What This Does

Creates an **intelligent executable** that:

- **Single-file deployment**: Just copy the executable, nothing else needed
- **Auto-environment setup**: Automatically creates `.venv` and installs dependencies on first run
- **Dual-mode operation**:
  - **Bundled mode**: All dependencies included for immediate execution
  - **Development mode**: Auto-creates virtual environment when `pyproject.toml` is present
- **Smart dependency management**: Handles large ML libraries by letting users manage their own `.venv`
- **Cross-platform**: Works on Windows, Linux, and macOS

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

**Copy just ONE file to any system:**

- `pyconsole-portable.exe` (Windows) or `pyconsole-portable` (Linux/macOS)

That's it! The executable handles everything automatically.

## Project Structure

```
pyconsole/
├── app.py              # Main application with auto-venv setup
├── build_exe.py        # Build script
├── pyproject.toml      # Project config and dependencies
├── CLAUDE.md           # Development guide for Claude Code
└── README.md           # This file
```

## How It Works

### Bundled Mode (Single File)
When you run the standalone executable:
- All dependencies are bundled inside the executable
- No external files or internet connection required
- Runs immediately on any system

### Development Mode (Auto-Venv)
When running from source or with `pyproject.toml` present:
1. **First run**: Automatically creates `.venv` and installs dependencies
2. **Subsequent runs**: Uses the existing virtual environment
3. **Dependency changes**: Auto-updates the virtual environment
4. **Large libraries**: Perfect for ML libraries - users manage their own `.venv`

### Smart Features

- **Environment detection**: Automatically detects if running from executable or source
- **uv first**: Uses `uv` for faster dependency management when available
- **Fallback support**: Gracefully falls back to standard `venv` if `uv` is not available
- **Error handling**: Continues even if venv setup fails
- **Cross-platform**: Works on Windows, Linux, and macOS

## Development

```bash
# Run in development (auto-sets up venv)
python app.py

# Force rebuild venv
rm -rf .venv && python app.py

# Build executable
python build_exe.py
```

## Use Cases

- **Distributing Python apps to end users**: Single file, no technical knowledge required
- **ML/AI applications**: Users can manage large dependencies in their own `.venv`
- **Corporate environments**: Restricted installations, no admin rights needed
- **Demos and prototypes**: "Just works" without setup hassle
- **CI/CD pipelines**: Automated testing and deployment
- **Education**: Students can run Python apps without installation

## Future Plans

- **pip package**: `pip install pyconsole-portable`
- **uvx support**: `uvx pyconsole-portable` (run without installation)
- **Plugin system**: Extendable architecture for different application types
- **GUI support**: Windowed applications with auto-dependency management

## Benefits Over Traditional Approaches

| Traditional PyInstaller | PyConsole |
|------------------------|-----------|
| Large executable size | Smart bundling |
| Manual dependency management | Automatic venv setup |
| No development mode | Dual-mode operation |
| Static dependencies | Dynamic dependency management |
| Single-use | Reusable across projects |
