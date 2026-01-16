@echo off
REM Setup script for Python virtual environment (Windows)

echo Setting up Python virtual environment for PHH VPN Client...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please download Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Found Python version:
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo Error: Failed to create virtual environment
    echo You may need to enable venv: python -m pip install --upgrade pip
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
if exist "requirements.txt" (
    echo Installing requirements...
    pip install -r requirements.txt
) else (
    echo Warning: requirements.txt not found, skipping package installation
)

echo.
echo Virtual environment setup complete!
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate.bat
echo.
echo To deactivate, run:
echo   deactivate
echo.
echo To run the VPN app:
echo   python vpn_app.py
echo.
pause
