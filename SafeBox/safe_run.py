# File: safe_run.py
import subprocess
import os

def setup():
    folders = ['workspace', 'logs', 'env_data']
    for f in folders:
        if not os.path.exists(f):
            os.makedirs(f)
    print("🛡️  SafeBox v3.0: Initializing Isolated Environment...")
    # Build container
    subprocess.run(["docker-compose", "build"], check=True)

def launch():
    print("\n" + "="*50)
    print("🚀 SAFEBOX TERMINAL IS NOW ACTIVE")
    print("🔒 Every 'pip install' inside this terminal will be SCANNED.")
    print("📦 Libraries are saved in 'env_data'.")
    print("="*50 + "\n")
    
    try:
        # Run container
        subprocess.run(["docker-compose", "run", "--rm", "python-sandbox"])
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup()
    launch()
