import sys
import os
import subprocess
import urllib3
import json
from pathlib import Path

# Configure console output for Windows compatibility
def setup_console():
    """Setup console for proper UTF-8 and emoji support on Windows"""
    if os.name == 'nt':  # Windows
        try:
            # Enable UTF-8 output on Windows
            sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
            sys.stderr.reconfigure(encoding='utf-8', errors='backslashreplace')

            # Try to set console code page to UTF-8
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleOutputCP(65001)  # UTF-8 code page
            kernel32.SetConsoleCP(65001)  # UTF-8 input code page

        except Exception:
            # If console setup fails, continue with basic functionality
            pass

# Initialize console settings
setup_console()

def setup_environment():
    """Automatically set up virtual environment and install dependencies"""
    # Get the correct directory based on execution context
    if getattr(sys, 'frozen', False):
        # Running from PyInstaller executable - use executable location
        app_dir = Path(sys.executable).parent.resolve()
    else:
        # Running from source - use script location
        app_dir = Path(__file__).parent.resolve()

    venv_dir = app_dir / ".venv"

    # Check if we're running from the executable - extract pyproject.toml if needed
    if getattr(sys, 'frozen', False):
        safe_print("📦 Running from executable - extracting dependencies...")

        # Extract pyproject.toml from the executable
        import shutil

        # Find the bundled pyproject.toml
        pyproject_path = app_dir / "pyproject.toml"
        if not pyproject_path.exists():
            # Try to extract from the executable bundle
            try:
                bundle_dir = Path(sys._MEIPASS)
                source_pyproject = bundle_dir / "pyproject.toml"
                if source_pyproject.exists():
                    shutil.copy2(source_pyproject, pyproject_path)
                    safe_print("✅ Extracted pyproject.toml")
            except Exception:
                safe_print("⚠️ Could not extract pyproject.toml")
                pyproject_path = None
        else:
            pyproject_path = app_dir / "pyproject.toml"
    else:
        # Running from source
        pyproject_path = app_dir / "pyproject.toml"

    # Check if running in development mode
    if not pyproject_path.exists():
        safe_print("⚠️  pyproject.toml not found - running without venv setup")
        return

    # Check if venv exists and has dependencies
    if venv_dir.exists():
        try:
            # Try to import main dependency to verify venv is functional
            result = subprocess.run([
                str(venv_dir / "bin" / "python" if os.name != 'nt' else venv_dir / "Scripts" / "python.exe"),
                "-c", "import urllib3; print('venv OK')"
            ], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                safe_print("✅ Virtual environment already set up")
                return
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            pass

    # Create or update venv
    safe_print("🔧 Setting up virtual environment...")

    # Check if uv is available in PATH
    uv_available = False
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True, timeout=5)
        uv_available = True
        safe_print("✅ Found uv package manager")
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        safe_print("⚠️ uv not found, using standard tools")

    try:
        if uv_available:
            # Use uv for faster setup
            subprocess.run(["uv", "venv", str(venv_dir)], check=True, capture_output=True)
            safe_print("✅ Created virtual environment with uv")

            # Install dependencies
            if pyproject_path.exists():
                safe_print("📦 Installing dependencies...")
                subprocess.run(["uv", "pip", "install", "-e", "."], check=True, timeout=60)
                safe_print("✅ Dependencies installed")
        else:
            # Use standard Python tools
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
            safe_print("✅ Created virtual environment")

            # Install dependencies with pip
            if pyproject_path.exists():
                pip_path = venv_dir / "bin" / "pip" if os.name != 'nt' else venv_dir / "Scripts" / "pip.exe"
                subprocess.run([str(pip_path), "install", "-e", "."], check=True, timeout=60)
                safe_print("✅ Dependencies installed")

    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        safe_print(f"⚠️ Failed to set up venv: {e}")
        safe_print("🔄 Running with bundled dependencies...")

def safe_print(text):
    """Safely print text with emoji fallback for Windows compatibility"""
    if os.name == 'nt':  # Windows
        # Fallback emoji mappings for Windows console
        emoji_fallbacks = {
            '🚀': '[START]',
            '📦': '[BUNDLE]',
            '✅': '[OK]',
            '❌': '[FAIL]',
            '⚠️': '[WARN]',
            '🔧': '[SETUP]',
            '📡': '[HTTP]',
            '💡': '[INFO]',
            '🌍': '[GLOBAL]'
        }

        # Replace emojis with text fallbacks
        for emoji, fallback in emoji_fallbacks.items():
            text = text.replace(emoji, fallback)

    print(text)

def main():
    safe_print("=== PyConsole ===")
    safe_print("🚀 Auto-setting up environment...")

    # Set up virtual environment if needed
    setup_environment()

    safe_print("\n📡 Making HTTP request to JSONPlaceholder API...")

    try:
        # Create HTTP connection pool manager
        http = urllib3.PoolManager()

        # Make GET request to a test API
        url = "https://jsonplaceholder.typicode.com/posts/1"
        response = http.request('GET', url)

        # Parse and display response
        if response.status == 200:
            data = json.loads(response.data.decode('utf-8'))
            safe_print(f"\n✅ API Response (Status: {response.status}):")
            safe_print(f"Title: {data.get('title', 'N/A')}")
            safe_print(f"Body: {data.get('body', 'N/A')[:100]}...")
        else:
            safe_print(f"❌ Request failed with status: {response.status}")

    except Exception as e:
        safe_print(f"❌ Error making HTTP request: {e}")

    safe_print("\n💡 Press Enter to exit...")
    try:
        input()  # Keep console window open until user presses Enter
    except EOFError:
        # Handle non-interactive environments
        pass


if __name__ == "__main__":
    main()
