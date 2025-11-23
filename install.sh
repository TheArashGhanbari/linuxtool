#!/bin/bash

echo "📦 Installing required dependencies using virtual environment..."

# Remove existing virtual environment if exists
if [ -d "linuxtool_venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf linuxtool_venv
fi

# Create virtual environment
python3 -m venv linuxtool_venv

# Activate virtual environment
source linuxtool_venv/bin/activate

# Install all required dependencies
pip install colorama requests stem PySocks pycryptodome rich psutil

echo "✅ Dependencies installed successfully in virtual environment"

# Check if Tor is installed
if ! command -v tor &> /dev/null; then
    echo "⚠️  Tor is not installed on this system"
    echo "💡 To install Tor use: sudo apt install tor"
else
    echo "✅ Tor is already installed"
fi

# Create run script
cat > run_toolkit.sh << 'EOF'
#!/bin/bash
source linuxtool_venv/bin/activate
python3 index.py
EOF

chmod +x run_toolkit.sh

echo ""
echo "🎯 Installation completed!"
echo "📝 Run the toolkit using: ./run_toolkit.sh"
echo "   Or manually: source linuxtool_venv/bin/activate && python3 index.py"