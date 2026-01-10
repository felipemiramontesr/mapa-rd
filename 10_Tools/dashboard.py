import sys
import subprocess
import os
import shutil

# Check for colorama
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print("Installing colorama...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

def print_header():
    print(Style.BRIGHT + Fore.CYAN + "="*60)
    print(Style.BRIGHT + Fore.CYAN + "      MAPA-RD  |  SYSTEM HEALTH DASHBOARD")
    print(Style.BRIGHT + Fore.CYAN + "="*60)
    print("")

def check_structure():
    print(Fore.WHITE + "[*] Checking Directory Structure...", end=" ")
    required = ["04_Data", "07_Src", "08_Templates", "09_Tests"]
    missing = [d for d in required if not os.path.exists(d)]
    
    if not missing:
        print(Fore.GREEN + "OK")
        return True
    else:
        print(Fore.RED + "FAIL")
        print(Fore.YELLOW + f"    Missing: {missing}")
        return False

def run_tests():
    print(Fore.WHITE + "[*] Running Automated Tests (Pytest)...")
    print("-" * 40)
    
    # Run pytest and capture output
    result = subprocess.run([sys.executable, "-m", "pytest"], capture_output=True, text=True)
    
    print(Fore.YELLOW + result.stdout)
    if result.stderr:
        print(Fore.RED + result.stderr)

    print("-" * 40)
    
    if result.returncode == 0:
        return True
    else:
        return False

def show_status(structure_ok, tests_ok):
    print("\n" + "="*60)
    print("                 FINAL STATUS")
    print("="*60 + "\n")

    if structure_ok and tests_ok:
        print(Back.GREEN + Fore.BLACK + Style.BRIGHT + "   [OK]  SYSTEM GREEN: ALL SYSTEMS OPERATIONAL   ")
    elif structure_ok and not tests_ok:
        print(Back.YELLOW + Fore.BLACK + Style.BRIGHT + "   [!!]  SYSTEM YELLOW: STRUCTURE OK, TESTS FAILING   ")
    else:
        print(Back.RED + Fore.WHITE + Style.BRIGHT + "   [XX]  SYSTEM RED: CRITICAL FAILURE   ")

    print(Style.RESET_ALL + "\n")

if __name__ == "__main__":
    print_header()
    s_ok = check_structure()
    t_ok = run_tests()
    show_status(s_ok, t_ok)
