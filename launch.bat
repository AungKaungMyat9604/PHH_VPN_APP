@echo off
REM Launch script for PHH VPN Client (Windows)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please download Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Run the application
python vpn_app.py
