import os
import shutil
import sys
import hashlib

BUILD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '05_Build')

def clean_build_dir():
    if os.path.exists(BUILD_DIR):
        print(f"[CD] Cleaning build directory: {BUILD_DIR}")
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR)

def copy_artifacts(src_dir, dest_name):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = os.path.join(base_dir, src_dir)
    dest = os.path.join(BUILD_DIR, dest_name)
    
    print(f"[CD] Copying {src} -> {dest}")
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.tmp'))

def verify_integrity():
    print("[CD] Verifying build integrity...")
    # Check essential files exist in build
    required = [
        os.path.join(BUILD_DIR, 'src', 'orchestrator.py'),
        os.path.join(BUILD_DIR, 'src', 'report_generator.py'),
        os.path.join(BUILD_DIR, 'templates', 'mapa-rd.tex')
    ]
    for r in required:
        if not os.path.exists(r):
            print(f"[CD] FATAL: Missing artifact {r}")
            return False
    return True

def main():
    print("\n[CD] STARTING CONTINUOUS DEPLOYMENT (SIMULATION)...")
    
    try:
        clean_build_dir()
        
        # Deploy Core Source
        copy_artifacts('07_Src', 'src')
        
        # Deploy Templates
        copy_artifacts('08_Templates', 'templates')
        
        # Verify
        if verify_integrity():
            print("[CD] DEPLOYMENT SUCCESSFUL. Artifacts ready in 05_Build.")
        else:
            print("[CD] DEPLOYMENT FAILED.")
            sys.exit(1)
            
    except Exception as e:
        print(f"[CD] ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
