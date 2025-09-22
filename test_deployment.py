#!/usr/bin/env python3
"""
Test deployment simulation - creates a clean directory and tests the portable exe
"""

import subprocess
import shutil
import tempfile
import platform
from pathlib import Path

def main():
    print("=== Testing Portable Deployment ===")
    
    # Check if executable exists
    exe_name = "pyconsole-portable.exe" if platform.system() == "Windows" else "pyconsole-portable"
    exe_path = Path("dist") / exe_name
    
    if not exe_path.exists():
        print(f"✗ {exe_name} not found. Run build_exe.py first.")
        return
    
    # Create temporary deployment directory
    with tempfile.TemporaryDirectory() as temp_dir:
        deploy_dir = Path(temp_dir) / "deployment_test"
        deploy_dir.mkdir()
        
        print(f"Testing deployment in: {deploy_dir}")
        
        # Copy required files
        files_to_copy = [exe_path, "app.py", "pyproject.toml"]
        for file_path in files_to_copy:
            if file_path.exists():
                shutil.copy2(file_path, deploy_dir)
                print(f"✓ Copied {file_path.name}")
            else:
                print(f"✗ Missing {file_path}")
                return
        
        # Test run the portable executable
        print(f"\n🚀 Testing portable executable...")
        try:
            result = subprocess.run([
                str(deploy_dir / exe_name)
            ], cwd=deploy_dir, timeout=30, capture_output=True, text=True)
            
            print(f"Exit code: {result.returncode}")
            if result.stdout:
                print("STDOUT:")
                print(result.stdout)
            if result.stderr:
                print("STDERR:")
                print(result.stderr)
                
            # Check if .venv was created
            venv_path = deploy_dir / ".venv"
            if venv_path.exists():
                print("✓ .venv directory created successfully")
            else:
                print("✗ .venv directory not found")
                
        except subprocess.TimeoutExpired:
            print("⏰ Test timed out (30s) - this might be normal for interactive apps")
        except Exception as e:
            print(f"✗ Test failed: {e}")

if __name__ == "__main__":
    main()