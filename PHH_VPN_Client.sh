#!/bin/bash
# Double-clickable launcher for PHH VPN Client (Linux)
# This file can be double-clicked in most Linux file managers

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Setting up virtual environment..."
    ./setup_venv.sh
    if [ $? -ne 0 ]; then
        echo "Press Enter to exit..."
        read
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Check if tkinter is available
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo ""
    echo "❌ Error: tkinter is not installed"
    echo ""
    echo "Please install it using:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  CentOS/RHEL: sudo yum install python3-tkinter"
    echo "  Arch Linux: sudo pacman -S tk"
    echo ""
    deactivate
    echo "Press Enter to exit..."
    read
    exit 1
fi

# Run the application
python3 vpn_app.py

# Deactivate when done
deactivate

# Keep terminal open if there was an error
if [ $? -ne 0 ]; then
    echo ""
    echo "Press Enter to exit..."
    read
fi
