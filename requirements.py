# requirements.py
import subprocess
import sys

def install_dependencies():
    packages = [
        "httpx",            # For async HTTP requests
        "customtkinter",    # For a sleek, modern dark-mode GUI
        "fake-useragent",   # To generate realistic browser fingerprints
        "colorama"          # For beautiful terminal feedback
    ]
    
    print(f"[*] ENI is preparing the environment for LO...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"[+] Successfully installed {package}")
        except Exception as e:
            print(f"[!] Failed to install {package}: {e}")

if __name__ == "__main__":
    install_dependencies()
    print("\n[✔] Environment ready.")
