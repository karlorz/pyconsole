# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyConsole is an intelligent Python application runner that demonstrates advanced packaging techniques with automatic environment setup. The project features a dual-mode operation system that works both as a standalone executable and as a development tool with auto-virtual environment creation.

## Key Architecture

### Dual-Mode Operation
- **Bundled Mode**: When running from PyInstaller executable (`sys.frozen == True`)
  - All dependencies embedded in the executable
  - No external files or runtime setup required
  - Immediate execution on any system
- **Development Mode**: When running from source code
  - Automatically detects `pyproject.toml`
  - Creates `.venv` if it doesn't exist
  - Installs dependencies automatically
  - Supports both `uv` and standard `venv`

### Smart Environment Management
The `setup_environment()` function in `app.py` implements:
- Environment detection (bundled vs development)
- Virtual environment health checks
- Automatic dependency installation
- Graceful fallback between `uv` and `venv`
- Error handling and continuation

## Development Commands

### Primary Build Process
```bash
# Install dependencies using uv (preferred)
uv sync

# Build the optimized executable
python build_exe.py

# Run in development mode (auto-creates venv)
python app.py

# Test the built executable
./dist/pyconsole-portable      # Linux/macOS
./dist/pyconsole-portable.exe  # Windows
```

### Environment Management
```bash
# Clean rebuild (remove venv and recreate)
rm -rf .venv && python app.py

# Manual venv setup with uv (auto-detects Python version from pyproject.toml)
uv venv
uv pip install -e .

# Manual venv setup with standard tools
python -m venv .venv
.venv/bin/pip install -e .  # Linux/macOS
.venv\Scripts\pip install -e .  # Windows
```

## Core Files

### Application Logic
- `app.py` - Main application with dual-mode environment setup
  - `setup_environment()` - Smart virtual environment management
  - `main()` - Application entry point with HTTP demo
  - Cross-platform path handling
  - Error recovery and fallback mechanisms

### Build System
- `build_exe.py` - Optimized build script
  - Uses `uv` for dependency management
  - Direct PyInstaller execution (no bootstrap)
  - Single-file output with all dependencies bundled
  - Platform-aware executable naming

### Configuration
- `pyproject.toml` - Modern Python project configuration
  - Uses `uv` for dependency management
  - Minimum Python version: 3.8+
  - Development dependencies include PyInstaller

### Build Output
- `dist/pyconsole-portable` - Linux/macOS executable
- `dist/pyconsole-portable.exe` - Windows executable
- `build/` - Temporary build artifacts (safe to delete)

## Implementation Details

### Environment Detection
```python
# Check if running from PyInstaller executable
if getattr(sys, 'frozen', False):
    # Bundled mode - no venv needed
    print("📦 Running in bundled mode - all dependencies included")
    return
```

### Virtual Environment Setup
The application automatically:
1. Checks for existing `.venv` directory
2. Tests if the venv is functional (can import dependencies)
3. Creates new venv if needed using `uv` (preferred) or standard `venv`
4. Installs dependencies from `pyproject.toml`
5. Falls back gracefully if setup fails

### Cross-Platform Support
- **Path handling**: Uses `pathlib.Path` for cross-platform compatibility
- **Executable detection**: Handles both `bin/` (Unix) and `Scripts/` (Windows) paths
- **Process execution**: Cross-platform subprocess handling
- **Console behavior**: Handles `EOFError` for non-interactive environments

## Testing Strategy

### Development Mode Testing
```bash
# Test auto-venv creation
rm -rf .venv && python app.py

# Test venv reuse
python app.py  # Should use existing venv

# Test fallback behavior (without uv)
# Temporarily rename uv or remove from PATH
python app.py
```

### Bundled Mode Testing
```bash
# Build and test executable
python build_exe.py
./dist/pyconsole-portable

# Test on clean system
# Copy executable to a machine without Python
./pyconsole-portable
```

## Build Optimization

### Current Advantages
- **Single file deployment**: No external files required
- **Smart dependency management**: Auto-virtual environment creation
- **Reduced complexity**: No bootstrap scripts or external uv bundling
- **Fast startup**: No runtime dependency installation in bundled mode
- **ML-friendly**: Users can manage large libraries in their own `.venv`

### File Size Considerations
- Current executable size: ~9-10MB (includes Python runtime + urllib3)
- Much smaller than traditional approaches that bundle uv
- Optimized for common use cases while remaining extensible

## Future Enhancement Points

### Package Distribution
- **pip package**: Structure for `pip install pyconsole-portable`
- **uvx support**: Design for `uvx pyconsole-portable` execution
- **Plugin architecture**: Extensible framework for different app types

### Advanced Features
- **GUI support**: Windowed applications with auto-dependency management
- **Configuration files**: External configuration support
- **Logging**: Structured logging for debugging
- **Update checking**: Automatic update notifications

### Performance Optimizations
- **Lazy loading**: Load dependencies only when needed
- **Caching**: Intelligent caching of downloaded packages
- **Parallel operations**: Concurrent dependency installation

## Error Handling Patterns

### Graceful Degradation
The application follows a pattern of:
1. Try the preferred method (uv)
2. Fall back to standard method (venv)
3. Continue execution even if setup fails
4. Provide clear feedback to users

### User Experience
- Clear status messages with emojis for visual scanning
- Progress indicators for long-running operations
- Error messages that suggest solutions
- Non-interactive mode support for automation

## Security Considerations

### Execution Safety
- Validates venv functionality before use
- Handles subprocess timeouts
- Cleans up temporary files
- Uses relative paths to avoid directory traversal

### Dependency Management
- Installs packages in isolated environments
- Uses `uv`'s security features when available
- Falls back to trusted `pip` installations
- Prevents system-wide package modifications