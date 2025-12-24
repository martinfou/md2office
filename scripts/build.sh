#!/bin/bash

# Build Script for macOS/Linux
# 
# This is a convenience wrapper that:
# 1. Sets up virtual environment (if needed)
# 2. Installs dependencies
# 3. Calls scripts/build.py to perform the actual build
#
# The actual build logic is in scripts/build.py to avoid duplication.
# This script handles platform-specific setup (venv, dependencies).

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory (scripts folder)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Project root (one level up from scripts)
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

# Virtual environment directory
VENV_DIR="venv"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}MD2Office Converter Build Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: Failed to create virtual environment${NC}"
        echo "Make sure Python 3 is installed and in your PATH"
        exit 1
    fi
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Failed to activate virtual environment${NC}"
    exit 1
fi

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip --quiet || echo -e "${YELLOW}⚠️  Warning: Failed to upgrade pip, continuing anyway...${NC}"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: Failed to install dependencies${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${RED}ERROR: requirements.txt not found${NC}"
    exit 1
fi

# Install PyInstaller (required for building)
echo -e "${YELLOW}Installing PyInstaller...${NC}"
pip install pyinstaller --quiet
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Failed to install PyInstaller${NC}"
    exit 1
fi
echo -e "${GREEN}✅ PyInstaller installed${NC}"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Starting build...${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Run the build script
python scripts/build.py
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}ERROR: Build failed!${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Build completed successfully!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Binary location: ${GREEN}dist/md2office/md2office${NC}"
echo -e "All files are in: ${GREEN}dist/md2office/${NC}"
echo ""
echo -e "You can run the application from: ${GREEN}dist/md2office/md2office${NC}"
echo ""

