#!/usr/bin/env python3
import subprocess
import sys


def install_requirements():
    """Install required packages"""
    requirements = [
        'requests',
        'pysocks',
        'cryptography',
        'pycryptodome'
    ]

    print("🔧 Installing required packages...")

    for package in requirements:
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")

    print("\n🎉 Installation completed!")


if __name__ == "__main__":
    install_requirements()
