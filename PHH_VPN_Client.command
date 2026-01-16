#!/bin/bash
# Double-clickable launcher for PHH VPN Client (macOS)
# This file can be double-clicked to run the app

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Setting up virtual environment..."
    ./setup_venv.sh
    if [ $? -ne 0 ]; then
        echo "Press any key to exit..."
        read -n 1
        exit 1
    fi
fi

# Function to find the best Python executable
find_python() {
    # On macOS, prefer Homebrew Python which has working Tkinter
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Check for Homebrew Python (check multiple locations for each version)
        for version in "3.12" "3.11" "3.10" "3.9"; do
            for base_path in "/opt/homebrew" "/usr/local"; do
                # Check libexec/bin (where symlinks are, preferred)
                brew_python="${base_path}/opt/python@${version}/libexec/bin/python3"
                if [ -f "$brew_python" ]; then
                    # Test if Tkinter works with this Python
                    if "$brew_python" -c "import tkinter" 2>/dev/null; then
                        echo "$brew_python"
                        return 0
                    fi
                fi
                # Check bin directory
                brew_python="${base_path}/bin/python${version}"
                if [ -f "$brew_python" ]; then
                    if "$brew_python" -c "import tkinter" 2>/dev/null; then
                        echo "$brew_python"
                        return 0
                    fi
                fi
                # Check opt/bin directory
                brew_python="${base_path}/opt/python@${version}/bin/python3"
                if [ -f "$brew_python" ]; then
                    if "$brew_python" -c "import tkinter" 2>/dev/null; then
                        echo "$brew_python"
                        return 0
                    fi
                fi
            done
        done
    fi
    
    # Fall back to system python3
    if command -v python3 &> /dev/null; then
        echo "python3"
        return 0
    fi
    
    return 1
}

# Find the best Python executable
PYTHON_CMD=$(find_python)
if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed"
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if tkinter is available and works
if ! "$PYTHON_CMD" -c "import tkinter; tk = tkinter.Tk(); tk.destroy()" 2>/dev/null; then
    echo ""
    echo "❌ Error: Tkinter is not working properly"
    echo ""
    echo "On macOS, the system Python from CommandLineTools has broken Tkinter."
    echo ""
    echo "Solution: Run the fix script:"
    echo "  ./fix_macos_tkinter.sh"
    echo ""
    echo "Or install Python via Homebrew:"
    echo "  brew install python@3.12"
    echo ""
    deactivate
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

# Run the application
"$PYTHON_CMD" vpn_app.py

# Deactivate when done
deactivate

# Keep terminal open if there was an error
if [ $? -ne 0 ]; then
    echo ""
    echo "Press any key to exit..."
    read -n 1
fi
