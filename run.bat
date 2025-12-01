@echo off
REM Installer Automation Tool - Launch Script

echo ==========================================
echo Installer Automation Tool
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found.
    echo Creating virtual environment...
    python -m venv venv
    echo.
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    echo.
) else (
    call venv\Scripts\activate.bat
)

echo Starting Installer Automation Tool...
echo.
python src\main.py

pause
