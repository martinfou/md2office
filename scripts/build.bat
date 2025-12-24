@echo off
REM Build Script for Windows
REM 
REM This is a convenience wrapper that:
REM 1. Sets up virtual environment (if needed)
REM 2. Installs dependencies
REM 3. Calls scripts\build.py to perform the actual build
REM
REM The actual build logic is in scripts\build.py to avoid duplication.
REM This script handles platform-specific setup (venv, dependencies).

setlocal enabledelayedexpansion

echo ========================================
echo MD2Office Converter Build Script
echo ========================================
echo.

REM Script directory (scripts folder)
set SCRIPT_DIR=%~dp0
REM Project root (one level up from scripts)
set PROJECT_ROOT=%SCRIPT_DIR%..
cd /d "%PROJECT_ROOT%"

REM Virtual environment directory
set VENV_DIR=venv

REM Check if virtual environment exists
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Make sure Python is installed and in your PATH
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
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)

REM Install dependencies
echo Installing dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed
) else (
    echo ERROR: requirements.txt not found
    pause
    exit /b 1
)

REM Install PyInstaller (required for building)
echo Installing PyInstaller...
pip install pyinstaller --quiet
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)
echo PyInstaller installed

echo.
echo ========================================
echo Starting build...
echo ========================================
echo.

REM Run the build script
python scripts\build.py
if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Binary location: dist\md2office\md2office.exe
echo All files are in: dist\md2office\
echo.
echo You can run the application from: dist\md2office\md2office.exe
echo.

pause
endlocal

