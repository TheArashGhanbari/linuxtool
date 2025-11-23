#!/usr/bin/env python3
import os
import sys
import subprocess
import platform


def check_python_version():
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        sys.exit(1)
    print("✅ Python version is compatible")


def install_requirements():
    print("📦 Installing requirements...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)


def setup_tor():
    print("🔧 Setting up Tor...")
    system = platform.system().lower()

    if system == "linux":
        try:
            # Install Tor
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "tor"], check=True)

            # Start Tor service
            subprocess.run(["sudo", "systemctl", "start", "tor"], check=True)
            subprocess.run(["sudo", "systemctl", "enable", "tor"], check=True)

            print("✅ Tor installed and started successfully")
        except subprocess.CalledProcessError:
            print("⚠️  Could not install Tor automatically")
            print("Please install Tor manually: sudo apt install tor")
    else:
        print("⚠️  Automatic Tor setup only available for Linux")
        print("Please install Tor manually for your system")


def set_permissions():
    print("🔐 Setting file permissions...")
    try:
        os.chmod("index.py", 0o755)
        os.chmod("setup.py", 0o755)
        os.chmod("sms.py", 0o755)
        os.chmod("tor.py", 0o755)
        print("✅ Permissions set successfully")
    except Exception as e:
        print(f"⚠️  Could not set permissions: {e}")


def main():
    print("🚀 Linux Toolkit Setup")
    print("=" * 40)

    check_python_version()
    install_requirements()
    setup_tor()
    set_permissions()

    print("\n🎉 Setup completed successfully!")
    print("\nTo run the toolkit:")
    print("  python3 index.py")
    print("  or")
    print("  ./index.py")


if __name__ == "__main__":
    main()
