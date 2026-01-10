"""
MAPA-RD: System Health & Observability Dashboard
------------------------------------------------
Author: Antigravity AI / Senior Python standards
Version: 1.5.0 (Pro)

Purpose:
    This tool provides a high-level overview of the system's operational 
    state. It performs sanity checks on the filesystem and executes the 
    automated test suite to ensure the environment is 'mission-ready'.
"""

import sys
import subprocess
import os
import shutil
from typing import List

# ---------------------------------------------------------
# DEPENDENCY MANAGEMENT (Auto-Recovery)
# We ensure the visualization library (colorama) is present 
# before initializing the dashboard.
# ---------------------------------------------------------
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print("[!] Dashboard requires 'colorama'. Attempting auto-install...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

def print_header() -> None:
    """Renders the professional MAPA-RD visual branding."""
    print(Style.BRIGHT + Fore.CYAN + "="*70)
    print(Style.BRIGHT + Fore.CYAN + "      MAPA-RD  |  OSINT SYSTEM HEALTH & OBSERVABILITY")
    print(Style.BRIGHT + Fore.CYAN + "="*70)
    print("")

def check_structure() -> bool:
    """Validates that all critical system directories are in place."""
    print(Fore.WHITE + "[*] Phase 1: Validating Logical Structure...", end=" ")
    
    # Core directories required for pipeline execution
    required_dirs = ["04_Data", "07_Src", "08_Templates", "09_Tests", "03_Config"]
    missing = [d for d in required_dirs if not os.path.exists(d)]
    
    if not missing:
        print(Fore.GREEN + "[OPERATIONAL]")
        return True
    else:
        print(Fore.RED + "[DEGRADED]")
        print(Fore.YELLOW + f"    Missing assets detected: {missing}")
        return False

def run_tests() -> bool:
    """Executes the Pytest suite and returns the binary health status."""
    print(Fore.WHITE + "[*] Phase 2: Running Intelligence Rigor Tests (Pytest)...")
    print("-" * 70)
    
    # Execution: Trigger pytest as a subprocess to capture results
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v"], 
            capture_output=True, 
            text=True
        )
        
        # Output filtering for readability
        print(Fore.CYAN + result.stdout)
        if result.stderr:
            print(Fore.RED + f"Standard Error Output:\n{result.stderr}")

        print("-" * 70)
        
        if result.returncode == 0:
            print(Fore.GREEN + " [+] All architectural tests passed.")
            return True
        else:
            print(Fore.RED + f" [!] Logic failure detected during tests (Code {result.returncode})")
            return False
            
    except Exception as e:
        print(Fore.RED + f" [X] Failed to launch test engine: {e}")
        return False

def show_summary(structure_ok: bool, tests_ok: bool) -> None:
    """Displays the final system status report using color-coded alerts."""
    print("\n" + "="*70)
    print("                 MISSION READINESS SUMMARY")
    print("="*70 + "\n")

    if structure_ok and tests_ok:
        # PURE GREEN: System is ready for production
        print(Back.GREEN + Fore.BLACK + Style.BRIGHT + "   [READY]    ALL SYSTEMS OPERATIONAL. MISSION READY.   ")
    elif structure_ok and not tests_ok:
        # YELLOW: Filesystem is fine, but logic is broken
        print(Back.YELLOW + Fore.BLACK + Style.BRIGHT + "   [WARNING]  STRUCTURE INTACT, BUT LOGIC FAILED VALIDATION   ")
    else:
        # RED: Environment is corrupted
        print(Back.RED + Fore.WHITE + Style.BRIGHT + "   [FAILURE]  CRITICAL SYSTEM INTEGRITY ERROR   ")

    print(Style.RESET_ALL + "\n")

if __name__ == "__main__":
    # ---------------------------------------------------------
    # DASHBOARD EXECUTION SEQUENCE
    # ---------------------------------------------------------
    print_header()
    
    s_health = check_structure()
    t_health = run_tests()
    
    show_summary(s_health, t_health)
