import sys
import os
import subprocess
import urllib3
import json
import argparse
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
            '🌍': '[GLOBAL]',
            '📤': '[PUBLISH]',
            '🔐': '[AUTH]',
            '📋': '[PREP]',
            '🔍': '[CHECK]'
        }

        # Replace emojis with text fallbacks
        for emoji, fallback in emoji_fallbacks.items():
            text = text.replace(emoji, fallback)

    print(text)

def validate_package():
    """Validate package contents before publishing"""
    safe_print("🔍 Validating package contents...")

    app_dir = Path(__file__).parent.resolve()

    # Check for required files
    required_files = ["pyproject.toml", "app.py", "build_exe.py"]
    for file in required_files:
        file_path = app_dir / file
        if not file_path.exists():
            safe_print(f"❌ Missing required file: {file}")
            return False

    # Check for sensitive files that shouldn't be published
    sensitive_patterns = [".env", ".key", ".secret", "password", "token"]
    for pattern in sensitive_patterns:
        if list(app_dir.glob(f"*{pattern}*")):
            safe_print(f"⚠️ Found files matching sensitive pattern: {pattern}")
            return False

    # Validate pyproject.toml structure
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            safe_print("⚠️ No TOML parser available for validation")
            return True

    try:
        with open(app_dir / "pyproject.toml", "rb") as f:
            config = tomllib.load(f)

        # Check required fields
        required_fields = ["project", "project.name", "project.version"]
        for field in required_fields:
            if not get_nested_value(config, field):
                safe_print(f"❌ Missing required field in pyproject.toml: {field}")
                return False

    except Exception as e:
        safe_print(f"❌ Error validating pyproject.toml: {e}")
        return False

    safe_print("✅ Package validation passed")
    return True

def get_nested_value(d, path):
    """Get nested value from dictionary using dot notation"""
    keys = path.split('.')
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return None
    return d

def prepare_package():
    """Prepare package for publishing"""
    safe_print("📋 Preparing package for publishing...")

    # Ensure we're in the right directory
    app_dir = Path(__file__).parent.resolve()
    os.chdir(app_dir)

    # Clean up any previous build artifacts
    for path in ["dist", "build", "*.egg-info"]:
        if Path(path).exists():
            if Path(path).is_dir():
                import shutil
                shutil.rmtree(path)
            else:
                Path(path).unlink()

    safe_print("✅ Package preparation completed")
    return True

def publish_package(dry_run=False):
    """Publish package using uv publish"""
    safe_print("📤 Publishing package...")

    # Check if uv is available
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True, timeout=5)
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        safe_print("❌ uv not found. Please install uv: https://docs.astral.sh/uv/")
        return False

    # Validate package
    if not validate_package():
        safe_print("❌ Package validation failed")
        return False

    # Prepare package
    if not prepare_package():
        safe_print("❌ Package preparation failed")
        return False

    # Check for authentication
    publish_token = os.environ.get("UV_PUBLISH_TOKEN")
    if not publish_token:
        safe_print("🔐 No UV_PUBLISH_TOKEN found in environment")
        safe_print("💡 Set your token with: export UV_PUBLISH_TOKEN=your_token")
        safe_print("   or on Windows: set UV_PUBLISH_TOKEN=your_token")
        return False

    # Build the publish command
    cmd = ["uv", "publish"]
    if dry_run:
        cmd.append("--dry-run")

    try:
        safe_print(f"📤 Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=300)

        if result.stdout:
            safe_print("✅ Publish output:")
            for line in result.stdout.split('\n'):
                if line.strip():
                    safe_print(f"   {line}")

        if result.stderr:
            safe_print("⚠️ Publish warnings/errors:")
            for line in result.stderr.split('\n'):
                if line.strip():
                    safe_print(f"   {line}")

        safe_print("✅ Package published successfully!")
        return True

    except subprocess.CalledProcessError as e:
        safe_print(f"❌ Publish failed: {e}")
        if e.stdout:
            safe_print(f"   Output: {e.stdout}")
        if e.stderr:
            safe_print(f"   Error: {e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        safe_print("❌ Publish timed out")
        return False

def main():
    parser = argparse.ArgumentParser(description="PyConsole - Self-contained Python application")
    parser.add_argument("--publish", action="store_true", help="Publish package to PyPI")
    parser.add_argument("--dry-run", action="store_true", help="Dry run publish without uploading")
    args = parser.parse_args()

    safe_print("=== PyConsole ===")

    if args.publish or args.dry_run:
        safe_print("📤 Publishing package...")
        success = publish_package(dry_run=args.dry_run)
        if success:
            safe_print("✅ Publish completed successfully!")
        else:
            safe_print("❌ Publish failed!")
            sys.exit(1)
        return

    # Normal operation
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
