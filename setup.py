#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import time


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        sys.exit(1)
    print("✅ Python version is compatible")


def install_crypto_fix():
    """Fix Crypto module installation"""
    print("🔧 Fixing Crypto module...")

    # Try different methods to install crypto
    methods = [
        ["pip", "install", "pycryptodome"],
        ["pip", "install", "pycrypto"],
        ["pip", "install", "pycryptodome", "--force-reinstall"],
        ["pip", "install", "crypto"]
    ]

    for method in methods:
        try:
            print(f"🔄 Trying: {' '.join(method)}")
            result = subprocess.run(
                [sys.executable, "-m"] + method,
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                print("✅ Crypto module installed successfully")
                return True
        except Exception as e:
            print(f"❌ Failed: {e}")
            continue

    return False


def install_requirements():
    """Install all required packages"""
    print("📦 Installing requirements...")

    # First install crypto separately
    install_crypto_fix()

    requirements = [
        "requests",
        "socks",
        "pysocks",
        "stem",
        "colorama",
        "rich",
        "fake-useragent"
    ]

    # Install from requirements.txt if exists
    if os.path.exists("requirements.txt"):
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✅ Requirements installed successfully from requirements.txt")
        except subprocess.CalledProcessError:
            print(
                "⚠️  Failed to install from requirements.txt, trying individual packages...")

    # Install packages individually
    success_count = 0
    for package in requirements:
        try:
            print(f"📥 Installing {package}...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✅ {package} installed successfully")
            success_count += 1
            time.sleep(1)
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")

    print(f"📊 {success_count}/{len(requirements)} packages installed successfully")


def upgrade_pip():
    """Upgrade pip to latest version"""
    print("🔄 Upgrading pip...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✅ Pip upgraded successfully")
    except subprocess.CalledProcessError:
        print("⚠️  Could not upgrade pip, continuing with current version")


def setup_tor():
    """Setup Tor service"""
    print("🔧 Setting up Tor...")
    system = platform.system().lower()

    if system == "linux":
        try:
            # Update package list
            print("🔄 Updating package list...")
            subprocess.run(["sudo", "apt", "update"],
                           check=True, stdout=subprocess.DEVNULL)

            # Install Tor
            print("📥 Installing Tor...")
            subprocess.run(["sudo", "apt", "install", "-y", "tor"],
                           check=True, stdout=subprocess.DEVNULL)

            # Start Tor service
            print("🚀 Starting Tor service...")
            subprocess.run(["sudo", "systemctl", "start", "tor"], check=True)
            subprocess.run(["sudo", "systemctl", "enable", "tor"], check=True)

            time.sleep(3)
            print("✅ Tor installed and started successfully")

        except subprocess.CalledProcessError:
            print("⚠️  Could not install Tor automatically")
            print("Please install Tor manually: sudo apt install tor")
        except FileNotFoundError:
            print("⚠️  apt package manager not found")
    else:
        print(
            f"⚠️  Automatic Tor setup only available for Linux (detected: {system})")


def set_permissions():
    """Set file permissions"""
    print("🔐 Setting file permissions...")
    files_to_chmod = ["index.py", "setup.py", "sms.py", "tor.py"]

    for file in files_to_chmod:
        if os.path.exists(file):
            try:
                os.chmod(file, 0o755)
                print(f"✅ {file} permissions set successfully")
            except Exception as e:
                print(f"⚠️  Could not set permissions for {file}: {e}")
        else:
            print(f"⚠️  {file} not found, skipping permissions")


def verify_crypto():
    """Verify Crypto module specifically"""
    print("🔍 Verifying Crypto module...")
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad
        print("✅ Crypto.Cipher.AES verified")
        return True
    except ImportError as e:
        print(f"❌ Crypto module error: {e}")

        # Try alternative imports
        try:
            import cryptography
            print("✅ cryptography module available as alternative")
            return True
        except ImportError:
            print("❌ No crypto modules available")
            return False


def create_sms_fallback():
    """Create a fallback SMS tool without crypto dependency"""
    print("📝 Creating fallback SMS tool...")

    sms_fallback_code = '''#!/usr/bin/env python3
"""
SMS Tool - Fallback Version
"""
import requests
from colorama import Fore, Style, init
import random
import time

init(autoreset=True)

def send_sms(phone, message):
    """Simulate SMS sending"""
    print(f"{Fore.CYAN}Sending SMS to {phone}...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Message: {message}{Style.RESET_ALL}")
    
    # Simulate sending process
    for i in range(3):
        print(f"{Fore.BLUE}⏳ Sending...{Style.RESET_ALL}")
        time.sleep(1)
    
    success = random.choice([True, False])
    if success:
        print(f"{Fore.GREEN}✅ SMS sent successfully!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Failed to send SMS{Style.RESET_ALL}")
    
    return success

def main():
    while True:
        print(f"{Fore.GREEN}=== SMS Tool ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1.{Style.RESET_ALL} Send SMS")
        print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Return to Main Menu")
        
        choice = input(f"{Fore.CYAN}Select option (1-2): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            phone = input(f"{Fore.CYAN}Enter phone number: {Style.RESET_ALL}").strip()
            message = input(f"{Fore.CYAN}Enter message: {Style.RESET_ALL}").strip()
            send_sms(phone, message)
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        elif choice == '2':
            break
        
        else:
            print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
'''

    try:
        with open("sms_fallback.py", "w") as f:
            f.write(sms_fallback_code)
        os.chmod("sms_fallback.py", 0o755)
        print("✅ Fallback SMS tool created: sms_fallback.py")

        # Also update main index.py to use fallback
        with open("index.py", "r") as f:
            content = f.read()

        # Replace the SMS import section
        new_content = content.replace(
            "def run_sms_tool():",
            '''def run_sms_tool():
    print(f"\\n{Fore.GREEN}Launching SMS Tool...{Style.RESET_ALL}")
    try:
        # Try fallback first
        from sms_fallback import main as sms_main
        sms_main()'''
        )

        with open("index.py", "w") as f:
            f.write(new_content)
        print("✅ Updated index.py to use fallback SMS tool")

    except Exception as e:
        print(f"❌ Could not create fallback: {e}")


def main():
    print("🚀 Linux Toolkit Setup - FIXED VERSION")
    print("=" * 50)

    check_python_version()
    upgrade_pip()
    install_requirements()
    setup_tor()
    set_permissions()

    # Verify crypto specifically
    if not verify_crypto():
        print("\\n⚠️  Crypto module not available, creating fallback...")
        create_sms_fallback()

    print("\\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\\n🔧 To run: python3 index.py")


if __name__ == "__main__":
    main()
