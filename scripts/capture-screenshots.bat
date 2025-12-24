@echo off
REM Screenshot Capture Script for md2office GUI (Windows)
REM Captures screenshots of the application and updates README.md

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
cd /d "%PROJECT_ROOT%"

set SCREENSHOT_DIR=%PROJECT_ROOT%\docs\assets\screenshots
if not exist "%SCREENSHOT_DIR%" mkdir "%SCREENSHOT_DIR%"

set VENV_DIR=venv

echo ========================================
echo md2office Screenshot Capture
echo ========================================
echo.

REM Activate virtual environment
if exist "%VENV_DIR%\Scripts\activate.bat" (
    call "%VENV_DIR%\Scripts\activate.bat"
) else (
    echo Error: Virtual environment not found
    echo Please run: python -m venv venv
    exit /b 1
)

echo Step 1: Launching md2office GUI...
start "md2office" python -m md2office --gui
echo Application started
echo.

echo Step 2: Waiting for GUI to load...
timeout /t 5 /nobreak >nul
echo.

echo Step 3: Capturing screenshots...
echo Please position the GUI window where you want it captured
echo You have 10 seconds to position the window...
timeout /t 10 /nobreak >nul
echo.

REM Capture screenshot using PowerShell
echo Capturing: Main GUI Window
powershell -Command "Add-Type -AssemblyName System.Windows.Forms,System.Drawing; $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; $bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height); $graphics = [System.Drawing.Graphics]::FromImage($bitmap); $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size); $bitmap.Save('%SCREENSHOT_DIR%\gui-main-window.png'); $graphics.Dispose(); $bitmap.Dispose()"

if exist "%SCREENSHOT_DIR%\gui-main-window.png" (
    echo Screenshot saved: %SCREENSHOT_DIR%\gui-main-window.png
) else (
    echo Failed to capture screenshot
    echo.
    echo Note: On Windows, you may need to manually capture screenshots:
    echo 1. Press Windows + Shift + S to open Snipping Tool
    echo 2. Capture the GUI window
    echo 3. Save to: %SCREENSHOT_DIR%\gui-main-window.png
)

echo.
echo Step 4: Updating README.md...
python "%SCRIPT_DIR%update_readme_screenshots.py"

echo.
echo ========================================
echo Screenshot capture complete!
echo ========================================
echo.
echo Screenshots saved to: %SCREENSHOT_DIR%
echo README.md has been updated with screenshot references
echo.
echo Note: You may want to review and adjust the screenshot
echo       placement in README.md manually

pause

