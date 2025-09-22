@echo off
echo ========================================
echo PyInstaller Build Script with uv
echo ========================================

REM Check if uv is installed
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: uv is not installed. Please install uv first:
    echo pip install uv
    exit /b 1
)

echo Syncing dependencies with uv...
uv sync

echo Building console app with uv...
uv run pyinstaller --onefile --console --name=pyconsole-console main.py

echo.
echo Build complete!
echo Executable location: dist\pyconsole-console.exe