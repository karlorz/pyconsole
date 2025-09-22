#!/bin/bash
echo "========================================"
echo "PyInstaller Build Script with uv"
echo "========================================"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Please install uv first:"
    echo "pip install uv"
    exit 1
fi

echo "Syncing dependencies with uv..."
uv sync

echo "Building console app with uv..."
uv run pyinstaller --onefile --console --name=pyconsole-console main.py

echo ""
echo "Build complete!"
echo "Executable location: dist/pyconsole-console"