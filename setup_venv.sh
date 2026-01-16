#!/bin/bash
# Setup script for Python virtual environment (Linux/macOS)

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

echo "Setting up Python virtual environment for PHH VPN Client..."
echo ""

# Find the best Python executable
PYTHON_CMD=$(find_python)
if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo ""
        echo "On macOS, we recommend installing Python via Homebrew:"
        echo "  brew install python@3.12"
    else
        echo "Please install Python 3.7 or higher"
    fi
    exit 1
fi

# Check Python version
PYTHON_VERSION=$("$PYTHON_CMD" --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Found Python: $PYTHON_CMD"
echo "Python version: $("$PYTHON_CMD" --version)"

# Check if Tkinter is available
echo "Checking Tkinter..."
if ! "$PYTHON_CMD" -c "import tkinter" 2>/dev/null; then
    echo "⚠ Warning: Tkinter is not available"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "On macOS, system Python may have broken Tkinter."
        echo "Consider installing Python via Homebrew: brew install python@3.12"
    fi
else
    echo "✓ Tkinter is available"
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
"$PYTHON_CMD" -m venv venv

if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    echo "You may need to install python3-venv:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-venv"
    echo "  macOS: python3 -m pip install --upgrade pip"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
"$PYTHON_CMD" -m pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    "$PYTHON_CMD" -m pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found, skipping package installation"
fi

echo ""
echo "✓ Virtual environment setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To deactivate, run:"
echo "  deactivate"
echo ""
echo "To run the VPN app:"
echo "  python3 vpn_app.py"
echo ""
