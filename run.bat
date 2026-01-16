@echo off
REM Run script that activates venv and runs the app (Windows)

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found!
    echo Setting up virtual environment...
    call setup_venv.bat
    if errorlevel 1 (
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the application
python vpn_app.py

REM Deactivate when done
deactivate
