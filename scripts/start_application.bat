@echo off
REM Start Application Script for Windows
REM Creates virtual environment, installs dependencies, and runs md2office

setlocal enabledelayedexpansion

echo ========================================
echo MD2Office Converter Setup ^& Run
echo ========================================
echo.

REM Script directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Virtual environment directory
set VENV_DIR=venv

REM Check if virtual environment exists
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo Installing dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt --quiet
    echo Dependencies installed
) else (
    echo WARNING: requirements.txt not found
    echo Installing basic dependencies...
    pip install python-docx python-pptx reportlab click PyYAML --quiet
)

REM Install package in development mode
echo Installing md2office package...
pip install -e . --quiet
echo Package installed

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.

REM Check if arguments were provided
if "%~1"=="" (
    echo No arguments provided. Showing help:
    echo.
    python -m md2office --help
) else (
    echo Running md2office with arguments: %*
    echo.
    python -m md2office %*
)

endlocal

