@echo off
echo Building console app (one-directory)...

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Build console app (one-directory)
echo Building one-directory console app...
pyinstaller --onedir --windowed --name=pyconsole-dir main.py

echo Build complete!
echo Executable location: dist\pyconsole-dir\pyconsole-dir.exe

pause