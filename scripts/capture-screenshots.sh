#!/bin/bash

# Screenshot Capture Script for md2office GUI
# Captures screenshots of the application in action and updates README.md

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

# Screenshot directory
SCREENSHOT_DIR="$PROJECT_ROOT/docs/assets/screenshots"
mkdir -p "$SCREENSHOT_DIR"

# Virtual environment
VENV_DIR="venv"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}md2office Screenshot Capture${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Activate virtual environment
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
else
    echo -e "${RED}Error: Virtual environment not found${NC}"
    echo "Please run: python3 -m venv venv && source venv/bin/activate"
    exit 1
fi

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     SCREENSHOT_CMD="gnome-screenshot" ;;
    Darwin*)    SCREENSHOT_CMD="screencapture" ;;
    *)          echo -e "${RED}Unsupported OS: ${OS}${NC}"; exit 1 ;;
esac

# Check if screenshot command exists
if ! command -v $SCREENSHOT_CMD &> /dev/null; then
    echo -e "${RED}Error: Screenshot command '$SCREENSHOT_CMD' not found${NC}"
    echo "Please install screenshot tools for your OS"
    exit 1
fi

echo -e "${YELLOW}Step 1: Launching md2office GUI...${NC}"
python -m md2office --gui &
APP_PID=$!
echo -e "${GREEN}✓ Application started (PID: $APP_PID)${NC}"

# Wait for GUI to load
echo -e "${YELLOW}Step 2: Waiting for GUI to load...${NC}"
sleep 5

# Function to capture screenshot
capture_screenshot() {
    local name=$1
    local description=$2
    local delay=${3:-1}
    local countdown=${4:-3}
    
    echo -e "${YELLOW}Capturing: $description${NC}"
    
    # Show countdown - make each number visible on a new line
    if [ $countdown -gt 0 ]; then
        echo -e "${BLUE}  Countdown: ${countdown} seconds...${NC}"
        for i in $(seq $countdown -1 1); do
            echo -e "${BLUE}  ⏱️  ${i}...${NC}"
            sleep 1
        done
        echo -e "${GREEN}  ✨ Capturing now! Click on the md2office window!${NC}"
    fi
    
    sleep $delay
    
    local filename="${SCREENSHOT_DIR}/${name}.png"
    
    case "${OS}" in
        Linux*)
            gnome-screenshot -w -f "$filename" 2>/dev/null || \
            gnome-screenshot -f "$filename" 2>/dev/null || \
            import -window root "$filename"
            ;;
        Darwin*)
            screencapture -w "$filename" 2>/dev/null || \
            screencapture -T 2 "$filename"
            ;;
    esac
    
    if [ -f "$filename" ]; then
        echo -e "${GREEN}✓ Screenshot saved: $filename${NC}"
        echo "$filename|$description"
    else
        echo -e "${RED}✗ Failed to capture screenshot${NC}"
        echo ""
    fi
}

echo ""
echo -e "${BLUE}Step 3: Capturing screenshots...${NC}"
echo -e "${YELLOW}Please make sure the md2office GUI window is:${NC}"
echo -e "${YELLOW}  1. Visible and not minimized${NC}"
echo -e "${YELLOW}  2. The active/frontmost window${NC}"
echo -e "${YELLOW}  3. Positioned where you want it captured${NC}"
echo -e "${YELLOW}You have 5 seconds to position the window...${NC}"
sleep 5

# Capture main window screenshot
echo ""
MAIN_SCREENSHOT=$(capture_screenshot "gui-main-window" "Main GUI Window" 1 3)

# Wait a bit more
sleep 1

# Capture with file selected (if possible)
echo ""
FILE_SCREENSHOT=$(capture_screenshot "gui-file-selected" "GUI with File Selected" 1 3)

echo ""
echo -e "${BLUE}Step 4: Updating README.md...${NC}"

# Create screenshot markdown content
SCREENSHOT_MD=""
if [ -f "${SCREENSHOT_DIR}/gui-main-window.png" ]; then
    SCREENSHOT_MD="![md2office GUI Main Window](docs/assets/screenshots/gui-main-window.png)"
fi

# Update README.md
if [ -f "README.md" ]; then
    # Check if screenshots section already exists
    if grep -q "## 📸 Screenshots" README.md; then
        echo -e "${YELLOW}Screenshots section already exists, updating...${NC}"
        # Remove old screenshots section
        sed -i.bak '/## 📸 Screenshots/,/^## /{ /^## 📸 Screenshots/d; /^## /!d; }' README.md
        rm -f README.md.bak
    fi
    
    # Find insertion point (after Features section, before Quick Start)
    if grep -q "## 🚀 Quick Start" README.md; then
        # Insert screenshots section before Quick Start
        if [ -n "$SCREENSHOT_MD" ]; then
            awk -v screenshots="$SCREENSHOT_MD" '
                /## 🚀 Quick Start/ {
                    print "## 📸 Screenshots"
                    print ""
                    print screenshots
                    print ""
                    print ""
                }
                { print }
            ' README.md > README.md.tmp && mv README.md.tmp README.md
            echo -e "${GREEN}✓ README.md updated with screenshots${NC}"
        fi
    fi
else
    echo -e "${RED}Error: README.md not found${NC}"
fi

echo ""
echo -e "${BLUE}Step 5: Cleaning up...${NC}"
# Kill the application
if kill -0 $APP_PID 2>/dev/null; then
    kill $APP_PID 2>/dev/null || true
    echo -e "${GREEN}✓ Application closed${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Screenshot capture complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Screenshots saved to: ${GREEN}${SCREENSHOT_DIR}${NC}"
echo -e "README.md has been updated with screenshot references"
echo ""
echo -e "${YELLOW}Note:${NC} You may want to review and adjust the screenshot"
echo -e "      placement in README.md manually"

