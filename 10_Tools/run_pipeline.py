import subprocess
import sys
import os

def run_step(step_name, command):
    print(f"\n[{step_name}] Running...")
    try:
        result = subprocess.run(command, text=True, capture_output=True)
        if result.returncode == 0:
            print(f"[{step_name}] PASSED")
            return True
        else:
            print(f"[{step_name}] FAILED")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[{step_name}] ERROR: {e}")
        return False

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)
    
    # 1. Unit Tests
    cmd_test = [sys.executable, "-m", "unittest", "discover", "-s", "09_Tests", "-p", "test_*.py"]
    if not run_step("Unit Tests", cmd_test):
        sys.exit(1)
        
    print("\n[SUCCESS] All checks passed. Ready for commit/deployment.")

if __name__ == "__main__":
    main()
