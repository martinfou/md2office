#!/usr/bin/env python3
"""
Screenshot Capture Script for md2office GUI
Cross-platform script to capture screenshots and update README.md
"""

import os
import sys
import time
import subprocess
import platform
from pathlib import Path
import signal

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
SCREENSHOT_DIR = PROJECT_ROOT / "docs" / "assets" / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# Colors
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_colored(message, color=Colors.NC, end="\n"):
    """Print colored message."""
    print(f"{color}{message}{Colors.NC}", end=end)

def detect_screenshot_command():
    """Detect available screenshot command for the OS."""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return "screencapture"
    elif system == "Linux":
        # Try different Linux screenshot tools
        for cmd in ["gnome-screenshot", "scrot", "import"]:
            if subprocess.run(["which", cmd], capture_output=True).returncode == 0:
                return cmd
        return None
    elif system == "Windows":
        return "snippingtool"  # Windows Snipping Tool
    return None

def capture_screenshot(filename, description, delay=2, countdown=3):
    """Capture a screenshot with countdown."""
    print_colored(f"Capturing: {description}", Colors.YELLOW)
    
    # Show countdown
    if countdown > 0:
        print_colored(f"  Countdown starting in {countdown} seconds...", Colors.BLUE)
        for i in range(countdown, 0, -1):
            print_colored(f"  {i}...", Colors.BLUE, end="\r")
            time.sleep(1)
        print_colored("  Capturing now!", Colors.GREEN)
    
    time.sleep(delay)
    
    filepath = SCREENSHOT_DIR / filename
    system = platform.system()
    success = False
    
    try:
        if system == "Darwin":
            # macOS: screencapture
            # -w: capture window (interactive selection), -T 2: 2 second delay
            # -l<windowid>: capture specific window, but we'll use -w for interactive
            print_colored("  Click on the md2office window to capture it...", Colors.YELLOW)
            result = subprocess.run(
                ["screencapture", "-w", "-T", "2", str(filepath)],
                capture_output=True,
                timeout=15
            )
            if result.returncode == 0 and filepath.exists():
                success = True
            else:
                # Fallback: try to find the window by name and capture it
                print_colored("  Trying to find md2office window automatically...", Colors.YELLOW)
                # Use osascript to get window ID and capture it
                applescript = '''
                tell application "System Events"
                    set frontApp to first application process whose frontmost is true
                    set frontAppName to name of frontApp
                    if frontAppName contains "Python" or frontAppName contains "md2office" then
                        set windowList to windows of frontApp
                        if (count of windowList) > 0 then
                            set frontWindow to first window of frontApp
                            return id of frontWindow
                        end if
                    end if
                end tell
                '''
                result = subprocess.run(
                    ["osascript", "-e", applescript],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0 and result.stdout.strip():
                    window_id = result.stdout.strip()
                    # Capture using window ID (not directly supported, so use -w)
                    result = subprocess.run(
                        ["screencapture", "-w", "-T", "1", str(filepath)],
                        capture_output=True,
                        timeout=15
                    )
                    if result.returncode == 0 and filepath.exists():
                        success = True
        elif system == "Linux":
            cmd = detect_screenshot_command()
            if cmd == "gnome-screenshot":
                # -w: capture window (interactive selection)
                print_colored("  Click on the md2office window to capture it...", Colors.YELLOW)
                result = subprocess.run(
                    ["gnome-screenshot", "-w", "-f", str(filepath)],
                    capture_output=True,
                    timeout=15
                )
                if result.returncode != 0:
                    print_colored("  Window selection failed, trying active window...", Colors.YELLOW)
                    # Try to capture active window using xdotool
                    try:
                        result = subprocess.run(
                            ["xdotool", "getactivewindow"],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if result.returncode == 0:
                            window_id = result.stdout.strip()
                            result = subprocess.run(
                                ["import", "-window", window_id, str(filepath)],
                                capture_output=True,
                                timeout=10
                            )
                    except:
                        pass
            elif cmd == "scrot":
                # -s: select window/area interactively
                print_colored("  Click and drag to select the md2office window...", Colors.YELLOW)
                result = subprocess.run(
                    ["scrot", "-s", str(filepath)],
                    capture_output=True,
                    timeout=15
                )
            elif cmd == "import":
                # Try to get active window first
                try:
                    result = subprocess.run(
                        ["xdotool", "getactivewindow"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        window_id = result.stdout.strip()
                        result = subprocess.run(
                            ["import", "-window", window_id, str(filepath)],
                            capture_output=True,
                            timeout=10
                        )
                    else:
                        print_colored("  Please click on the md2office window...", Colors.YELLOW)
                        result = subprocess.run(
                            ["import", "-window", "root", str(filepath)],
                            capture_output=True,
                            timeout=10
                        )
                except:
                    print_colored("  Please click on the md2office window...", Colors.YELLOW)
                    result = subprocess.run(
                        ["import", "-window", "root", str(filepath)],
                        capture_output=True,
                        timeout=10
                    )
            
            if result.returncode == 0 and filepath.exists():
                success = True
        elif system == "Windows":
            # Windows: Use PowerShell to capture screenshot
            ps_script = f"""
            Add-Type -AssemblyName System.Windows.Forms,System.Drawing
            $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
            $bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
            $bitmap.Save('{filepath}')
            $graphics.Dispose()
            $bitmap.Dispose()
            """
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True,
                timeout=10
            )
            if result.returncode == 0 and filepath.exists():
                success = True
        
        if success:
            print_colored(f"✓ Screenshot saved: {filepath}", Colors.GREEN)
            return str(filepath)
        else:
            print_colored("✗ Failed to capture screenshot", Colors.RED)
            return None
            
    except subprocess.TimeoutExpired:
        print_colored("✗ Screenshot capture timed out", Colors.RED)
        return None
    except Exception as e:
        print_colored(f"✗ Error capturing screenshot: {e}", Colors.RED)
        return None

def update_readme(screenshot_paths):
    """Update README.md with screenshot references."""
    readme_path = PROJECT_ROOT / "README.md"
    
    if not readme_path.exists():
        print_colored("Error: README.md not found", Colors.RED)
        return False
    
    # Read README
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create screenshots section
    screenshots_section = "## 📸 Screenshots\n\n"
    
    for i, path in enumerate(screenshot_paths, 1):
        if path and Path(path).exists():
            rel_path = Path(path).relative_to(PROJECT_ROOT)
            if i == 1:
                screenshots_section += f"![md2office GUI Main Window]({rel_path})\n\n"
            else:
                screenshots_section += f"![md2office GUI - Screenshot {i}]({rel_path})\n\n"
    
    screenshots_section += "\n"
    
    # Find insertion point (after Features, before Quick Start)
    if "## 🚀 Quick Start" in content:
        # Remove existing screenshots section if present
        import re
        content = re.sub(r'## 📸 Screenshots.*?(?=\n## |$)', '', content, flags=re.DOTALL)
        
        # Insert before Quick Start
        content = content.replace(
            "## 🚀 Quick Start",
            screenshots_section + "## 🚀 Quick Start"
        )
        
        # Write back
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print_colored("✓ README.md updated with screenshots", Colors.GREEN)
        return True
    else:
        print_colored("Warning: Could not find insertion point in README.md", Colors.YELLOW)
        return False

def main():
    """Main function."""
    print_colored("=" * 40, Colors.BLUE)
    print_colored("md2office Screenshot Capture", Colors.BLUE)
    print_colored("=" * 40, Colors.BLUE)
    print()
    
    # Check virtual environment
    venv_path = PROJECT_ROOT / "venv"
    if not venv_path.exists():
        print_colored("Error: Virtual environment not found", Colors.RED)
        print("Please run: python3 -m venv venv && source venv/bin/activate")
        sys.exit(1)
    
    # Detect screenshot command
    screenshot_cmd = detect_screenshot_command()
    if not screenshot_cmd:
        print_colored("Error: No screenshot command found", Colors.RED)
        print("Please install screenshot tools for your OS:")
        print("  macOS: Built-in (screencapture)")
        print("  Linux: gnome-screenshot, scrot, or ImageMagick")
        print("  Windows: Built-in (Snipping Tool)")
        sys.exit(1)
    
    print_colored(f"Using screenshot command: {screenshot_cmd}", Colors.BLUE)
    print()
    
    # Launch application
    print_colored("Step 1: Launching md2office GUI...", Colors.YELLOW)
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "md2office", "--gui"],
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print_colored(f"✓ Application started (PID: {process.pid})", Colors.GREEN)
    except Exception as e:
        print_colored(f"Error launching application: {e}", Colors.RED)
        sys.exit(1)
    
    # Wait for GUI to load
    print_colored("Step 2: Waiting for GUI to load...", Colors.YELLOW)
    time.sleep(5)
    
    print()
    print_colored("Step 3: Capturing screenshots...", Colors.BLUE)
    print_colored("Please make sure the md2office GUI window is:", Colors.YELLOW)
    print_colored("  1. Visible and not minimized", Colors.YELLOW)
    print_colored("  2. The active/frontmost window", Colors.YELLOW)
    print_colored("  3. Positioned where you want it captured", Colors.YELLOW)
    print_colored("You have 5 seconds to position the window...", Colors.YELLOW)
    time.sleep(5)
    
    # Capture screenshots
    screenshot_paths = []
    
    # Main window
    print()
    path = capture_screenshot("gui-main-window.png", "Main GUI Window", delay=1, countdown=3)
    if path:
        screenshot_paths.append(path)
    
    time.sleep(1)
    
    # Additional screenshot (file selected)
    print()
    path = capture_screenshot("gui-file-selected.png", "GUI with File Selected", delay=1, countdown=3)
    if path:
        screenshot_paths.append(path)
    
    print()
    print_colored("Step 4: Updating README.md...", Colors.BLUE)
    update_readme(screenshot_paths)
    
    print()
    print_colored("Step 5: Cleaning up...", Colors.BLUE)
    try:
        process.terminate()
        process.wait(timeout=5)
        print_colored("✓ Application closed", Colors.GREEN)
    except:
        try:
            process.kill()
        except:
            pass
    
    print()
    print_colored("=" * 40, Colors.BLUE)
    print_colored("Screenshot capture complete!", Colors.GREEN)
    print_colored("=" * 40, Colors.BLUE)
    print()
    print_colored(f"Screenshots saved to: {SCREENSHOT_DIR}", Colors.GREEN)
    print_colored("README.md has been updated with screenshot references", Colors.GREEN)
    print()
    print_colored("Note: You may want to review and adjust the screenshot", Colors.YELLOW)
    print_colored("      placement in README.md manually", Colors.YELLOW)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\nInterrupted by user", Colors.YELLOW)
        sys.exit(1)

