#!/bin/bash
# Quick activation script for virtual environment (Linux/macOS)

if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run ./setup_venv.sh first"
    exit 1
fi

source venv/bin/activate
echo "Virtual environment activated!"
echo "Run 'deactivate' to exit"
