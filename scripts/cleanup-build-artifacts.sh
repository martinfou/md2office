#!/bin/bash
# Script to remove build artifacts from git tracking
# Run this script to clean up build artifacts that were accidentally committed

set -e

echo "Removing build artifacts from git tracking..."

# Remove build directories
if [ -d "build" ]; then
    echo "Removing build/ directory from git tracking..."
    git rm -r --cached build/ 2>/dev/null || echo "  build/ not tracked or already removed"
fi

# Remove dist directories
if [ -d "dist" ]; then
    echo "Removing dist/ directory from git tracking..."
    git rm -r --cached dist/ 2>/dev/null || echo "  dist/ not tracked or already removed"
fi

# Remove venv directory
if [ -d "venv" ]; then
    echo "Removing venv/ directory from git tracking..."
    git rm -r --cached venv/ 2>/dev/null || echo "  venv/ not tracked or already removed"
fi

# Remove egg-info directories
find . -type d -name "*.egg-info" -exec git rm -r --cached {} \; 2>/dev/null || echo "  No egg-info directories found"

# Remove __pycache__ directories
find . -type d -name "__pycache__" -exec git rm -r --cached {} \; 2>/dev/null || echo "  No __pycache__ directories found"

echo ""
echo "Done! Build artifacts have been removed from git tracking."
echo "These files are now ignored by .gitignore and won't be committed in the future."
echo ""
echo "Next steps:"
echo "  1. Review the changes: git status"
echo "  2. Commit the removal: git commit -m 'chore: remove build artifacts from git tracking'"
echo "  3. Verify .gitignore is working: git status (should not show build artifacts)"

