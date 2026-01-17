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
        os.path.join(BUILD_DIR, '07_Src', 'orchestrator.py'),
        os.path.join(BUILD_DIR, 'report_engine', 'run_report.py'),
        os.path.join(BUILD_DIR, 'main.py'),
        os.path.join(BUILD_DIR, 'requirements.txt')
    ]
    for r in required:
        if not os.path.exists(r):
            print(f"[CD] FATAL: Missing artifact {r}")
            return False
    return True

def main():
    print("\n[CD] STARTING CONTINUOUS DEPLOYMENT (BUILD PACKAGE)...")
    
    try:
        clean_build_dir()
        
        # Deploy Core Source
        copy_artifacts('07_Src', '07_Src')
        
        # Deploy Report Engine (The new "Elite" engine)
        copy_artifacts('report_engine', 'report_engine')
        
        # Deploy Config Scaffolding
        copy_artifacts('03_Config', '03_Config')

        # Deploy Root Files
        shutil.copy(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'main.py'), BUILD_DIR)
        shutil.copy(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'requirements.txt'), BUILD_DIR)
        
        # Verify
        if verify_integrity():
            print("[CD] DEPLOYMENT SUCCESSFUL. Artifacts ready in 05_Build.")
        else:
            print("[CD] DEPLOYMENT FAILED.")
            sys.exit(1)
            
    except Exception as e:
        print(f"[CD] ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
