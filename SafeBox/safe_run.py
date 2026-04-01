# File: safe_run.py
import subprocess
import os
import sys
import time

def setup_folders():
    """Create necessary directory structure for the sandbox"""
    folders = ['workspace', 'logs', 'env_data', 'temp_scan']
    for f in folders:
        if not os.path.exists(f):
            os.makedirs(f)
            print(f"✅ Created folder: {f}")

def run_scan(package_name):
    """Phase 1: Scan the library using Bandit before installation"""
    print(f"\n🔍 PHASE 1: Scanning '{package_name}' for vulnerabilities...")
    
    # Download the source code of the package (no binaries)
    subprocess.run(f"pip download {package_name} --no-binary :all: -d temp_scan", 
                   shell=True, capture_output=True)

    # Run Bandit Analysis (Security Linter)
    scan = subprocess.run(f"bandit -r temp_scan", shell=True, capture_output=True, text=True)
    
    if "High" in scan.stdout or "Medium" in scan.stdout:
        print("⚠️  SECURITY ALERT: Suspicious code patterns detected!")
        print("-" * 40)
        # Displaying the first 500 characters of the scan report
        print(scan.stdout[:500]) 
        print("-" * 40)
        if input("\nDo you still want to proceed with the installation? (y/n): ").lower() != 'y':
            return False
    else:
        print("✅ Scan Clean: No major security issues found.")
    return True

def start_sandbox():
    """Phase 2: Launch a fresh and isolated Docker container"""
    print("\n🚀 PHASE 2: Launching Fresh Sandbox Environment...")
    print("📦 Note: Libraries are being loaded from the 'env_data' persistent storage.")
    print("📝 Network activity is being recorded in the logs folder.")
    print("-" * 50)
    
    try:
        # Build and Run the Docker container
        subprocess.run(["docker-compose", "build"], check=True)
        subprocess.run(["docker-compose", "run", "--rm", "python-sandbox"])
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_folders()
    
    print("🛡️  SafeBox v2.0 - Persistent & Isolated Environment")
    pkg = input("\nInstall a new library? (Enter package name or press Enter to skip): ").strip()
    
    if pkg:
        # Scan first, then launch if safe
        if run_scan(pkg):
            start_sandbox()
    else:
        # Just launch the sandbox if no new package is requested
        start_sandbox()