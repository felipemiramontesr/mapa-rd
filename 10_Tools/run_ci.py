import sys
import os
import subprocess
import compileall

def run_step(name, func, *args):
    print(f"\n[CI] Running: {name}...")
    try:
        if func(*args):
            print(f"[CI] {name}: PASSED")
            return True
        else:
            print(f"[CI] {name}: FAILED")
            return False
    except Exception as e:
        print(f"[CI] {name}: ERROR ({e})")
        return False

def check_syntax(src_dir):
    """Compile all python files to check for syntax errors."""
    print(f"    Scanning {src_dir}...")
    return compileall.compile_dir(src_dir, quiet=1, force=True)

def run_tests():
    """Run unittest suite."""
    cmd = [sys.executable, "-m", "unittest", "discover", "-s", "09_Tests", "-p", "test_*.py"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        return False
    return True

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)
    
    # 1. Syntax Verification (Poor man's lint if flake8 missing)
    if not run_step("Syntax Check (07_Src)", check_syntax, "07_Src"):
        sys.exit(1)
    if not run_step("Syntax Check (10_Tools)", check_syntax, "10_Tools"):
        sys.exit(1)

    # 2. Unit Tests
    if not run_step("Unit Test Suite", run_tests):
        sys.exit(1)

    print("\n[CI] CONTINUOUS INTEGRATION PASSED SUCCESSFULY.")

if __name__ == "__main__":
    main()
