#!/bin/bash

echo "📦 Installing required dependencies..."

pip3 install colorama requests stem PySocks pycryptodome

echo "✅ Dependencies installed successfully"

# Check if Tor is installed
if ! command -v tor &> /dev/null; then
    echo "⚠️  Tor is not installed on this system"
    echo "💡 To install Tor use:"
    echo "   Ubuntu/Debian: sudo apt install tor"
    echo "   CentOS/RHEL: sudo yum install tor"
    echo "   Arch: sudo pacman -S tor"
fi