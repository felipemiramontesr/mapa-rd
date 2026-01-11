import subprocess
import sys
import os
import time

def run_script(script_path):
    cmd = [sys.executable, script_path]
    result = subprocess.run(cmd, text=True)
    return result.returncode == 0

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tools_dir = os.path.join(base_dir, '10_Tools')
    
    print("=========================================")
    print("   MAPA-RD MASTERSHIP PIPELINE v1.0")
    print("=========================================")
    start = time.time()
    
    # 1. Continuous Integration
    print("\n>>> STAGE 1: CI (Quality Verification)")
    if not run_script(os.path.join(tools_dir, 'run_ci.py')):
        print("\n[!] PIPE HALTED: CI FAILED.")
        sys.exit(1)
        
    # 2. Continuous Deployment
    print("\n>>> STAGE 2: CD (Artifact Assembly)")
    if not run_script(os.path.join(tools_dir, 'run_cd.py')):
        print("\n[!] PIPE HALTED: CD FAILED.")
        sys.exit(1)
        
    duration = round(time.time() - start, 2)
    print("=========================================")
    print(f"   PIPELINE FINISHED SUCCESSFULLY ({duration}s)")
    print("=========================================")

if __name__ == "__main__":
    main()
