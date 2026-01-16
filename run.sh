#!/bin/bash
# Run script that activates venv and runs the app (Linux/macOS)

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Setting up virtual environment..."
    ./setup_venv.sh
    if [ $? -ne 0 ]; then
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Check if tkinter is available
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: tkinter is not installed"
    echo "Please install it using:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  macOS: Should be pre-installed with Python"
    deactivate
    exit 1
fi

# Run the application
python3 vpn_app.py

# Deactivate when done
deactivate
