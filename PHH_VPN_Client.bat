@echo off
REM Double-clickable launcher for PHH VPN Client (Windows)
REM This file can be double-clicked to run the app

REM Change to the script directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found!
    echo Setting up virtual environment...
    call setup_venv.bat
    if errorlevel 1 (
        echo.
        echo Setup failed. Press any key to exit...
        pause >nul
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the application
python vpn_app.py

REM Deactivate when done
deactivate

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Press any key to exit...
    pause >nul
)
