#!/bin/bash

# Start Application Script
# Creates virtual environment, installs dependencies, and runs md2office

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Virtual environment directory
VENV_DIR="venv"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}MD2Office Converter Setup & Run${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip --quiet

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${RED}⚠️  requirements.txt not found${NC}"
    echo -e "${YELLOW}Installing basic dependencies...${NC}"
    pip install python-docx python-pptx reportlab click PyYAML --quiet
fi

# Install package in development mode
echo -e "${YELLOW}Installing md2office package...${NC}"
pip install -e . --quiet
echo -e "${GREEN}✅ Package installed${NC}"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Setup complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if arguments were provided
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}No arguments provided. Showing help:${NC}"
    echo ""
    python -m md2office --help
else
    echo -e "${GREEN}Running md2office with arguments: $@${NC}"
    echo ""
    python -m md2office "$@"
fi

