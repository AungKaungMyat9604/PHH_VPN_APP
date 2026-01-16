#!/bin/bash
# Quick fix script for macOS Tkinter crash issue

echo "🔧 macOS Tkinter Fix Script"
echo "=========================="
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed"
    echo ""
    echo "Please install Homebrew first:"
    echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

echo "✓ Homebrew is installed"
echo ""

# Check for existing Homebrew Python
BREW_PYTHON=""
PYTHON_VERSION=""
for version in "3.12" "3.11" "3.10" "3.9"; do
    # Check common Homebrew Python locations
    for base_path in "/opt/homebrew" "/usr/local"; do
        # Check libexec/bin (where symlinks are)
        if [ -f "${base_path}/opt/python@${version}/libexec/bin/python3" ]; then
            BREW_PYTHON="${base_path}/opt/python@${version}/libexec/bin/python3"
            PYTHON_VERSION="$version"
            break 2
        # Check bin directory
        elif [ -f "${base_path}/bin/python${version}" ]; then
            BREW_PYTHON="${base_path}/bin/python${version}"
            PYTHON_VERSION="$version"
            break 2
        # Check opt directory
        elif [ -f "${base_path}/opt/python@${version}/bin/python3" ]; then
            BREW_PYTHON="${base_path}/opt/python@${version}/bin/python3"
            PYTHON_VERSION="$version"
            break 2
        fi
    done
done

if [ -z "$BREW_PYTHON" ]; then
    echo "⚠ Homebrew Python not found"
    echo ""
    echo "Installing Python 3.12 via Homebrew..."
    brew install python@3.12
    
    if [ $? -eq 0 ]; then
        PYTHON_VERSION="3.12"
        # Try to find the installed Python
        for base_path in "/opt/homebrew" "/usr/local"; do
            if [ -f "${base_path}/opt/python@3.12/libexec/bin/python3" ]; then
                BREW_PYTHON="${base_path}/opt/python@3.12/libexec/bin/python3"
                break
            elif [ -f "${base_path}/bin/python3.12" ]; then
                BREW_PYTHON="${base_path}/bin/python3.12"
                break
            elif [ -f "${base_path}/opt/python@3.12/bin/python3" ]; then
                BREW_PYTHON="${base_path}/opt/python@3.12/bin/python3"
                break
            fi
        done
        
        if [ -z "$BREW_PYTHON" ]; then
            echo "❌ Could not find installed Python"
            exit 1
        fi
        echo "✓ Python 3.12 installed at: $BREW_PYTHON"
    else
        echo "❌ Failed to install Python"
        exit 1
    fi
else
    echo "✓ Found Homebrew Python: $BREW_PYTHON (version $PYTHON_VERSION)"
fi

# Test Tkinter
echo ""
echo "Testing Tkinter..."
if "$BREW_PYTHON" -c "import tkinter; tk = tkinter.Tk(); tk.destroy()" 2>/dev/null; then
    echo "✓ Tkinter is working!"
else
    echo "⚠ Tkinter not available, installing python-tk@${PYTHON_VERSION}..."
    brew install "python-tk@${PYTHON_VERSION}"
    
    if [ $? -eq 0 ]; then
        echo "✓ python-tk@${PYTHON_VERSION} installed"
        echo ""
        echo "Testing Tkinter again..."
        if "$BREW_PYTHON" -c "import tkinter; tk = tkinter.Tk(); tk.destroy()" 2>/dev/null; then
            echo "✓ Tkinter is now working!"
        else
            echo "❌ Tkinter still not working after installation"
            echo ""
            echo "Try restarting your terminal and running this script again."
            exit 1
        fi
    else
        echo "❌ Failed to install python-tk@${PYTHON_VERSION}"
        echo ""
        echo "You can try installing it manually:"
        echo "  brew install python-tk@${PYTHON_VERSION}"
        exit 1
    fi
fi

# Recreate virtual environment
echo ""
echo "Recreating virtual environment with Homebrew Python..."
if [ -d "venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf venv
fi

"$BREW_PYTHON" -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✓ Virtual environment created"

# Activate and upgrade pip
source venv/bin/activate
pip install --upgrade pip

# Install requirements if they exist
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

deactivate

echo ""
echo "✅ Fix complete!"
echo ""
echo "You can now run the app with:"
echo "  ./run.sh"
echo ""
