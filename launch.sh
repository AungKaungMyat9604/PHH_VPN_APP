#!/bin/bash
# Launch script for PHH VPN Client (Linux/macOS)

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if tkinter is available
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: tkinter is not installed"
    echo "Please install it using:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  CentOS/RHEL: sudo yum install python3-tkinter"
    echo "  Arch Linux: sudo pacman -S tk"
    exit 1
fi

# Run the application
python3 vpn_app.py
