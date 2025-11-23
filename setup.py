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


def install_requirements():
    """Install all required packages"""
    print("📦 Installing requirements...")

    requirements = [
        "requests",
        "socks",
        "pysocks",
        "stem",
        "colorama",
        "rich",
        "fake-useragent",
        "pycryptodome"
    ]

    # First try to install from requirements.txt
    if os.path.exists("requirements.txt"):
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✅ Requirements installed successfully from requirements.txt")
            return
        except subprocess.CalledProcessError:
            print(
                "⚠️  Failed to install from requirements.txt, trying individual packages...")

    # If requirements.txt fails, install packages individually
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
            time.sleep(0.5)  # Small delay between installations
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")

    if success_count == len(requirements):
        print("✅ All requirements installed successfully")
    else:
        print(
            f"⚠️  {success_count}/{len(requirements)} packages installed successfully")
        print("Some packages may not be available")


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
            subprocess.run(["sudo", "apt", "update"], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Install Tor
            print("📥 Installing Tor...")
            subprocess.run(["sudo", "apt", "install", "-y", "tor"], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Start Tor service
            print("🚀 Starting Tor service...")
            subprocess.run(["sudo", "systemctl", "start", "tor"], check=True)
            subprocess.run(["sudo", "systemctl", "enable", "tor"], check=True)

            # Wait a bit for Tor to start
            time.sleep(3)

            print("✅ Tor installed and started successfully")

        except subprocess.CalledProcessError as e:
            print(f"⚠️  Could not install Tor automatically: {e}")
            print("Please install Tor manually: sudo apt install tor")
        except FileNotFoundError:
            print("⚠️  apt package manager not found")
            print("Please install Tor manually for your distribution")
    elif system == "darwin":  # macOS
        print("⚠️  macOS detected")
        print("Please install Tor manually: brew install tor")
    else:
        print(
            f"⚠️  Automatic Tor setup only available for Linux (detected: {system})")
        print("Please install Tor manually for your system")


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


def verify_installation():
    """Verify that all packages are installed correctly"""
    print("🔍 Verifying installation...")

    packages_to_check = [
        "requests",
        "socks",
        "pysocks",
        "stem",
        "colorama",
        "rich",
        "fake_useragent",
        "Crypto"
    ]

    missing_packages = []

    for package in packages_to_check:
        try:
            if package == "Crypto":
                __import__("Crypto.Cipher.AES")
            else:
                __import__(package)
            print(f"✅ {package} verified")
        except ImportError as e:
            print(f"❌ {package} not available: {e}")
            missing_packages.append(package)

    if missing_packages:
        print(f"⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Please install them manually: pip install " +
              " ".join(missing_packages))
    else:
        print("✅ All packages verified successfully")


def create_example_config():
    """Create example configuration files if needed"""
    print("📝 Creating example files...")

    # Example sms.py if it doesn't exist or is encrypted
    if not os.path.exists("sms.py") or os.path.getsize("sms.py") < 100:
        try:
            with open("sms_example.py", "w") as f:
                f.write('''#!/usr/bin/env python3
"""
Example SMS Tool
Replace this with your actual SMS functionality
"""
from colorama import Fore, Style, init

init(autoreset=True)

def main():
    print(f"{Fore.GREEN}=== SMS Tool ==={Style.RESET_ALL}")
    print("This is an example SMS tool.")
    print("Replace this file with your actual SMS functionality.")
    input(f"{Fore.YELLOW}Press Enter to return to main menu...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
''')
            os.chmod("sms_example.py", 0o755)
            print("✅ Created sms_example.py")
        except Exception as e:
            print(f"⚠️  Could not create example file: {e}")


def main():
    print("🚀 Linux Toolkit Setup")
    print("=" * 50)

    # Check Python version
    check_python_version()

    # Upgrade pip first
    upgrade_pip()

    # Install requirements
    install_requirements()

    # Setup Tor (Linux only)
    setup_tor()

    # Set permissions
    set_permissions()

    # Verify installation
    verify_installation()

    # Create example files
    create_example_config()

    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 To run the toolkit:")
    print("  python3 index.py")
    print("  or")
    print("  ./index.py")

    print("\n🔧 Available tools:")
    print("  - SMS Tool (option 1)")
    print("  - Tor Connection Tool (option 2)")

    print("\n⚠️  Note: If SMS tool doesn't work, check sms.py file")
    print("   You may need to replace it with your actual implementation")


if __name__ == "__main__":
    main()
