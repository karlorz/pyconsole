#!/bin/bash
echo "Building PyInstaller console app..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Build console app (one-file)
echo "Building one-file console app..."
pyinstaller --onefile --windowed --name=pyconsole main.py

echo "Build complete!"
echo "Executable location: dist/pyconsole"