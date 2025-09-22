@echo off
echo Building console app with console window...

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Build console app (one-file with console)
echo Building one-file console app with console...
pyinstaller --onefile --console --name=pyconsole-console main.py

echo Build complete!
echo Executable location: dist\pyconsole-console.exe

pause